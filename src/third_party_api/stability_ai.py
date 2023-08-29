import base64
import hashlib
from datetime import datetime
import json

import boto3
import httpx

from src.utils.param_singleton import Params
from src.utils.logging_util import measure_execution_time
from src.utils.logging_util import logging
from src.utils.metrics import ERROR_COUNTER, IMAGE_GENERATION_COUNTER


def process_image_description(image_description):
    """Process the image_description so that it doesn't have sensitive words and clearly indicate the gender of
    subject"""

    for phase in ['sexy']:
        image_description = image_description.replace(phase, '')

    for phase in [' you ', 'You ', ' your ', 'Your ']:
        image_description = image_description.replace(phase, ' a beautiful girl ')

    for phase in ['We ', 'Our ', ' we ', ' our ', '  couple']:
        image_description = image_description.replace(phase, ' a handsome man and a beautiful girl ')

    for phase in [' I ', ' my ', 'My ', ' me ', 'Evan ', ' guy ']:
        image_description = image_description.replace(phase, ' a handsome man ')

    return image_description


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
