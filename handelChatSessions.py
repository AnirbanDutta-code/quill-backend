import aiofiles
import asyncio
import json
import os
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


async def load_conv(conv_name: str):
    try:
        conv_dir = f"chats/{conv_name}"
        conv_json = f"chats/{conv_name}/chat.json"

        if not os.path.isdir(conv_dir):

            return f"Directory not exists {conv_name}"

        if not os.path.isfile(conv_json):

            return f"File not exists{conv_name}"

        async with aiofiles.open(conv_json, "r", encoding="utf-8") as file:
            conv = await file.read()

        return conv

    except Exception as e:
        return e


## <---------- handle chat history ----------->
def _build_messages_with_history(query: str, old_chats: str = "") -> list:

    messages = [
        SystemMessage(
            content="if user previous chat is added reply with the relative context "
        ),
    ]

    # Load old chat history if provided
    if old_chats:
        try:
            chat_history = json.loads(old_chats)
            for chat in chat_history:
                if chat.get("role") == "user":
                    messages.append(HumanMessage(content=chat.get("content", "")))
                elif chat.get("role") == "ai":
                    messages.append(AIMessage(content=chat.get("content", "")))
        except (json.JSONDecodeError, AttributeError):
            # If parsing fails, just use current query
            pass

    # Add current query as latest user message
    messages.append(HumanMessage(content=query))

    return messages


if __name__ == "__main__":
    sata = asyncio.run(load_conv("hello"))
    print(sata)
