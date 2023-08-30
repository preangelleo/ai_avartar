import base64
import hashlib
from datetime import datetime, timedelta
import json

import asyncio
import boto3
import httpx

from src.utils.param_singleton import Params
from src.utils.logging_util import measure_execution_time
from src.utils.logging_util import logging
from src.utils.metrics import ERROR_COUNTER, IMAGE_GENERATION_COUNTER
from src.utils.prompt_template import negative_stability_ai_prompt

SD_SERVER_AVAILABLE_TIME_LOCK = asyncio.Lock()
SD_SERVER_AVAILABLE_TIME = datetime.now()


def update_sd_server_available_time():
    global SD_SERVER_AVAILABLE_TIME
    SD_SERVER_AVAILABLE_TIME = datetime.now() + timedelta(seconds=1 / Params().SD_IMAGE_THROUGHPUT)
    logging.info(f'Update SD_SERVER_AVAILABLE_TIME = {SD_SERVER_AVAILABLE_TIME.strftime("%Y-%m-%d %H:%M:%S")}')


async def should_use_customized_sd_server():
    global SD_SERVER_AVAILABLE_TIME

    async with SD_SERVER_AVAILABLE_TIME_LOCK:
        # If we are allowed to call customized SD server now
        if datetime.now() >= SD_SERVER_AVAILABLE_TIME:
            # Check if the customized sd server is alive
            try:
                async with httpx.AsyncClient() as client:
                    client.timeout = 5
                    response = await client.get(f'http://{Params().SD_SERVER_IP}:8889/heartbeat/')
                    if response.status_code != 200:
                        logging.error(f"Customized SD Server is dead: {response}")
                        return False
            except Exception as e:
                logging.error(f"Customized SD Server is dead: {e}")
                return False

            update_sd_server_available_time()
            logging.info(
                f'SD_SERVER_AVAILABLE_TIME={SD_SERVER_AVAILABLE_TIME.strftime("%Y-%m-%d %H:%M:%S")}: Use Customized SD Server'
            )
            return True

    logging.info(f'SD_SERVER_AVAILABLE_TIME={SD_SERVER_AVAILABLE_TIME.strftime("%Y-%m-%d %H:%M:%S")}: Use Stability.ai')
    return False


def process_image_description(image_description):
    """Process the image_description so that it doesn't have sensitive words and clearly indicate the gender of
    subject"""

    for phase in ['sexy']:
        image_description = image_description.replace(phase, '')

    for phase in [' you ', 'You ', ' your ', 'Your ']:
        image_description = image_description.replace(phase, ' a beautiful girl ')

    for phase in ['We ', 'Our ', ' we ', ' our ', '  couple']:
        image_description = image_description.replace(phase, ' a handsome man and a beautiful girl ')

    for phase in [' I ', ' my ', 'My ', ' me ', 'Evan ', ' guy ', ' person ']:
        image_description = image_description.replace(phase, ' a handsome man ')

    return image_description


async def generate_image(
    raw_image_description,
    is_bot_picture,
    cfg_scale=7,
    clip_guidance_preset="FAST_BLUE",
    height=512,
    width=512,
    samples=1,
    steps=30,
    seed=1,
    engine_id="stable-diffusion-xl-1024-v1-0",
    style_preset=None,
):
    # If the user wants to see portrait of bot, we append the system defined image prompt
    if is_bot_picture:
        prompt = (
            'anime style, soft lighting, high-resolution, Shinkai Makoto, '
            + process_image_description(raw_image_description)
            + ', a handsome man'
        )
    else:
        prompt = 'anime style, soft lighting, high-resolution, Shinkai Makoto, ' + process_image_description(
            raw_image_description
        )

    image_description = [
        {
            "text": prompt,
            "weight": 1,
        },
        {
            "text": negative_stability_ai_prompt,
            "weight": -1,
        },
    ]

    if await should_use_customized_sd_server():
        return await customized_sd_server_generate_image(prompt, negative_stability_ai_prompt, steps)
    else:
        return await stability_generate_image(
            image_description,
            cfg_scale,
            clip_guidance_preset,
            height,
            width,
            samples,
            steps,
            seed,
            engine_id,
            style_preset,
        )


async def customized_sd_server_generate_image(prompt, negative_prompt, steps):
    async with httpx.AsyncClient() as client:
        client.timeout = 60
        payload = {'prompt': prompt, 'negative_prompt': negative_prompt, 'num_inference_steps': steps}
        response = await client.post(
            f'http://{Params().SD_SERVER_IP}:8889/text_to_image/',
            data=json.dumps(payload),
            headers={'Content-type': 'application/json'},
        )
        IMAGE_GENERATION_COUNTER.labels('customized_server').inc()
        data = response.json()
        return [data['url']]


@measure_execution_time
async def stability_generate_image(
    text_prompts,
    cfg_scale=7,
    clip_guidance_preset="FAST_BLUE",
    height=512,
    width=512,
    samples=1,
    steps=30,
    seed=1,
    engine_id="stable-diffusion-xl-1024-v1-0",
    style_preset=None,
):
    timeout = 60
    if isinstance(text_prompts, str):
        text_prompts_hash = text_prompts
        text_prompts = [{"text": text_prompts}]
    elif isinstance(text_prompts, list):
        text_prompts_hash = ''.join([t['text'] for t in text_prompts])
    else:
        raise ValueError(f"Wrong text_prompts provided: {text_prompts}")

    logging.info(f"stability_generate_image() text_prompts={text_prompts}")
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(
            f"{Params().STABILITY_URL}generation/{engine_id}/text-to-image",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {Params().STABILITY_API_KEY}",
            },
            json={
                "text_prompts": text_prompts,
                "cfg_scale": cfg_scale,
                "clip_guidance_preset": clip_guidance_preset,
                "height": height,
                "width": width,
                "seed": seed,
                "samples": samples,
                "steps": steps,
                'style_preset': style_preset,
            },
        )

        if response.status_code != 200:
            ERROR_COUNTER.labels('generate_image_' + json.loads(response.text)["name"], 'chatgpt').inc()
            logging.error(f'generate_image error: {json.loads(response.text)["name"]}')
            raise Exception("Non-200 response: " + str(response.text))

        data = response.json()
        file_url_list = []

        for i, image in enumerate(data["artifacts"]):
            IMAGE_GENERATION_COUNTER.labels('dream_studio_total').inc()
            if image['finishReason'] != 'SUCCESS':
                logging.info(f"stability_generate_image() fail to generate an clear image: {image['finishReason']}")
                IMAGE_GENERATION_COUNTER.labels('dream_studio_blurred').inc()
                continue

            current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            filename = hashlib.md5(
                (text_prompts_hash + '_' + str(i) + '_' + str(current_timestamp)).encode()
            ).hexdigest()

            filename_pic = 'stability_ai/' + filename + '.png'

            s3_resource = boto3.resource(
                's3',
                region_name=Params().S3_REGION,
                aws_access_key_id=Params().AWS_ACCESS_KEY_ID,
                aws_secret_access_key=Params().AWS_SECRET_ACCESS_KEY,
            )
            # Create a new S3 object
            object = s3_resource.Object(Params().S3_IMAGE_BUCKET_NAME, filename_pic)
            # Write the image to S3
            object.put(Body=base64.b64decode(image["base64"]))

            s3_client = boto3.client(
                's3',
                region_name=Params().S3_REGION,
                aws_access_key_id=Params().AWS_ACCESS_KEY_ID,
                aws_secret_access_key=Params().AWS_SECRET_ACCESS_KEY,
            )
            url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': Params().S3_IMAGE_BUCKET_NAME, 'Key': filename_pic},
                # 30 days
                ExpiresIn=3600 * 24 * 30,
            )
            file_url_list.append(url)

        return file_url_list
