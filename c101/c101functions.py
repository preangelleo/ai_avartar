from c101dictionary import *

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# create an engine to connect to your database
engine = db_engine

# create a base for your declarative class
Base = declarative_base()

# create your table model


class OneTimePasscodeKey(Base):
    __tablename__ = 'one_time_passcode_key'
    id = Column(Integer, primary_key=True)
    app_name = Column(String(100))
    otp_key = Column(String(200))
    update_time = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f'<OneTimePasscodeKey(app_name={self.app_name}, otp_key={self.otp_key}, update_time={self.update_time})>'

# create the table in your database
# Base.metadata.create_all(engine)

# function to add app_name and its corresponding otp_key to the table


def add_otp_key(app_name, otp_key):
    # create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()

    # create a new OneTimePasscodeKey object
    otp = OneTimePasscodeKey(app_name=app_name, otp_key=otp_key)

    # add the new object to the session and commit the changes to the database
    session.add(otp)
    session.commit()

    # close the session
    session.close()
    return True

# function to validate the input passcode


def validate_otp(app_name, input_otp):
    # create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()

    # get the latest otp_key for the given app_name
    otp = session.query(OneTimePasscodeKey).filter_by(
        app_name=app_name).order_by(OneTimePasscodeKey.update_time.desc()).first()

    # validate the input passcode against the otp_key
    totp = pyotp.TOTP(otp.otp_key)
    is_valid = totp.verify(input_otp)

    # close the session
    session.close()

    return is_valid

# function to validate the input passcode


def read_otp(app_name):
    # create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()

    # get the latest otp_key for the given app_name
    otp = session.query(OneTimePasscodeKey).filter_by(
        app_name=app_name).order_by(OneTimePasscodeKey.update_time.desc()).first()

    # validate the input passcode against the otp_key
    totp = pyotp.TOTP(otp.otp_key)
    current_otp = totp.now()

    # close the session
    session.close()
    return current_otp

# st_binance_otp_key = pyotp.random_base32()
# print(st_binance_otp_key)
# add a new app_name and otp_key to the table
# add_otp_key('st_binance', st_binance_otp_key)


metadata = MetaData()

# define the table
notes_and_memos = Table('notes_and_memos', metadata,
                        Column('id', Integer, primary_key=True),
                        Column('notes_memos', Text),
                        Column('update_time', DateTime)
                        )

# create the table


def create_table_notes_and_memos():
    Session = sessionmaker(bind=engine)
    session = Session()
    metadata.create_all(engine)
    session.close()
    return

# insert a new record into the table


def update_table_notes_and_memos(input_notes):
    conn = engine.connect()
    conn.execute(notes_and_memos.insert().values(
        notes_memos=input_notes, update_time=datetime.now()))
    conn.close()
    return True

# search for records in the table


def search_table_notes_and_memos(key_words):
    conn = engine.connect()
    result = pd.read_sql_query(notes_and_memos.select().where(
        notes_and_memos.c.notes_memos.like(f'%{key_words}%')), conn)
    conn.close()
    notes_memos_list = result['notes_memos'].tolist(
    ) if not result.empty else []
    return notes_memos_list


# define the table
svb_creditcard_chuck = Table('svb_creditcard_chuck', metadata,
                             Column('id', Integer, primary_key=True),
                             Column('payments_note', Text),
                             Column('amount', Float),
                             Column('update_time', DateTime)
                             )

# create the table


def create_table_svb_creditcard_chuck():
    Session = sessionmaker(bind=engine)
    session = Session()
    metadata.create_all(engine)
    session.close()
    return

# insert a new record into the table


def update_svb_creditcard_chuck(input_amount, input_date_string):
    conn = engine.connect()
    update_time = datetime.strptime(input_date_string, '%m/%d/%Y')
    conn.execute(svb_creditcard_chuck.insert().values(
        payments_note='SVB CREDIT CARD PAYMENT 547854001082608 NG,CHARLES K', amount=input_amount, update_time=update_time))
    conn.close()
    return True

# calculate the sum of 'amount' column


def calculate_total_amount_svb_creditcard_chuck():
    from sqlalchemy import select, func
    conn = engine.connect()
    total_amount = conn.execute(
        select([func.sum(svb_creditcard_chuck.columns.amount)])).scalar()
    conn.close()
    return total_amount

# conn.execute("DROP TABLE `prompt_words`")
# conn.execute("DROP TABLE `prompt_examples`")
# conn.execute("DROP TABLE `pre_prompt_examples`")
# conn.execute("CREATE TABLE `prompt_words` (`id` INT UNSIGNED PRIMARY KEY NOT NULL AUTO_INCREMENT, `word` VARCHAR(30) NOT NULL, `word_rank` INT DEFAULT 0, `counts` INT DEFAULT 1, `chinese_meaning` TEXT, `update_time` DATETIME)")
# conn.execute("CREATE TABLE `prompt_examples` (`id` INT UNSIGNED PRIMARY KEY NOT NULL AUTO_INCREMENT, `prompt` TEXT, `update_time` DATETIME)")
# conn.execute("CREATE TABLE `pre_prompt_examples` (`id` INT UNSIGNED PRIMARY KEY NOT NULL AUTO_INCREMENT, `prompt` TEXT)")

# df = pd.read_sql_query(f"SELECT * FROM `pre_prompt_examples`", db_engine)
# conn.execute(f"DELETE FROM `pre_prompt_examples` WHERE `id` = 17")


def add_pre_prompt_and_words(prompt):
    prompt = prompt.lower()
    striped_prompt = str(prompt).translate(
        str.maketrans('', '', string.punctuation))

    try:
        df = pd.read_sql_query(
            f"SELECT prompt FROM `pre_prompt_examples` WHERE `prompt` = '{prompt}'", db_engine)
        if not df.empty:
            return

        prompt_conn = db_engine.connect()
        prompt_conn.execute(
            "INSERT INTO `pre_prompt_examples` (prompt, update_time) VALUES (%s, %s)", (prompt, datetime.now()))
    except:
        df = pd.read_sql_query(
            f"SELECT prompt FROM `pre_prompt_examples` WHERE `prompt` = '{striped_prompt}'", db_engine)
        if not df.empty:
            return

        prompt_conn = db_engine.connect()
        prompt_conn.execute(
            "INSERT INTO `pre_prompt_examples` (prompt, update_time) VALUES (%s, %s)", (striped_prompt, datetime.now()))

    prompt_conn.close()
    return True


def add_prompt_and_words(prompt, image_url=''):
    prompt = prompt.lower()

    striped_prompt = prompt.replace('"', '')
    striped_prompt = striped_prompt.replace("'", '')

    if not image_url:
        try:
            df = pd.read_sql_query(
                f"SELECT prompt FROM `prompt_examples` WHERE `prompt` = '{prompt}'", db_engine)
            if not df.empty:
                return

            prompt_conn = db_engine.connect()
            prompt_conn.execute(
                "INSERT INTO `prompt_examples` (prompt, update_time) VALUES (%s, %s)", (prompt, datetime.now()))
            if debug:
                print(
                    f"DEBUG: add_prompt_and_words() prompts have been added to DB table prompt_examples, without image_url")

        except:
            df = pd.read_sql_query(
                f"SELECT `prompt` FROM `prompt_examples` WHERE `prompt` = '{striped_prompt}'", db_engine)
            if not df.empty:
                return

            prompt_conn = db_engine.connect()
            prompt_conn.execute(
                "INSERT INTO `prompt_examples` (prompt, update_time) VALUES (%s, %s)", (striped_prompt, datetime.now()))
            if debug:
                print(f"DEBUG: add_prompt_and_words() prompts have been added to DB table prompt_examples, without image_url tried twice")

    else:
        try:
            df = pd.read_sql_query(
                f"SELECT prompt FROM `prompt_examples` WHERE `prompt` = '{prompt}'", db_engine)
            if not df.empty:
                return

            prompt_conn = db_engine.connect()
            prompt_conn.execute(
                "INSERT INTO `prompt_examples` (prompt, img_url, update_time) VALUES (%s, %s, %s)", (prompt, image_url, datetime.now()))

            if debug:
                print(
                    f"DEBUG: add_prompt_and_words() prompts have been added to DB table prompt_examples, with image_url")

        except:
            df = pd.read_sql_query(
                f"SELECT prompt FROM `prompt_examples` WHERE `prompt` = '{striped_prompt}'", db_engine)
            if not df.empty:
                return

            prompt_conn = db_engine.connect()
            prompt_conn.execute("INSERT INTO `prompt_examples` (prompt, img_url, update_time) VALUES (%s, %s, %s)", (
                striped_prompt, image_url, datetime.now()))

            if debug:
                print(
                    f"DEBUG: add_prompt_and_words() prompts have been added to DB table prompt_examples, with image_url tried twice")

    word_list = []
    synonyms_word_list = st_remove_puctuations_and_duplicated_contents(
        striped_prompt)
    word_set = set(synonyms_word_list)
    # print(f"DEBUG: add_prompt_and_words() word_set: \n{word_set}\n")

    for word in word_set:
        try:
            if '/' in word or len(word) < 2 or ':' in word:
                continue

            df_daily_words = pd.read_sql_query(
                f"SELECT `word`, `us-phonetic`, `rank`, `chinese` FROM `db_daily_words` WHERE word='{word}'", db_engine)
            if df_daily_words.empty:
                continue

            word_rank = df_daily_words.iloc[0]['rank']
            # phonetic = df_daily_words.iloc[0]['us-phonetic']
            chinese_meaning = df_daily_words.iloc[0]['chinese']

            is_mastered = 0
            df_word = pd.read_sql_query(
                f"SELECT `word`, `counts`, `is_mastered` FROM `prompt_words` WHERE `word` = '{word}'", db_engine)
            if df_word.empty:
                prompt_conn.execute("INSERT INTO `prompt_words` (word, word_rank, chinese_meaning, update_time) VALUES (%s, %s, %s, %s)", (word, int(
                    word_rank), chinese_meaning, datetime.now()))
                counts = 1
            else:
                counts = df_word.iloc[0]['counts']
                is_mastered = df_word.iloc[0]['is_mastered']
                counts += 1
                prompt_conn.execute(
                    f"UPDATE `prompt_words` SET counts={counts} WHERE word = '{word}'")

            if word_rank > 15000 and not is_mastered:
                word_list.append(
                    f"{word} | rank: {word_rank} | counts: {counts} | {chinese_meaning}")
        except Exception as e:
            print(f"ERROR: add_prompt_and_words(): \n{e}")

    prompt_conn.close()
    return word_list


def words_from_chose_prompt(prompt):
    word_list = []
    striped_prompt = str(prompt).translate(
        str.maketrans('', '', string.punctuation))

    for word in set(striped_prompt.lower().split()):
        df_word = pd.read_sql_query(
            f"SELECT `word`, `word_rank`, `counts`, `chinese_meaning` FROM `prompt_words` WHERE `word` = '{word}' AND `word_rank` > 5000", db_engine)
        if df_word.empty:
            continue

        word_rank = df_word.iloc[0]['word_rank']
        chinese_meaning = df_word.iloc[0]['chinese_meaning']
        counts = df_word.iloc[0]['counts']

        word_list.append(
            f"{word} | rank: {word_rank} | counts: {counts} | {chinese_meaning}")

    return word_list


if __name__ == '__main__':
    print(f"c101functions.py is running...")
