from src.bot.bot_branch.bot_branch import BotBranch
from src.third_party_api.chatgpt import chat_gpt_english
from src.utils.utils import *


# 定义一个 chat_gpt_english() 的前置函数, 先检查用户的 prompt 是否在历史数据库中出现过, 如果出现过就直接调用相应的 explanation_gpt, 如果没有记录就调用
# chat_gpt_english() 生成新的 explanation 发给用户 from_id 并记录到数据库中
def chat_gpt_english_explanation(bot, chat_id, prompt, gpt_model=Params().OPENAI_MODEL):
    if not chat_id or not prompt: return
    prompt = prompt.lower().strip()
    with Params().Session() as session:
        # 如果 fronm_id 不存在于表中, 则插入新的数据；如果已经存在, 则更新数据
        explanation_exists = session.query(sqlalchemy.exists().where(GptEnglishExplanation.word == prompt)).scalar()
        if not explanation_exists:
            bot.send_msg(
                f"收到, 我我去找 EnglishGPT 老师咨询一下 {prompt} 的意思, 然后再来告诉你 😗, 1 分钟以内答复你哈...",
                chat_id)
            gpt_explanation = chat_gpt_english(prompt, gpt_model)
            new_explanation = GptEnglishExplanation(word=prompt, explanation=gpt_explanation,
                                                    update_time=datetime.now(), gpt_model=gpt_model)
            session.add(new_explanation)
            session.commit()
        else:
            gpt_explanation = \
                session.query(GptEnglishExplanation.explanation).filter(
                    GptEnglishExplanation.word == prompt).first()[0]
    if gpt_explanation: bot.send_msg(gpt_explanation, chat_id)
    return


class EnglishTeacherBranch(BotBranch):
    def __init__(self):
        pass

    def handle_single_msg(self, msg, bot):
        msg_lower = msg.msg_text.lower()
        is_amy_command = True if msg_lower.startswith('/') else False
        msg_lower = msg_lower.replace('/', '')

        if bot.last_word_checked != msg_lower:
            bot.last_word_checked = msg_lower
            word_dict = st_find_ranks_for_word(msg_lower)
            if word_dict:
                word = word_dict.get('word', '')
                word_category = [key.upper() for key, value in word_dict.items() if
                                 value != 0 and key in ['toefl', 'gre', 'gmat', 'sat']]
                word_category_str = ' / '.join(word_category)
                word_trans = {
                    '单词': word,
                    '排名': word_dict.get('rank', ''),
                    '发音': word_dict.get('us-phonetic', ''),
                    '词库': word_category_str,
                    '词意': word_dict.get('chinese', ''),
                }
                results = '\n'.join(f"{k}:\t {v}" for k, v in word_trans.items() if v)
                append_info = f"\n\n让 Amy 老师来帮你解读: \n/{word}"
                try:
                    bot.send_msg(results + append_info, msg.chat_id)
                except Exception as e:
                    logging.error(f"Amy bot.send_msg()failed: \n\n{e}")
            else:
                is_amy_command = True

        if not is_amy_command: return
        return chat_gpt_english_explanation(bot, msg.chat_id, msg_lower, gpt_model=Params().OPENAI_MODEL)
