from agents import build_srcaping_agent
from tools import websearch
from agents import llm_model
from handelChatSessions import _build_messages_with_history

## <---------- state dictioney for saving all response in one ----------->
state = {}





def run_research(query: str, type: str, is_new: bool, old_chats: str = ""):

    ai_message= _build_messages_with_history(query=query, old_chats=old_chats)

    ## <------------ Genarate new converstion from model  -------------->
    if is_new:
        # For conversation title
        conv_nameByModel = llm_model(
            query=f"Generate a concise title for this conversation.Rules:- 2–6 words,-Title Case,- Main topic only ,- No quotes or extra text Conversation:{query}"
        )
        state["convname"] = conv_nameByModel.content

    ## <------------------------------------ handle deep search query ------------------------------------>
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

        ## <------------ save to state ------------>
        sources = {
            1: {
                "urls": scraping_result["messages"][1].tool_calls[0]["args"]["url"],
                "content": scraping_result["messages"][2].content,
            },
            2: {
                "urls": scraping_result["messages"][1].tool_calls[1]["args"]["url"],
                "content": scraping_result["messages"][3].content,
            },
            3: {
                "urls": scraping_result["messages"][1].tool_calls[2]["args"]["url"],
                "content": scraping_result["messages"][4].content,
            },
            4: {
                "urls": scraping_result["messages"][1].tool_calls[3]["args"]["url"],
                "content": scraping_result["messages"][5].content,
            },
            5: {
                "urls": scraping_result["messages"][1].tool_calls[4]["args"]["url"],
                "content": scraping_result["messages"][6].content,
            },
        }

        state["sources"] = sources
        state["reponse"] = scraping_result["messages"][7].content

    ## <------------------------------------ handels deep thinking query ------------------------------------>
    elif type == "deep_thinking":
        sources = {
            1: {
                "urls": "only available on deep reseacrh",
                "content": "type is deep thinking  , no sources",
            }
        }
        # Build messages with chat history
        smart_reponse = llm_model(query=ai_message, temp=1)

        ## <------------ save to state ------------>
        state["sources"] = sources
        state["reponse"] = smart_reponse.content

    ## <------------------------------------- handels normal ask query ------------------------------------>
    elif type == "ask":

        sources = {
            1: {
                "urls": "only available on deep reseacrh",
                "content": "type is ask , no sources",
            }
        }
        # Build messages with chat history
        reponse = llm_model(query=ai_message, temp=0)

        ## <------------ save to state ------------>
        state["sources"] = sources
        state["reponse"] = reponse.content
    return state
