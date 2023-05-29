import hashlib
import json
import os
import subprocess
import requests
from src.utils.param_singleton import Params
from src.utils.prompt_template import (
    elevenlabs_apikey_saved,
    elevenlabs_not_activate,
    eleven_labs_tts_failed_alert,
    eleven_labs_no_apikey_alert,
    eleven_labs_no_original_voice_alert,
)
from src.utils.utils import format_number
from src.database.mysql import *


# 当用户每次提交 elevenlabs_api_key 的时候, 需要检查用户输入的 elevenlabs_api_key 是否有效, 并将 get_elevenlabs_userinfo 返回的结果中的 subscription
# 写入数据库, 再通过 get_elevenlabs_voices 获得目前的 voice_id dict
def check_and_save_elevenlabs_api_key(bot, elevenlabs_api_key, from_id):
    subscription = get_elevenlabs_userinfo(elevenlabs_api_key)
    if subscription:
        if (
            subscription.get('status') == 'active'
            and subscription.get('can_use_instant_voice_cloning') == True
        ):
            print(f"DEBUG: check_elevenlabs_api_key() subscription: {subscription}")
            # 将 from_id, elevenlabs_api_key 插入ElevenLabsUser
            with Params().Session() as session:
                # 如果表单不存在则创建表单
                Base.metadata.create_all(Params().engine, checkfirst=True)
                # 检查 from_id 是否在 ElevenLabsUser 表中, 如果不在, 则创建新的记录, 如果在, 则更新 elevenlabs_api_key
                elevenlabs_user = (
                    session.query(ElevenLabsUser)
                    .filter(ElevenLabsUser.from_id == from_id)
                    .first()
                )
                if not elevenlabs_user:
                    elevenlabs_user = ElevenLabsUser(
                        from_id=from_id, elevenlabs_api_key=elevenlabs_api_key
                    )
                    session.add(elevenlabs_user)
                else:
                    # 更新 ElevenLabsUser 表中 from_id 用户的 elevenlabs_api_key
                    session.query(ElevenLabsUser).filter(
                        ElevenLabsUser.from_id == from_id
                    ).update({'elevenlabs_api_key': elevenlabs_api_key})
                session.commit()
            bot.send_msg(elevenlabs_apikey_saved, from_id)
            return subscription
        else:
            subscription_string = '\n'.join(
                [f"{k}: {v}" for k, v in subscription.items()]
            )
            failed_notice = f"{elevenlabs_not_activate}\n\n你的订阅信息如下, 请仔细查看是哪一项有问题:\n\n{subscription_string}"
            return bot.send_msg(failed_notice, from_id)
    else:
        return bot.send_msg(elevenlabs_not_activate, from_id)


def get_elevenlabs_userinfo(elevenlabs_api_key):
    url = "https://api.elevenlabs.io/v1/user"
    headers = {"accept": "application/json", "xi-api-key": elevenlabs_api_key}
    response = requests.get(url, headers=headers)
    return response.json().get('subscription', {})


'''
{
  "subscription": {
    "tier": "creator",
    "character_count": 18107,
    "character_limit": 100000,
    "can_extend_character_limit": true,
    "allowed_to_extend_character_limit": true,
    "next_character_count_reset_unix": 1680361833,
    "voice_limit": 30,
    "professional_voice_limit": 1,
    "can_extend_voice_limit": false,
    "can_use_instant_voice_cloning": true,
    "can_use_professional_voice_cloning": true,
    "currency": "usd",
    "status": "active"
  },
  "is_new_user": true,
  "xi_api_key": "7506563f79bd85dbf7dade0cc8412b42",
  "can_use_delayed_payment_methods": false
}
'''


'''
    class ElevenLabsUser(Base):
        __tablename__ = 'elevenlabs_user'

        id = Column(Integer, primary_key=True, autoincrement=True)
        from_id = Column(String(255))
        elevenlabs_api_key = Column(String(255))
        voice_id = Column(Text)
        last_time_voice_id = Column(String(255))
        original_voice_filepath = Column(String(255))
        test_count = Column(Integer, default=0)

        '''


# 根据 from_id 读取用户的 elevenlabs_api_key 和 original_voice_filepath 和 voice_id
def get_elevenlabs_api_key(from_id):
    with Params().Session() as session:
        # 读出 ElevenLabsUser 表中 from_id 用户的 elevenlabs_api_key 和 original_voice_filepath 和 voice_id 和 user_title
        elevenlabs_user = (
            session.query(ElevenLabsUser)
            .filter(ElevenLabsUser.from_id == from_id)
            .first()
        )
        if elevenlabs_user:
            return (
                elevenlabs_user.elevenlabs_api_key,
                elevenlabs_user.original_voice_filepath,
                elevenlabs_user.voice_id,
                elevenlabs_user.user_title,
            )
        else:
            return None, None, None, None


# 将 ElevenLabsUser 表中 from_id 的 ready_to_clone 字段更新为 1, user_title 更新为 user_title
def update_elevenlabs_user_ready_to_clone(from_id, user_title):
    with Params().Session() as session:
        # 如果用户存在, 则更新 ready_to_clone 字段为 1, 如果不存在则顺便创建
        elevenlabs_user = (
            session.query(ElevenLabsUser)
            .filter(ElevenLabsUser.from_id == from_id)
            .first()
        )
        if not elevenlabs_user:
            elevenlabs_user = ElevenLabsUser(
                from_id=from_id, ready_to_clone=1, user_title=user_title
            )
            session.add(elevenlabs_user)
        else:
            session.query(ElevenLabsUser).filter(
                ElevenLabsUser.from_id == from_id
            ).update({'ready_to_clone': 1, 'user_title': user_title})
        session.commit()
    return True


# 将输入的 original_voice_filepath 和 from_id 和 user_title 更新到 ElevenLabsUser 表中
def update_elevenlabs_user_original_voice_filepath(
    original_voice_filepath, from_id, user_title
):
    with Params().Session() as session:
        session.query(ElevenLabsUser).filter(ElevenLabsUser.from_id == from_id).update(
            {
                'original_voice_filepath': original_voice_filepath,
                'user_title': user_title,
            }
        )
        session.commit()
    return True


# 并将 ready_to_clone 字段更新为 0
def update_elevenlabs_user_ready_to_clone_to_0(
    bot, from_id, user_title, cmd='close_clone_voice'
):
    with Params().Session() as session:
        # 读取表中的 original_voice_filepath, 如果为空, 则说明用户没有上传过语音文件, 返回 False
        elevenlabs_user = (
            session.query(ElevenLabsUser)
            .filter(ElevenLabsUser.from_id == from_id)
            .first()
        )
        if not elevenlabs_user:
            # 将 from_id, user_title 插入ElevenLabsUser
            elevenlabs_user = ElevenLabsUser(
                from_id=from_id, ready_to_clone=0, user_title=user_title
            )
            session.add(elevenlabs_user)
            session.commit()

        if not elevenlabs_user.original_voice_filepath and cmd == 'confirm_my_voice':
            bot.send_msg(
                "你还没有上传过语音素材文件哦, 克隆还没成功呢, 请先上传语音文件再点击:\n/confirm_my_voice\n\n如果不想克隆你的声音了, 请点击:\n/close_clone_voice",
                from_id,
            )
            return

            # 更新 ready_to_clone 字段为 0
        session.query(ElevenLabsUser).filter(ElevenLabsUser.from_id == from_id).update(
            {'ready_to_clone': 0}
        )
        session.commit()
    if cmd == 'close_clone_voice':
        bot.send_msg(
            f"@{user_title} 你已经成功关闭了克隆声音功能, 以后你发来的语音我就当跟我聊天了, 不会用来当做训练克隆声音的素材, 放心哈。",
            from_id,
        )
    if cmd == 'confirm_my_voice':
        bot.send_msg(
            f"@{user_title}, 你的声音训练素材已经保存好了, 以后你发来的语音我就当跟我聊天了, 不会用来当做训练克隆声音的素材, 放心哈。",
            from_id,
        )
    return True


# 检查 ElevenLabsUser 表中 from_id 的 ready_to_clone 字段是否为 1
def elevenlabs_user_ready_to_clone(from_id):
    with Params().Session() as session:
        # 读出 ElevenLabsUser 表中 from_id 用户的 ready_to_clone = 1 的记录, 如果无记录, 说明用户不存在或者 ready_to_clone 字段不为 1, 返回 False, 否则返回 True
        elevenlabs_user = (
            session.query(ElevenLabsUser)
            .filter(
                ElevenLabsUser.from_id == from_id, ElevenLabsUser.ready_to_clone == 1
            )
            .first()
        )
        if not elevenlabs_user:
            return False
        else:
            return True


# 将 voice_id 添加到 ElevenLabsUser 表中
def update_elevenlabs_user_voice_id(voice_id, from_id):
    with Params().Session() as session:
        session.query(ElevenLabsUser).filter(ElevenLabsUser.from_id == from_id).update(
            {'voice_id': voice_id}
        )
        session.commit()
    return voice_id


# 为 elevenlabs 添加新的 voice
def elevenlabs_add_voice(name, from_id, original_voice_filepath, elevenlabs_api_key):
    url = "https://api.elevenlabs.io/v1/voices/add"
    headers = {"Accept": "application/json", "xi-api-key": elevenlabs_api_key}
    data = {'name': name, 'labels': '{"accent": "American"}', 'description': from_id}
    files = [
        (
            'files',
            (
                f'{original_voice_filepath}',
                open(f'{original_voice_filepath}', 'rb'),
                'audio/mpeg',
            ),
        )
    ]

    response = requests.post(url, headers=headers, data=data, files=files)
    print(response.text)
    voice_id = response.json().get('voice_id', None)
    if voice_id:
        return update_elevenlabs_user_voice_id(voice_id, from_id)


# r = elevenlabs_add_voice()
# print(json.dumps(r, indent=2))


def elevenlabs_update_voice(
    voice_id, voice_name, audio_file_path, user_eleven_labs_api_key
):
    curl_command = (
        f"curl -X 'POST' "
        f"'https://api.elevenlabs.io/v1/voices/{voice_id}/edit' "
        f"-H 'accept: application/json' "
        f"-H 'xi-api-key: {user_eleven_labs_api_key}' "
        f"-H 'Content-Type: multipart/form-data' "
        f"-F 'name={voice_name}' "
        f"-F 'files=@{audio_file_path};type=audio/wav' "
        f"-F 'labels='"
    )

    # Execute the curl command
    process = subprocess.Popen(
        curl_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    # Check if the command was successful
    if process.returncode != 0:
        raise Exception(f"Curl command failed: {stderr.decode('utf-8')}")

    # Parse the JSON response
    response = json.loads(stdout.decode('utf-8'))
    return response


# r = elevenlabs_update_voice(voice_id, voice_name, audio_file_path)
# print(json.dumps(r, indent=2))


def get_elevenlabs_voices(user_eleven_labs_api_key):
    url = 'https://api.elevenlabs.io/v1/voices'
    headers = {'accept': 'application/json', 'xi-api-key': user_eleven_labs_api_key}
    response = requests.get(url, headers=headers).json()
    # print(f"DEBUG: {response}")
    voices_dict = {}
    for voice in response['voices']:
        if voice['category'] == 'cloned':
            voices_dict[voice['name']] = voice['voice_id']
    # print(f"DEBUG: {voices_dict}")
    return voices_dict


'''
{
  "nanyang": "9ljiVpdb6qpxKPTng736",
  "chaochao": "CCgIdKx0m0QHHQUgFAVR",
  "anthony": "F6sIjTfa5MRpZTJiUrWH",
  "frankhu": "OE7bDvPK9rylQqr62NeZ",
  "vivianliu": "OX0yg3cTsrvlqUdlAbH5",
  "my_english_voice": "YEhWVRrlzrtA9MzdS8vE",
  "leowang_slow": "eXhbluainLzpz4zVbWr0",
  "yuchen": "h3TnXnm8yL5bQdjZsiWE"
}
'''
# r = get_elevenlabs_voices()
# print(json.dumps(r, indent=2))

'''
{
  "subscription": {
    "tier": "creator",
    "character_count": 18107,
    "character_limit": 100000,
    "can_extend_character_limit": true,
    "allowed_to_extend_character_limit": true,
    "next_character_count_reset_unix": 1680361833,
    "voice_limit": 30,
    "professional_voice_limit": 1,
    "can_extend_voice_limit": false,
    "can_use_instant_voice_cloning": true,
    "can_use_professional_voice_cloning": true,
    "currency": "usd",
    "status": "active"
  },
  "is_new_user": true,
  "xi_api_key": "7506563f79bd85dbf7dade0cc8412b42",
  "can_use_delayed_payment_methods": false
}
'''


def eleven_labs_tts(
    bot, content, from_id, tts_file_name, voice_id, user_eleven_labs_api_key
):
    print(f"DEBUG: eleven_labs_tts() voice_id: {voice_id}")

    subscription_started = get_elevenlabs_userinfo(user_eleven_labs_api_key)
    '''
    {
    "tier": "creator",
    "character_count": 21501,
    "character_limit": 100000,
    "can_extend_character_limit": true,
    "allowed_to_extend_character_limit": true,
    "next_character_count_reset_unix": 1680361833,
    "voice_limit": 30,
    "professional_voice_limit": 1,
    "can_extend_voice_limit": false,
    "can_use_instant_voice_cloning": true,
    "can_use_professional_voice_cloning": true,
    "currency": "usd",
    "status": "active"
    }
    '''

    words_remained = (
        subscription_started['character_limit']
        - subscription_started['character_count']
    )
    len_content = len(content)
    can_extend_character_limit = subscription_started['can_extend_character_limit']
    if len_content > words_remained and not can_extend_character_limit:
        out_range = f'''
        你的 Eleven Labs 每月可以合成语音的总单词量是 {format_number(subscription_started['character_limit'])}, 你本月已经使用的单词总数是 {format_number(subscription_started['character_count'])}, 你本次提交的单词总数是 {format_number(len_content)}, 超过了你的剩余可用额度 {format_number(words_remained)}, 与此同时你目前没有开通'即用即付(allowed_to_extend_character_limit)' 的功能, 建议如下:

        1) 减少本次生成的内容单词数到 {format_number(words_remained)} 以下;

        2) 激活即用即付的功能 (超出每月限量之后, 每 1000 个单词 0.3美金, 仅限 22 美金/月 级更高级别用户才可以激活此功能)

        具体的激活方法如下:
        登录 https://beta.elevenlabs.io/subscription 找到 Enable usage based billing (surpass 100000 characters), 把它右边的按钮打开即可。
        '''
        bot.send_msg(out_range, from_id)
        return

    API_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {"xi-api-key": user_eleven_labs_api_key}
    data = {
        "text": content,
        "voice_settings": {"stability": 0.95, "similarity_boost": 0.95},
    }
    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        with open(tts_file_name, "wb") as f:
            f.write(response.content)

        if os.path.isfile(tts_file_name):
            bot.send_audio(tts_file_name, from_id)

        subscription_finished = get_elevenlabs_userinfo(user_eleven_labs_api_key)
        '''
        {
        "tier": "creator",
        "character_count": 22083,
        "character_limit": 100000,
        "can_extend_character_limit": true,
        "allowed_to_extend_character_limit": true,
        "next_character_count_reset_unix": 1680361833,
        "voice_limit": 30,
        "professional_voice_limit": 1,
        "can_extend_voice_limit": false,
        "can_use_instant_voice_cloning": true,
        "can_use_professional_voice_cloning": true,
        "currency": "usd",
        "status": "active"
        }
        '''

        words_used = (
            subscription_finished['character_count']
            - subscription_started['character_count']
        )

        usd_cost = (
            ((words_used - words_remained) / 1000) * 0.3
            if words_used > words_remained and can_extend_character_limit
            else 0
        )
        usd_cost = round(usd_cost, 2)
        bot.send_msg(
            f"本次调用 Eleven Labs API 合成语音一共用量 {format_number(words_used)} 个单词, 实际消费 {usd_cost} usd, 本月剩余可用单词数 {format_number(subscription_finished['character_limit'] - subscription_finished['character_count'])}",
            from_id,
        )
        ''' response dir
        ['__attrs__', '__bool__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__enter__', '__eq__', '__exit__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__nonzero__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_content', '_content_consumed', '_next', 'apparent_encoding', 'close', 'connection', 'content', 'cookies', 'elapsed', 'encoding', 'headers', 'history', 'is_permanent_redirect', 'is_redirect', 'iter_content', 'iter_lines', 'json', 'links', 'next', 'ok', 'raise_for_status', 'raw', 'reason', 'request', 'status_code', 'text', 'url']
        '''
        # 将 response 的 text , reason, json 内容打印出来, 尝试过很多次, 打不出来, 可能没有文字内容, 只有音频内容, 反正音频内容是正常的。
        # print(response.text)
        # print(response.reason)
        # print(response.json())

        return True


def generate_clone_voice_audio_with_eleven_labs(
    bot, content, from_id, user_title, folder='files/audio/clone_voice'
):
    (
        elevenlabs_api_key,
        original_voice_filepath,
        voice_id,
        user_title_read,
    ) = get_elevenlabs_api_key(from_id)
    if not elevenlabs_api_key:
        bot.send_msg(eleven_labs_no_apikey_alert, from_id)
        return False
    if not original_voice_filepath:
        bot.send_msg(eleven_labs_no_original_voice_alert, from_id)
        return False
    if not user_title_read or user_title_read != user_title:
        update_elevenlabs_user_original_voice_filepath(
            original_voice_filepath, from_id, user_title
        )
    if not voice_id:
        voice_id = elevenlabs_add_voice(
            name=user_title,
            from_id=from_id,
            original_voice_filepath=original_voice_filepath,
            elevenlabs_api_key=elevenlabs_api_key,
        )
        if not voice_id:
            subscription = get_elevenlabs_userinfo(elevenlabs_api_key)
            if subscription:
                subscription_string = '\n'.join(
                    [f"{k}: {v}" for k, v in subscription.items()]
                )
                failed_notice = (
                    f"Eleven Labs 订阅信息如下, 请仔细查看是哪一项有问题:\n\n{subscription_string}"
                )
                eleven_labs_add_voice_failed_alert = (
                    f"{user_title}, 用你的克隆声音创建音频失败了, 😭😭😭...\n\n{failed_notice}"
                )
                bot.send_msg(eleven_labs_add_voice_failed_alert, from_id)
                # 发送错误信息以及相关参数给 BOTCREATER_CHAT_ID
                bot.send_msg(
                    f"ERROR: elevenlabs_add_voice() failed: \n\n@{user_title}\n/{from_id}\n{failed_notice}",
                    bot.bot_creator_id,
                )
                return False

    user_folder = f"{folder}/{from_id}"
    hashed_content = hashlib.md5(content.lower().encode('utf-8')).hexdigest()
    new_file_name = f"{from_id}_{user_title}_{hashed_content[-7:]}.mp3"
    tts_file_name = f"{user_folder}/{new_file_name}.mp3"
    if os.path.isfile(tts_file_name):
        bot.send_audio(tts_file_name, from_id)
        return True

    bot.send_msg(f"正在用你的声音克隆语音哈, 请稍等 1 分钟, 做好了马上发给你哦 😘", from_id)
    r = eleven_labs_tts(
        bot, content, from_id, tts_file_name, voice_id, elevenlabs_api_key
    )
    if r:
        return True
    else:
        bot.send_msg(
            f"{eleven_labs_tts_failed_alert}\n如果你的账号正常, 请转发本消息给 @laogege6 帮忙诊断一下把。",
            from_id,
        )
        return False
