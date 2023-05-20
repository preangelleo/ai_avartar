from main import *

# Generating img based on replicate api


def generative_ai_replicate(prompt, folder, filename, seed=5357, steps=45, scale=9, num=1, model_name='midjourney', negative=False):
    if not filename or not folder:
        return

    if debug:
        print(f"DEBUG: generative_ai_replicate()")
    prompt = prompt.lower()

    os.environ["REPLICATE_API_TOKEN"] = os.getenv('REPLICATE')

    inputs = {
        # Input prompt
        'prompt': prompt,

        # Specify things to not see in the output
        # 'negative_prompt': ...,

        # Width of output image. Maximum size is 1024x768 or 768x1024 because
        # of memory limits
        'width': 1024,

        # Height of output image. Maximum size is 1024x768 or 768x1024 because
        # of memory limits
        'height': 576,

        # Number of images to output.
        # Range: 1 to 4
        'num_outputs': 1,

        # Number of denoising steps
        # Range: 1 to 500
        'num_inference_steps': 50,

        # Scale for classifier-free guidance
        # Range: 1 to 20
        'guidance_scale': 7.5,

        # Random seed. Leave blank to randomize the seed
        # 'seed': ...,
    }

    if seed:
        inputs['seed'] = seed
    if steps:
        inputs['num_inference_steps'] = steps
    if scale:
        inputs['guidance_scale'] = scale
    if num:
        inputs['num_outputs'] = num
    if negative:
        inputs['negative_prompt'] = negative

    if model_name == 'midjourney':
        inputs['prompt_strength'] = 0.8
        inputs['scheduler'] = 'DPMSolverMultistep'

    output = replicate.run(
        "tstramer/midjourney-diffusion:436b051ebd8f68d23e83d22de5e198e0995357afef113768c20f0b6fcef23c8b",
        input=inputs
    )

    file_path = f"{folder}/{filename}.png"
    urlretrieve(output[0], file_path)

    return file_path


def create_story_images(story_file_name, folder='/Users/lgg/Downloads/stories'):
    # story_file='/Users/lgg/Downloads/stories/20230404_182710_The_Golden_Treasure.txt'
    story_file = f"{folder}/{story_file_name}"

    with open(story_file, 'r') as f:
        story = f.read()

    system_prompt = '''
You are the best prompt generator for Midjourney's AI program, your job is creating detailed and imaginative descriptions to inspire unique images. Read the provided story thoroughly to understand its context, then generate concise prompts (under 100 words) for each paragraph. Ensure consistency and coherence throughout the prompts, which will be used to create images corresponding to the story's paragraphs. Remember, avoid using character names, instead using general terms like boy, old man, girl, or woman. Output the prompts only, labeled as Prompt_0: for the title, Prompt_1: for the first paragraph, and so on.
'''

    user_prompt = '''
The Golden Treasure

In a small village, nestled between two mountains, lived a poor but content family. They were old Lars, his wife Marianne, and their son Erik. They lived in a humble cottage by the woods and grew their own vegetables on a small plot of land. Life was simple, but there was a sense of peace and happiness in their home.

One day, Erik overheard some villagers talking about a hidden chamber inside the tallest mountain, at the top of which dwelt an enchanted bird called the Golden Songbird. This bird was said to bring good fortune and prosperity to anyone who could find it and persuade the bird to sing its magical song.

With curiosity racing through his mind, Erik decided to search for this fabled bird. He told his parents about his quest, and although Lars and Marianne were skeptical, they knew that their son's adventurous spirit would only grow stronger if they tried to dissuade him. 

So, with a heavy heart and full of blessings from his parents, Erik set out on his journey. He trekked through the dense forests and climbed the steep mountain paths. As he climbed higher, the air grew colder and the journey more treacherous. Yet Erik's determination never wavered, for he was driven by the hope of finding the Golden Songbird and bringing prosperity to his family.

After several days of strenuous travel, Erik finally reached the summit of the mountain and discovered a cave filled with the most beautiful crystal formations. As Erik ventured further into the chamber, he saw a magnificent cage, within which sat the Golden Songbird. As the light from the crystals reflected on its golden feathers, the small room dazzled with a mesmerizing light.

Erik approached the cage and spoke gently to the bird, "Oh, mighty Golden Songbird, I have come from afar to hear your magical song. I wish to bring prosperity to my family and my village."

The Golden Songbird cocked its head towards Erik and said, "Many have come before you, desiring the same. But to hear my song, you must prove your worthiness by passing three tests."

Erik bravely nodded and agreed to take on the challenges. The first test, the bird explained, was to be an act of kindness. Erik descended the mountain and aided an elderly woman in gathering her belongings which had fallen from her carriage. The second test was an act of courage. Erik saved a young boy who had wandered into the forest and was threatened by a wild wolf. The third test was an act of wisdom. Erik spent days helping the village leaders to find a peaceful resolution to a longstanding land dispute among the farmers.

With the tests completed, Erik returned to the summit of the mountain and told the Golden Songbird of his deeds. The Songbird, impressed by Erik's noble acts, nodded in approval.

"Very well, Erik," said the bird, "I shall now sing the song that you so eagerly seek."

The Golden Songbird's melodious voice filled the chamber and cast a radiant glow on the sparkling crystals. As the enchanting music echoed through the air, Erik felt an overwhelming sense of joy and fulfillment.

When the song came to an end, the Songbird spoke, "Remember, my dear boy, the true treasure lies not in gold or riches, but in the acts of kindness, courage, and wisdom that one performs in their life."

With newfound wisdom, Erik thanked the Golden Songbird and began his journey back to his village. As he walked through the forest, he realized that the bird had granted him a greater treasure than gold - the understanding that a heart full of love, courage, and wisdom would outshine even the brightest material wealth.

From that day forward, Erik, along with the entire village, gained a deeper appreciation for what truly mattered in life. And as for the Golden Songbird, it continued to reside high up on the mountain, where its magical song could still be heard, reminding all who listened of the golden treasure that lay within them.
'''

    assistant_prompt = '''
Prompt_0:
A whimsical, sentimental cartoon scene featuring the captivating and mysterious Golden Treasure.

Prompt_1:
A tranquil village cradled by mountains, featuring a cozy cottage, loving family tending their vibrant vegetable garden, and a backdrop of content villagers amidst whimsical homes.

Prompt_2:
A quaint village near the tallest mountain, with a hidden chamber housing the enchanting Golden Songbird, known to bring fortune and prosperity through its magical song.

Prompt_3:
A boy talking about a fabled bird with his parents, eyes full of desire, showcasing his adventurous spirit.

Prompt_4:
A boy embarking on a challenging journey, climbing steep mountain paths and trekking through dense forests, driven by his determination to find the Golden Songbird.

Prompt_5:
A boy discovering a crystal-filled cave at the mountain's summit, where a mesmerizing light illuminates the magnificent Golden Songbird in its cage.

Prompt_6:
A boy speaking to the Golden Songbird, asking for the chance to hear its magical song to bring prosperity to his family and village.

Prompt_7:
A boy performing acts of kindness, courage, and wisdom to pass the Golden Songbird's tests, helping people in the village and overcoming difficult situations.

Prompt_8:
A boy standing before the Golden Songbird, confidently sharing the details of his noble deeds to prove his worthiness.

Prompt_9:
The Golden Songbird singing its enchanting song in the crystal chamber, casting a radiant glow and filling Erik with a deep sense of joy and fulfillment.

Prompt_10:
A boy gaining wisdom from the Golden Songbird, understanding the true treasures in life, and feeling grateful for the experience.

Prompt_11:
A boy returning to his village, with a newfound appreciation for life and love, and the entire village experiencing transformation through the Golden Songbird's wisdom.

Prompt_12:
The Golden Songbird remaining atop the mountain, with its magical song echoing through the air, reminding all who listened of the golden treasure that lay within them.
'''

    try:
        message = chat_gpt_full(f"{story}", system_prompt, user_prompt,
                                assistant_prompt, dynamic_model='gpt-4', chatgpt_key=OPENAI_API_KEY)
    except Exception as e:
        return e

    prompt_file = story_file.replace('.txt', '_prompt.txt')
    with open(prompt_file, 'w') as f:
        f.write(message)

    # prompt_suffix = "fairytale , matte painting, highly detailed, dynamic lighting, cinematic, realism, realistic, photo real, sunset, high contrast, denoised, centered, michael whelan"
    # story_paragraphs_list = message.split('\n')
    # i = 0
    # for story_paragraph in story_paragraphs_list:
    #     if len(story_paragraph.strip('\n').strip()) > 0:
    #         i += 1
    #         print(f"story_paragraph: {story_paragraph}")
    #         filename = f"{story_file_name.replace('.txt', f'_{str(i)}')}"

    #         try: generative_ai_replicate(f"{story_paragraph}, {prompt_suffix}", folder, filename, seed=5357, steps=45, scale=9, num=1, model_name = 'midjourney', negative=False)
    #         except Exception as e: print(f"ERROR: paragraph {i} {e}")

    return prompt_file


def merge_cover_with_audio(cover_filepath):
    if not cover_filepath:
        return
    if not os.path.isfile(cover_filepath):
        return

    audio_path = f"{os.path.splitext(cover_filepath)[0]}.mp3"

    # Crop the cover image to 1280x720 and save it as a new file
    os.system(
        f'ffmpeg -i {cover_filepath} -vf "crop=\'min(iw\,ih*16/9):min(ih\,iw*9/16)\',scale=1280:720" -y {cover_filepath}')
    # Create a 1:1 ratio image and save it as cover_1v1.png
    os.system(
        f'ffmpeg -i {cover_filepath} -vf "crop=\'min(iw\,ih)\':\'min(iw\,ih)\'" -vframes 1 {os.path.splitext(cover_filepath)[0]}_1v1.jpg')
    # Merge the cover image with the audio file
    # os.system(f'ffmpeg -loop 1 -i {cover_filepath} -i {audio_path} -c:v libx264 -preset slow -crf 18 -c:a aac -shortest {os.path.splitext(cover_filepath)[0]}.mp4')
    os.system(
        f'ffmpeg -loop 1 -i {cover_filepath} -i {audio_path} -c:v libx264 -profile:v high -level:v 4.2 -crf 23 -preset slow -pix_fmt yuv420p -c:a aac -b:a 192k -shortest {os.path.splitext(cover_filepath)[0]}.mp4')

    return True


def merge_cover_with_audio_zh(cover_filepath):
    if not cover_filepath:
        return
    if not os.path.isfile(cover_filepath):
        return

    audio_path = f"{os.path.splitext(cover_filepath)[0]}_zh.wav"

    # Merge the cover image with the audio file
    # os.system(f'ffmpeg -loop 1 -i {cover_filepath} -i {audio_path} -c:v libx264 -preset slow -crf 18 -c:a aac -shortest {os.path.splitext(cover_filepath)[0]}.mp4')
    os.system(
        f'ffmpeg -loop 1 -i {cover_filepath} -i {audio_path} -c:v libx264 -profile:v high -level:v 4.2 -crf 23 -preset slow -pix_fmt yuv420p -c:a aac -b:a 192k -shortest {os.path.splitext(cover_filepath)[0]}_zh.mp4')

    return True


if __name__ == "__main__":
    print(f"DEBUG: create_image.py started")

    merge_cover_with_audio_zh(
        '/Users/lgg/Downloads/stories/Enchanted_Shadow_Woods/Enchanted_Shadow_Woods.jpg')
