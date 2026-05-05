from agents import build_srcaping_agent
from tools import websearch
import json
from agents import llm_model
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

state = {}


def run_research(query: str, type: str, is_new):
    if is_new == False:
        # conversation name
        conv_name = llm_model(
            query=f"just reply with  a conversation name in 2  words based on the frist  message that is  {query} ",
            temp=1,
        )
        state["convname"] = conv_name.content
        print(
            f"just reply with  a conversation name in 2  words based on the frist  message that is  {query}"
        )
        print(conv_name.content)
        print(type)

    # user query
    if type == "deep_research":

        research_result = websearch(query=query)

        state["urls"] = research_result
        # Build and run the scraping agent to get content from URLs
        scraping_model = build_srcaping_agent()
        scraping_result = scraping_model.invoke(
            {
                "messages": [
                    (
                        "user",
                        f"search on the {query}, go to the urls {state['urls']} ,find the the most hot topics ",
                    )
                ]
            }
        )

        sources = {
            1: {
                "urls": scraping_result["messages"][1].tool_calls[0]["args"]["query"],
                "content": scraping_result["messages"][2].content,
            },
            2: {
                "urls": scraping_result["messages"][1].tool_calls[1]["args"]["query"],
                "content": scraping_result["messages"][3].content,
            },
            3: {
                "urls": scraping_result["messages"][1].tool_calls[2]["args"]["query"],
                "content": scraping_result["messages"][4].content,
            },
            4: {
                "urls": scraping_result["messages"][1].tool_calls[3]["args"]["query"],
                "content": scraping_result["messages"][5].content,
            },
            5: {
                "urls": scraping_result["messages"][1].tool_calls[4]["args"]["query"],
                "content": scraping_result["messages"][6].content,
            },
        }

        state["sources"] = sources
        state["reponse"] = scraping_result["messages"][7].content

    elif type == "deep_thinking":
        sources = {1: {"only available on deep reseacrh": "blah", "content": "type is deep thinking  , no sources"}}

        state["sources"] = sources

        smart_reponse = llm_model(query=query, temp=1)
        state["reponse"] = smart_reponse.content

    elif type == "ask":
        sources = {1: {"urls": "only available on deep reseacrh", "content": "type is ask , no sources"}}

        state["sources"] = sources

        reponse = llm_model(query=query, temp=1)
        state["reponse"] = reponse.content

    return state


if __name__ == "__main__":
    topic = input("\n Enter a research topic : ")
    run_research(topic)
