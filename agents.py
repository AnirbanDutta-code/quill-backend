from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from tools import webScraping
from dotenv import main

main.load_dotenv()


llm = ChatMistralAI(model_name="mistral-small-latest", temperature=0)

def llm_model(query: str, temp: int = 0) -> str:
    model = ChatMistralAI(model_name="mistral-small-latest", temperature=temp)
    res = model.invoke(query)
    return res


def build_srcaping_agent():

    return create_agent(model=llm, tools=[webScraping])
