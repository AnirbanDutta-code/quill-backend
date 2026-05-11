import aiofiles
import asyncio
import json
import os


async def load_conv(conv_name: str):
    try:
        conv_dir = f"chats/{conv_name}"
        conv_json = f"chats/{conv_name}/chat.json"

        if not os.path.isdir(conv_dir):

            return f"Directory not exists{conv_name}"

        if not os.path.isfile(conv_json):

            return f"File not exists{conv_name}"

        async with aiofiles.open(conv_json, "r", encoding="utf-8") as file:
            conv = await file.read()

        return conv

    except Exception as e:
        return e


if __name__ == "__main__":
    sata = asyncio.run(load_conv("hello"))
    print(sata)
