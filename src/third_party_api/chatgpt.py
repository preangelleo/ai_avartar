import random
import time

import openai
import pandas as pd

from src.bot.single_message import SingleMessage
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
from src.utils.utils import get_system_prompt_and_dialogue_tone, insert_gpt_story
from datetime import datetime

from src.utils.param_singleton import Params
from src.utils.prompt_template import (
    midjourney_prompt_fomula,
    midjourney_prompt_1,
    midjourney_user_prompt_fomula,
    midjourney_assistant_prompt_fomula,
)
from src.utils.metrics import (
    ERROR_COUNTER,
    OPENAI_LATENCY_METRICS,
    OPENAI_FINISH_REASON_COUNTER,
    OPENAI_TOKEN_PER_CONVERSATION_HISTOGRAM,
    OPENAI_COMPLETION_TOKEN_USED_COUNTER,
)
from src.utils.metrics import OPENAI_PROMPT_TOKEN_USED_COUNTER


def get_openai_key():
    # Select different API key in a Round Robin way.
    return random.choice(Params().OPENAI_API_KEY_POOL)


def get_total_content_lenght_from_messages(msg_history):
    res = 0
    for msg in msg_history:
        res += len(msg.get('content', ''))
    return res


async def get_response_from_chatgpt(model, messages, branch, functions=None, function_call=None):
    openai_start = time.perf_counter()
    response = await openai.ChatCompletion.acreate(
        model=model, messages=messages, functions=functions, function_call=function_call
    )
    OPENAI_LATENCY_METRICS.labels(get_total_content_lenght_from_messages(messages) // 10 * 10, branch).observe(
        time.perf_counter() - openai_start
    )
    OPENAI_PROMPT_TOKEN_USED_COUNTER.labels(branch).inc(response['usage']['prompt_tokens'])
    OPENAI_COMPLETION_TOKEN_USED_COUNTER.labels(branch).inc(response['usage']['completion_tokens'])
    OPENAI_TOKEN_PER_CONVERSATION_HISTOGRAM.labels(branch).observe(response['usage']['total_tokens'])
    if response:
        reason = response['choices'][0]['finish_reason']
        OPENAI_FINISH_REASON_COUNTER.labels(reason).inc()

    logging.debug('Chatgpt response:', response)

    return response


async def chat_gpt_full(
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
    openai.api_key = get_openai_key()
    print(f"DEBUG: {dynamic_model} 正在创作...")
    response = await get_response_from_chatgpt(
        model=dynamic_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": assistant_prompt},
            {"role": "user", "content": prompt},
        ],
        branch='full',
    )

    reply = response['choices'][0]['message']['content']
    reply = reply.strip('\n').strip()

    return reply


# Call chatgpt and restore reply and send to msg.chat_id:
async def local_chatgpt_to_reply(bot, msg: SingleMessage):
    openai.api_key = get_openai_key()

    try:
        df = pd.read_sql_query(
            f"SELECT * FROM (SELECT `id`, `username`, `msg_text` FROM `avatar_chat_history` WHERE `from_id` = '{msg.from_id}' AND `msg_text` IS NOT NULL ORDER BY `id` DESC LIMIT 10) sub ORDER BY `id` ASC",
            Params().engine,
        )
    except Exception as e:
        ERROR_COUNTER.labels('error_query_avatar_chat_history', 'chatgpt').inc()
        logging.error(f"local_chatgpt_to_reply() read_sql_query() failed: \n\n{e}")
        return

    msg_history = get_system_prompt_and_dialogue_tone(msg.first_name)
    previous_role = 'assistant'
    for i in range(df.shape[0]):
        history_conversation = df.iloc[i]
        user_or_assistant = 'assistant' if history_conversation['username'] == bot.bot_name else 'user'
        if user_or_assistant == previous_role:
            continue
        if i == df.shape[0] - 1 and user_or_assistant == 'user':
            continue
        if len(history_conversation['msg_text']) > 1200:
            continue
        need_to_be_appended = {
            "role": user_or_assistant,
            # Prevent the bot admit that he is a AI model.
            "content": history_conversation['msg_text'].replace('AI语言模型', bot.bot_name).replace('人工智能程序', bot.bot_name),
        }
        msg_history.append(need_to_be_appended)
        previous_role = user_or_assistant
    msg_history.append({"role": "user", "content": msg.msg_text})
    logging.info("msg_history: ", msg_history)

    try:
        response = await get_response_from_chatgpt(
            model=Params().OPENAI_MODEL,
            messages=msg_history,
            branch='local_reply',
            functions=[
                {
                    "name": "generate_image",
                    "description": "Generate an image according to user chat context. Only called when user want to see images",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "image_description": {
                                "type": "string",
                                "description": "The prompt that will be used to feed into stable diffusion model to "
                                "generate image, infer this from messages. "
                                "the model is stable-diffusion-xl-beta-v2-2-2."
                                "Here are some examples: "
                                "1. A portrait of a cyborg in a golden suit, D&D sci-fi, artstation, concept art, highly detailed illustration. "
                                "2. A full portrait of a beautiful post apocalyptic offworld nanotechnician, intricate, elegant, highly detailed, digital painting, artstation, concept art, smooth, sharp focus, illustration, art by Krenz Cushart and Artem Demura and alphonse mucha. "
                                "Remember the following when you generate. "
                                "the audience enjoy japanese anime game, so the prompt should reflect the japanese anima style"
                                "this image description should be in engligh",
                            },
                            "response_to_user_message": {
                                "type": "string",
                                "description": "The response text sent to user after we send this image, it should have the same tone as system prompts.",
                            },
                        },
                        "required": ["image_description", "response_to_user_message"],
                    },
                }
            ],
            function_call="auto",
        )

    except Exception as e:
        ERROR_COUNTER.labels('error_call_open_ai', 'chatgpt').inc()
        logging.error(f"local_chatgpt_to_reply chat_gpt() failed: \n\n{e}")
        return

    if not response:
        return

    logging.info(f"local_chatgpt_to_reply() success: {response}")
    return response


async def chat_gpt_english(prompt, gpt_model=Params().OPENAI_MODEL):
    if not prompt:
        return
    logging.info(f"chat_gpt_english() user prompt: {prompt}")

    try:
        response = await get_response_from_chatgpt(
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
            branch='english',
        )
        reply = response['choices'][0]['message']['content']
        reply = reply.strip('\n').strip()

    except Exception as e:
        ERROR_COUNTER.labels('error_call_open_ai', 'english_teacher').inc()
        logging.error(f"chat_gpt_english() failed: \n\n{e}")
        return

    return reply


async def chat_gpt_regular(prompt, chatgpt_key=Params().OPENAI_API_KEY, use_model=Params().OPENAI_MODEL):
    if not prompt:
        return

    # Load your API key from an environment variable or secret management service
    openai.api_key = get_openai_key()

    response = await get_response_from_chatgpt(
        model=use_model, messages=[{"role": "user", "content": prompt}], branch='regular'
    )

    reply = response['choices'][0]['message']['content']
    reply = reply.strip('\n').strip()

    return reply


async def chat_gpt_write_story(bot, chat_id, from_id, prompt, gpt_model=Params().OPENAI_MODEL):
    if not prompt:
        return
    try:
        logging.info(f"chat_gpt_write_story() user prompt: {prompt}")
        response = await get_response_from_chatgpt(
            model=gpt_model,
            messages=[
                {"role": "system", "content": kids_story_system_prompt},
                {"role": "user", "content": kids_story_user_prompt},
                {"role": "assistant", "content": kids_story_assistant_prompt},
                {"role": "user", "content": prompt},
            ],
            branch='story',
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


async def create_midjourney_prompt(prompt):
    system_prompt = midjourney_prompt_fomula if 'fomula' in prompt else midjourney_prompt_1
    prompt = prompt.replace('fomula', '').strip()

    try:
        beautiful_midjourney_prompt = await chat_gpt_full(
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
