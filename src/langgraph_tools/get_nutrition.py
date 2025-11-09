import requests
from langchain.tools import tool
from src.common.utils import get_gcp_secret
import base64
import json

FATSECRET_TOKEN_URL = "https://oauth.fatsecret.com/connect/token"
FATSECRET_API_URL = "https://platform.fatsecret.com/rest/server.api"


class NutritionAPIError(Exception):
    pass


def get_fatsecret_creds() -> dict:
    creds_json = get_gcp_secret("fat-secret-api-id", version="latest")
    return json.loads(creds_json)


def get_fatsecret_token(client_id: str, client_secret: str) -> str:
    auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials", "scope": "basic"}
    response = requests.post(
        FATSECRET_TOKEN_URL, headers=headers, data=data, timeout=10
    )
    if response.status_code != 200:
        raise NutritionAPIError(
            f"FatSecret token error {response.status_code}: {response.text}"
        )
    return response.json()["access_token"]


@tool
def get_nutrition(query: str) -> dict:
    """
    Fetch nutrition info for a food item using FatSecret Platform API.
    Args:
        query (str): Food name or recipe description
    Returns:
        dict: Nutrition data from FatSecret API
    Raises:
        NutritionAPIError: If API call fails or returns error
    """
    creds = get_fatsecret_creds()
    token = get_fatsecret_token(creds["client_id"], creds["client_secret"])
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "method": "foods.search",
        "max_results": "3",
        "search_expression": query,
        "format": "json",
    }
    response = requests.get(
        FATSECRET_API_URL, headers=headers, params=params, timeout=10
    )
    if response.status_code != 200:
        raise NutritionAPIError(
            f"FatSecret API error {response.status_code}: {response.text}"
        )
    data = response.json()
    if not data or "foods" not in data:
        raise NutritionAPIError("No nutrition data returned.")
    return data["foods"]


# Example usage:
if __name__ == "__main__":
    import sys

    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "apple"
    result = get_nutrition.invoke({"query": query})
    print(result)
