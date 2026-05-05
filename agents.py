from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from tools import webScraping
from dotenv import main
import os

main.load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
# Initialize the language model
llm = ChatMistralAI(model_name="mistral-small-latest", api_key=MISTRAL_API_KEY, temperature=0)


def llm_model(query: str, temp: int = 0) -> str:
    model = ChatMistralAI(model_name="mistral-small-latest", api_key=MISTRAL_API_KEY, temperature=temp)
    res = model.invoke(query)
    return res


def build_srcaping_agent():

    return create_agent(model=llm, tools=[webScraping])
