
from src.langgraph_tools.gcp_secrets import get_gcp_secret

from langchain_core.tools import Tool
from langchain_google_community import GoogleSearchAPIWrapper
from langchain_community.document_loaders import WebBaseLoader

import requests
from langchain.tools import tool

@tool
def fetch_url_content(url: str) -> str:
    """Fetch text content from a URL"""
    loader = WebBaseLoader(url)
    documents = loader.load()
    if documents:
        return documents[0].page_content
    else:
        return ""




api_key = get_gcp_secret("google-cloud-api-key", version="1")
cse_id = get_gcp_secret("recipe-search-id", version="1")
search = GoogleSearchAPIWrapper(google_api_key=api_key, google_cse_id=cse_id, k=10)


def top3_results(query: str) -> str:
    return search.results(query, 3)


search_tool = Tool(
    name="recipe_search",
    description="Useful for searching recipes on the web given a query. ",
    func=top3_results,
)



if __name__ == "__main__":
    query = "Moroccan"
    results = search_tool.run(query)
    print(results)
    site_contents = fetch_url_content.invoke({"url": results[0]['link']}).replace("\n", " ")

    print(site_contents)