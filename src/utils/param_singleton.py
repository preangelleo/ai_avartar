import logging
import threading

from database.mysql import OwnerParameter


from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.utilities.wolfram_alpha import WolframAlphaAPIWrapper
from langchain.utilities import WikipediaAPIWrapper

import os
from sqlalchemy import create_engine
from sqlalchemy.schema import MetaData
from sqlalchemy.orm import sessionmaker
import openai

import pinecone
from web3 import Web3

from dotenv import load_dotenv
from src.utils.prompt_template import REFILL_TEASER_DEFAULT


class Params:
    __initialized = False
    _instance = None
    _lock = threading.Lock()
    free_user_free_talk_per_month_lock = threading.Lock()
    refill_teaser_lock = threading.Lock()

    # 读出 avatar_owner_parameters 表中现有的 parameter_name 和 parameter_value, 并返回一个字典
    def get_owner_parameters(self):
        print('DEBUG: get_owner_parameters()')
        # Create a new session
        with self.Session() as session:
            # Query the table 'avatar_owner_parameters'
            owner_parameters = session.query(OwnerParameter).all()
            # Create a new empty dictionary
            owner_parameters_dict = {}
            # Loop through the owner_parameters and add them into the dictionary
            for owner_parameter in owner_parameters:
                owner_parameters_dict[owner_parameter.parameter_name] = owner_parameter.parameter_value
        return owner_parameters_dict

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                # Another thread could have created the instance
                # before we acquired the lock. So check that the
                # instance is still nonexistent.
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self.__initialized:
            return
        self.__initialized = True
        load_dotenv()

        # 获取环境变量
        db_host = os.getenv('DB_HOST')
        db_port = os.getenv('DB_PORT')
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')
        db_name = os.getenv('DB_NAME')

        self.INFURA_KEY = os.getenv('INFURA_KEY')
        self.DEBANK_API = os.getenv('DEBANK_API')
        self.CMC_PA_API = os.getenv('CMC_PA_API')
        self.MORALIS_API = os.getenv('MORALIS_API')
        self.ETHERSCAN_API = os.getenv('ETHERSCAN_API')
        # default to 0.0 if not configured
        self.MONTHLY_FEE = float(os.getenv('MONTHLY_FEE'))

        self.INFURA = ("https://mainnet.infura.io/v3/" + self.INFURA_KEY) if self.INFURA_KEY else None
        self.web3 = Web3(Web3.HTTPProvider(self.INFURA)) if self.INFURA else None

        self.ETH_REGEX = r'0x[a-fA-F0-9]{40}'
        self.TRX_REGEX = r'T[1-9A-HJ-NP-Za-km-z]{33}'
        self.EMAIL_ADDRESS_REGEX = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'

        self.USDT_ERC20 = '0xdAC17F958D2ee523a2206206994597C13D831ec7'
        self.USDT_ERC20_DECIMALS = 6

        self.USDC_ERC20 = '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'
        self.USDC_ERC20_DECIMALS = 6

        self.REFILL_TEASER = (
            "亲爱的, 该交公粮咯, 不过现在我们也还没分手, 所以你还可以继续用我, 就像其他免费用户一样; "
            "如果想要我继续为你贴身服务, 请点击 /pay 获得独享的充值地址, 并根据提示交完公粮哈,"
            " 交了公粮我就又可以一心一意服侍你啦 😘, 放心, 活好不粘人哦... 🙈"
        )

        # 连接本地数据库
        self.engine = create_engine(
            f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}',
            pool_pre_ping=True,
        )
        self.Session = sessionmaker(bind=self.engine)

        owner_parameters_dict = self.get_owner_parameters()

        # Get the environment variables
        self.USER_AVATAR_NAME = owner_parameters_dict.get('USER_AVATAR_NAME')
        self.UBUNTU_SERVER_IP_ADDRESS = owner_parameters_dict.get('UBUNTU_SERVER_IP_ADDRESS')
        self.DOMAIN_NAME = owner_parameters_dict.get('DOMAIN_NAME')
        self.OPENAI_API_KEY = owner_parameters_dict.get('OPENAI_API_KEY')
        self.REPLICATE_KEY = owner_parameters_dict.get('REPLICATE_KEY')
        self.STABILITY_API_KEY = owner_parameters_dict.get('STABILITY_API_KEY')
        self.OPENAI_MODEL = owner_parameters_dict.get('OPENAI_MODEL')
        self.WOLFRAM_ALPHA_APPID = owner_parameters_dict.get('WOLFRAM_ALPHA_APPID')
        self.MAX_CONVERSATION_PER_MONTH = owner_parameters_dict.get('MAX_CONVERSATION_PER_MONTH')
        self.PINECONE_FREE = owner_parameters_dict.get('PINECONE_FREE')
        self.PINECONE_FREE_ENV = owner_parameters_dict.get('PINECONE_FREE_ENV')
        self.INFURA_KEY = owner_parameters_dict.get('INFURA_KEY')
        self.CMC_PA_API = owner_parameters_dict.get('CMC_PA_API')
        self.FINNHUB_API = owner_parameters_dict.get('FINNHUB_API')
        self.ETHERSCAN_API = owner_parameters_dict.get('ETHERSCAN_API')
        self.MORALIS_API = owner_parameters_dict.get('MORALIS_API')
        self.MORALIS_ID = owner_parameters_dict.get('MORALIS_ID')
        self.MORALIS_APP_ID = owner_parameters_dict.get('MORALIS_APP_ID')
        self.DEBANK_API = owner_parameters_dict.get('DEBANK_API')
        self.MONTHLY_FEE = float(owner_parameters_dict.get('MONTHLY_FEE'))
        self.REFILL_TEASER = owner_parameters_dict.get('REFILL_TEASER')
        self.ELEVEN_API_KEY = owner_parameters_dict.get('ELEVEN_API_KEY')
        self.ELEVENLABS_STATUS = owner_parameters_dict.get('ELEVENLABS_STATUS')

        # 查看当前目录并决定 TELEGRAM_BOT_RUNNING 的值
        self.TELEGRAM_BOTOWNER_CHAT_ID = owner_parameters_dict.get('BOTOWNER_CHAT_ID')
        self.TELEGRAM_BOTCREATER_CHAT_ID = owner_parameters_dict.get('BOTCREATER_CHAT_ID')
        self.TELEGRAM_BOT_TOKEN = owner_parameters_dict.get('BOT_TOKEN')
        self.TELEGRAM_BOT_NAME = owner_parameters_dict.get('BOT_USERNAME')
        self.TELEGRAM_BOTOWNER_NAME = owner_parameters_dict.get('USER_TELEGRAM_LINK').split('/')[-1]

        # Fanbook Param

        self.FANBOOK_BOT_TOKEN = owner_parameters_dict.get('FANBOOK_BOT_TOKEN')
        self.FANBOOK_BOT_NAME = owner_parameters_dict.get('FANBOOK_BOT_USERNAME')
        self.FANBOOK_BOT_ID = owner_parameters_dict.get('FANBOOK_BOT_ID')
        self.FANBOOK_BOT_OWNER_NAME = owner_parameters_dict.get('FANBOOK_BOT_OWNER_NAME')
        self.FANBOOK_BOT_OWNER_ID = owner_parameters_dict.get('FANBOOK_BOT_OWNER_ID')
        self.FANBOOK_BOT_CREATOR_ID = owner_parameters_dict.get('FANBOOK_BOT_CREATOR_ID')
        self.FANBOOK_CLIENT_ID = owner_parameters_dict.get('FANBOOK_CLIENT_ID')
        self.FANBOOK_MAX_NUM_USER = owner_parameters_dict.get('FANBOOK_MAX_NUM_USER')

        logging.info(f'FANBOOK_BOT_NAME: {self.FANBOOK_BOT_NAME}')

        openai.api_key = self.OPENAI_API_KEY
        os.environ["OPENAI_API_KEY"] = self.OPENAI_API_KEY

        self.ELEVENLABS_API = self.ELEVEN_API_KEY
        self.BING_SEARCH_API_KEY = os.getenv("BING_SEARCH_API")
        self.STABILITY_URL = "https://api.stability.ai/v1/"

        self.ETHERSCAN_WALLET_URL_PREFIX = 'https://etherscan.io/address/'
        self.ETHERSCAN_TX_URL_PREFIX = 'https://etherscan.io/tx/'
        self.ETHERSCAN_TOKEN_URL_PREFIX = 'https://etherscan.io/token/'

        self.BOTCREATER_TELEGRAM_HANDLE = '@laogege6'

        # initialize pinecone
        pinecone.init(api_key=self.PINECONE_FREE, environment=self.PINECONE_FREE_ENV)

        os.environ["WOLFRAM_ALPHA_APPID"] = os.getenv('WOLFRAM_ALPHA_APPID')
        self.wolfram = WolframAlphaAPIWrapper()
        self.wikipedia = WikipediaAPIWrapper()

        self.embeddings = OpenAIEmbeddings(openai_api_key=self.OPENAI_API_KEY)
        self.llm = ChatOpenAI(
            model_name="gpt-4",
            temperature=0,
            openai_api_key=self.OPENAI_API_KEY,
        )

        self.avatar_png = 'files/images/512.png'
        self.avatar_command_png = 'files/images/avatar_command.png'
        self.avatar_create = (
            f"如果您也希望拥有一个像 @{self.TELEGRAM_BOT_NAME} "
            f"这样的 <AI分身> 来服务您的朋友们, 以您的语气陪他们/她们聊天, "
            f"帮他们完成 OpenAI 大语言模型可以做的一切任务, 可以点击 /more_information 了解, 非诚勿扰, 谢谢! 😋"
        )
        self.avatar_more_information = (
            "<AI分身> 电报机器人由酷爱 Python 的老哥哥 @laogege6 "
            "利用业余时间开发创造 😊:\n\n- 技术服务费: 100美金/月;\n- 支持 USDT 等各种付款方式;\n"
            "- 需要您提供自己的 OpenAI API;\n- 需要您在 @BotFather 开通机器人账号;\n-"
            " 您可以随时修改 <AI分身> 的人设背景;\n- 您可以自由修改 <AI分身> 的语调语气."
            "\n\n详情邮件咨询:\nadmin@leonardohuang.com"
        )

        self.metadata = MetaData()

        self.free_user_free_talk_per_month = int(self.MAX_CONVERSATION_PER_MONTH)
        self.refill_teaser = self.REFILL_TEASER if self.REFILL_TEASER else REFILL_TEASER_DEFAULT

    def update_free_user_free_talk_per_month(self, new_value):
        with self.free_user_free_talk_per_month_lock:
            self.free_user_free_talk_per_month = new_value

    def update_refill_teaser(self, new_value):
        with self.refill_teaser_lock:
            self.refill_teaser = new_value
