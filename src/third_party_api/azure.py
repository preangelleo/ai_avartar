import os

from src.utils.utils import convert_mp3_to_wav

import azure.cognitiveservices.speech as speechsdk

from src.third_party_api.chatgpt import chat_gpt_full
from src.utils.param_singleton import Params
from src.utils.prompt_template import (
    news_reporter_system_prompt,
    news_reporter_user_prompt,
    news_reporter_assistant_prompt,
)


def from_voice_to_text_azure(audio_file_path):
    wave_file_path = convert_mp3_to_wav(audio_file_path)

    speech_config = speechsdk.SpeechConfig(
        subscription=os.getenv('SPEECH_KEY'), region=os.getenv('SPEECH_REGION')
    )
    audio_config = speechsdk.AudioConfig(filename=wave_file_path)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )
    result = speech_recognizer.recognize_once_async().get()
    return result.text


def microsoft_azure_tts(text, voice='zh-CN-YunxiNeural', output_filename='output.wav'):
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(
        subscription=os.getenv('SPEECH_KEY'), region=os.getenv('SPEECH_REGION')
    )
    audio_config = speechsdk.audio.AudioOutputConfig(
        use_default_speaker=True, filename=output_filename
    )

    # The language of the voice that speaks.
    speech_config.speech_synthesis_voice_name = voice
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    if (
        speech_synthesis_result.reason
        == speechsdk.ResultReason.SynthesizingAudioCompleted
    ):
        return output_filename
    return False


def create_news_podcast(filepath='', prompt='', openai_model=Params().OPENAI_MODEL):
    if not filepath and not prompt:
        return

    if filepath and not prompt:
        with open(filepath, 'r') as f:
            prompt = f.read()

    if not prompt:
        return

    message = chat_gpt_full(
        prompt,
        news_reporter_system_prompt,
        news_reporter_user_prompt,
        news_reporter_assistant_prompt,
        openai_model,
        Params().OPENAI_API_KEY,
    )

    filepath_news = filepath.replace('_snippet.txt', '_news.txt')
    with open(filepath_news, 'w') as f:
        f.write(message)

    filepath_news_mp3 = filepath_news.replace('.txt', '.mp3')
    if filepath_news:
        filepath_news_mp3 = microsoft_azure_tts(
            message, 'en-US-JaneNeural', filepath_news_mp3
        )

    return filepath_news_mp3
