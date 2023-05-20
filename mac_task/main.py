from my_config import *


def bing_search(query, mkt='en-US'):
    '''
    This sample makes a call to the Bing Web Search API with a query and returns relevant web search.
    Documentation: https://docs.microsoft.com/en-us/bing/search-apis/bing-web-search/overview
    '''
    endpoint = "https://api.bing.microsoft.com/v7.0/search"

    # Construct a request
    params = {'q': query, 'mkt': mkt}
    headers = {'Ocp-Apim-Subscription-Key': BING_SEARCH_API_KEY}

    # Call the API
    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()

        folder = 'json_datas/bing_search'
        if not os.path.exists(folder):
            os.makedirs(folder)
        query = query.lower()

        query_name = query.replace(',', '')
        query_name = query_name.replace(' ', '_')
        query_name = query_name.replace('?', '')
        query_name = query_name.replace('!', '')
        query_name = query_name.replace('(', '')
        query_name = query_name.replace(')', '')
        query_name = query_name.replace('\'', '')
        query_name = query_name.replace('\"', '')
        query_name = query_name.replace(':', '')
        query_name = query_name.replace(';', '')
        query_name = query_name.replace('+', '')
        query_name = query_name.replace('=', '')
        query_name = query_name.replace('*', '')
        query_name = query_name.replace('&', '')
        query_name = query_name.replace('%', '')
        query_name = query_name.replace('$', '')
        query_name = query_name.replace('#', '')
        query_name = query_name.replace('@', '')
        query_name = query_name.replace('~', '')
        query_name = query_name.replace('`', '')
        query_name = query_name.replace('^', '')
        query_name = query_name.replace('/', '')
        query_name = query_name.replace('\\', '')
        query_name = query_name.replace('|', '')
        query_name = query_name.replace('<', '')
        query_name = query_name.replace('>', '')
        query_name = query_name.replace('[', '')
        query_name = query_name.replace(']', '')
        query_name = query_name.replace('{', '')
        query_name = query_name.replace('}', '')
        query_name = query_name.replace('’', '')
        query_name = query_name.replace('‘', '')
        query_name = query_name.replace('“', '')
        query_name = query_name.replace('”', '')

        file_path = f'{folder}/{str(datetime.now().strftime("%Y-%m-%d %H:%M:%S").split()[0])}-{query_name[:66]}.txt'
        if os.path.isfile(file_path):
            os.remove(file_path)

        with open(file_path, 'a') as file:
            for k, v in response.json().items():
                if k in ['news']:
                    file.write(k.upper() + '\n\n')
                    if type(v) is not dict:
                        continue
                    for a, b in v.items():
                        if a in ['value']:
                            for c in b:
                                if c.get('name'):
                                    file.write('name: '.upper() +
                                               c.get('name') + '\n')
                                if c.get('description'):
                                    file.write('snippet: '.upper() +
                                               c.get('description') + '\n')
                                if c.get('url'):
                                    file.write('url: '.upper() +
                                               c.get('url') + '\n')
                                if c.get('image'):
                                    file.write(
                                        'image: '.upper() + c.get('image').get('contentUrl').split('?')[0] + '\n')
                                if c.get('datePublished'):
                                    file.write('DATE: '.upper() + c.get('datePublished').split('T')[
                                               0] + ' ' + c.get('datePublished').split('T')[1].split('.')[0] + '\n')
                                file.write('\n')
                    file.write('\n')

                if k in ['videos']:
                    file.write(k.upper() + '\n\n')
                    if type(v) is not dict:
                        continue
                    for a, b in v.items():
                        if a in ['value']:
                            for c in b:
                                if c.get('name'):
                                    file.write('name: '.upper() +
                                               c.get('name') + '\n')
                                if c.get('description'):
                                    file.write('snippet: '.upper() +
                                               c.get('description') + '\n')
                                if c.get('contentUrl'):
                                    file.write('url: '.upper() +
                                               c.get('contentUrl') + '\n')
                                if c.get('datePublished'):
                                    file.write('DATE: '.upper() + c.get('datePublished').split('T')[
                                               0] + ' ' + c.get('datePublished').split('T')[1].split('.')[0] + '\n')
                                file.write('\n')
                    file.write('\n')

                if k in ['webPages']:
                    file.write(k.upper() + '\n\n')
                    if type(v) is not dict:
                        continue
                    for a, b in v.items():
                        if a in ['value']:
                            for c in b:
                                if c.get('name'):
                                    file.write('name: '.upper() +
                                               c.get('name') + '\n')
                                if c.get('snippet'):
                                    file.write('snippet: '.upper() +
                                               c.get('snippet') + '\n')
                                if c.get('url'):
                                    file.write('url: '.upper() +
                                               c.get('url') + '\n')
                                if c.get('dateLastCrawled'):
                                    file.write('DATE: '.upper() + c.get('dateLastCrawled').split('T')[
                                               0] + ' ' + c.get('dateLastCrawled').split('T')[1].split('.')[0] + '\n')
                                file.write('\n')
                    file.write('\n')
            return file_path

    except Exception as e:
        print(f"ERROR: Bing search failed: {e}")
        return


def get_elevenlabs_userinfo():
    url = "https://api.elevenlabs.io/v1/user"
    headers = {
        "accept": "application/json",
        "xi-api-key": ELEVEN_API_KEY
    }
    response = requests.get(url, headers=headers)
    return response.json()


'''
{
    "subscription": {
        "tier": "creator",
        "character_count": 117568,
        "character_limit": 103151,
        "can_extend_character_limit": true,
        "allowed_to_extend_character_limit": true,
        "next_character_count_reset_unix": 1680361833,
        "voice_limit": 30,
        "professional_voice_limit": 1,
        "can_extend_voice_limit": false,
        "can_use_instant_voice_cloning": true,
        "can_use_professional_voice_cloning": false,
        "available_models": [
            {
                "model_id": "prod",
                "display_name": "Prod",
                "supported_language": [
                    {
                        "iso_code": "en-us",
                        "display_name": "English"
                    }
                ]
            }
        ],
        "can_use_delayed_payment_methods": false,
        "currency": "usd",
        "status": "active"
    },
    "is_new_user": true,
    "xi_api_key": "7506563f79bd85dbf7dade0cc8412b42"
}
'''


def eleven_labs_status_check():

    r = get_elevenlabs_userinfo()
    try:
        print(
            f"DEBUG: character_count {r.get('subscription').get('character_count')}")
        print(
            f"DEBUG: character_limit {r.get('subscription').get('character_limit')}")
        print(
            f"DEBUG: character_over_used {int(r.get('subscription').get('character_count')) - int(r.get('subscription').get('character_limit'))}")
        if int(r.get('subscription').get('character_count')) - int(r.get('subscription').get('character_limit')) > 0:
            # Additional usage-based characters at $0.30 per 1000 characters
            print(
                f"DEBUG: character_over_used_cost {round((int(r.get('subscription').get('character_count')) - int(r.get('subscription').get('character_limit'))) * 0.0003, 2)}")

        if not r.get('subscription').get('allowed_to_extend_character_limit'):
            print(
                f"ERROR: eleven_labs_tts() failed: allowed_to_extend_character_limit: {r.get('subscription').get('allowed_to_extend_character_limit')}")
            return

        if not r.get('subscription').get('can_extend_character_limit'):
            print(
                f"ERROR: eleven_labs_tts() failed: can_extend_character_limit: {r.get('subscription').get('can_extend_character_limit')}")
            return

        # "next_character_count_reset_unix": 1680361833, convert timestamp to date time
        print(
            f"DEBUG: next_character_count_reset_unix {datetime.fromtimestamp(r.get('subscription').get('next_character_count_reset_unix'))}")

        return True

    except Exception as e:
        print(f"ERROR: get_elevenlabs_userinfo() failed: {e}")
        print(json.dumps(r, indent=4))
        return


def eleven_labs_tts(content, tts_file_name, voice_id='YEhWVRrlzrtA9MzdS8vE'):

    r = eleven_labs_status_check()
    if not r:
        return

    if debug:
        print(f"DEBUG: eleven_labs_tts() voice_id: {voice_id}")
    API_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    if debug:
        print(f"DEBUG: eleven_labs_tts() API_URL : {API_URL}")

    headers = {"xi-api-key": ELEVEN_API_KEY}
    data = {
        "text": content,
        "voice_settings": {
            "stability": 0.95,
            "similarity_boost": 0.95
        }
    }
    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        try:
            with open(tts_file_name, "wb") as f:
                f.write(response.content)
            return tts_file_name
        except Exception as e:
            print(
                f"ERROR : wring response.content to tts_file_name FAILED.\response.reason:{response.reason}\ntts_file_name:{tts_file_name}\nerror: {e}")
    return False

# Generate tts from google gTTS api or find audio file if exist from eleven labs with my voice


def generate_or_read_tts_11_labs(content='you forgot to put a content', voice_id='YEhWVRrlzrtA9MzdS8vE', tts_file_name='', folder="/Users/lgg/Downloads/news_podcasts"):
    if not folder:
        folder = "/Users/lgg/Downloads"
    if not tts_file_name:
        tts_file_name = f'{folder}/{str(datetime.now().strftime("%Y-%m-%d %H:%M:%S").split()[0])}_leo_voice.mp3'

    if os.path.isfile(tts_file_name):
        return tts_file_name
    characters_counts = len(content)
    # Additional usage-based characters at $0.30 per 1000 characters
    characters_costs = characters_counts * 0.30 / 1000
    if debug:
        print(
            f"DEBUG: 11_labs working for {tts_file_name.split('/')[-1]}, characters_counts: {characters_counts}, costs: {characters_costs:.3f}...")

    try:
        new_tts_file_name = ''
        new_tts_file_name = eleven_labs_tts(content, tts_file_name, voice_id)
        if debug:
            print(
                f"DEBUG: generate_or_read_tts_11_labs() new_tts_file_name : {new_tts_file_name}")
        if new_tts_file_name:
            return new_tts_file_name
    except Exception as e:
        print(
            f"ERROR: generate_or_read_tts_11_labs() eleven_labs_tts() FAILED. error: \n{e}")
        return


def get_search_results(key_words, working_folder='/Users/lgg/Downloads'):
    key_words = key_words.replace(' ', '+')
    url = f"https://lexica.art/api/v1/search?q={key_words}"
    response = requests.get(url)
    data = response.json()
    output_file = os.path.join(working_folder, f'{key_words}.json')

    with open(output_file, 'w') as f:
        json.dump(data, f)

    img_folder = os.path.join(working_folder, 'images')
    if not os.path.isdir(img_folder):
        os.mkdir(img_folder)

    for img in data.get('images'):
        img_url = img.get('src')
        img_prompt = img.get('prompt')
        img_width = str(img.get('width'))
        img_height = str(img.get('height'))
        img_model = img.get('model')
        img_seed = img.get('seed')

        # Download square images
        img_data = requests.get(img_url)
        img_path = os.path.join(
            img_folder, f'{"_".join(img_prompt.split()[:6]+[img_width, img_height])}.jpg')
        prompt_text_path = os.path.join(
            img_folder, f'{"_".join(img_prompt.split()[:6]+[img_width, img_height])}.txt')
        with open(img_path, 'wb') as img_file:
            img_file.write(img_data.content)
        with open(prompt_text_path, 'w') as prompt_file:
            prompt_file.write('\n'.join(
                [img_prompt, 'url: ' + img_url, 'model: ' + img_model, 'seed: ' + img_seed]))

    return True


def convert_mp3_to_wav(mp3_file_path):
    from pydub import AudioSegment
    wav_file_path = mp3_file_path.replace('.mp3', '.wav')
    # Load the mp3 file
    sound = AudioSegment.from_file(mp3_file_path)
    # Set the parameters for the output WAV file
    sample_width = 2  # 16-bit samples
    frame_rate = 16000  # 16 kHz
    # Convert the sound to a mono (single channel) AudioSegment
    sound = sound.set_channels(1)

    # Export the sound as a WAV file with the specified parameters
    sound.export(wav_file_path, format="wav", parameters=[
                 "-f", "wav", "-ac", "1", "-ar", "16000"])
    return wav_file_path


def microsoft_speech_recognition(audio_file_path):
    wave_file_path = convert_mp3_to_wav(audio_file_path)

    speech_config = speechsdk.SpeechConfig(subscription=os.getenv(
        'SPEECH_KEY'), region=os.getenv('SPEECH_REGION'))
    audio_config = speechsdk.AudioConfig(filename=wave_file_path)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config)

    result = speech_recognizer.recognize_once_async().get()
    return result.text


def microsoft_azure_tts(text, voice='zh-CN-YunxiNeural', output_filename='output.wav'):
    if debug: print(f"DEBUG: 正在进行中文语音合成...")
    if os.path.isfile(output_filename): return output_filename
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(subscription=os.getenv('SPEECH_KEY'), region=os.getenv('SPEECH_REGION'))
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True, filename=output_filename)

    # The language of the voice that speaks.
    speech_config.speech_synthesis_voice_name = voice
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted: 
        print(f"DEBUG: 中文语音合成成功, 保存到 {output_filename}...")
        return output_filename
    else: return False


def chunk_text(text, max_length=1500):
    import nltk
    nltk.download('punkt')

    sentences = nltk.sent_tokenize(text)
    chunks = []
    current_chunk = ''

    for sentence in sentences:
        if len(current_chunk.split()) + len(sentence.split()) > max_length:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
        else: current_chunk += ' ' + sentence

    chunks.append(current_chunk.strip())
    return chunks


def translate_txt_en_to_zh(filepath, video_url):
    if debug: print(f"DEBUG: translate_txt_en_to_zh() 开始翻译脚本并合成中文语音: {filepath.split('/')[-1]}")

    if filepath[-4:] in ['.wav', '.mp4']: filepath = filepath[:-4] + '.srt'

    if not filepath.endswith('.txt') and not filepath.endswith('.srt'): return False

    filepath_translated = filepath[:-4] + '_zh.txt'
    filepath_report = filepath[:-4] + '_report.txt'
    filepath_translated_wav = filepath[:-4] + '_zh.wav'

    text = ''
    # Replace 'example.txt' with the actual filepath of your file
    for line in read_lines(filepath):
        if not line or not line.strip() or '-->' in line or line.isnumeric(): continue
        text += line + ' '

    text = text.replace('\h', ' ').strip()
    text = text.replace('  ', ' ').strip()

    if not text: return False
    if not is_english(text): 
        print('ERROR: 该脚本不是英文脚本, 无需转录, 退出程序!')
        return False

    # if debug: print('DEBUG: 从英文脚本文件中读出全部脚本:\n\n', text)
    # if debug: print(f"DEBUG: ChatGPT 接下来会把以上英文脚本分段翻译成中文...")
    max_length = 1000

    chunks = chunk_text(text, max_length)
    if debug: print(f"DEBUG: 英文脚本脚本分成了 {len(chunks)} 个块, 每个块不超过 {max_length} 字符.")
    i = 0
    cn_wav_list = []
    for chunck_text in chunks:
        i += 1
        if debug: print(f"DEBUG: 正在翻译第 {i} 个 chunk, length: {len(chunck_text.split())} words: \n\n{chunck_text}")
        message = ''
        try: message = chat_gpt(f"You are an English and Chinese bilingual master, I will send an English transcript to you, it's transcripted from an audio, so the content might not accurate, so you need to read the context to correct it first and then translate the whole transcripted text into Chinese, but when it comes to short terms like LLM, NLP, keep it in that term, when it comes to names like John Wick, keep the name in English as well.:\n\n{chunck_text}", 'gpt-3.5-turbo')
        except Exception as e: print(f'ERROR: 第 {i} 个 chunk 英文脚本翻译成中文脚本失败, 退出程序!', e)

        if message: print(f"DEBUG: 第 {i} 个 chunk 英文脚本翻译成功...")
        else: return print(f'ERROR: 第 {i} 个 chunk 英文脚本翻译成中文脚本失败, 退出程序!', e)

        try:
            with open(filepath_translated, 'a') as f: f.write(message)
        except: return print(f'ERROR: 第 {i} 个 chunk 中文脚本加入文件失败, 退出程序!', e)

        try: 
            output_filename = microsoft_azure_tts(message, voice='zh-CN-YunxiNeural', output_filename=filepath[:-4] + f'_{i}_zh.wav')
            if os.path.isfile(output_filename): cn_wav_list.append(output_filename)
        except Exception as e: return print(f'ERROR: 第 {i} 个 chunk 中文脚本语音合成失败, 退出程序!', e)

    # 读出 filepath_translated 的 message 内容
    try:
        with open(filepath_translated, 'r') as f: message = f.read()
    except: return print('ERROR: 中文脚本读取失败, 退出程序!', e)

    # try: output_filename = microsoft_azure_tts(message, voice='zh-CN-YunxiNeural', output_filename=filepath_translated_wav)
    # except Exception as e: return print('ERROR: 中文脚本语音合成失败, 退出程序!', e)

    # 将 cn_wav_list 中的所有 wav 文件合并成一个 wav 文件
    try:
        sound = AudioSegment.from_wav(cn_wav_list[0])
        for wav_file in cn_wav_list[1:]:
            if debug: print(f"DEBUG: 正在将 {len(cn_wav_list)} 个中文语音文件合并成一个中文语音文件...")
            sound += AudioSegment.from_wav(wav_file)
        sound.export(filepath_translated_wav, format="wav")
        if not os.path.isfile(filepath_translated_wav): return print('ERROR: 中文语音文件合并失败, 退出程序!')
    except Exception as e: return print('ERROR: 中文语音文件合并失败, 退出程序!', e)

    # 删除 cn_wav_list 中的所有 wav 文件
    for wav_file in cn_wav_list:
        try: os.remove(wav_file)
        except Exception as e: print('ERROR: 删除中文语音文件失败, 继续执行程序...', e)

    if debug: print(f"DEBUG: 正在将中文脚本改写为视频中文简介...")
    cn_report = ''
    try: 
        cn_report = chat_gpt(f"你是一位资深的中文科技记者，你很擅长根据一段视频脚本重写一段独立的、有趣的、有价值的视频内容中文简介, 简介字数不超过 3000 汉字。请注意，这段脚本是从视频文件自动转录并翻译的，转录过程中可能会因为音频质量导致转录的文本出现各种各样的错误，也可能会有不通顺或者单词拼写错误，翻译的过程也可能出现信息误差。请根据全文的语境和上下文语义来理解修正这些错误，不要把错误的内容重写到你的视频简介中，请用中文创作。\n\n{message}", 'gpt-4')
        print(f"DEBUG: 视频中文简介改写成功, 进行保存...")
    except Exception as e: 
        print(f'ERROR: 视频中文简介改写失败, 继续执行程序...', e)
        return filepath_translated_wav

    cn_report = f"英文视频源链接: \n{video_url}\n\n视频内容简介:\n\n{cn_report}"
    
    try:
        with open(filepath_report, 'a') as f: f.write(cn_report)
    except Exception as e: print('ERROR: 保存视频中文简介失败', e)

    try: 
        send_message(text=cn_report, chat_id=BOTOWNER_CHAT_ID)
        if debug: print(f"DEBUG: 视频中文简介已发送到 Telegram...")
    except Exception as e: print('ERROR: 视频中文简介发送 Telegram 失败', e)
    
    return filepath_translated_wav


def microsoft_azure_tts_from_filepath(filepath):
    filepath_translated_wav = filepath.replace('.txt', '_zh.wav')

    i = 0
    # Read the input text from the file
    for line in read_lines(filepath):
        if not line or not line.strip():
            continue
        i += 1
        if debug:
            print(i, '原始内容:', line)

        try:
            output_filename = microsoft_azure_tts(
                line, voice='zh-CN-YunxiNeural')
            if os.path.isfile(filepath_translated_wav):
                # merge output_filename to filepath_translated_wav
                sound1 = AudioSegment.from_wav(filepath_translated_wav)
                sound2 = AudioSegment.from_wav(output_filename)
                combined_sounds = sound1 + sound2
                combined_sounds.export(filepath_translated_wav, format="wav")
            else:
                # copy output_filename to filepath_translated_wav
                os.rename(output_filename, filepath_translated_wav)
        except:
            print(f'合成失败 {str(i)}: ' + line)

    return


def merge_wav(output_filename):
    if debug:
        print(
            f"DEBUG: merge_wav() started to merging {output_filename.split('/')[-1]}")

    first_file = output_filename.replace('.wav', '_1.wav')

    sound = AudioSegment.from_wav(first_file)
    sound.export(output_filename, format="wav")

    # Replace 'example.txt' with the actual filepath of your file
    for i in range(2, 426):
        filepath = f'json_datas/openai_chatgpt_sam_interview/tts_content_zh_{str(i)}.wav'

        # merge output_filename to filepath_translated_wav
        sound1 = AudioSegment.from_wav(output_filename)
        sound2 = AudioSegment.from_wav(filepath)
        combined_sounds = sound1 + sound2
        combined_sounds.export(output_filename, format="wav")

    if debug:
        print(f"DEBUG: merge_wav() {output_filename} was merged successfully")
    return output_filename


def get_media_length(filepath):
    cmd = f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {filepath}"
    output = subprocess.check_output(cmd, shell=True, text=True)
    try:
        return float(output.strip())
    except ValueError:
        print(
            f"Warning: Could not extract duration for {filepath}. Returning 0.")
        return 0


def process_video(input_video, video_url):
    input_audio = input_video.replace('.mp4', '_zh.wav')
    output_video = input_video.replace('.mp4', '_fasten.mp4')

    if not os.path.isfile(input_video): 
        print(f"DEBUG: 视频文件读取错误 {input_video}.")
        return

    if not os.path.isfile(input_audio):
        print(f"DEBUG: 现有文件夹中找不到中文音频文件, 开始尝试翻译英文脚本并生成中文音频.")
        input_audio = translate_txt_en_to_zh(input_video, video_url)
        if not input_audio or not os.path.isfile(input_audio): 
            print(f"DEBUG: 翻译英文脚本并生成中文音频失败, 退出程序!")
            return 

    video_length = get_media_length(input_video)
    audio_length = get_media_length(input_audio)
    if not video_length or not audio_length: 
        print(f"DEBUG: 视频或音频文件的长度读取错误 {input_video} {input_audio}, 退出程序!")
        return

    speed_factor = audio_length / video_length

    cmd = f'ffmpeg -i "{input_video}" -i "{input_audio}" -filter_complex "[0:a]volume=0.1[lv];[0:v]setpts={speed_factor}*PTS[v];[lv][1:a]amix=inputs=2[outa]" -map "[v]" -map "[outa]" -c:v libx264 -preset ultrafast -c:a aac "{output_video}"'
    subprocess.run(cmd, shell=True, check=True)

    return output_video


def convert_vtt_to_srt(working_folder='/Users/lgg/Downloads'):
    if debug: print(f"DEBUG: convert_vtt_to_srt() 查找 vtt 字幕文件并转换为 srt 字幕文件...")

    latest_vtt_file = get_latest_file_in_folder(working_folder, '.vtt')
    if not latest_vtt_file: return

    latest_mp4_file = get_latest_file_in_folder(working_folder, '.mp4')
    if not latest_mp4_file: return

    srt_file_path = latest_mp4_file.replace('.mp4', '.srt')

    command = f'ffmpeg -i "{latest_vtt_file}" -c:s srt "{srt_file_path}"'
    subprocess.run(command, shell=True, check=True)
    os.remove(latest_vtt_file)
    
    if debug: print(f"DEBUG: vtt 字幕文件成功转换为 srt 字幕文件!")
    return srt_file_path


def download_youtube_video(video_url, working_folder='/Users/lgg/Downloads'):
    if not video_url.startswith('https://www.youtube.com/watch?v='): video_url = f'https://www.youtube.com/watch?v={video_url}'
    if debug: print(f"DEBUG: download_youtube_video() 正在下载视频 {video_url}")

    # 将 video_url 保存到 working_folder 中的 today_video_url.txt 文件中
    today_video_url_file = os.path.join(working_folder, 'today_video_url.txt')
    with open(today_video_url_file, 'w') as f: f.write(video_url)
    
    command = f'yt-dlp -f bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4] --write-sub --sub-format best --output "{working_folder}/%(title)s.%(ext)s" {video_url}'

    subprocess.run(command, shell=True, check=True)
    if debug: print(f"DEBUG: download_youtube_video() 视频下载成功!")

    r = remove_punctuation(working_folder)
    if not r: return

    srt_file_path = get_latest_file_in_folder(working_folder, '.srt')
    if not srt_file_path: srt_file_path = convert_vtt_to_srt(working_folder)
    else: print(f"DEBUG: 文件夹中已经存在 srt 字幕文件, 接下来直接进行翻译!")

    return srt_file_path


def polish_srt(filepath):
    if debug:
        print(
            f"DEBUG: polish_srt() started to polash: {filepath.split('/')[-1]}")

    if not filepath.endswith('.txt') and not filepath.endswith('.srt'):
        return False

    polished_file = filepath[:-4] + '_polished.txt'

    text = ''
    # Replace 'example.txt' with the actual filepath of your file
    for line in read_lines(filepath):
        if not line or not line.strip() or '-->' in line or line.isnumeric():
            continue

        if debug:
            print('DEBUG: ', line)

        text += line + ' '

    text = text.replace('\h', ' ').strip()
    text = text.replace('  ', ' ').strip()

    if not text:
        return False

    try:
        with open(polished_file, 'w') as f:
            f.write(text)
    except:
        return False


if __name__ == "__main__":
    print(f"DEBUG: __main__ started", str(
        datetime.now().strftime("%Y-%m-%d %H:%M:%S").split()[0]))
