## <---------- imports ---------->
import os
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from dotenv import main
import httpx
from rich import print
from tavily import TavilyClient

## <---------- Load .env file ---------->
main.load_dotenv()


## <---------- Initialize the Tavily ---------->
tabily_client = TavilyClient(api_key=os.getenv("TABILY_API_KEY"))


## <---------- search web and get urls ---------->
def websearch(query: str):

    ## !do not remove this discription
    """Search the web for recent and reliable information on a topic . Returns Titles , URLs and snippets."""

    clear_urls = []

    # Perform a search
    tabily_res = tabily_client.search(query, max_results=5)

    # Extract the URLS
    for list in tabily_res["results"]:
        clear_urls.append(list["url"])

    return clear_urls


## <---------- scrap contents from url ---------->
def webScraping(url: str):

    ## !do not remove this discription
    """Scrape and return clean text content from a given URL for deeper reading"""
    state = {}

    try:

        response = requests.get(
            str(url), timeout=8, headers={"User-Agent": "Mozila/5.0"}
        )
        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        result = soup.get_text(separator=" ", strip=True)[:3000]
        return result

    except Exception as e:
        print(f"error : {e}")
        return f"Could not scrape URL: {str(e)}"


## <---------- scrap photos form url ---------->
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
        return f"Error: {e}"

    return sources


if __name__ == "__main__":
    import asyncio

    webScraping("https://comatozze.net/")
