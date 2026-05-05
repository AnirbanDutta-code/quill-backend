import asyncio
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import httpx


async def ScrapPhoto(urls: list) -> list:
    sources = []

    try:
        async with httpx.AsyncClient() as client:
            for url in urls:
                try:
                    response = await client.get(url, timeout=10)
                    htmldata = response.text
                    soup = BeautifulSoup(htmldata, "html.parser")

                    for item in soup.find_all("img"):
                        if item.get("src") and item["src"].endswith(
                            (".png", ".jpg", ".jpeg", ".webp")
                        ):
                            img = item["src"]
                            if item["src"].startswith("/"):
                                img = urljoin(url, item["src"])
                            sources.append(img)

                except Exception as e:
                    print(f"Error fetching {url}: {e}")

    except Exception as e:
        print(f"Error: {e}")

    return sources


import json


def append_to_chat(filename, new_entry):

    with open(filename, "r") as f:
        data = json.load(f)

    chat_obj = data["chat"][0]

    next_num = str(max(int(k) for k in chat_obj.keys()) + 1)
    chat_obj[next_num] = new_entry

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    # append_to_chat(
    #     "chats/chat.json",
    #     {
    #         "human": "new question",
    #         "queryType": "ask",
    #         "ai": "new answer",
    #         "source": "[https://new.com]",
    #     },
    # )
    
    import uuid
    id=uuid.uuid3(namespace=uuid.uuid1(),name="anirban")
    
    print(id.fields)


# 
    # asyncio.run(
        # ScrapPhoto(["https://www.imdb.com/title/tt11378946/", "https://comatozze.net/"])
    # )
