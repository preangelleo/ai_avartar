import requests
import json
from PIL import Image
import time
from io import BytesIO
import httpx
import asyncio
from src.utils.logging_util import logging

MSG_PER_SECOND = 0.1
LOAD_TEST_DURARION_SECONDS = 30

SEND_MSG_INTERVAL_SECOND = 1.0 / MSG_PER_SECOND
SD_SERVER_IP = '18.181.24.181'

prompt = """
masterpiece, high quality, best quality, absurdres, 1 girl, depth of field, chinese-girl-v1.0 , cowboy-shot , looking at viewer, skinny face , closed mouth, blue jacket,cityscape,  street,  neon lights ,  <lora:chinese-girl-000008:0.0.8>
"""
num_inference_steps = 30


async def send_msg_async(prompt, num_inference_steps):
    headers = {'Content-type': 'application/json'}
    payload = {'prompt': prompt, 'num_inference_steps': num_inference_steps}

    try:
        async with httpx.AsyncClient() as client:
            client.timeout = 60
            handle_single_msg_start = time.perf_counter()
            response = await client.post(
                f'http://{SD_SERVER_IP}:8889/text_to_image/', data=json.dumps(payload), headers=headers
            )
            data = response.json()
            latency = time.perf_counter() - handle_single_msg_start
            print(f'{data} latency: {latency}s')
    except Exception as e:
        logging.error('Error: %s', e)


async def main():
    total_msg_accum = 0
    tasks = []
    while total_msg_accum < LOAD_TEST_DURARION_SECONDS * MSG_PER_SECOND:
        # Randomly send a msg to tested bot
        tasks.append(asyncio.create_task(send_msg_async(prompt, num_inference_steps)))
        total_msg_accum += 1
        await asyncio.sleep(SEND_MSG_INTERVAL_SECOND)

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    logging.info('Start load tests')

    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter() - start
    logging.info(f'Finish load tests in {end:0.2f} seconds.')
