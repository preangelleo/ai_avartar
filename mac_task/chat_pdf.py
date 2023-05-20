# from my_config import *
from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from langchain import OpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent
from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.docstore import InMemoryDocstore
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.retrievers import TimeWeightedVectorStoreRetriever
from langchain.schema import BaseLanguageModel, Document
from langchain.vectorstores import FAISS
from abc import ABC, abstractmethod
from typing import List
from langchain.schema import Document
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
# from langchain.document_loaders import UnstructuredFileLoader, UnstructuredHTMLLoader, TextLoader, UnstructuredPDFLoader, UnstructuredEmailLoader, UnstructuredPowerPointLoader, UnstructuredWordDocumentLoader, UnstructuredURLLoader
from langchain.document_loaders import PyPDFLoader

from langchain.indexes import VectorstoreIndexCreator
import nltk

import os
from dotenv import load_dotenv
load_dotenv()

if 'LOAD VARIABLES':
    BING_SEARCH_API_KEY = os.getenv("BING_SEARCH_API")
    SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

    GMAIL_PREANGELLEO = 'preangelleo@gmail.com'
    GMAIL_CHATGPT_ADDRESS = 'emailchatgptbot@gmail.com'
    GMAIL_CHATGPT_PASSWD = os.getenv("GMAIL_CHATGPT")

    TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
    TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/"

    ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
    YOUTUBE_API = os.getenv('YOUTUBE_API')

    BOTOWNER_CHAT_ID = os.getenv("BOTOWNER_CHAT_ID")

    DISCORD_BOT_TOKEN = os.getenv("DISCORD_TOKEN")
    # Load your API key from an environment variable or secret management service

    debug = True

    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    os.environ['SERPAPI_API_KEY'] = SERPAPI_API_KEY


class BaseRetriever(ABC):
    @abstractmethod
    def get_relevant_documents(self, query: str) -> List[Document]:
        """Get texts relevant for a query.

        Args:
            query: string to find relevant texts for

        Returns:
            List of relevant documents
        """

loader = PyPDFLoader("/Users/lgg/Downloads/7_share_file.pdf")
# pages = loader.load_and_split()

# print(pages[6])
index = VectorstoreIndexCreator().from_loaders([loader])



if __name__ == "__main__":
    print("LangChain Started...")
    while True:
        query = input("Enter your query: ")
        if not query: break

        r = index.query(query)
        print(r)