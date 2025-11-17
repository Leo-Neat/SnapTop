import pytest
from backend.src.langgraph_tools.nutrition import get_nutrition


@pytest.mark.parametrize("query", ["apple", "chickpeas", "tofu", "quinoa"])
def test_get_nutrition(query):
    result = get_nutrition.invoke({"query": query})
    assert result, f"No nutrition data returned for {query}"
    print(f"Nutrition for {query}: {result}")
