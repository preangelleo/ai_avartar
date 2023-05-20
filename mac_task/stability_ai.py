import os
import json
import requests
import base64
from dotenv import load_dotenv
load_dotenv()

STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")
STABILITY_URL = f"https://api.stability.ai/v1/"


def stability_user():
    STABILITY_URL_ACCOUNT = f"{STABILITY_URL}user/account"
    response = requests.get(STABILITY_URL_ACCOUNT, headers={
        "Authorization": f"Bearer {STABILITY_API_KEY}"
    })

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    # Do something with the payload...
    payload = response.json()
    # print(json.dumps(payload, indent=4))
    return payload


def stability_balance():
    STABILITY_URL_BALANCE = f"{STABILITY_URL}user/balance"
    response = requests.get(STABILITY_URL_BALANCE, headers={
        "Authorization": f"Bearer {STABILITY_API_KEY}"
    })

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    # Do something with the payload...
    payload = response.json()
    # print(json.dumps(payload, indent=4))
    return payload


def stability_engines():
    STABILITY_URL_ENGINES = f"{STABILITY_URL}engines/list"
    response = requests.get(STABILITY_URL_ENGINES, headers={
        "Authorization": f"Bearer {STABILITY_API_KEY}"
    })

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    # Do something with the payload...
    payload = response.json()
    # print(json.dumps(payload, indent=4))
    return payload


'''
[
    {
        "description": "Real-ESRGAN_x2plus upscaler model",
        "id": "esrgan-v1-x2plus",
        "name": "Real-ESRGAN x2",
        "type": "PICTURE"
    },
    {
        "description": "Stability-AI Stable Diffusion v1.4",
        "id": "stable-diffusion-v1",
        "name": "Stable Diffusion v1.4",
        "type": "PICTURE"
    },
    {
        "description": "Stability-AI Stable Diffusion v1.5",
        "id": "stable-diffusion-v1-5",
        "name": "Stable Diffusion v1.5",
        "type": "PICTURE"
    },
    {
        "description": "Stability-AI Stable Diffusion v2.0",
        "id": "stable-diffusion-512-v2-0",
        "name": "Stable Diffusion v2.0",
        "type": "PICTURE"
    },
    {
        "description": "Stability-AI Stable Diffusion 768 v2.0",
        "id": "stable-diffusion-768-v2-0",
        "name": "Stable Diffusion v2.0-768",
        "type": "PICTURE"
    },
    {
        "description": "Stability-AI Stable Diffusion v2.1",
        "id": "stable-diffusion-512-v2-1",
        "name": "Stable Diffusion v2.1",
        "type": "PICTURE"
    },
    {
        "description": "Stability-AI Stable Diffusion 768 v2.1",
        "id": "stable-diffusion-768-v2-1",
        "name": "Stable Diffusion v2.1-768",
        "type": "PICTURE"
    },
    {
        "description": "Stability-AI Stable Diffusion XL Beta v2.2.2",
        "id": "stable-diffusion-xl-beta-v2-2-2",
        "name": "Stable Diffusion v2.2.2-XL Beta",
        "type": "PICTURE"
    },
    {
        "description": "Stability-AI Stable Inpainting v1.0",
        "id": "stable-inpainting-v1-0",
        "name": "Stable Inpainting v1.0",
        "type": "PICTURE"
    },
    {
        "description": "Stability-AI Stable Inpainting v2.0",
        "id": "stable-inpainting-512-v2-0",
        "name": "Stable Inpainting v2.0",
        "type": "PICTURE"
    }
]
'''


def stability_generate_image(text_prompts, cfg_scale=7, clip_guidance_preset="FAST_BLUE", height=512, width=512, samples=1, steps=30, engine_id="stable-diffusion-xl-beta-v2-2-2"):
    response = requests.post(
        f"{STABILITY_URL}generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {STABILITY_API_KEY}"
        },
        json={
            "text_prompts": [
                {
                    "text": text_prompts
                }
            ],
            "cfg_scale": cfg_scale,
            "clip_guidance_preset": clip_guidance_preset,
            "height": height,
            "width": width,
            "samples": samples,
            "steps": steps
        }
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()
    file_path_list = []
    working_folder = 'json_datas/dream_studio/'
    if not os.path.exists(working_folder):
        os.makedirs(working_folder)

    for i, image in enumerate(data["artifacts"]):
        with open(f"json_datas/dream_studio/v1_txt2img_{i}.png", "wb") as f:
            f.write(base64.b64decode(image["base64"]))
            file_path_list.append(
                f"json_datas/dream_studio/sd_txt2img_{i}.png")

    return file_path_list
