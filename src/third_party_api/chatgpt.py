import json
import random
import time

import openai
import tiktoken
import pandas as pd

from src.bot.single_message import SingleMessage
from src.database.mysql import ChatHistory
from src.utils.logging_util import logging
from src.utils.prompt_template import (
    english_system_prompt,
    english_user_prompt,
    english_assistant_prompt,
    confirm_read_story_guide,
    kids_story_system_prompt,
    kids_story_user_prompt,
    kids_story_assistant_prompt,
    image_description_prompt,
    response_to_user_message_prompt,
    is_bot_picture_prompt,
    system_role_prompt,
    improve_image_description_prompt,
    prompt_exposed,
    prompt_invalid,
    prompt_low_quality,
    system_role_gpt4_prompt,
    role_tone_examples,
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
    OPENAI_COST_USD_COUNTER,
    INITIAL_TEXT_REPLY_CRITIQUE_COUNTER,
)
from src.utils.metrics import OPENAI_PROMPT_TOKEN_USED_COUNTER
from src.utils.constants import OPENAI_PRICE_MAP


def get_openai_key():
    # Select different API key in a Round Robin way.
    return random.choice(Params().OPENAI_API_KEY_POOL)


def get_total_content_length_from_messages(msg_history):
    res = 0
    for msg in msg_history:
        res += len(msg.get('content', ''))
    return res


def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
    }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens


def get_cost_from_openai_response(model, response):
    return (
        response['usage']['prompt_tokens'] * OPENAI_PRICE_MAP[model]['prompt_tokens']
        + response['usage']['completion_tokens'] * OPENAI_PRICE_MAP[model]['completion_tokens']
    )


def get_text_reply_from_openai_response(response):
    return response['choices'][0]['message']['content']


async def get_response_from_chatgpt(model, messages, branch, functions=None, function_call=None, temperature=1.0):
    openai_start = time.perf_counter()
    if functions is not None:
        response = await openai.ChatCompletion.acreate(
            model=model, messages=messages, functions=functions, function_call=function_call, temperature=temperature
        )
    else:
        response = await openai.ChatCompletion.acreate(model=model, messages=messages, temperature=temperature)

    OPENAI_LATENCY_METRICS.labels(get_total_content_length_from_messages(messages) // 10 * 10, branch).observe(
        time.perf_counter() - openai_start
    )
    if response:
        OPENAI_PROMPT_TOKEN_USED_COUNTER.labels(branch).inc(response['usage']['prompt_tokens'])
        OPENAI_COMPLETION_TOKEN_USED_COUNTER.labels(branch).inc(response['usage']['completion_tokens'])
        OPENAI_TOKEN_PER_CONVERSATION_HISTOGRAM.labels(branch).observe(response['usage']['total_tokens'])

        cost = get_cost_from_openai_response(model, response)
        OPENAI_COST_USD_COUNTER.labels(branch).inc(cost)

        reason = response['choices'][0]['finish_reason']
        OPENAI_FINISH_REASON_COUNTER.labels(reason).inc()

    logging.debug('Chatgpt response:', response)

    if response is None:
        raise Exception("Empty openai response")

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


def is_exposed(text: str, user_msg: str) -> bool:
    exposure_keywords = ["虚拟", "没有身体", "没有真实的身体", "人工智能", "AI", "虚拟助手", "实体接触", "语言模型", "现实生活", "知识库", "模仿人类", "肉体"]
    for key in exposure_keywords:
        if key in text:
            return True
    return False


def is_invalid(text: str, user_msg: str) -> bool:
    invalid_keywords = ["无需改进"]
    for key in invalid_keywords:
        if key in text:
            return True
    return False


def is_request_long_reply(user_msg: str) -> bool:
    for key in ["故事", "作文", "论文", "情书", "全文", "背诵", "写一篇", "现代文", "古代文"]:
        if key in user_msg:
            return True
    return False


def is_request_image(user_msg: str) -> bool:
    for key in ["画", "照片", "图片"]:
        if key in user_msg:
            return True
    return False


def is_low_quality(text: str, user_msg: str) -> bool:
    # TODO: Use a small bert classifier in the future?
    low_quality_keywords = ["建议", "抱歉"]
    for key in low_quality_keywords:
        if key in text:
            return True
    if is_request_long_reply(user_msg):
        return False
    return len(text) > 100


def get_improved_text(full_text: str):
    if "improved_response" in full_text:
        return full_text.split("improved_response")[1].strip(": \n")
    elif (
        "original_response:" in full_text
        or "first_response:" in full_text
        or "reasoning:" in full_text
        or full_text.startswith("1. ")
    ):
        # If the response tried to reason but without "improved_response", return None for a final corrective call.
        return None
    else:
        # The LM returns the final response directly without reasoning
        return full_text


# Call chatgpt and get the text response or image description to send to users.
async def local_chatgpt_to_reply(bot, msg: SingleMessage):
    openai.api_key = get_openai_key()

    try:
        df = pd.read_sql_query(
            f"""
                SELECT * FROM (
                    SELECT 
                        a.`id`, a.`update_time`, a.`is_replied`, a.`username`, a.`msg_text`, b.`msg_text` as reply_text, b.`image_description`, b.`cost_usd`
                    FROM (
                        SELECT * from `avatar_chat_history` 
                        WHERE NOT (`first_name` = 'ChatGPT' AND `last_name` = 'Bot' )
                        AND `from_id` = {msg.from_id}
                        AND `msg_text` IS NOT NULL
                    ) a left outer join `avatar_chat_history` b on (a.`replied_message_id` = b.`message_id`)
                    ORDER BY a.`update_time` DESC LIMIT 6
                ) sub ORDER BY `update_time` ASC
            """,
            Params().engine,
        )
    except Exception as e:
        ERROR_COUNTER.labels('error_query_avatar_chat_history', 'chatgpt').inc()
        logging.error(f"local_chatgpt_to_reply() read_sql_query() failed: \n\n{e}")
        return

    initial_model_name = 'gpt-4-0613' if msg.user_is_treatment else 'gpt-3.5-turbo-16k-0613'
    if is_request_long_reply(msg.msg_text):
        logging.info(f"Use 16k model for initial story request")
        initial_model_name = 'gpt-3.5-turbo-16k-0613'
    if is_request_image(msg.msg_text):
        logging.info(f"Use 16k model for initial image request")
        initial_model_name = 'gpt-3.5-turbo-16k-0613'
    else:
        logging.info(
            f"{'Treatment' if msg.user_is_treatment else 'Control'}: Use {initial_model_name} for initial request"
        )

    if initial_model_name == 'gpt-4-0613':
        system_prompt_history = [
            {
                "role": "system",
                "content": system_role_gpt4_prompt.replace("{user_name}", msg.first_name).replace(
                    "{head_msg}", msg.msg_text
                ),
            }
        ]
    else:
        system_prompt_history = [{"role": "system", "content": system_role_prompt.format(user_name=msg.first_name)}]

    user_history_msg_list = role_tone_examples
    for i in range(df.shape[0]):
        history_conversation = df.iloc[i]
        user_history_msg_list.append({"role": "user", "content": history_conversation['msg_text']})
        if history_conversation['reply_text'] is not None and len(history_conversation['reply_text']) < 500:
            image_description = ''
            if history_conversation['image_description'] is not None:
                image_description = f"I draw a picture of {history_conversation['image_description']}."
            user_history_msg_list.append(
                {"role": "assistant", "content": image_description + history_conversation['reply_text']}
            )

    if initial_model_name == 'gpt-4-0613':
        initial_msg_request = user_history_msg_list[:-1] + system_prompt_history
    else:
        initial_msg_request = system_prompt_history + user_history_msg_list

    logging.info(f"initial_msg_request: {initial_msg_request}")

    try:
        # if num_tokens_from_messages(initial_msg_request) > 8000:
        #     logging.info(f"Use 16k model for initial long history request")
        #     initial_model_name = 'gpt-3.5-turbo-16k-0613'

        if initial_model_name == 'gpt-4-0613':
            function_call_params = {}
        else:
            function_call_params = {
                'functions': [
                    {
                        "name": "generate_image",
                        "description": "Only called when user explicitly want to see images. Generate an image according to user chat context.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "is_bot_picture": {
                                    "type": "boolean",
                                    "description": is_bot_picture_prompt,
                                },
                                "image_description": {
                                    "type": "string",
                                    "description": image_description_prompt,
                                },
                                "response_to_user_message": {
                                    "type": "string",
                                    "description": response_to_user_message_prompt,
                                },
                            },
                            "required": ["is_bot_picture", "image_description", "response_to_user_message"],
                        },
                    }
                ],
                'function_call': "auto",
            }
        response = await get_response_from_chatgpt(
            model=initial_model_name,
            messages=initial_msg_request,
            branch='local_reply',
            temperature=1.0,
            **function_call_params,
        )

        initial_call_cost = get_cost_from_openai_response(initial_model_name, response)
    except Exception as e:
        ERROR_COUNTER.labels('error_call_open_ai', 'chatgpt').inc()
        logging.error(f"initial call chat_gpt() failed: \n\n{e}")
        return

    # If the user want to see an image, we returned the comment as well as image description
    if 'function_call' in response['choices'][0]['message']:
        function_args = json.loads(response['choices'][0]['message']["function_call"]["arguments"])
        response_to_user_message = function_args.get('response_to_user_message')
        initial_image_description = function_args.get('image_description')
        is_bot_picture = function_args.get('is_bot_picture')

        logging.info(
            f"generate_image:\n"
            f"  image_description:{initial_image_description}\n"
            f"  response_to_user_message:{response_to_user_message}\n"
            f"  is_bot_picture:{is_bot_picture}"
        )
        image_description = initial_image_description
        refine_image_description_cost = 0
        try:
            # Refine the image description
            image_desc_refine_model = 'gpt-3.5-turbo'
            response = await get_response_from_chatgpt(
                model=image_desc_refine_model,
                messages=system_prompt_history
                + [{'role': 'user', 'content': msg.msg_text}]
                + [
                    {
                        'role': 'system',
                        'content': improve_image_description_prompt.replace(
                            "{image_description}", initial_image_description
                        ),
                    }
                ],
                branch='local_reply',
                temperature=0.5,
            )
            refine_image_description_cost = get_cost_from_openai_response(image_desc_refine_model, response)
            try:
                image_description_json = json.loads(get_text_reply_from_openai_response(response).strip())
                image_description = image_description_json['output']
                logging.info(f'Improved image_description: {image_description}')
            except json.JSONDecodeError:
                logging.info('fallback to use original image_description')
        except Exception as e:
            ERROR_COUNTER.labels('error_call_open_ai', 'chatgpt').inc()
            logging.error(f"refine image description call chat_gpt() failed: \n\n{e}")
        return (
            response_to_user_message,
            image_description,
            is_bot_picture,
            initial_call_cost + refine_image_description_cost,
        )

    # if no image is request, we need to refine the initial text reply
    initial_text_reply = get_text_reply_from_openai_response(response).strip("\"' :")
    if initial_model_name == 'gpt-4-0613':
        improved_text = get_improved_text(initial_text_reply)
        if improved_text is None:
            ERROR_COUNTER.labels('error_empty_gpt4_initial_response', 'chatgpt').inc()
            logging.error(f"local_chatgpt_to_reply() gpt4_initial_response failed: {initial_text_reply}")
            return
        initial_text_reply = improved_text

    logging.info(f'initial_text_reply: {initial_text_reply}')
    final_response = initial_text_reply
    critique_text_cost = 0
    ############################## Branch and Critique the initial response ##############################
    template = None
    # We don't need to handle low_quality and invalid case in gpt4 as it is powerful enough.
    if initial_model_name == 'gpt-4-0613':
        template_list = [('exposed_ai', is_exposed, prompt_exposed)]
    else:
        template_list = [
            ('exposed_ai', is_exposed, prompt_exposed),
            ('invalid_response', is_invalid, prompt_invalid),
            ('low_quality_response', is_low_quality, prompt_low_quality),
        ]

    for pair in template_list:
        if pair[1](initial_text_reply, msg.msg_text):
            template = pair[2]
            logging.info(f'critique reason: {pair[0]}')
            INITIAL_TEXT_REPLY_CRITIQUE_COUNTER.labels(pair[0]).inc()
            break

    # If we do find something to critique
    if template:
        critique_prompt = (
            template.replace("{user_name}", msg.first_name)
            .replace("{user_question}", msg.msg_text)
            .replace("{original_response}", initial_text_reply)
        )
        logging.debug(f"critique_prompt: {critique_prompt}")
        try:
            critique_model = 'gpt-4-0613' if initial_model_name == 'gpt-4-0613' else 'gpt-3.5-turbo'
            response = await get_response_from_chatgpt(
                model=critique_model,
                messages=([] if critique_model == 'gpt-4-0613' else system_prompt_history)
                + [{'role': 'user', 'content': msg.msg_text}, {'role': 'system', 'content': critique_prompt}],
                branch='local_reply',
                temperature=0.5,
            )
            critique_text_cost = get_cost_from_openai_response(critique_model, response)
            critique_text_reply = get_text_reply_from_openai_response(response).strip()
            logging.info(f'critique_text_reply: {critique_text_reply}')

            improved_response = get_improved_text(critique_text_reply)
            if improved_response is not None:
                final_response = improved_response

        except Exception as e:
            ERROR_COUNTER.labels('error_call_open_ai', 'chatgpt').inc()
            logging.error(f"text critique call chat_gpt() failed: \n\n{e}")

    final_response = final_response.strip("\"'")

    logging.debug(f"local_chatgpt_to_reply() success: {response}")
    return final_response, None, None, initial_call_cost + critique_text_cost


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
