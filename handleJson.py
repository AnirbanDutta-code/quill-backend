import json
import os


async def saveChatfile(body, conv_name):
    chatFolder = f"chats/{conv_name}/"
    if not os.path.exists(chatFolder):
        os.mkdir(chatFolder)
        print(os.listdir("chats"))

    with open(f"{chatFolder}/chat.json", "w", encoding="utf-8") as file:
        json.dump(body, file)
    return {"received_data": body}


async def handleSaveSourceJson(body, conv_name):
    chatFolder = f"chats/{conv_name}/"
    if not os.path.exists(chatFolder):
        os.mkdir(chatFolder)
        print(os.listdir("chats"))

    with open(f"{chatFolder}/sources.json", "w", encoding="utf-8") as file:
        json.dump(body, file)
    return {"received_data": body}
