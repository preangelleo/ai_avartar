from c101functions import *

def chat_gpt_article_for_today():
    if debug: print(f"DEBUG : chat_gpt_article_for_today()")
    # 检查数据库今天是否已经更新过了，如果已经更新过了就跳过（返回），避免重复更新。
    df = pd.read_sql_query("SELECT * FROM `db_daily_articles` ORDER BY `id` DESC LIMIT 5", db_engine)
    df_today = df[df["update_time"].dt.date.eq(datetime.now().date())]

    # revised by chatgpt
    if len(df_today) >= 2: return
    if len(df_today) == 1:
        time_diff = (datetime.now() - df_today.iloc[1]["update_time"]).total_seconds()
        if time_diff < 43200: return

    try: REPORTS_FULL_LIST = st_english_study_report()
    except: return

    if debug: print(f"DEBUG : chat_gpt_article_for_today () got REPORTS_FULL_LIST")
    report, today_words_count, today_essential_words_list, df_category_list, sealed_words_list = REPORTS_FULL_LIST
    if not today_essential_words_list or len(today_essential_words_list) < 3: return
    
    responsed_content = ''
    today_words_str = ' '.join(today_essential_words_list[:100])
    if debug: print(f"DEBUG : chat_gpt_article_for_today () got today_words_str, length({len(today_words_str)})")
    try: responsed_content = chat_gpt(f"Can you write an article with these words below? \n\n {today_words_str}")
    except: return
    if not responsed_content: return
    if debug: print(f"DEBUG : chat_gpt_article_for_today () got responsed_content")
    word_conn = db_engine.connect()
    try: word_conn.execute("INSERT INTO `db_daily_articles` (`article`, `update_time`) VALUES (%s, %s)", (responsed_content, datetime.now()))
    except: print(f"ERROR : chat_gpt_article_for_today () database INSERT failed")
    word_conn.close()
    return


def daily_report_and_update(chat_id=bot_owner_chat_id):
    # 1
    try: chat_gpt_article_for_today()
    except: time.sleep(1)
    # 2
    send_msg(f"\nALI 101 每日定时任务已经成功执行完毕...\n{str(datetime.now()).split('.')[0]}", chat_id)
    return


if __name__ == "__main__":
    print(f"c101operation.py is running...")
