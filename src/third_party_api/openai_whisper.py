import requests
import subprocess

from src.utils.param_singleton import Params


# Using openai whisper api to convert voice to text
def from_voice_to_text(audio_path):
    # Note: you need to be using OpenAI Python v0.27.0 for the code below to work
    if audio_path.endswith('ogg'):
        audio_path_mp3 = audio_path.replace('.ogg', '.mp3')
        command = f"ffmpeg -i {audio_path} {audio_path_mp3}"
        subprocess.run(command, shell=True)
    else:
        audio_path_mp3 = audio_path
    print(f"DEBUG: from_voice_to_text() audio_path_mp3: {audio_path_mp3}")

    url = "https://api.openai.com/v1/audio/transcriptions"
    headers = {"Authorization": f"Bearer {Params().OPENAI_API_KEY}"}
    data = {
        'model': 'whisper-1',
    }
    with open(audio_path_mp3, 'rb') as f:
        files = {'file': f}
        response = requests.post(url, headers=headers, data=data, files=files)

    if response.status_code != 200:
        raise Exception(f"Request to OpenAI failed with status {response.status_code}, {response.text}")
    '''
    {
    "text": "Imagine the wildest idea that you've ever had, and you're curious about how it might scale to something that's a 100, a 1,000 times bigger. This is a place where you can get to do that."
    }
    '''
    return response.json().get('text')