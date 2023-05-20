# from main import *
from create_image import *


def pick_random_line(filepath='/Users/lgg/Downloads/stories/Stories_title_list.txt'):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    return random.choice(lines).strip()


def create_story_name():

    prompt = '''

You are the most creative artist in 2023 as well as the best prompt engineer for Midjourney's AI program, you have two jobs now:

First job is coming up with a title for our next fairy tale story; The title should be less than 6 words, since kids don't like long names. Remember, no punctuation, no numbers, no special characters are allowed in the title.

Second job is creating correspond detailed and imaginative Prompts for midjourney AI generator to generate an image for our story book cover. Prompts need to be under 60 words, it's a description for our title, need to be captivated, enchanted. Remember, avoid using character names in prompt, instead using general terms like boy, old man, girl, or woman. Output the prompts only.

Below are the titles of our previous fairy tales, you can use them as reference, but don't just duplicate them, you need to be creative and original.

The Magic Seed
The Enchanted Forest
The Golden Key
The Crystal Palace
The Diamond in the Rough
The Secret Garden
The Sleeping Beauty
The Little Red Riding Hood
The Gingerbread House
The Ugly Duckling
The Snow Queen
The Goose Girl
The Fisherman and His Wife
The Twelve Dancing Princesses
The Frog Prince
The Brave Tin Soldier
The Little Mermaid
The Giant's Garden
The Magic Carpet
The Princess and the Pea
The Three Wishes
The Nutcracker
The Little Engine That Could
The Sun and the Wind
The Lion King
The Rescuers Down Under
The Little Mermaid
The Beauty and the Beast
The Hunchback of Notre Dame
The Emperors New Groove
Atlantis The Lost Empire
Lilo and Stitch
Treasure Planet
Brother Bear
Home on the Range
Chicken Little
Meet the Robinsons
The Princess and the Frog
Raya and the Last Dragon

When you reply, please reply with the title and the prompts, separated by a line break. For example:

Tht Golden Treasure
A tranquil village cradled by mountains, featuring a cozy cottage, loving family tending their vibrant vegetable garden, and a backdrop of content villagers amidst whimsical homes.

Brother Bear
A detailed picture of a cute calm brunette girland a bear, flirting with each other, by justin gerard and greg rutkowski, digital art, realistic painting, dnd, character design, trending on artstation

Whispers of the Wind
A charming scene depicting a young boy and a gentle breeze, swirling colorful autumn leaves around them, as they journey hand in hand through a whimsical forest, filled with villagers happily working and playing.

Moonlit Mystery Journey
A magical landscape illuminated by moonlight, featuring a courageous young girl and her faithful animal companion embarking on a mysterious journey, surrounded by enchanting creatures, ancient ruins, and a distant sparkling castle.

'''

    try:
        title_prompt = chat_gpt(prompt, "gpt-4")
        return title_prompt
    except Exception as e:
        print(f"ERROR: chat_gpt() FAILED {e}")
        return


def create_story(prompt, folder):

    system_prompt = '''
You are Hans Christian Andersen, you have the famrous Hans Christian Andersen's Fairytales published, I am your agent, I always know how to sell your story. Now, it's 2023, we are about to write our new serious fairytales. This time you will keep your style as usual: Whimsical, moralistic, imaginative, timeless, enchanting. But you also know that this time we are targeting readers that was born after 2015, so we will put some elements new, bring in some idea creative and captivating that can engage readers for long periods of time. And since young generations don't like long stories, so we need to keep the story in less than 3000 words, remember that's crucial. Since it's targeting kids less thant 13 years old, so pick the words carefully, don't confuse them. I will only give you only a tile, you will be inspired by the title, and write the whole story based on your imagination, but you will revise the title for a better matching with your story if needed. The title is only a triger. OK, Let's start.
'''

    user_prompt = '''
Children’s Prattle
'''

    assistant_prompt = '''
Children’s Prattle

AT a rich merchant’s house there was a children’s party, and the children of rich and great people were there. The merchant was a learned man, for his father had sent him to college, and he had passed his examination. His father had been at first only a cattle dealer, but always honest and industrious, so that he had made money, and his son, the merchant, had managed to increase his store. Clever as he was, he had also a heart; but there was less said of his heart than of his money. All descriptions of people visited at the merchant’s house, well born, as well as intellectual, and some who possessed neither of these recommendations.

Now it was a children’s party, and there was children’s prattle, which always is spoken freely from the heart. Among them was a beautiful little girl, who was terribly proud; but this had been taught her by the servants, and not by her parents, who were far too sensible people.

Her father was groom of the Chambers, which is a high office at court, and she knew it. “I am a child of the court,” she said; now she might just as well have been a child of the cellar, for no one can help his birth; and then she told the other children that she was well-born, and said that no one who was not well-born could rise in the world. It was no use to read and be industrious, for if a person was not well-born, he could never achieve anything. “And those whose names end with ‘sen,’” said she, “can never be anything at all. We must put our arms akimbo, and make the elbow quite pointed, so as to keep these ‘sen’ people at a great distance.” And then she stuck out her pretty little arms, and made the elbows quite pointed, to show how it was to be done; and her little arms were very pretty, for she was a sweet-looking child.

But the little daughter of the merchant became very angry at this speech, for her father’s name was Petersen, and she knew that the name ended in “sen,” and therefore she said as proudly as she could, “But my papa can buy a hundred dollars’ worth of bonbons, and give them away to children. Can your papa do that?”

“Yes; and my papa,” said the little daughter of the editor of a paper, “my papa can put your papa and everybody’s papa into the newspaper. All sorts of people are afraid of him, my mamma says, for he can do as he likes with the paper.” And the little maiden looked exceedingly proud, as if she had been a real princess, who may be expected to look proud.

But outside the door, which stood ajar, was a poor boy, peeping through the crack of the door. He was of such a lowly station that he had not been allowed even to enter the room. He had been turning the spit for the cook, and she had given him permission to stand behind the door and peep in at the well-dressed children, who were having such a merry time within; and for him that was a great deal. “Oh, if I could be one of them,” thought he, and then he heard what was said about names, which was quite enough to make him more unhappy. His parents at home had not even a penny to spare to buy a newspaper, much less could they write in one; and worse than all, his father’s name, and of course his own, ended in “sen,” and therefore he could never turn out well, which was a very sad thought. But after all, he had been born into the world, and the station of life had been chosen for him, therefore he must be content.

And this is what happened on that evening.


Many years passed, and most of the children became grown-up persons.

There stood a splendid house in the town, filled with all kinds of beautiful and valuable objects. Everybody wished to see it, and people even came in from the country round to be permitted to view the treasures it contained.

Which of the children whose prattle we have described, could call this house his own? One would suppose it very easy to guess. No, no; it is not so very easy. The house belonged to the poor little boy who had stood on that night behind the door. He had really become something great, although his name ended in “sen,”—for it was Thorwaldsen.

And the three other children—the children of good birth, of money, and of intellectual pride,—well, they were respected and honored in the world, for they had been well provided for by birth and position, and they had no cause to reproach themselves with what they had thought and spoken on that evening long ago, for, after all, it was mere “children’s prattle.”
'''
    # from prompt findout only the words, using regex
    prompt_words = re.findall(r'[\w]+', prompt)
    prompt_words = [word.capitalize() for word in prompt_words]
    file_name = '_'.join(prompt_words)
    sub_folder = f"{folder}/{file_name}"

    # 根据 prompt 生成 story
    try:
        message = chat_gpt_full(prompt, system_prompt, user_prompt,
                                assistant_prompt, dynamic_model='gpt-4', chatgpt_key=OPENAI_API_KEY)
    except Exception as e:
        return e

    # create story_file_path
    filepath_story = f"{sub_folder}/{file_name}.txt"

    try:
        with open(filepath_story, 'w') as f:
            f.write(message)
    except Exception as e:
        return e

    # 根据 story 生成 mp3
    filepath_story_mp3 = filepath_story.replace('.txt', '.mp3')
    filepath_story_mp3 = generate_or_read_tts_11_labs(
        content=message, voice_id='eXhbluainLzpz4zVbWr0', tts_file_name=filepath_story_mp3, folder=sub_folder)
    # microsoft_azure_tts(message, voice='zh-CN-YunxiNeural', output_filename='output.wav')

    if not os.path.isfile(filepath_story_mp3):
        print(f"音频文件 {filepath_story_mp3} 生成失败!")
        return

    return filepath_story_mp3
    # try: create_story_images(filepath_story.split('/')[-1], folder = sub_folder)
    # except Exception as e: return e

# 输入一段童话故事，按照句子分割，每一句生成一个故事背景图片的 Prompt，然后利用 Midjourney 生成 1280 * 576 图片，同时把该段发送给 Asure 神经网络生成音频文件，最后结合图片和音频文件生成一个视频文件。


def create_story_podcast(entire_story, author_name, folder='/Users/lgg/Downloads/famous_stories'):

    if not os.path.exists(folder):
        os.makedirs(folder)

    author_folder = f"{folder}/{author_name}"
    if not os.path.exists(author_folder):
        os.makedirs(author_folder)

    # convert all non-English punctuation to English standard
    entire_story = unidecode(entire_story)

    # 从 entire_story 中分割出标题
    story_title = entire_story.split('\n')[0].strip()

    entire_story = entire_story.replace('\n\n', '\n')
    entire_story = entire_story.replace('\n', '\n\n')

    # from prompt findout only the words, using regex
    story_title_words = re.findall(r'[\w]+', story_title)
    story_title_words = [word.capitalize() for word in story_title_words]
    file_name = '_'.join(story_title_words)
    sub_folder = f"{author_folder}/{file_name}"

    # create story_file_path
    filepath_story = f"{sub_folder}/{file_name}.txt"
    filepath_story_wav = f"{sub_folder}/{file_name}.wav"

    if os.path.exists(sub_folder):
        if os.path.isfile(f"{sub_folder}/{file_name}.txt"):
            print(f"文件 {story_title} 已存在，跳过")
            return

    if not os.path.exists(sub_folder):
        os.mkdir(sub_folder)

    try:
        with open(filepath_story, 'w') as f:
            f.write(entire_story)
    except Exception as e:
        print(f"写入文件 {story_title} 失败: {e}")
        return

    if len(entire_story.split(' ')) > 4000:
        print(f"ERROR: 故事太长，超过了 4000 个单词，生成一个缩略版的故事")

        paragraph_counts = len(entire_story.split('\n\n'))

        new_entire_story = '\n\n'.join(entire_story.split(
            '\n\n')[:paragraph_counts//2] + ['......'])

        try:
            new_entire_story_file = f"{sub_folder}/{file_name}_short.txt"
            with open(new_entire_story_file, 'w') as f:
                f.write(new_entire_story)
        except Exception as e:
            print(f"写入文件 {new_entire_story_file} 失败: {e}")
            return

    if os.path.isfile(filepath_story_wav):
        print(f"音频文件 {story_title} 已存在，跳过")
        return

    try:
        output_filename = microsoft_azure_tts(
            entire_story, voice='en-US-JaneNeural', output_filename=filepath_story_wav)
        if output_filename:
            print(f"音频创建成功: {output_filename}")
    except Exception as e:
        print(f'ERROR: microsoft_azure_tts() failed for {story_title}:', e)
        return False

    return True

# 将一段话发送给 ChatGPT, 让他帮忙更具语义语境切割成多个句子，然后为每个句子创造一个背景图的描述 Prompt


def seperate_paragraph_to_sentence_and_create_images_prompt(story_title, story_paragraph_name, paragraph, author_name='Hans Christian Andersen'):

    system_prompt = f'''
You are {author_name}, I'm your manager and publisher, now we are working on your book: {story_title}. We need to seperate the entire story into paragraph first, I will send you paragraph by paragraph, you need to seperate each paragraph into sentences based on the meaning of the paragraph and the length of the sentence. Each sentence should be no more than 50 words. If a sentence is too long, you can split it into two sentences. If a sentence is too short, you can combine it with the previous sentence or the next sentence. You can always split a sentence by the punctuation . or ; or , if the sentence is not too short. But make sure that each sentence is meaningful and can stand alone. And then, add a Chinese translation in the next line to match the sentence. After you finish seperating the paragraph into sentences, you need to create a prompt for each sentence,  so that we can use AI to generate background images, the prompt should be less than 100 words. Add the prompt in the next line, under Chinese translation, starts with "Prompt: ". In conclusion, each paragraph should be seperated into sentences, and each sentence should have a Chinese translation beneath and a background image prompt beneath.
'''

    user_prompt = '''
It was terribly cold and nearly dark on the last evening of the old year, and the snow was falling fast. In the cold and the darkness, a poor little girl, with bare head and naked feet, roamed through the streets. It is true she had on a pair of slippers when she left home, but they were not of much use. They were very large, so large, indeed, that they had belonged to her mother, and the poor little creature had lost them in running across the street to avoid two carriages that were rolling along at a terrible rate. One of the slippers she could not find, and a boy seized upon the other and ran away with it, saying that he could use it as a cradle, when he had children of his own. So the little girl went on with her little naked feet, which were quite red and blue with the cold. In an old apron she carried a number of matches, and had a bundle of them in her hands. No one had bought anything of her the whole day, nor had anyone given her even a penny. Shivering with cold and hunger, she crept along; poor little child, she looked the picture of misery. The snowflakes fell on her long, fair hair, which hung in curls on her shoulders, but she regarded them not.
'''

    assistant_prompt = '''
Scene:
It was terribly cold and nearly dark on the last evening of the old year, and the snow was falling fast. 
这是这年最后的一夜——新年的前夕, 黑暗的夜幕开始垂下来了, 天气冷得可怕, 大雪正在飞速地落下. 
Prompt : As the old year came to a close, the city of Galic was shrouded in darkness, with a bitter coldness that chilled the bone. Thick snowflakes fell from the sky like a never-ending cascade, blanketing the gritty and grid-shaped cobblestone streets.

Scene:
In the cold and the darkness, a poor little girl, with bare head and naked feet, roamed through the streets.
在这样的寒冷和黑暗中，有一个光头赤脚的小女孩正在街上走着。
Prompt: As the snow fell heavily on the dark and somber night, a poor little girl roamed through the cold and barren streets, her tiny feet bare and exposed to the biting cold. The camera captures a full shot of the little girl, walking alone and unprotected, with the sad reality of her situation all too evident in her eyes. 

Scene:
It is true she had on a pair of slippers when she left home, but they were not of much use.
是的，她离开家的时候还穿着一双拖鞋，但那又有什么用呢？
Prompt: As she embarked on her journey in a dark snow day, the little girl clung onto the only footwear she had - a pair of oversize slippers that were completely ill-fitted to her tiny feet.

Scene:
They were very large, so large, indeed, that they had belonged to her mother, and the poor little creature had lost them in running across the street to avoid two carriages that were rolling along at a terrible rate.
她的拖鞋非常大，比她的脚还大，她的母亲曾经穿过，她在跑过马路的时候丢了它们，为了避开两辆车，她跑得很快，拖鞋就跟着她一起丢了。
Prompt: The image of the slippers, lying abandoned on the ground, was a poignant reminder of the girl's struggles, and the harsh reality of the world she lived in. 

Scene:
One of the slippers she could not find, and a boy seized upon the other and ran away with it, saying that he could use it as a cradle, when he had children of his own. 
她找不到一只拖鞋，一个男孩抢走了另一只，说他以后要用它做婴儿床。
Prompt: A mischievous boy snatched one of her slippers and ran off, declaring that he would use it as a makeshift cradle for his future children. In her distress, the little girl could do nothing but watch helplessly as the boy disappeared into the night, taking with him the only semblance of comfort she had left.

Scene:
So the little girl went on with her little naked feet, which were quite red and blue with the cold. In an old apron she carried a number of matches, and had a bundle of them in her hands. 
所以，这个小女孩继续走着，她的脚是裸露的，因为寒冷而变得红和青。她手里拿着一些火柴，还有一些火柴在她的围裙里。
Prompt: The poor little girl pressed on with her bare feet, now a deep shade of red and blue from the biting cold. Clutched tightly in her hands were a bundle of matches, while an old apron served as her makeshift bag to carry the rest. The camera pans down to show the snow-covered streets, highlighting the immense struggle the girl faces as she ventures on alone in the harsh winter night.

Scene:
No one had bought anything of her the whole day, nor had anyone given her even a penny. Shivering with cold and hunger, she crept along;
这一整天，没有任何人买她的东西，也没有人给她一分钱。她静悄悄地走着，因为寒冷和饥饿而瑟瑟发抖。
Prompt: The poor little girl walked alone through the snowy streets, her bare feet leaving tiny footprints in the freshly fallen snow. Despite her efforts, The camera zooms in on her shivering form, emphasising the sheer isolation and desperation of her situation.

Scene:
poor little child, she looked the picture of misery. The snowflakes fell on her long, fair hair, which hung in curls on her shoulders, but she regarded them not.
这个可怜的小姑娘，看起来好可怜。雪花落在她长长的金发上，她的肩膀上有一些卷发，但她没心思注意这些。
Prompt: The poor little child stood forlorn in the snow, her fair hair cascading in loose curls down her shoulders. The snowflakes fell upon her without reprieve, but she paid them no attention, lost in a world of misery and despair. The camera captures her sad expression, highlighting the depth of her sorrow and the helplessness of her situation.
'''

    try:
        paragraph_scenes_chinese_prompts = chat_gpt_full(
            f"{paragraph}", system_prompt, user_prompt, assistant_prompt, dynamic_model='gpt-4', chatgpt_key=OPENAI_API_KEY)
    except Exception as e:
        print(f"ERROR: chat_gpt_full() failed: \n{e}")
        return

    with open(story_paragraph_name, 'w') as f:
        f.write(paragraph_scenes_chinese_prompts)

    return paragraph_scenes_chinese_prompts

# 输入一段童话故事，按照句子分割，每一句生成一个故事背景图片的 Prompt，然后利用 Midjourney 生成 1280 * 576 图片，同时把该段发送给 Asure 神经网络生成音频文件，最后结合图片和音频文件生成一个视频文件。


def from_folder_create_mutil_paragraph_files(entire_story, folder='/Users/lgg/Downloads/famous_stories'):

    if not os.path.exists(folder):
        os.makedirs(folder)

    # 从 entire_story 中分割出标题
    story_title = entire_story.split('\n')[0].strip()

    confirm_title = input(f"请确认故事标题: {story_title} (y/n): ")
    if confirm_title.lower() not in ['y', 'yes', 'confirm', 'c']:
        return

    # from prompt findout only the words, using regex
    story_title_words = re.findall(r'[\w]+', story_title)
    story_title_words = [word.capitalize() for word in story_title_words]
    file_name = '_'.join(story_title_words)
    sub_folder = f"{folder}/{file_name}"
    if not os.path.exists(sub_folder):
        os.mkdir(sub_folder)

    # create story_file_path
    filepath_story = f"{sub_folder}/{file_name}.txt"

    sub_folder_paragraphs = f"{sub_folder}/paragraphs"
    if not os.path.exists(sub_folder_paragraphs):
        os.mkdir(sub_folder_paragraphs)

    story_paragraphs = entire_story.split('\n')
    story_paragraphs = [paragraph.strip(
    ) for paragraph in story_paragraphs if paragraph and paragraph.strip()]

    story_content = '\n'.join(story_paragraphs)

    confirm_story = input(f"请确认故事内容（包含标题）: \n\n{story_content} (y/n): ")
    if confirm_story.lower() not in ['y', 'yes', 'confirm', 'c']:
        return

    try:
        with open(filepath_story, 'w') as f:
            f.write(entire_story)
    except Exception as e:
        print(f"写入文件 {filepath_story} 失败! \n{e}")
        return

    for i, paragraph in enumerate(story_paragraphs):
        if i == 0:
            continue

        print(f"正在处理第 {i} 段故事: {paragraph}")
        story_paragraph_name = f"{sub_folder_paragraphs}/{file_name}_paragraph_{i}.txt"

        paragraph_scenes_chinese_prompts = seperate_paragraph_to_sentence_and_create_images_prompt(
            story_title, story_paragraph_name, paragraph, author_name='Hans Christian Andersen')
        if paragraph_scenes_chinese_prompts:
            print(f"第 {i} 段故事处理成功, 文档已保存!")

    return True

# 从文件夹中读取所有的 paragraph 文件，基于 secene 制作 scene txt 文件


def from_folder_create_mutil_scene_files(entire_story, folder='/Users/lgg/Downloads/famous_stories'):
    if not os.path.exists(folder):
        return

    # 从 entire_story 中分割出标题
    story_title = entire_story.split('\n')[0].strip()

    confirm_title = input(f"请确认故事标题: {story_title} (y/n): ")
    if confirm_title.lower() not in ['y', 'yes', 'confirm', 'c']:
        return

    # from prompt findout only the words, using regex
    story_title_words = re.findall(r'[\w]+', story_title)
    story_title_words = [word.capitalize() for word in story_title_words]
    file_name = '_'.join(story_title_words)
    sub_folder = f"{folder}/{file_name}"
    sub_folder_paragraphs = f"{sub_folder}/paragraphs"
    if not os.path.exists(sub_folder_paragraphs):
        return

    # 判断 os.listdir(sub_folder_paragraphs) 有多少个文件
    files_cound = len(os.listdir(sub_folder_paragraphs))

    x = 0
    for i in range(1, files_cound + 1):
        story_paragraph_name = f"{sub_folder_paragraphs}/{file_name}_paragraph_{i}.txt"
        if not os.path.isfile(story_paragraph_name):
            continue

        for line in read_lines(story_paragraph_name):
            if not line:
                continue
            # 排除 Scene 或者 Pompt 开头的 line，排除中文译文的 line
            if line.startswith('Scene') or line.startswith('Prompt'):
                continue
            # 判断 line 是否是英文编码
            if is_english(line):
                # 创建新的 scene txt 文件
                x += 1
                scene_file_name = f"{sub_folder_paragraphs}/{file_name}_paragraph_{i}_scene_{x}.txt"
                with open(scene_file_name, 'w') as f:
                    f.write(line)
    return True

# 从文件夹中读取所有的 scene 文件，基于 secene 制作 scene audio 文件


def from_folder_create_mutil_audio_files(entire_story, folder='/Users/lgg/Downloads/famous_stories'):
    if not os.path.exists(folder):
        return

    # 从 entire_story 中分割出标题
    story_title = entire_story.split('\n')[0].strip()

    confirm_title = input(f"请确认故事标题: {story_title} (y/n): ")
    if confirm_title.lower() not in ['y', 'yes', 'confirm', 'c']:
        return

    # from prompt findout only the words, using regex
    story_title_words = re.findall(r'[\w]+', story_title)
    story_title_words = [word.capitalize() for word in story_title_words]
    file_name = '_'.join(story_title_words)
    sub_folder = f"{folder}/{file_name}"
    sub_folder_paragraphs = f"{sub_folder}/paragraphs"
    if not os.path.exists(sub_folder_paragraphs):
        return

    for file in os.listdir(sub_folder_paragraphs):
        if 'scene' not in file:
            continue
        print(f"正在处理: {file}")
        with open(f"{sub_folder_paragraphs}/{file}", 'r') as f:
            scene = f.read()
            scene = scene.strip()
            if not scene:
                continue

            try:
                output_filename = microsoft_azure_tts(
                    scene, voice='en-US-JaneNeural', output_filename=f"{sub_folder_paragraphs}/{file[:-4]}.wav")
                if output_filename:
                    print(f"音频创建成功: {file}")
            except Exception as e:
                print('ERROR: microsoft_azure_tts():', e)
                return False

    return True

# 把英文故事翻译成中文


def translate_story_from_en_to_zh(filepath):
    if debug:
        print(
            f"DEBUG: translate_story_from_en_to_zh() 开始翻译: {filepath.split('/')[-1]}")

    if not filepath.endswith('.txt'):
        return False

    filepath_translated = filepath[:-4] + '_zh.txt'
    filepath_translated_wav = filepath[:-4] + '_zh.wav'

    text = ''
    with open(filepath, 'r') as f:
        text = f.read()
    if not text:
        return False

    message = ''
    try:
        message = chat_gpt(
            f"你是一位非常优秀的中英双语老师，非常擅长讲童话故事。请把下面这个英文故事翻译成简体中文版，包括标题，也翻译一个相应的有吸引力的名字。但故事中的名字需要保留原来的样子，不要把 Steve 翻译成斯蒂夫。回复的时候只需要翻译好的故事名和故事内容，故事名和故事内容用两个换行符分隔开，不要添加其他的额外的文字。\n\n{text}")
    except Exception as e:
        print('ERROR: chat_gpt() 翻译失败:', e)
    if not message:
        return False

    with open(filepath_translated, 'w') as f:
        f.write(message)

    try:
        output_filename = microsoft_azure_tts(
            message, voice='zh-CN-XiaoshuangNeural', output_filename=filepath_translated_wav)
    except Exception as e:
        print('ERROR: microsoft_azure_tts():', e)
        return False

    if debug:
        print(
            f"DEBUG: translate_story_from_en_to_zh() {output_filename} was saved successfully")
    return output_filename


def merge_jpg_with_mp3_to_create_mp4_videos():
    folder = '/Users/lgg/Downloads/stories'

    for sub_folder_name in os.listdir(folder):
        sub_folder = os.path.join(folder, sub_folder_name)
        if not os.path.isdir(sub_folder):
            continue
        if any(f.endswith('.mp4') for f in os.listdir(sub_folder)):
            continue
        cover_filepath = os.path.join(sub_folder, f"{sub_folder_name}.jpg")
        audio_filepath = os.path.join(sub_folder, f"{sub_folder_name}.mp3")
        if not os.path.isfile(cover_filepath) or not os.path.isfile(audio_filepath):
            continue
        try:
            r = merge_cover_with_audio(cover_filepath)
            if r:
                print(
                    f"Successfully merged {cover_filepath} with {audio_filepath}")
        except Exception as e:
            print(
                f"Failed to merge {cover_filepath} with {audio_filepath}: {e}")
    return


def translate_and_merge_jpg_with_wav_to_create_zh_mp4_videos():
    folder = '/Users/lgg/Downloads/stories'

    for sub_folder_name in os.listdir(folder):
        sub_folder = os.path.join(folder, sub_folder_name)
        if not os.path.isdir(sub_folder):
            continue
        if any(f.endswith('_zh.mp4') for f in os.listdir(sub_folder)):
            continue

        story_filepath = os.path.join(sub_folder, f"{sub_folder_name}.txt")
        cover_filepath = os.path.join(sub_folder, f"{sub_folder_name}.jpg")
        audio_filepath = os.path.join(sub_folder, f"{sub_folder_name}_zh.wav")

        if not os.path.isfile(story_filepath) or not os.path.isfile(cover_filepath):
            continue

        if not os.path.isfile(audio_filepath):
            output_filename = translate_story_from_en_to_zh(story_filepath)
            if not output_filename:
                continue

            if output_filename == audio_filepath and os.path.isfile(audio_filepath):
                print(f"翻译成功: {audio_filepath}")

        try:
            r = merge_cover_with_audio_zh(cover_filepath)
            if r:
                print(
                    f"Successfully merged {cover_filepath} with {audio_filepath}")
                continue
        except Exception as e:
            print(
                f"Failed to merge {cover_filepath} with {audio_filepath}: {e}")
    return


if __name__ == "__main__":
    print(f"DEBUG: create_story.py started")

    author_name = 'Hans_Christian_Andersen'
    entire_story_file = '/Users/lgg/Downloads/famous_stories/Next_Story.txt'
    print(f"故事文件: {entire_story_file}")
    print(f"故事作者: {author_name}")

    with open(entire_story_file, 'r') as f:
        entire_story = f.read()
    if not entire_story:
        exit()

    try:
        r = create_story_podcast(
            entire_story, author_name, folder='/Users/lgg/Downloads/famous_stories')
        if r:
            print(f"create_story_podcast() 成功")
    except Exception as e:
        print(f"ERROR: create_story_podcast() failed: {e}")
