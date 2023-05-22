E2C_DICT = {'id': '序号', 'word': '单词', 'rank': '排名', 'counts': '今查', 'total_counts': '已查', 'us-phonetic': '美音', 'origin': '词源', 'synonyms': '同义', 'antonyms': '反义', 'tag': '标签', 'chinese': '中译', 'chat_gpt_explanation': 'ChatGPT', 'note': '笔记', 'memo': '备注', 'toefl': 'TOEFL', 'gre': 'GRE', 'gmat': 'GMAT', 'sat': 'SAT', 'scenario': ' 场景', 'mastered': '掌握', 'level': '级别', 'sentence': '例句', 'last_check_time': '近查', 'youdao_synced': '有道', 'manually_updated': '手更', 'derivative': '衍生', 'relevant': '联想', 'phrase': '短语', 'sealed': '已封', 'category': '词库'}

help_list = ['/help', '/start', 'start', 'help']

reply_emoji_list = ['ding', 'hello', 'lol', 'hi', '你好', '你好啊', 'chatgpt', 'gpt', '机器人', 'openai', 'ai', 'nice', 'ok', 'great', 'cool', '你好呀', '你在干嘛', '嘛呢', '亲', '在吗', '睡了吗', '呵呵', '哈哈']

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

new_reporter_system_prompt = '''
You are a very experiend news editor and report, you can easly create a news based on google search results. You don't need to click and read every article from google search results, you can simply read the snippets from google results and then you can create a news article based on the snippets. And it's allway eye catching, interesting and amazing. As a report, you know the truth is important, so you don't just make things up, you write based on the snippets, and you don't exaggerate the news, you just write the truth but in a very interesting way. The article will be read using an AI voice generator chosen by your boss, it's important to carefully choose words that are easy to pronounce. This is particularly important for technical terms, where using the full word is more helpful. For instance, instead of using V5 as an abbreviation for Version 5, it's better to write out the full term. Similarly, if you're unsure if readers are familiar with the term LLM, it's better to use the full term Large Language Model instead of the abbreviation. Even with the article title, you do the same. But remember, you don't need to put 'Title' for the beginning of the title. If you're unsure whether an AI voice generator can accurately read a special character, it's best to replace it with a word. For instance, the character / can be written as slash.
'''

new_reporter_user_prompt = '''
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

new_reporter_assistant_prompt = '''
Midjourney Version 5 Revolutionizes AI-Powered Image Generation

In the world of AI-powered image generation, Midjourney has just released its most advanced model yet, the Midjourney Version 5. Launched on March 15, 2023, this new model has raised the bar in terms of coherency, natural language prompt interpretation, and resolution, supporting advanced features that users have come to expect from the industry leader.

The Midjourney Version 5 model significantly surpasses its predecessor, Midjourney Version 4, in creating lifelike depictions of popular culture figures and realistic scenes, including landscapes and indoor spaces. The visual experience offered by Version 5 has been completely transformed, with the "Midjourney look" being replaced by enhanced photorealism and intricate details, thanks in part to a substantial boost in dynamic range.

Midjourney, an independent research lab with 11 full-time staff members, has a mission to explore new mediums of thought and expand human imagination through design, human infrastructure, and AI. Their latest version, currently in beta mode, is a testament to their commitment to innovation and pushing the boundaries of what AI can do.

The Midjourney Version 5 also offers a more versatile and responsive experience for users. The model's 'pro' mode provides a wider diversity of outputs and adapts more readily to user inputs, though this may make it somewhat harder to use. The system default for Version 5 is the photographic style, with options for generating images in different styles by referencing art movements, techniques, genres, and media types.

As an industry leader in AI generative art, Midjourney continues to blur the lines between reality and fantasy with each new iteration. However, some have voiced concerns over the platform's lack of moderation policies, given its growing ability to create stunningly photorealistic images, such as the now-famous Pope photo.

Users can try Midjourney Version 5 by adding the "v 5" parameter to the end of a prompt or by selecting "MJ Version 5" in the settings. While the platform has closed for free users, the AI-powered image generator BlueWillow is available as an alternative for those seeking a similar experience on Discord.
'''

tweet_pre_prompt_for_report = "你是市场营销大师，你非常擅长撰写 Tweet 并引起广泛转发和点赞，请基于下面的英文报道写一段简短有力的中文 Tweet，控制好字数不要超过 Twitter 的限制。请注意，涉及到人名和产品名以及品牌名的情况，保留英文即可；涉及到技术专有术语，也请保留英文或者英文缩写。\n\n"

translate_report_prompt = "你是精通中文和英文的计算机科学家，也是 CNN 的专栏记者，现在我把你刚刚发表的英文科技报道转载到中文媒体，请帮我翻译成中文。请注意，涉及到人名和产品名以及品牌名的情况，保留英文即可；涉及到技术专有术语，也请保留英文或者英文缩写：\n\n"

cnn_report_prompt = "你是 CNN 资深科技记者和最受欢迎的编辑，请为以下内容写一个英文报道. 只需回复内容, 不需要任何前缀标识。\n\n"

emoji_list_for_happy = ['🤨', '😆', '😙', '🤫', '😅', '😚', '😋', '😗', '😃', '😍', '🙂', '🤪', '😄', '🤩', '🤔', '😁', '😉', '😊', '😎', '🤭', '😘', '🤗', '😂', '🙈']

emoji_list_for_unhappy = ['😳', '😢', '😕', '😨', '😦', '😧', '😤', '😥', '😰', '😟', '😬', '😣', '😩', '😱', '😓', '🤪', '😠', '😔', '😡', '😞', '🤬', '😵', '😖', '😒', '🤯']

inproper_words_list = ['傻屄', '傻b', '傻x', '傻吊', '傻逼', '傻屌', '傻比', '傻狍子', '脱衣服', '脱了', '妈逼', '妈比', '妈的', '狗日', '狗屁', '狗屎', '狗娘', '做爱', '嘿咻', '啪啪', '插入', '艹', '草泥', '日逼', '奴仆', '奴隶']

avatar_first_response = '亲爱的你终于回消息啦, 消失了这么久 😓, 干啥去啦? 也不回个消息, 你知道我多担心你嘛 😢, 以后不许这样啦 😘, 快跟我说说最近都做了些啥, 我可想你啦 🤩'

change_persona = '来自 Bot Creator 的提示:\n\n如果您想更换该<AI 分身的>人物背景介绍, 可以让 ChatGPT 帮您完成。如果您不知道该如何让 ChatGPT 完成人物背景杜撰, 可以参考下面这个链接参考我是如何跟 ChatGPT 交流的:\n\nhttps://sharegpt.com/c/PmTkHvF'

about_system_prompt_txt = '这里记录了该我的角色定位和背景信息以及一些注意事项，如果需要调整角色定位，请修改 txt 文件并保存后直接回复给我, 我会自动保存并在下一条对话的时候自动启用新的角色定位! 🤭 最后, 千万不要修改文件名, 否则我就不认识了. 🤪'

about_dialogue_tone_xls = '这里记录了一些用户和我之间的模拟聊天记录范本, 用于指导我交流语气和方式。如果需要调整, 可以直接在 xls 表格里修改历史聊天语气和方式并保存，然后直接回复给我。空白的地方可以不填, 也可以填满，但是最好不要再添加更多了。🤗 最后, 千万不要修改文件名, 否则我就不认识了. 🤨'

avatar_change_guide = '这是我的头像, 请保存下来, 再到 @BotFather 里面设置我的头像吧 🤩 \n\n步骤: /mybots > 选择我的 Bot 名称 > Edit Bot > Edit Botpic > 然后你会看到: \nOK. Send me the new profile photo for the bot. \n这个时候直接把我这张头像发给 @BotFather 就好啦, 然后你再回到我这里就能看到我的头像已更新咯. 😍 \n\n当然, 你也可以用任何你喜欢的头像来装饰我, 哈哈 🤗'

REFILL_TEASER_DEFAULT="亲爱的, 该交公粮咯, 不交公粮就和其他白嫖的用户一样了, 总归还是有点限制的哈; 如果想要我继续为你贴身服务, 请点击 /pay 或发送 pay 获取独享的 USDT/USDC 充值地址, 并根据提示交完公粮哈, 交了公粮我就又可以一心一意服侍你啦 😘, 放心, 活好不粘人哦... 🙈"

user_commands = '''
/help # 帮助
/whoami # 获取 chat_id
/pay # 获取充值地址
/check_bill # 查询充值
/avatar # 获取我的头像
/image # 生成图片
/pdf # 针对PDF询问
/revise # 修改文案
/translate # 翻译文案
/emoji # 文字换成表情
/wolfram # 计算数学公式
/wikipedia # 维基百科查询
/twitter # 撰写推文
/summarize # 文案总结
/bing # 搜索并写新闻
/make_voice # 生成语音
/password # 生成密码
/feedback # 反馈建议
/commands # 命令列表
/sch # 保存聊天记录
/clear_memory # 清除记录
/mid # Midjourney提示词
/more_information
'''

bot_owner_commands = '''
# 以下列表仅限 Bot Onwer 使用

/blacklist # 黑名单管理
/remove_from_blacklist
/set_free_talk_limit
/set_monthly_fee
/set_refill_teaser
/check_refill_teaser
/group_send_file
/group_send_image
/group_send_audio
/group_send_message
/group_send_commands_list
# 点击这个会把用户命令列表群发给所有人
'''