import aiofiles
import asyncio

# from langchain_mistralai import MistralAIEmbeddings
# from langchain_community.vectorstores import Chroma


# def handel_old_conv(cov_name:str):

# chat_db_path=f"chats/{cov_name}"

# vectordb = Chroma(
#     persist_directory=chat_db_path,
#     embedding_function=MistralAIEmbeddings()
# )

#  masaage=item['messages']
#  with open("chat/example.txt", "w", encoding="utf-8") as file:
#         file.write(str(masaage))


async def load_conv(conv_name: str = "example"):
    conv_dir = f"chats/{conv_name}/chat.json"
    async with aiofiles.open(conv_dir, "r", encoding="utf-8") as file:
        conv = await file.read()
    # Parse conversation data into a list
    import json

    try:
        conv_list = json.loads(conv)
        if isinstance(conv_list, list):
            # Remove quotes from list items if they're strings
            return [
                item.strip('"') if isinstance(item, str) else item for item in conv_list
            ]
        else:
            return [conv_list]
    except json.JSONDecodeError:
        # If not JSON, split by lines or return as single item list
        return conv.strip().split("\n") if conv.strip() else []


if __name__ == "__main__":
    asyncio.run(load_conv())
