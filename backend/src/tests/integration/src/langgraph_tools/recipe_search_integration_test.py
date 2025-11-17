import pytest
from backend.src.langgraph_tools.recipe_search import search_tool, fetch_url_content


@pytest.mark.parametrize(
    "query", ["Moroccan chickpea stew", "vegan lasagna", "chocolate chip cookies"]
)
def test_recipe_search(query):
    results = search_tool.run(query)
    assert results and isinstance(results, list), f"No results for {query}"
    print(f"Top results for '{query}': {results}")
    # Optionally fetch content from the first result
    if results and "link" in results[0]:
        content = fetch_url_content.invoke({"url": results[0]["link"]})
        assert content, "No content fetched from top result URL"
        print(f"Content from top result: {content[:200]}...")
