from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pipeline import run_research
from handelChatSessions import load_conv
import os
from handleJson import append_to_chat

app = FastAPI()

## <------------ allow cors origin ------------>
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


## <------------ greetings ------------>
@app.get("/")
def hi():
    return "welcome to Quillai"


## <------------ model run function ------------>
@app.get("/llm_search")
async def run_search(
    query: str,
    search_type: str,
    incognito: bool,
    createNewSession: bool,
    convname="",
):

    ## <---------- Return error if parameters make no sense  ------------>

    if incognito and createNewSession:
        return "cannot create new conversation in incognito , please set to false"

    if createNewSession and convname == "":
        return "convname needed if create new session is true"

    ## <---------- run if chat is not incognito ------------>

    if not incognito:
        conv_context = await load_conv(conv_name=convname)
        if conv_context == f"Directory not exists {convname}":
            return f"no Directory named `{convname}` please create one"

        model_res = run_research(
            query=query,
            type=search_type,
            is_new=createNewSession,
            old_chats=conv_context,
        )

        ## <---------- create session if needed ------------>
        if createNewSession:
            name = model_res["convname"]
        else:
            name = convname

        newBody = {
            "human": query,
            "queryType": search_type,
            "ai": model_res["reponse"],
            "source": model_res["sources"],
        }

        append_to_chat(convname=name, new_entry=newBody)

        return [model_res, conv_context]

    ## <---------- do not save or retrive anything if incognito ------------>
    elif incognito:

        model_res = run_research(query=query, type=search_type, is_new=createNewSession)

    return model_res


## <------------ imgs urls ------------>
# @app.get("/llm_search/img_results")
# def img_results(url: list) -> list:
#     img_url_list = ScrapPhoto(url)
#     return img_url_list


## <------------ get list of chats in folder ------------>
@app.get("/list_chats")
def list_dir():

    if os.path.isdir("chats"):
        print("Directory exists")
    else:
        os.mkdir("chats")
    return os.listdir("chats")


## <------------ retrive saved chats ------------>
@app.get("/get_conv")
async def get_conv(conv_name: str):

    res = await load_conv(conv_name=conv_name)
    return res
    # eturn "chat dir not exits making new"
