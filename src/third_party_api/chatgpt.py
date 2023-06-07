import openai
import pandas as pd

from database.mysql import ChatHistory
from src.utils.logging_util import logging
from src.utils.prompt_template import (
    english_system_prompt,
    english_user_prompt,
    english_assistant_prompt,
    confirm_read_story_guide,
    kids_story_system_prompt,
    kids_story_user_prompt,
    kids_story_assistant_prompt,
)
from src.utils.utils import get_dialogue_tone, insert_gpt_story
from datetime import datetime

from src.utils.param_singleton import Params
from src.utils.prompt_template import (
    midjourney_prompt_fomula,
    midjourney_prompt_1,
    midjourney_user_prompt_fomula,
    midjourney_assistant_prompt_fomula,
)


def chat_gpt_full(
    prompt,
    system_prompt='',
    user_prompt='',
    assistant_prompt='',
    dynamic_model=Params().OPENAI_MODEL,
    chatgpt_key=Params().OPENAI_API_KEY,
):
    if not prompt:
        return
    if not system_prompt:
        system_prompt = "You are a very knowledgeable sage, and well-informed. You often help people to solve problems and answer questions, and people gain valuable information from your answers, which have a great impact on their lives and work."
    if not user_prompt:
        user_prompt = "Who won the world series in 2020?"
    if not assistant_prompt:
        assistant_prompt = "The Los Angeles Dodgers won the World Series in 2020."

    # Load your API key from an environment variable or secret management service
    openai.api_key = chatgpt_key
    print(f"DEBUG: {dynamic_model} 正在创作...")
    response = openai.ChatCompletion.create(
        model=dynamic_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": assistant_prompt},
            {"role": "user", "content": prompt},
        ],
    )

    reply = response['choices'][0]['message']['content']
    reply = reply.strip('\n').strip()

    return reply


# Call chatgpt and restore reply and send to chat_id:
async def local_chatgpt_to_reply(bot, msg_text, from_id, chat_id):
    openai.api_key = Params().OPENAI_API_KEY
    reply = ''

    try:
        df = pd.read_sql_query(
            f"SELECT * FROM (SELECT `id`, `username`, `msg_text` FROM `avatar_chat_history` WHERE `from_id` = '{from_id}' AND `msg_text` IS NOT NULL ORDER BY `id` DESC LIMIT 10) sub ORDER BY `id` ASC",
            Params().engine,
        )
    except Exception as e:
        logging.error(f"local_chatgpt_to_reply() read_sql_query() failed: \n\n{e}")
        return

    try:
        msg_history = get_dialogue_tone()
        previous_role = 'assistant'
        for i in range(df.shape[0]):
            history_conversation = df.iloc[i]
            user_or_assistant = 'assistant' if history_conversation['username'] in [bot.bot_name] else 'user'
            if user_or_assistant == previous_role:
                continue
            if i == df.shape[0] - 1 and user_or_assistant == 'user':
                continue
            if len(history_conversation['msg_text']) > 1200:
                continue
            need_to_be_appended = {
                "role": user_or_assistant,
                "content": history_conversation['msg_text'],
            }
            msg_history.append(need_to_be_appended)
            previous_role = user_or_assistant
        msg_history.append({"role": "user", "content": msg_text})

        response = await openai.ChatCompletion.acreate(model=Params().OPENAI_MODEL, messages=msg_history)
        reply = response['choices'][0]['message']['content']
        reply = reply.strip('\n').strip()

    except Exception as e:
        logging.error(f"local_chatgpt_to_reply chat_gpt() failed: \n\n{e}")

    if not reply:
        return

    store_reply = reply.replace("'", "")
    store_reply = store_reply.replace('"', '')
    try:
        with Params().Session() as session:
            new_record = ChatHistory(
                first_name='ChatGPT',
                last_name='Bot',
                username=bot.bot_name,
                from_id=from_id,
                chat_id=chat_id,
                update_time=datetime.now(),
                msg_text=store_reply,
                black_list=0,
            )
            # Add the new record to the session
            session.add(new_record)
            # Commit the session
            session.commit()
    except Exception as e:
        return logging.error(f"local_chatgpt_to_reply() save to avatar_chat_history failed: {e}")

    return reply


def chat_gpt_english(prompt, gpt_model=Params().OPENAI_MODEL):
    if not prompt:
        return
    logging.info(f"chat_gpt_english() user prompt: {prompt}")
    response = openai.ChatCompletion.create(
        model=gpt_model,
        messages=[
            {"role": "system", "content": english_system_prompt},
            {"role": "user", "content": english_user_prompt},
            {"role": "assistant", "content": english_assistant_prompt},
            # {"role": "user", "content": 'Vector database technology has continued to improve, offering better performance and more personalized user experiences for customers.'},
            # {"role": "assistant", "content": '/英译中:\n矢量数据库技术一直在不断改进, 为客户提供更佳的性能和更个性化的用户体验。'},
            # {"role": "user", "content": '''To address the challenges of digital intelligance in digital economy, artificial intelligence generate content (AIGC) has emerge. AIGC use artificial intalligence to assist or replace manual content generation by generating content based on userinputted keywords or requirements. '''},
            # {"role": "assistant", "content": english_assistant_prompt_2},
            # {"role": "user", "content": '''vector database'''},
            # {"role": "assistant", "content": english_assistant_prompt_3},
            # {"role": "user", "content": '''LLaMA'''},
            # {"role": "assistant", "content": english_assistant_prompt_4},
            {"role": "user", "content": prompt},
        ],
    )
    reply = response['choices'][0]['message']['content']
    reply = reply.strip('\n').strip()
    return reply


def chat_gpt_regular(prompt, chatgpt_key=Params().OPENAI_API_KEY, use_model=Params().OPENAI_MODEL):
    if not prompt:
        return

    # Load your API key from an environment variable or secret management service
    openai.api_key = chatgpt_key

    response = openai.ChatCompletion.create(model=use_model, messages=[{"role": "user", "content": prompt}])

    reply = response['choices'][0]['message']['content']
    reply = reply.strip('\n').strip()

    return reply


def chat_gpt_write_story(bot, chat_id, from_id, prompt, gpt_model=Params().OPENAI_MODEL):
    if not prompt:
        return
    try:
        logging.info(f"chat_gpt_write_story() user prompt: {prompt}")
        response = openai.ChatCompletion.create(
            model=gpt_model,
            messages=[
                {"role": "system", "content": kids_story_system_prompt},
                {"role": "user", "content": kids_story_user_prompt},
                {"role": "assistant", "content": kids_story_assistant_prompt},
                {"role": "user", "content": prompt},
            ],
        )
        story = response['choices'][0]['message']['content']
        story = story.strip('\n').strip()
        title = story.split('\n')[0]
        title = str(title).capitalize()
        insert_gpt_story(prompt, title, story, gpt_model, from_id, chat_id)
        bot.send_msg(story, chat_id)
        bot.send_msg(confirm_read_story_guide, chat_id)
        return

    except Exception as e:
        logging.error(f"chat_gpt_write_story():\n\n{e}")
    return


def create_midjourney_prompt(prompt):
    system_prompt = midjourney_prompt_fomula if 'fomula' in prompt else midjourney_prompt_1
    prompt = prompt.replace('fomula', '').strip()

    try:
        beautiful_midjourney_prompt = chat_gpt_full(
            prompt,
            system_prompt,
            midjourney_user_prompt_fomula,
            midjourney_assistant_prompt_fomula,
            dynamic_model=Params().OPENAI_MODEL,
            chatgpt_key=Params().OPENAI_API_KEY,
        )
    except Exception as e:
        print(f"ERROR: create_midjourney_prompt() failed with error: \n{e}")
        return

    return beautiful_midjourney_prompt
