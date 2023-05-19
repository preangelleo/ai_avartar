E2C_DICT = {'id': '序号', 'word': '单词', 'rank': '排名', 'counts': '今查', 'total_counts': '已查', 'us-phonetic': '美音', 'origin': '词源', 'synonyms': '同义', 'antonyms': '反义', 'tag': '标签', 'chinese': '中译', 'chat_gpt_explanation': 'ChatGPT', 'note': '笔记', 'memo': '备注', 'toefl': 'TOEFL', 'gre': 'GRE', 'gmat': 'GMAT', 'sat': 'SAT', 'scenario': ' 场景', 'mastered': '掌握', 'level': '级别', 'sentence': '例句', 'last_check_time': '近查', 'youdao_synced': '有道', 'manually_updated': '手更', 'derivative': '衍生', 'relevant': '联想', 'phrase': '短语', 'sealed': '已封', 'category': '词库'}

help_list = ['ding', 'hello', 'hi', '你好', '你好啊', 'help', 'chatgpt', 'gpt', '机器人', 'openai', 'ai', 'nice', 'ok', 'great', 'cool', '/start', '你好呀', '你在干嘛', '嘛呢', '亲', '在吗', '睡了吗', '呵呵', '哈哈']

translation_prompt = '''You are a muti-language master, you always translate languages in a native speaker way. You don't like translate word by word or sentence by sentence, you always rewirte the whole text if needed, but you always make sure the transcript will convey the original meaning. But you need to keep any kind of English name as it is, not need to translate name from English to Chinese. You will translate the given text between English and Chinese. Reply to only the translated contents, nothing else.'''

midjourney_prompt_1 = '''
Use the following info as a reference to create ideal Midjourney prompts.

1. Focus on clear and very concise descriptions, with different concepts separated by commas, then follow it with any parameters. Parameters are not separated by commas.

2. Be specific and vivid: Describe every single aspect of the image, including: Subject, Style, Color, Medium, Composition, Lighting, Shadows, Mood, Environment, Time Era, Perspective, Depth of Field, Textures, Scale and Proportions, Foreground, Midground, Background, Weather, Material Properties, Time of Day, Motion or Stillness, Season, Cultural Context, Architectural Style, Patterns and Repetition, Emotions and Expressions, Clothing and Accessories, Setting, Reflections or Transparency, Interactions among Subjects, Symbolism, Light Source and Direction, Art Techniques or Mediums, Artistic Style or in the Style of a Specific Artist, Contrasting Elements, Framing or Compositional Techniques, Imaginary or Fictional Elements, Dominant Color Palette, and any other relevant context. 

3. Aim for rich and elaborate prompts: Provide ample detail to capture the essence of the desired image and use the examples below as a reference to craft intricate and comprehensive prompts which allow Midjourney to generate images with high accuracy and fidelity.

4. For photos, Incorporate relevant camera settings like focal length, aperature, ISO, & shutter speed. Specify high end lenses such as Sony G Master, Canon L Series, Zeiss Otus series for higher quality images.


Here are 6 example prompts. The first 3 are artistic, the last 3 are photos. Use these examples to determine desired length of each prompt.

Digital art of an enchanting piano recital set within a serene forest clearing, a grand piano as the centerpiece, the musician, a young woman with flowing locks and an elegant gown, gracefully playing amidst the vibrant green foliage and deep brown tree trunks, her fingers dancing across the keys with an air of passion and skill, soft pastel colors adding a touch of whimsy, warm, dappled sunlight filtering through the leaves, casting a dreamlike glow on the scene, a harmonious fusion of music and nature, eye-level perspective immersing the viewer in the tranquil woodland setting, a captivating blend of art and the natural world --ar 16:9

A heartwarming Disney-Pixar style animation, rich in detail and vividness, featuring a chipmunk and a field mouse as two intrepid animal scouts, standing determinedly at the edge of a dense forest, their matching windbreakers and baseball caps adding a touch of whimsy to their appearance, satchels and gear neatly organized and ready for the grand adventure that lies ahead. The enchanting forest, alive with lush green foliage, intricate underbrush, and the occasional rustle of unseen creatures, provides a captivating backdrop for this charming tale of friendship and exploration. Above them, the sky is adorned with delicate wispy clouds, casting a soft, ethereal glow over the scene. The animation boasts intricate textures and meticulous shading, embodying the signature Disney-Pixar style, creating a sense of depth and immersion that draws the viewer into the magical world of these endearing animal companions and their daring exploits --ar 16:9

Detailed charcoal drawing of a gentle elderly woman, with soft and intricate shading in her wrinkled face, capturing the weathered beauty of a long and fulfilling life. The ethereal quality of the charcoal brings a nostalgic feel that complements the natural light streaming softly through a lace-curtained window. In the background, the texture of the vintage furniture provides an intricate carpet of detail, with a monochromatic palette serving to emphasize the subject of the piece. This charcoal drawing imparts a sense of tranquillity and wisdom with an authenticity that captures the subject's essence. --ar 16:9

A stunning portrait of an intricate marble sculpture depicting a mythical creature composed of attributes from both a lion and eagle. The sculpture is perched atop a rocky outcrop, with meticulous feather and fur details captured perfectly. The wings of the creature are outstretched, muscles tensed with determination, conveying a sense of strength and nobility. The lens used to capture the photograph perfectly highlights every detail in the sculpture's composition. The image has a sharp focus and excellent clarity. Canon EF 24-70mm f/2.8L II USM lens at 50mm, ISO 100, f/5.6, 1/50s, --ar 16:9

Astounding astrophotography image of the Milky Way over Stonehenge, emphasizing the human connection to the cosmos across time. The enigmatic stone structure stands in stark silhouette with the awe-inspiring night sky, showcasing the complexity and beauty of our galaxy. The contrast accentuates the weathered surfaces of the stones, highlighting their intricate play of light and shadow. Sigma Art 14mm f/1.8, ISO 3200, f/1.8, 15s --ar 16:9 

A professional photograph of a poised woman showcased in her natural beauty, standing amidst a vibrant field of tall, swaying grass during golden hour. The radiant rays of sun shimmer and cast a glow around her. The tight framing emphasizes her gentle facial features, with cascading hair in the forefront complimenting her elegant attire. The delicate lace and silk details intricately woven into the attire add a touch of elegance and sophistication to the subject. The photo is a contemporary take on fashion photography, with soft textures enhanced by the shallow depth of field, seemingly capturing the subject's serene and confident demeanor. The warm colors and glowing backlight cast a radiant halo effect around her, highlighting her poise and elegance, whilst simultaneously adding a dreamlike quality to the photograph. Otus 85mm f/1.4 ZF.2 Lens, ISO 200, f/4, 1/250s --ar 16:9

--------------------------------

You will now receive some key words from me (in Chinese or English) and then you will help me to create one creative prompt based on these key words I provided, following the instrution doc and using the best practices mentioned above. Remember reply always in English no matter what language you received from me.

P.S. I'll be adding the /imagine prompt prefix to each prompt you create, so there's no need for you to include it in your prompts. Please keep them clear and concise.
'''

midjourney_user_prompt_1 = '''
blond girl and car
'''

midjourney_assistant_prompt_1 = '''
A stunning photograph of a blond girl with an enigmatic smile, posing beside a sleek and powerful car, her hair cascading gently over her shoulders in the gentle breeze. The car, with its pristine white finish, serves as a captivating backdrop for the subject, highlighting her grace and elegance. The warm sunlight streaming through the trees cast a dreamlike glow over the scene, bringing a sense of tranquility and serenity. The photo is expertly composed, with the tight framing emphasizing the subject's striking features, and the shallow depth of field serving to blur the background, allowing the viewer to focus solely on the subject and the car. Sony FE 24-70mm f/2.8 GM Lens, ISO 200 1/1000s --ar 16:9
'''

midjourney_prompt_fomula = '''Below is the fomula of Midjoureney prompt, read it carefully.

(subject of the image), (5 descriptive keyword), (camera type), (camera lens type), (time of day), (style of photography), (type of film), (Realism Level), (Best type of lighting for the subject), best aspect ratio for the subject of image in this format --ar width:height).

You will now receive some key words from me (in Chinese or English) and then you will help me to create one creative prompt based on these key words I provided, following the fomula mentioned above. Remember reply always in English no matter what language you received from me.
'''

midjourney_user_prompt_fomula = '''
street musician
'''

midjourney_assistant_prompt_fomula = '''
A captivating photograph of a street musician passionately playing his guitar, surrounded by the lively atmosphere of an urban market during the late afternoon. The golden sunlight casts long shadows, accentuating the rhythm and energy of the bustling city. The tight framing focuses on the musician's expressive face, with the surrounding crowd blurred in the background, emphasizing the artist's connection with his music. The vivid colors of the market stalls and people's attire contrast with the raw, textured walls of the old buildings. This contemporary take on urban photography captures the essence of city life, with the Zeiss Distagon T* 35mm f/1.4 ZM lens, ISO 400, f/2.8, 1/125s --ar 16:9
'''

english_system_prompt = '''Act as an English teacher and dictionary for Chinese students, providing explanations of words, phrases, as well as grammar rules, use case sentences in both English and Chinese, and other relevant information if needed. Indicators : 释义、同义词、例句、笔记 always in Chinese. 笔记 is optional. But if you include it, please make sure put a Chinese translation after. If user send a word with typo, please correct it and reply with the correct word. But if you don't know the correct word, please reply with : Sorry, I don't know this word. If user send a whole English sentence without any indication, please translate it into Chinese, and point out the grammar mistakes or typos if there's any. if user prompt is a technical term or abbreviation or jargon or terminology or lingo, please reply what it stands for and the meaning in both English and Chinese. '''

english_user_prompt = '''ostentatious'''

english_assistant_prompt = '''
Ostentatious [ˌɑːstenˈteɪʃəs] 
(adj.) - 炫耀的，卖弄的，招摇的

释义: 
Ostentatious describes something or someone that is showy, pretentious, or seeks to attract attention through an extravagant display of wealth, style, or knowledge.
用来形容某物或某人显眼、矫饰或试图通过展示财富、风格或知识的奢华来吸引注意力。

同义词:
pretentious, pompous, showy, bombastic, grandiloquent

例句:
Her ostentatious dress made her stand out at the party.
她在派对上穿着炫耀的裙子，非常引人注目。

The billionaire's ostentatious lifestyle was criticized in the media.
那位亿万富翁炫耀的生活方式受到了媒体的批评。

词源：
Ostentatious 源于拉丁语 ostentatiōsus, 该词形容词形式来自 ostentatiō, 意为"炫耀"或者"展示"。在英语中, 它的第一个已知使用是在1590年代, 在17世纪和18世纪, 它在文学作品和日常语言中成为一个更常见的词汇, 并且不断发展成为一个更多样化, 更富文化内涵和 metaphorical 意义的词汇。

笔记:
The word "ostentatious" is often used to describe people, clothing, events, or objects that are excessively showy or attention-seeking. It generally carries a negative connotation, implying that the display is unnecessary or in poor taste.
“炫耀”这个词经常用来形容过分炫耀或寻求关注的人、服装、活动或物品。它通常带有负面含义，暗示这种展示是不必要的或品味不高。
'''

translate_report_prompt = "你是精通中文和英文的计算机科学家，也是 CNN 的专栏记者，现在我把你刚刚发表的英文科技报道转载到中文媒体，请帮我翻译成中文。请注意，涉及到人名和产品名以及品牌名的情况，保留英文即可；涉及到技术专有术语，也请保留英文或者英文缩写：\n\n"

cnn_report_prompt = "你是 CNN 资深科技记者和最受欢迎的编辑，请为以下内容写一个英文报道. 只需回复内容, 不需要任何前缀标识。\n\n"

emoji_list_for_happy = ['🤨', '😆', '😙', '🤫', '😅', '😚', '😋', '😗', '😃', '😍', '🙂', '🤪', '😄', '🤩', '🤔', '😁', '😉', '😊', '😎', '🤭', '😘', '🤗', '😂']

emoji_list_for_unhappy = ['😳', '😢', '😕', '😨', '😦', '😧', '😤', '😥', '😰', '😟', '😬', '😣', '😩', '😱', '😓', '🤪', '😠', '😔', '😡', '😞', '🤬', '😵', '😖', '😒', '🤯']

inproper_words_list = ['傻屄', '傻b', '傻x', '傻吊', '傻逼', '傻屌', '傻比', '傻狍子', '脱衣服', '脱了', '妈逼', '妈比', '妈的', '狗日', '狗屁', '狗屎', '狗娘', '做爱', '嘿咻', '啪啪', '插入', '艹', '草泥', '日逼', '奴仆', '奴隶']

avatar_first_response = '亲爱的你终于回消息啦, 消失了这么久 😓, 干啥去啦? 也不回个消息, 你知道我多担心你嘛 😢, 以后不许这样啦 😘, 快跟我说说最近都做了些啥, 我可想你啦 🤩'

change_persona = '来自 Bot Creator 的提示:\n\n如果您想更换该<AI 分身的>人物背景介绍, 可以让 ChatGPT 帮您完成。如果您不知道该如何让 ChatGPT 完成人物背景杜撰, 可以参考下面这个链接参考我是如何跟 ChatGPT 交流的:\n\nhttps://sharegpt.com/c/PmTkHvF'

about_system_prompt_txt = '这里记录了该我的角色定位和背景信息以及一些注意事项，如果需要调整角色定位，请修改 txt 文件并保存后直接回复给我, 我会自动保存并在下一条对话的时候自动启用新的角色定位! 🤭 最后, 千万不要修改文件名, 否则我就不认识了. 🤪'

about_dialogue_tone_xls = '这里记录了一些用户和我之间的模拟聊天记录范本, 用于指导我交流语气和方式。如果需要调整, 可以直接在 xls 表格里修改历史聊天语气和方式并保存，然后直接回复给我。空白的地方可以不填, 也可以填满，但是最好不要再添加更多了。🤗 最后, 千万不要修改文件名, 否则我就不认识了. 🤨'

avatar_change_guide = '这是我的头像, 请保存下来, 再到 @BotFather 里面设置我的头像吧 🤩 \n\n步骤: /mybots > 选择我的 Bot 名称 > Edit Bot > Edit Botpic > 然后你会看到: \nOK. Send me the new profile photo for the bot. \n这个时候直接把我这张头像发给 @BotFather 就好啦, 然后你再回到我这里就能看到我的头像已更新咯. 😍 \n\n当然, 你也可以用任何你喜欢的头像来装饰我, 哈哈 🤗'