from enum import Enum as PyEnum

from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, Text, Boolean, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class PlanType(PyEnum):
    CREDIT_BASED = "credit_based"
    SUBSCRIPTION_BASED = "subscription_based"


class ChannelType(PyEnum):
    PUBLIC = "public"
    UNIVERSAL = "universal"  # universal means both private and public


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_from_id = Column(String(255), unique=True)
    subscriptions = relationship("Subscription", back_populates="user")
    plan_credits = relationship("PlanCredit", back_populates="user")


class Subscription(Base):
    __tablename__ = 'subscriptions'
    id = Column(Integer, primary_key=True)
    user_id = Column(String(255), ForeignKey('users.user_from_id'))
    start_date = Column(DateTime, default=datetime.now())
    end_date = Column(DateTime)
    user = relationship("User", back_populates="subscriptions")


class PlanCredit(Base):
    __tablename__ = 'plan_credits'
    id = Column(Integer, primary_key=True)
    user_id = Column(String(255), ForeignKey('users.user_from_id'))
    conversation_credit_count = Column(Integer)
    drawing_credit_count = Column(Integer)
    chat_type = Column(Enum(ChannelType))
    user = relationship("User", back_populates="plan_credits")


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    external_txn_id = Column(String(255), unique=True)
    subscription_id = Column(Integer, ForeignKey('subscriptions.id'), nullable=True)
    plan_credit_id = Column(Integer, ForeignKey('plan_credits.id'), nullable=True)
    transaction_time = Column(DateTime, default=datetime.now())  # New field for transaction time
    callback_json = Column(JSON)  # New field for storing callback JSON
    user_id = Column(String(255), ForeignKey('users.user_from_id'))
    subscription = relationship("Subscription")
    plan_credit = relationship("PlanCredit")
    # additional fields you may need


class ChatHistory(Base):
    __tablename__ = 'avatar_chat_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    username = Column(String(255))
    from_id = Column(String(255))
    chat_id = Column(String(255))
    update_time = Column(DateTime)
    msg_text = Column(Text)
    raw_msg = Column(Text)
    black_list = Column(Integer, default=0)
    is_private = Column(Boolean, default=0)
    is_mentioned = Column(Boolean, default=0)
    is_replied = Column(Boolean, default=0)
    branch = Column(String(255), default='local_chatgpt')
    replied_message_id = Column(String(255))
    image_description = Column(Text)
    comma_separated_image_url = Column(Text)
    cost_usd = Column(Float)


class OwnerParameter(Base):
    __tablename__ = 'avatar_owner_parameters'

    parameter_name = Column(String(255), primary_key=True)
    parameter_value = Column(String(255))
    update_time = Column(DateTime)


class SystemPrompt(Base):
    __tablename__ = 'avatar_system_prompt'

    id = Column(Integer, primary_key=True, autoincrement=True)
    system_prompt = Column(Text)
    update_time = Column(DateTime)


class DialogueTone(Base):
    __tablename__ = 'avatar_dialogue_tone'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tone_id = Column(Integer)
    role = Column(String(255))
    content = Column(Text)
    update_time = Column(DateTime)


class EthWallet(Base):
    __tablename__ = 'avatar_eth_wallet'

    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(Text)
    private_key = Column(Text)
    user_from_id = Column(String(255))
    create_time = Column(DateTime)


class CryptoPayments(Base):
    __tablename__ = 'avatar_crypto_payments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_from_id = Column(String(255))
    address = Column(String(255))
    usdt_paid_in = Column(Float, default=0)
    usdc_paid_in = Column(Float, default=0)
    eth_paid_in = Column(Float, default=0)
    update_time = Column(DateTime)
    Hash_id = Column(Text)


class UserPriority(Base):
    __tablename__ = 'avatar_user_priority'

    user_from_id = Column(String(255), primary_key=True)
    priority = Column(Integer, default=0)
    is_blacklist = Column(Integer, default=0)
    free_until = Column(DateTime, default=datetime.now())
    is_admin = Column(Integer, default=0)
    is_owner = Column(Integer, default=0)
    is_vip = Column(Integer, default=0)
    is_paid = Column(Integer, default=0)
    is_active = Column(Integer, default=0)
    is_deleted = Column(Integer, default=0)
    update_time = Column(DateTime, default=datetime.now())
    next_payment_time = Column(DateTime, default=datetime.now())


'''mysql> DESCRIBE db_cmc_total_supply;
+-----------------------+---------------+------+-----+---------+-------+
| Field                 | Type          | Null | Key | Default | Extra |
+-----------------------+---------------+------+-----+---------+-------+
| symbol                | varchar(20)   | NO   | PRI | NULL    |       |
| name                  | text          | YES  |     | NULL    |       |
| cmc_rank              | double        | YES  |     | NULL    |       |
| price                 | double        | YES  |     | NULL    |       |
| max_supply            | double        | YES  |     | NULL    |       |
| circulating_supply    | double        | YES  |     | NULL    |       |
| total_supply          | double        | YES  |     | NULL    |       |
| circulating_cap       | double        | YES  |     | NULL    |       |
| fdm_cap               | double        | YES  |     | NULL    |       |
| platform              | text          | YES  |     | NULL    |       |
| token_address         | text          | YES  |     | NULL    |       |
| date_added            | datetime      | YES  |     | NULL    |       |
| last_updated          | datetime      | YES  |     | NULL    |       |
| is_fiat               | bigint        | YES  |     | NULL    |       |
| first_historical_data | datetime      | YES  |     | NULL    |       |
| is_deleted            | bigint        | YES  |     | NULL    |       |
| bep_token_address     | text          | YES  |     | NULL    |       |
| tags                  | varchar(1000) | YES  |     | NULL    |       |
| decimals              | int           | YES  |     | NULL    |       |
| imple_address         | varchar(100)  | YES  |     | NULL    |       |
| listed_in_binance     | tinyint       | YES  |     | 0       |       |
| chain                 | varchar(10)   | YES  |     | NULL    |       |
| token_abi             | blob          | YES  |     | NULL    |       |
| in_1inch              | tinyint       | YES  |     | 0       |       |
| in_mylist             | tinyint       | YES  |     | 0       |       |
| in_blacklist          | tinyint       | YES  |     | 0       |       |
| in_alertlist          | tinyint       | YES  |     | 0       |       |
+-----------------------+---------------+------+-----+---------+-------+
27 rows in set (0.00 sec)
'''


class CmcTotalSupply(Base):
    __tablename__ = 'db_cmc_total_supply'

    symbol = Column(String(20), primary_key=True)
    name = Column(Text)
    cmc_rank = Column(Float)
    price = Column(Float)
    max_supply = Column(Float)
    circulating_supply = Column(Float)
    total_supply = Column(Float)
    circulating_cap = Column(Float)
    fdm_cap = Column(Float)
    platform = Column(Text)
    token_address = Column(Text)
    date_added = Column(DateTime)
    last_updated = Column(DateTime)
    is_fiat = Column(Float)
    first_historical_data = Column(DateTime)
    is_deleted = Column(Float)
    bep_token_address = Column(Text)
    tags = Column(String(1000))
    decimals = Column(Integer)
    imple_address = Column(String(100))
    listed_in_binance = Column(Integer)
    chain = Column(String(10))
    token_abi = Column(Text)
    in_1inch = Column(Integer)
    in_mylist = Column(Integer)
    in_blacklist = Column(Integer)
    in_alertlist = Column(Integer)


'''mysql> DESCRIBE db_daily_words;
+----------------------+--------------+------+-----+---------+----------------+
| Field                | Type         | Null | Key | Default | Extra          |
+----------------------+--------------+------+-----+---------+----------------+
| id                   | int unsigned | NO   | PRI | NULL    | auto_increment |
| word                 | varchar(20)  | NO   |     | NULL    |                |
| rank                 | int unsigned | YES  |     | NULL    |                |
| counts               | int unsigned | NO   |     | 0       |                |
| total_counts         | int unsigned | NO   |     | 0       |                |
| us-phonetic          | varchar(100) | YES  |     | NULL    |                |
| origin               | text         | YES  |     | NULL    |                |
| synonyms             | text         | YES  |     | NULL    |                |
| antonyms             | text         | YES  |     | NULL    |                |
| tag                  | varchar(100) | YES  |     | NULL    |                |
| chinese              | text         | YES  |     | NULL    |                |
| chat_gpt_explanation | text         | YES  |     | NULL    |                |
| note                 | text         | YES  |     | NULL    |                |
| memo                 | text         | YES  |     | NULL    |                |
| toefl                | tinyint      | NO   |     | 0       |                |
| gre                  | tinyint      | NO   |     | 0       |                |
| gmat                 | tinyint      | NO   |     | 0       |                |
| sat                  | tinyint      | NO   |     | 0       |                |
| scenario             | text         | YES  |     | NULL    |                |
| mastered             | tinyint      | NO   |     | 0       |                |
| level                | tinyint      | NO   |     | 0       |                |
| sentence             | text         | YES  |     | NULL    |                |
| last_check_time      | datetime     | YES  |     | NULL    |                |
| youdao_synced        | tinyint      | NO   |     | 0       |                |
| manually_updated     | tinyint      | NO   |     | 0       |                |
| derivative           | text         | YES  |     | NULL    |                |
| relevant             | text         | YES  |     | NULL    |                |
| phrase               | text         | YES  |     | NULL    |                |
| sealed               | tinyint      | NO   |     | 0       |                |
+----------------------+--------------+------+-----+---------+----------------+
29 rows in set (0.00 sec)
'''


class DailyWords(Base):
    __tablename__ = 'db_daily_words'

    id = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(String(20))
    rank = Column(Integer)
    counts = Column(Integer)
    total_counts = Column(Integer)
    us_phonetic = Column(String(100))
    origin = Column(Text)
    synonyms = Column(Text)
    antonyms = Column(Text)
    tag = Column(String(100))
    chinese = Column(Text)
    chat_gpt_explanation = Column(Text)
    note = Column(Text)
    memo = Column(Text)
    toefl = Column(Integer)
    gre = Column(Integer)
    gmat = Column(Integer)
    sat = Column(Integer)
    scenario = Column(Text)
    mastered = Column(Integer)
    level = Column(Integer)
    sentence = Column(Text)
    last_check_time = Column(DateTime)
    youdao_synced = Column(Integer)
    manually_updated = Column(Integer)
    derivative = Column(Text)
    relevant = Column(Text)
    phrase = Column(Text)
    sealed = Column(Integer)


class GptEnglishExplanation(Base):
    __tablename__ = 'gpt_english_explanation'

    id = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(String(30))
    explanation = Column(Text)
    gpt_model = Column(String(30))
    update_time = Column(DateTime)


class GptStory(Base):
    __tablename__ = 'gpt_story'

    id = Column(Integer, primary_key=True, autoincrement=True)
    prompt = Column(Text)
    title = Column(Text)
    story = Column(Text)
    gpt_model = Column(String(30))
    from_id = Column(String(255))
    chat_id = Column(String(255))
    update_time = Column(DateTime)


class ElevenLabsUser(Base):
    __tablename__ = 'elevenlabs_user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    from_id = Column(String(255))
    user_title = Column(String(255))
    elevenlabs_api_key = Column(String(255))
    voice_id = Column(Text)
    last_time_voice_id = Column(String(255))
    original_voice_filepath = Column(String(255))
    test_count = Column(Integer, default=0)
    ready_to_clone = Column(Integer, default=0)
