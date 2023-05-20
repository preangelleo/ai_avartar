from main import *
from playsound import playsound


def create_leo_english_voice(voice_folder="/Users/lgg/Downloads/Leo_English_Voices"):

    while True:
        print("本程序会将 /Users/lgg/Downloads/Leo_English_Voices/text_voice.txt 内的文本读出并生成相应的音频文件.")

        chose_command = input("\n请输入您要执行的命令: \n\n1. 输入英文并直接生成 Leo Voice 英文音频；\n2. 输入中文，由 ChatGPT 翻译后再生成 Leo Voice 英文音频；\n3. 输入英文，由 ChatGPT 修改后再生成 Leo Voice 英文音频；\n4. 输入英文并直接通过 Azure 生成英文音频，女声；\n5. 输入中文并通过 Azure 生成中文音频，男声；\n6. 输入中文并通过 ChatGPT 翻译后再生成英文音频，女声；\n7. 输入英文并经过 ChatGPT 修改后再生成英文音频，女声；\n0. 退出菜单（或者任意键退出程序）\n\n")

        if chose_command.lower() not in ['1', '2', '3', '4', '5', '6', '7']: break

        # open '/Users/lgg/Downloads/Leo_English_Voices/text_voice.txt' and read to message
        with open('/Users/lgg/Downloads/Leo_English_Voices/text_voice.txt', 'r') as f:  message = f.read()
        if not message: continue

        prompt = f"Translate below Chinese to vocal English like a native speaker and reply only the translation result, nothing else: \n\n{message}" if chose_command in ['2', '6'] else f"Revise below text to vocal English like a native speaker and reply only the revised result, nothing else: \n\n{message}" if chose_command in ['3', '7'] else ''

        english_msg = chat_gpt_regular(prompt, use_model='gpt-4', chatgpt_key=OPENAI_API_KEY) if prompt else message

        print(f"STEP 1: 正在将以下内容会生成合成语音: \n\n{english_msg}")

        if chose_command in ['5']:
            azure_voice = 'zh-CN-YunxiNeural'
            for i in range(3, len(english_msg)):
                filepath_mp3 = f"{voice_folder}/{english_msg[:i]}.mp3"
                if not os.path.isfile(filepath_mp3): break
        else:
            azure_voice = 'en-US-SaraNeural' 
            for i in range(3, len(english_msg.lower().split())):
                filepath_mp3 = f"{voice_folder}/{'_'.join(english_msg.lower().split()[:i])}.mp3"
                if not os.path.isfile(filepath_mp3): break

        print(f"STEP 2: 合成语音文件路径: {filepath_mp3}")

        filepath_new = generate_or_read_tts_11_labs(content=english_msg, voice_id='YEhWVRrlzrtA9MzdS8vE', tts_file_name=filepath_mp3, folder=voice_folder) if chose_command in [
            '1', '2', '3'] else microsoft_azure_tts(english_msg, voice=azure_voice, output_filename=filepath_mp3) if chose_command in ['4', '5', '6', '7'] else ''

        if filepath_new: print('STEP 3: 成功合成 AI 语音: ', filepath_new)
        else: print("ERROR: AI 语音合成失败.")
        


if __name__ == "__main__":
    print(f"DEBUG: create_wav.py started")

    file_path = '/Users/lgg/Downloads/Leo_English_Voices/text_voice.txt'
    subprocess.call(['open', '-a', 'Sublime Text', file_path])

    try:
        create_leo_english_voice(
            voice_folder="/Users/lgg/Downloads/Leo_English_Voices")
    except Exception as e:
        print("ERROR: \n\n", e)
