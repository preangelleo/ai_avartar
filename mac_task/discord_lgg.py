from main import *
import discord
from discord.ext import commands

# Replace 'YOUR_BOT_TOKEN' with the bot token you copied from the Discord Developer Portal
bot_token = DISCORD_BOT_TOKEN

# Create a new bot client
intents=discord.Intents.all()
#intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

def create_midjourney_prompt(prompt):

    system_prompt = '''
Instruction of how to create Midjourney Prompt for image greneration

------------------------------

The /imagine command generates a unique image from a short text description (known as a Prompt).

A Prompt is a short text phrase that the Midjourney Bot interprets to produce an image. The Midjourney Bot breaks down the words and phrases in a prompt into smaller pieces, called tokens, that can be compared to its training data and then used to generate an image. A well-crafted prompt can help make unique and exciting images.

Structure

Basic Prompts
A basic prompt can be as simple as a single word, phrase or emoji

Advanced Prompts
More advanced prompts can include one or more image URLs, multiple text phrases, and one or more parameters

Image Prompts
Image URLs can be added to a prompt to influence the style and content of the finished result. Image URLs always go at the front of a prompt.

Prompt Text
The text description of what image you want to generate. See below for prompting information and tips. Well-written prompts help generate amazing images.

Parameters
Parameters change how an image generates. Parameters can change aspect ratios, models, upscalers, and lots more. Parameters go at the end of the prompt.


Prompting Notes

Prompt Length
Prompts can be very simple. Single words (or even an emoji!) will produce an image. Very short prompts will rely heavily on Midjourney’s default style, so a more descriptive prompt is better for a unique look. However, super-long prompts aren’t always better. Concentrate on the main concepts you want to create.

Grammar
The Midjourney Bot does not understand grammar, sentence structure, or words like humans. Word choice also matters. More specific synonyms work better in many circumstances. Instead of big, try gigantic, enormous, or immense. Remove words when possible. Fewer words mean each word has a more powerful influence. Use commas, brackets, and hyphens to help organize your thoughts, but know the Midjourney Bot will not reliably interpret them. The Midjourney Bot does not consider capitalization.

Focus on What you Want
It is better to describe what you want instead of what you don’t want. If you ask for a party with 'no cake', your image will probably include a cake. If you want to ensure an object is not in the final image, try advance prompting using the --no parameter.

Think About What Details Matter
Anything left unsaid may suprise you. Be as specific or vague as you want, but anything you leave out will be randomized. Being vague is a great way to get variety, but you may not get the specific details you want.

Try to be clear about any context or details that are important to you. Think about:

Subject: person, animal, character, location, object, etc.
Medium: photo, painting, illustration, sculpture, doodle, tapestry, etc.
Environment: indoors, outdoors, on the moon, in Narnia, underwater, the Emerald City, etc.
Lighting: soft, ambient, overcast, neon, studio lights, etc
Color: vibrant, muted, bright, monochromatic, colorful, black and white, pastel, etc.
Mood: Sedate, calm, raucous, energetic, etc.
Composition: Portrait, headshot, closeup, birds-eye view, etc.

Use Collective Nouns
Plural words leave a lot to chance. Try specific numbers. Three cats is more specific than cats. Collective nouns also work, flock of birds instead of birds.


Explore Prompting

Even short single-word prompts will produce beautiful images in Midjourney's default style, but you can create more interesting personalized results by combining concepts like artistic medium, historical periods, location, and more.

Pick A Medium
Break out the paint, crayons, scratchboard, printing presses, glitter, ink, and colored paper. One of the best ways to generate a stylish image is by specifying an artistic medium.

prompt example: /imagine prompt <any art style> style cat

Art style examples:

Block Print 
Folk Art 
Cyanotype 
Graffiti 
Paint-by-Numbers 
Risograph 
Ukiyo-e 
Pencil Sketch 
Watercolor 
Pixel Art 
Blacklight 
Cross Stitch

Get Specific
More precise words and phrases will help create an image with exactly the right look and feel.

prompt example: /imagine prompt <style> sketch of a cat

a life drawing sketch of a cat
a continuous line sketch of a cat
a Loose Gestural sketch of a cat
a blind contour sketch of a cat
a value study sketch of a cat
a charcoal sketch of a cat

Parameter List

Parameters are options added to a prompt that change how an image generates. Parameters can change an image's Aspect Ratios, switch between Midjourney Model Versions, change which Upscaler is used, and lots more.

Parameters are always added to the end of a prompt. You can add multiple parameters to each prompt.

Basic Parameters

Aspect Ratios
--aspect, or --ar Change the aspect ratio of a generation. I use --ar 16:9 the most, so if I don't specifically put --ar parameters, then you help me to add --ar 16:9

No
--no Negative prompting, --no plants would try to remove plants from the image.

Style
--style <4a, 4b or 4c> Switch between versions of the Midjourney Model Version 4

Stylize
--stylize <number>, or --s <number> parameter influences how strongly Midjourney's default aesthetic style is applied to Jobs.

Sameseed
--sameseed Seed values create a single large random noise field applied across all images in the initial grid. When --sameseed is specified, all images in the initial grid use the same starting noise and will produce very similar generated images.

Niji
--niji An alternative model focused on anime style images.

The niji model is a collaboration between Midjourney and Spellbrush tuned to produce anime and illustrative styles. The --niji model has vastly more knowledge of anime, anime styles, and anime aesthetics. It's excellent at dynamic and action shots and character-focused compositions in general.

Notes on the --niji model:
Niji does not support the --stylize parameter. 

prompt example: vibrant California poppies --niji


Multi Prompts

It is possible to have the Midjourney Bot consider two or more separate concepts individually using :: as a separator. Separating prompts allows you to assign relative importance to parts of a prompt.

Multi-Prompt Basics
Adding a double colon :: to a prompt indicates to the Midjourney Bot that it should consider each part of the prompt separately. In the example below, for the prompt hot dog all words are considered together, and the Midjourney Bot produces images of tasty hotdogs. If the prompt is separated into two parts, hot:: dog both concepts are considered separately, creating a picture of a dog that is warm.

For examples:

cup cake illustration
Cup cake illustration is considered together producing illustrated images of cup cakes.

cup:: cake illustration
Cup is considered separately from cake illustration producing images of cakes in cups.

cup:: cake:: illustration
Cup, cake, and illustration are considered separately, producing a cake in a cup with common illustration elements like flowers and butterflies.

Prompt Weights
When a double colon :: is used to separate a prompt into different parts, you can add a number immediately after the double colon to assign the relative importance to that part of the prompt.

In the example below, the prompt hot:: dog produced a dog that is hot. Changing the prompt to hot::2 dog makes the word hot twice as important as the word dog, producing an image of a dog that is very hot!

Weights are normalized:
hot:: dog is the same as hot::1 dog, hot:: dog::1,hot::2 dog::2, hot::100 dog::100, etc.
cup::2 cake is the same as cup::4 cake::2, cup::100 cake::50 etc.
cup:: cake:: illustration is the same as cup::1 cake::1 illustration::1, cup::1 cake:: illustration::, cup::2 cake::2 illustration::2 etc.

Negative Prompt Weights
Negative weights can be added to prompts to remove unwanted elements.
The sum of all weights must be a positive number.

For examples:

vibrant tulip fields
A range of colored tulips are produced.
vibrant tulip fields:: red::-.5
Tulip fields are less likely to contain the color red.

Weights are normalized so:
tulips:: red::-.5 is the same as tulips::2 red::-1, tulips::200 red::-100, etc.

The --no Parameter
The --no parameter is the same as weighing part of a multi prompt to -.5 vibrant tulip fields:: red::-.5 is the same as vibrant tulip fields --no red.


Permutation Prompts

Permutation Prompts allow you to quickly generate variations of a Prompt with a single /imagine command. By including lists of options separated with commas , within curly braces {} in your prompt, you can create multiple versions of a prompt with different combinations of those options.

Permutation Prompt Basics
Separate your list of options within curly brackets {} to quickly create and process multiple prompt variations.


Prompt Example:

/imagine prompt a {red, green, yellow} bird 

Above prompt creates and processes three Jobs below:

/imagine prompt a red bird
/imagine prompt a green bird
/imagine prompt a yellow bird

Banned words can not use:

intimate, naked, nude, etc.

-----------------------------------

Read above instruction and use the following info as a reference to create ideal Midjourney prompts.

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

You will now receive some key words from me and then you will help me to create one creative prompts based on these key words I provided, following the instrution doc and using the best practices mentioned above. Do not include explanations or other unnecessary informations in your response. 

P.S. I'll be adding the /imagine prompt prefix to each prompt you create, so there's no need for you to include it in your prompts. Please keep them clear and concise.
'''

    user_prompt = '''
blond girl and car
'''

    assistant_prompt = '''
A stunning photograph of a blond girl with an enigmatic smile, posing beside a sleek and powerful car, her hair cascading gently over her shoulders in the gentle breeze. The car, with its pristine white finish, serves as a captivating backdrop for the subject, highlighting her grace and elegance. The warm sunlight streaming through the trees cast a dreamlike glow over the scene, bringing a sense of tranquility and serenity. The photo is expertly composed, with the tight framing emphasizing the subject's striking features, and the shallow depth of field serving to blur the background, allowing the viewer to focus solely on the subject and the car. Sony FE 24-70mm f/2.8 GM Lens, ISO 200, f/2.8, 1/1000s --ar 16:9
'''

    # 根据 prompt 生成 story
    try: message = chat_gpt_full(prompt, system_prompt, user_prompt, assistant_prompt, dynamic_model = 'gpt-4', chatgpt_key = OPENAI_API_KEY)
    except Exception as e: 
        print(f"ERROR: create_midjourney_prompt() failed with error: \n{e}")
        return
    
    return message

# Message listener
@bot.event
async def on_message(message: discord.Message):
    # Ignore messages sent by the bot itself
    if message.author == bot.user: return

    first_command = message.content.lower().split()[0]
    # Reply to the channel with a custom message
    if first_command == "/prompt":
        prompt = message.content.lower().split("/prompt ", 1)[-1]
        try:
            msg = create_midjourney_prompt(prompt)
            if msg: 
                msg = f"/imagine prompt: {msg}"
                if not '--ar ' in msg: msg += ' --ar 16:9'
                await message.channel.send(msg)
                
        except Exception as e: print(f"ERROR: on_message() failed with error: \n{e}")
        return
        
    elif first_command == "/bot" or first_command == "<@1094383785795137606>":
        prompt = message.content.lower().split("/bot ", 1)[-1] if first_command == "/bot" else message.content.lower().split("<@1094383785795137606> ", 1)[-1]
        try: 
            msg = chat_gpt_regular(prompt, use_model = 'gpt-4', chatgpt_key = OPENAI_API_KEY)
            if msg: await message.channel.send(msg)
        except Exception as e: print(f"ERROR: on_message() failed with error: \n{e}")
        return
    
    # Process commands after checking for custom replies
    await bot.process_commands(message)
    return 

if __name__ == "__main__":
    print(f"DEBUG: discord_lgg.py started")
    
    # Start the Discord bot
    bot.run(bot_token)
