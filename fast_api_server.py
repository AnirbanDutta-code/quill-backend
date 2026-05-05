from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pipeline import run_research
from handelChatSessions import load_conv
import os
from handleJson import saveChatfile

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def hi():
    return "hi"


## model run function
@app.get("/llm_model_search")
def run_search(query: str, search_type: str, is_new: bool = False):
    response = run_research(query=query, type=search_type, is_new=is_new)
    return response


@app.get("/list_chats")
def list_dir():
    import os

    if os.path.isdir("chats"):
        print("Directory exists")
    else:
        os.mkdir("chats")
    return os.listdir("chats")


@app.post("/convJsonFile")
async def create_convJsonfile(item: Request, conv_name):
    body = await item.json()
    reponse = await saveChatfile(body=body, conv_name=conv_name)
    # handleSaveSourceJson()
    return reponse


@app.get("/get_conv")
async def get_conv(conv_name: str):

    chatFolder = f"chats/{conv_name}/"

    if os.path.isdir(chatFolder):

        res = await load_conv(conv_name=conv_name)
        return res
    else:
        return "chat dir not exits making new"
