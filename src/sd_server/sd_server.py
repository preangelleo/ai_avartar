from datetime import datetime
import hashlib

import boto3
from flask import Flask, request
from diffusers import DiffusionPipeline
import torch
import time
from io import BytesIO

PORT = 8889

AWS_ACCESS_KEY_ID = 'AKIARABLVTUG4DJNDPVZ'
AWS_SECRET_ACCESS_KEY = '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'
S3_IMAGE_BUCKET_NAME = 'avatado-sdxl'
S3_REGION = 'ap-northeast-1'

app = Flask(__name__)


def initialize():
    global base_model
    global refiner_model
    # load both base & refiner
    base_model = DiffusionPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, variant="fp16", use_safetensors=True
    )
    base_model.to("cuda")

    refiner_model = DiffusionPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-refiner-1.0",
        text_encoder_2=base_model.text_encoder_2,
        vae=base_model.vae,
        torch_dtype=torch.float16,
        use_safetensors=True,
        variant="fp16",
    )
    refiner_model.to("cuda")


initialize()


def generate_image(prompt, negative_prompt, n_steps):
    high_noise_frac = 0.8
    handle_single_msg_start = time.perf_counter()
    # run both experts
    image = base_model(
        prompt=prompt,
        negative_prompt=negative_prompt,
        num_inference_steps=n_steps,
        denoising_end=high_noise_frac,
        output_type="latent",
    ).images
    image = refiner_model(
        prompt=prompt,
        negative_prompt=negative_prompt,
        num_inference_steps=n_steps,
        denoising_start=high_noise_frac,
        image=image,
    ).images[0]
    latency = time.perf_counter() - handle_single_msg_start
    print(f'latency: {latency}s')

    return image


def store_image_to_s3_and_return_url(image, prompt):
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = hashlib.md5((prompt + '_' + str(current_timestamp)).encode()).hexdigest()

    filename_pic = 'stability_ai/' + filename + '.png'

    s3_client = boto3.client(
        's3',
        region_name=S3_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )

    in_mem_file = BytesIO()
    image.save(in_mem_file, format='PNG')
    in_mem_file.seek(0)

    # Upload image to s3
    s3_client.upload_fileobj(in_mem_file, S3_IMAGE_BUCKET_NAME, filename_pic)

    url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': S3_IMAGE_BUCKET_NAME, 'Key': filename_pic},
        # 30 days
        ExpiresIn=3600 * 24 * 30,
    )

    return url


@app.route('/text_to_image/', methods=['POST'])
def text_to_image():
    data = request.get_json()
    print(f'Received {data}')
    prompt = data.get('prompt')
    negative_prompt = data.get('negative_prompt')
    num_inference_steps = int(data.get('num_inference_steps'))
    image = generate_image(prompt, negative_prompt, num_inference_steps)
    url = store_image_to_s3_and_return_url(image, prompt)

    return {'url': url}


@app.route('/heartbeat/', methods=['GET'])
def heartbeat():
    return 'ok'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
