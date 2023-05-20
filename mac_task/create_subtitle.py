from main import *


def create_news_subtitle(filepath_en='/Users/lgg/Downloads/news_podcasts/Runway_gen_1_en.srt', split_number=17):
    if not os.path.isfile(filepath_en): return
    filepath_cn= filepath_en.replace('_en.srt', '_cn.srt')
    if not os.path.isfile(filepath_cn): return

    system_prompt = '''
You are a very experienced movie editer, as well as a biligual master, you speak both English and Chiese very well. I'm about to send you a video subtile content, first part is English, second part is Chinese, together with the timeline. 

The Chinses subtitle was translated by some stupid mechine, sometimes the mechine don't understand where it's an English word or a product name or human name, they even translated the famerous product name or brand name into Chinese, which totally make no sense. The stupid mechine was translating line by line, which make the Chinese subtitle reads wield when you link the line together.

You will help me to check if the Chinese version was making any sense, for the part make no sense, you will revise it for me, for example, Stable Diffusion is a product name, so no need to be translated into '稳定扩散'. So you need to revise the 稳定扩散 back to Stable Diffusion. Another example, see below subtiles:

13
00:00:36,253 --> 00:00:40,342
生成式人工智能的进步 一、视频生成
forward in generative AI gen One, a video generation

14
00:00:40,343 --> 00:00:43,216
能够在任何情况下有效生成视频的人工智能系统
AI system that can efficiently generate video in any

15
00:00:43,217 --> 00:00:46,830
风格，同时保留了质量和灵活性。
style, all while retaining quality and flexibility.

it's very obious that: 能够在任何情况下有效生成视频的人工智能系统风格，同时保留了质量和灵活性。 Sounds wield, shoule be revised to:

14
00:00:40,343 --> 00:00:43,216
能够在任何情况下有效生成格式风格视频的人工智能系统
AI system that can efficiently generate video in any

15
00:00:43,217 --> 00:00:46,830
同时保留了质量和灵活性。
style, all while retaining quality and flexibility.

After everthing is revised, you will reply me the new version of Chinese subtitle, if your virsion is better than the mechine, I will use your version to generate AI audio voice, if not, I will use the mechine version instead.:


'''

    user_prompt = '''
1
00:00:01,130 --> 00:00:04,474
Image generation models have taken the world by storm.

2
00:00:04,475 --> 00:00:06,772
It's now possible for anyone to turn their

3
00:00:06,773 --> 00:00:10,548
ideas into images using nothing but words.

4
00:00:10,549 --> 00:00:12,698
The explosion of creativity these models

5
00:00:12,699 --> 00:00:15,040
unleashed was years in the making.

6
00:00:15,570 --> 00:00:19,162
In 2021, Runway introduced Latent Diffusion, an AI

7
00:00:19,163 --> 00:00:21,466
system that was able to generate realistic images

8
00:00:21,467 --> 00:00:24,308
using an improved image generation technique and in

9
00:00:24,309 --> 00:00:27,724
2022, Stable Diffusion, a further improved version of

10
00:00:27,725 --> 00:00:29,708
latent diffusion that caused a tidal wave of

11
00:00:29,709 --> 00:00:32,600
creativity and mass adoption of the technology.

12
00:00:33,370 --> 00:00:36,252
Today, Runway is excited to introduce the next step

13
00:00:36,253 --> 00:00:40,342
forward in generative AI gen One a video generation

14
00:00:40,343 --> 00:00:43,216
AI system that can efficiently generate video in any

15
00:00:43,217 --> 00:00:46,830
style, all while retaining quality and flexibility.

1
00:00:01,130 --> 00:00:04,474
图像生成模型已经在世界范围内掀起了风暴。

2
00:00:04,475 --> 00:00:06,772
现在任何人都有可能将他们的

3
00:00:06,773 --> 00:00:10,548
只用文字就能把想法变成图像。

4
00:00:10,549 --> 00:00:12,698
这些模型的创造力的爆发

5
00:00:12,699 --> 00:00:15,040
释放出来的是多年来的成果。

6
00:00:15,570 --> 00:00:19,162
2021年，Runway推出了Latent Diffusion，一种AI

7
00:00:19,163 --> 00:00:21,466
能够生成逼真图像的系统

8
00:00:21,467 --> 00:00:24,308
使用改进的图像生成技术，在

9
00:00:24,309 --> 00:00:27,724
2022年，"稳定扩散 "是一个进一步改进的版本。

10
00:00:27,725 --> 00:00:29,708
潜移默化的扩散，造成了一个潮汐式的

11
00:00:29,709 --> 00:00:32,600
创造性和大规模采用该技术。

12
00:00:33,370 --> 00:00:36,252
今天，Runway很高兴地介绍下一个步骤

13
00:00:36,253 --> 00:00:40,342
生成式人工智能的进步 一、视频生成

14
00:00:40,343 --> 00:00:43,216
能够在任何情况下有效生成视频的人工智能系统

15
00:00:43,217 --> 00:00:46,830
风格，同时保留了质量和灵活性。

'''

    assistant_prompt = '''
1
00:00:01,130 --> 00:00:04,474
图像生成模型已经在世界范围内掀起了风暴。
Image generation models have taken the world by storm.

2
00:00:04,475 --> 00:00:06,772
现在，任何人都有可能只通过文字
It's now possible for anyone to turn their

3
00:00:06,773 --> 00:00:10,548
就能把他们的想法变成图像。
ideas into images using nothing but words.

4
00:00:10,549 --> 00:00:12,698
这些模型释放出来的创造力的大爆发
The explosion of creativity these models

5
00:00:12,699 --> 00:00:15,040
是多年来积累的成果。
unleashed was years in the making.

6
00:00:15,570 --> 00:00:19,162
2021年，Runway 推出了 Latent Diffusion，
In 2021, Runway introduced Latent Diffusion, an AI

7
00:00:19,163 --> 00:00:21,466
一种使用改进的图像生成技术，
system that was able to generate realistic images

8
00:00:21,467 --> 00:00:24,308
能够生成逼真图像的人工智能系统
using an improved image generation technique and in

9
00:00:24,309 --> 00:00:27,724
2022年，一个基于 Latent Diffusion 进一步改进的版本
2022, Stable Diffusion, a further improved version of

10
00:00:27,725 --> 00:00:29,708
Stable Diffusion 导致了创造性潮汐式的大爆发
latent diffusion that caused a tidal wave of

11
00:00:29,709 --> 00:00:32,600
市场开始大规模采用该技术。
creativity and mass adoption of the technology.

12
00:00:33,370 --> 00:00:36,252
今天，Runway 很高兴地介绍下一个生成式人工智能的进步：
Today, Runway is excited to introduce the next step

13
00:00:36,253 --> 00:00:40,342
Gen One，一个视频生成系统，
forward in generative AI: Gen One, a video generation

14
00:00:40,343 --> 00:00:43,216
能够在任何情况下有效生成各式风格视频的人工智能系统
AI system that can efficiently generate video in any style

15
00:00:43,217 --> 00:00:46,830
同时保留了视频质量和灵活性。
while retaining quality and flexibility.
'''

    dynamic_model = 'gpt-4'
    chatgpt_key = OPENAI_API_KEY

    try: 
        with open(filepath_en, 'r') as f: subtitle_en = f.read()
    except: return

    try: 
        with open(filepath_cn, 'r') as f: subtitle_cn = f.read()
    except: return

    en_split_list = subtitle_en.split(str(split_number))
    cn_split_list = subtitle_cn.split(str(split_number))

    final_subtitles = []

    for i in range(len(en_split_list)):
        en_split = en_split_list[i].strip()
        cn_split = cn_split_list[i].strip()
        prompt = '\n\n'.join([en_split, cn_split])

        message = ''
        try: message = chat_gpt_full(prompt, system_prompt, user_prompt, assistant_prompt, dynamic_model, chatgpt_key)
        except Exception as e: print('ERROR: chat_gpt_full() failed:', e)
        if not message: return message

        final_subtitles.append(message)

    filepath_combined = ''
    try:
        filepath_combined = filepath_en.replace('_en.srt', '_combined.srt')
        with open(filepath_combined, 'w') as f: f.write('\n\n'.join(final_subtitles))
    except Exception as e: print('ERROR: writing to file failed:', e)

    # if filepath_news:
    #     filepath_news_mp3 = filepath_news.replace('.txt', '.mp3')
    #     filepath_news_mp3 = generate_or_read_tts_11_labs(content = message, voice_id='YEhWVRrlzrtA9MzdS8vE', tts_file_name=filepath_news_mp3, folder = "/Users/lgg/Downloads/news_podcasts")
    #     # microsoft_azure_tts(message, voice='zh-CN-YunxiNeural', output_filename='output.wav')
    #     return filepath_news_mp3

    return filepath_combined

if __name__ == "__main__":
    print(f"DEBUG: create_wav.py started")

    filepath_combined = create_news_subtitle(filepath_en='/Users/lgg/Downloads/news_podcasts/Runway_gen_2_en.srt', split_number=17)
    print(f"DEBUG: {filepath_combined} was created successfully")
