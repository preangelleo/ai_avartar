import random

import asyncio
import time

from src.utils.logging_util import logging

import json
import httpx

MSG_PER_SECOND = 1
SEND_MSG_INTERVAL_SECOND = 1. / MSG_PER_SECOND
LOAD_TEST_DURARION_SECONDS = 60 * 5

LOAD_TEST_FANBOOK_BOT_TOKEN = ''
LOAD_TEST_FANBOOK_SEND_MSG_URL = f'https://a1.fanbook.mobi/api/bot/{LOAD_TEST_FANBOOK_BOT_TOKEN}/sendMessage'  # noqa
LOAD_TEST_CHAT_ID = ''
QUESTIONS_LIST = ['你喜欢读书吗？', '你觉得诚实重要吗？', '你觉得耐心重要吗？', '你喜欢冒险吗？', '你觉得学习与实践哪个更重要？', '你觉得梦想能实现吗？', '你有什么兴趣爱好？', '你喜欢海滩还是山区？', '你最喜欢的颜色是什么？', '你有什么关于沟通的建议吗？', '你喜欢喝茶还是果汁？', '你喜欢城市生活还是乡村生活？', '你喜欢大城市还是小城镇？', '你有什么关于目标设定的建议吗？', '你有什么关于工作的建议吗？', '你喜欢听音乐还是看电影？', '你喜欢夏天还是冬天？', '你有什么关于人际沟通的技巧吗？', '你觉得自律重要吗？', '最近有什么好看的电影推荐吗？', '你觉得幽默重要吗？', '你有什么关于成功的经验分享吗？', '你觉得忍耐力重要吗？', '你觉得勤奋重要吗？', '你会做饭吗？', '你认为人工智能会取代人类吗？', '你喜欢运动吗？', '你知道怎样学好英语吗？', '你觉得家庭重要吗？', '你有什么关于爱情的看法吗？', '你喜欢什么样的音乐？', '你觉得坚持重要吗？', '你喜欢购物吗？', '你好！', '你有什么关于幸福的定义吗？', '明天有什么特别的活动吗？', '你觉得学历重要吗？', '你有什么关于健康的建议吗？', '你有什么关于克服挫折的建议吗？', '你有什么关于心理健康的建议吗？', '你有什么关于个人形象的建议吗？', '你有什么关于解决问题的建议吗？', '你有什么关于情绪管理的建议吗？', '你喜欢室内运动还是户外运动？', '你觉得教育的意义是什么？', '你觉得坚持自己的价值观重要吗？', '你有什么旅行的计划吗？', '你觉得钱重要吗？', '你对环境保护有什么看法？', '你喜欢看喜剧还是惊悚片？', '你觉得生活中最重要的是什么？', '你喜欢喝牛奶还是果汁？', '你有什么关于身体健康的建议吗？', '你喜欢游戏吗？', '你觉得责任感重要吗？', '你喜欢喝咖啡还是茶？', '你喜欢喝果汁还是汽水？', '你觉得信任重要吗？', '你对未来有什么展望？', '喜欢喝咖啡还是茶？', '你有什么关于个人成长的建议吗？', '你有什么梦想？', '你觉得坚持梦想重要吗？', '你有看过什么好的电视剧吗？', '你会唱歌吗？', '你觉得团队合作重要吗？', '你喜欢参加派对吗？', '你喜欢看纪录片还是电影？', '你有什么关于职业规划的建议吗？', '你喜欢狗还是猫？', '你觉得友谊重要吗？', '你有什么关于克服困难的建议吗？', '你喜欢读小说还是非小说？', '你喜欢大吃大喝还是健康饮食？', '你有兄弟姐妹吗？', '你喜欢户外运动还是室内运动？', '今天天气怎么样？', '你觉得谦虚重要吗？', '你喜欢阳光明媚的天气吗？', '你有什么关于人际关系的建议吗？', '你有什么关于创造力的建议吗？', '你能告诉我一些关于人工智能的知识吗？', '你有什么关于生活态度的建议吗？', '你知道怎样放松自己吗？', '你喜欢室内活动还是户外活动？', '你觉得自由重要吗？', '你有什么关于时间管理的建议吗？', '你有什么关于人生哲理的思考吗？', '你觉得乐观态度重要吗？', '你觉得学习编程难吗？', '你觉得人生的意义是什么？', '你喜欢阅读小说还是非小说？', '你有什么关于学习的技巧吗？', '你有什么关于职业生涯的建议吗？', '你喜欢购物还是旅行？', '你能给我一些建议吗？']


async def send_msg_async(msg: str, chat_id):
    headers = {'Content-type': 'application/json'}
    payload = {'chat_id': int(chat_id), 'text': msg, 'desc': msg}

    async with httpx.AsyncClient() as client:
        response = await client.post(LOAD_TEST_FANBOOK_SEND_MSG_URL, data=json.dumps(payload), headers=headers)

    logging.debug(f'send_msg(): {response.json()}')
    return response.json()


async def main():
    total_msg_accum = 0
    tasks = []
    while total_msg_accum < LOAD_TEST_DURARION_SECONDS * MSG_PER_SECOND:
        await asyncio.sleep(SEND_MSG_INTERVAL_SECOND)
        # Randomly send a msg to tested bot
        tasks.append(
            asyncio.create_task(send_msg_async(random.choice(QUESTIONS_LIST), LOAD_TEST_CHAT_ID))
        )
        total_msg_accum += 1

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    logging.info('Start load tests')

    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter() - start
    logging.info(f'Finish load tests in {end:0.2f} seconds.')
