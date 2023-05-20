from main import *


def create_podcast_wav_1():

    filepath = input("请输入文件路径，或者输入 n 使用 Download 文件夹的最新 .srt 文件: \n")
    if filepath == 'n': filepath = get_latest_file_in_folder('/Users/lgg/Downloads', '.srt')
    
    if not '/' in filepath: filepath = f'/Users/lgg/Downloads/{filepath}'
    if not '.txt' in filepath and not '.srt' in filepath: 
        for extention in ['.txt', '.srt']:
            if os.path.isfile(filepath + extention): filepath += extention

    if os.path.isfile(filepath): 
        print(f"DEBUG: {filepath} was found successfully")

        filepath_list = rename_target_file(filepath)
        for filepath in filepath_list:
            if '.srt' not in filepath and '.txt' not in filepath: continue

            filepath_translated = translate_txt_en_to_zh(filepath)

            if not filepath_translated: print(f"ERROR: translate_txt_en_to_zh() failed to translate {filepath}")
            else: print(f"DEBUG: translate_txt_en_to_zh() {filepath_translated} was created successfully")
    return filepath_translated

def copy_latest_snippet(remote_host = "root@47.91.25.101", remote_directory = "/root/major/json_datas/bing_search/*_snippet.txt", local_directory = "/Users/lgg/Downloads/news_podcasts/"):
    
    # SSH into the remote server, list files, and get the latest file
    find_latest_file_cmd = f"ssh {remote_host} 'ls -t {remote_directory}' | head -1"
    latest_file = subprocess.check_output(find_latest_file_cmd, shell=True, text=True).strip()

    # Extract the file name from the remote path
    file_name = os.path.basename(latest_file)

    # Construct the local file path
    local_file_path = os.path.join(local_directory, file_name)

    # check if the file already exists
    if os.path.isfile(local_file_path): return

    # Copy the latest file to the local directory
    scp_cmd = f"scp {remote_host}:{latest_file} {local_file_path}"
    subprocess.run(scp_cmd, shell=True, check=True)

    # Return the local file path
    return local_file_path

def create_news_podcast():

    filepath = copy_latest_snippet(remote_host = "root@47.91.25.101", remote_directory = "/root/major/json_datas/bing_search/*_snippet.txt", local_directory = "/Users/lgg/Downloads/news_podcasts/")
    if not filepath: return

    prompt = ''
    try: 
        with open(filepath, 'r') as f: prompt = f.read()
    except Exception as e: print(f"ERROR: Can not open {filepath}: {e}")
    if not prompt: return

    system_prompt = '''
You are a very experiend news editor and report, you can easly create a news based on google search results. You don't need to click and read every article from google search results, you can simply read the snippets from google results and then you can create a news article based on the snippets. And it's allway eye catching, interesting and amazing. As a report, you know the truth is important, so you don't just make things up, you write based on the snippets, and you don't exaggerate the news, you just write the truth but in a very interesting way. The article will be read using an AI voice generator chosen by your boss, it's important to carefully choose words that are easy to pronounce. This is particularly important for technical terms, where using the full word is more helpful. For instance, instead of using V5 as an abbreviation for Version 5, it's better to write out the full term. Similarly, if you're unsure if readers are familiar with the term LLM, it's better to use the full term Large Language Model instead of the abbreviation. Even with the article title, you do the same. But remember, you don't need to put 'Title' for the beginning of the title. If you're unsure whether an AI voice generator can accurately read a special character, it's best to replace it with a word. For instance, the character / can be written as slash.
'''

    user_prompt = '''
Today's top news about  midjourney v5

1. Newest Model. The Midjourney V5 model is the newest and most advanced model, released on March 15th, 2023. To use this model, add the v 5 parameter to the end of a prompt, or use the slash settings command and select MJ Version 5. This model has very high Coherency, excels at interpreting natural language prompts, is higher resolution, and supports advanced features like repeating ...

2. Midjourney v4 vs Midjourney v5 The fifth edition is a significant improvement, especially when it comes to creating wellknown figures from popular culture. The distinction is most noticeable when the neural network attempts to depict a realistic scene, such as an image, landscape, or indoor space.

3. About. . Midjourney is an independent research lab exploring new mediums of thought and expanding the imaginative powers of the human species. We are a small selffunded team focused on design, human infrastructure, and AI. We have 11 fulltime staff and an incredible set of advisors.

4. MidJourney, the widely popular AIpowered image generator, has just launched its latest version, MidJourney V5. MidJourney decided to drop V5 just a day after OpenAI released GPT4. Crazy week for…

5. To set Midjourney v5 as default, use the /settings command to access your Midjourney settings and then select MJ version 5. To temporarily use Midjourney v5 without setting it as default, use the –v 5 parameter. March 31, 2023: With Midjourney closing for free users, you may want to give BlueWillow a try. Available on Discord, too, it’s ...

6. Midjourney v5 leaps out in front of v4 in the overall visual experience. In v5, we completely lose the "Midjourney look". The new v5 could easily be considered another universe, both in terms of photorealism and details. One of the key factors is a boost in dynamic range that's widely abundant in Midjourney v5 imagery.

7. Midjourney V5. V5 is the latest iteration of Midjourney. It is most definitely better than all its previous versions. For a bit of context, Midjourney released the 5th version a week ago, but it is only in its beta mode now. The V5 is considered more enhanced and powerful than its previous version. For example, it draws a line between artwork ...

8. Style and prompting for V5.  Today’s test is basically a ‘pro’ mode of the model.  It’s MUCH more ‘unopinionated’ than v3 and v4, and is tuned to provide a wide diversity of outputs and to be very responsive to your inputs.  The tradeoff here is that it may be harder to use.

9. Midjourney V5’s system default is the photographic style. It’s what shows up if the prompter does not specify any other styling. In v 5, to generate something other than a photographic image, you will need to reference art movements, artistic techniques, genres, media types, games titles, ...

10. Midjourney is an industry leader in AI generative art. With each new version, it manages to increasingly blur the lines between reality and fantasy. Thanks to ongoing development in algorithms that serve to boost photorealism and dynamic range,

11. На примерах в шапке: Скоро и айфон подруге не нужно будет покупать, можно будет промтом обойтись. Больше интересного у меня в телеге:

12. Make photorealistic images with Midjourney v5, the texttoimage AI that bamboozled the internet with the Pope photo.

13. Make photorealistic images with Midjourney v5, the texttoimage AI that bamboozled the internet with the Pope photo.

14. The problem is, Midjourney is too good. And, the lack of moderation policies makes its case even more concerning
'''

    assistant_prompt = '''
Midjourney Version 5 Revolutionizes AI-Powered Image Generation

In the world of AI-powered image generation, Midjourney has just released its most advanced model yet, the Midjourney Version 5. Launched on March 15, 2023, this new model has raised the bar in terms of coherency, natural language prompt interpretation, and resolution, supporting advanced features that users have come to expect from the industry leader.

The Midjourney Version 5 model significantly surpasses its predecessor, Midjourney Version 4, in creating lifelike depictions of popular culture figures and realistic scenes, including landscapes and indoor spaces. The visual experience offered by Version 5 has been completely transformed, with the "Midjourney look" being replaced by enhanced photorealism and intricate details, thanks in part to a substantial boost in dynamic range.

Midjourney, an independent research lab with 11 full-time staff members, has a mission to explore new mediums of thought and expand human imagination through design, human infrastructure, and AI. Their latest version, currently in beta mode, is a testament to their commitment to innovation and pushing the boundaries of what AI can do.

The Midjourney Version 5 also offers a more versatile and responsive experience for users. The model's 'pro' mode provides a wider diversity of outputs and adapts more readily to user inputs, though this may make it somewhat harder to use. The system default for Version 5 is the photographic style, with options for generating images in different styles by referencing art movements, techniques, genres, and media types.

As an industry leader in AI generative art, Midjourney continues to blur the lines between reality and fantasy with each new iteration. However, some have voiced concerns over the platform's lack of moderation policies, given its growing ability to create stunningly photorealistic images, such as the now-famous Pope photo.

Users can try Midjourney Version 5 by adding the "v 5" parameter to the end of a prompt or by selecting "MJ Version 5" in the settings. While the platform has closed for free users, the AI-powered image generator BlueWillow is available as an alternative for those seeking a similar experience on Discord.
'''

    dynamic_model = 'gpt-4'
    chatgpt_key = OPENAI_API_KEY
    
    message = ''
    try: message = chat_gpt_full(prompt, system_prompt, user_prompt, assistant_prompt, dynamic_model, chatgpt_key)
    except Exception as e: print('ERROR: chat_gpt_full() failed:', e)
    if not message: return message

    filepath_news = ''
    try:
        filepath_news = filepath.replace('_snippet.txt', '_news.txt')
        with open(filepath_news, 'w') as f: f.write(message)
    except Exception as e: print('ERROR: writing to file failed:', e)

    if filepath_news:
        filepath_news_mp3 = filepath_news.replace('.txt', '.mp3')

        # 英文女生
        azure_voice = 'en-US-JaneNeural'
        filepath_news_mp3 = microsoft_azure_tts(message, voice=azure_voice, output_filename=filepath_news_mp3)

        # filepath_news_mp3 = generate_or_read_tts_11_labs(content = message, voice_id='YEhWVRrlzrtA9MzdS8vE', tts_file_name=filepath_news_mp3, folder = "/Users/lgg/Downloads/news_podcasts")
        # microsoft_azure_tts(message, voice='zh-CN-YunxiNeural', output_filename='output.wav')
        return filepath_news_mp3

    return

if __name__ == "__main__":
    print(f"DEBUG: create_wav.py started")

    filepath_news_mp3 = create_news_podcast()
    print(f"DEBUG: {filepath_news_mp3} was created successfully")
