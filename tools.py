from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import main
from rich import print
import requests

# Load environment variables from .env file
main.load_dotenv()

# Initialize the Tavily client for web searches
tabily_client = TavilyClient(api_key=os.getenv("TABILY_API_KEY"))


def websearch(query: str) -> str:

    ## !do not remove this discription
    """Search the web for recent and reliable information on a topic . Returns Titles , URLs and snippets."""

    clear_urls = []

    # Perform a search using the Tavily client
    tabily_res = tabily_client.search(query, max_results=5)

    # Extract the URLs from the search results
    for list in tabily_res["results"]:
        clear_urls.append(list["url"])

    return clear_urls


def webScraping(query: str):
    ## !do not remove this discription

    """Scrape and return clean text content from a given URL for deeper reading"""

    try:
        # Send a GET request to the URL
        response = requests.get(
            str(query), timeout=8, headers={"User-Agent": "Mozila/5.0"}
        )

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove script, style, nav, and footer tags
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        # Return the cleaned text content, limited to 3000 characters
        return soup.get_text(separator=" ", strip=True)[:3000]

    except Exception as e:
        return f"Could not scrape URL: {str(e)}"


if __name__ == "__main__":
    # Example of how to use the webScraping function
    webScraping("https://www.bbc.com/news/articles/cz67nqvz3vno")
