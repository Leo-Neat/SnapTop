import requests
from langchain.tools import tool
from backend.src.common.utils import get_gcp_secret
import base64
import json
import time
import logging

logger = logging.getLogger(__name__)

FATSECRET_TOKEN_URL = "https://oauth.fatsecret.com/connect/token"
FATSECRET_API_URL = "https://platform.fatsecret.com/rest/server.api"

class NutritionAPIError(Exception):
    pass

# simple in-memory caches to avoid repeated Secret Manager calls and token requests
_FATSECRET_CREDS_CACHE: dict | None = None
_FATSECRET_TOKEN = None
_FATSECRET_TOKEN_EXP = 0


def get_fatsecret_creds() -> dict:
    global _FATSECRET_CREDS_CACHE
    if _FATSECRET_CREDS_CACHE:
        return _FATSECRET_CREDS_CACHE
    _FATSECRET_CREDS_CACHE = json.loads(get_gcp_secret("fat-secret-api-id", version="latest"))
    return _FATSECRET_CREDS_CACHE


def get_fatsecret_token(client_id: str, client_secret: str) -> str:
    global _FATSECRET_TOKEN, _FATSECRET_TOKEN_EXP
    now = time.time()
    if _FATSECRET_TOKEN and _FATSECRET_TOKEN_EXP > now + 10:
        return _FATSECRET_TOKEN

    auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    resp = requests.post(
        FATSECRET_TOKEN_URL,
        headers={"Authorization": f"Basic {auth}", "Content-Type": "application/x-www-form-urlencoded"},
        data={"grant_type": "client_credentials", "scope": "basic"},
        timeout=10,
    )
    if resp.status_code != 200:
        raise NutritionAPIError(f"FatSecret token error {resp.status_code}: {resp.text}")

    j = resp.json()
    _FATSECRET_TOKEN = j.get("access_token")
    _FATSECRET_TOKEN_EXP = now + int(j.get("expires_in", 300))
    return _FATSECRET_TOKEN


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
    params = {"method": "foods.search", "max_results": "3", "search_expression": query, "format": "json"}

    resp = requests.get(FATSECRET_API_URL, headers=headers, params=params, timeout=10)
    if resp.status_code != 200:
        # one quick retry
        resp = requests.get(FATSECRET_API_URL, headers=headers, params=params, timeout=10)
        if resp.status_code != 200:
            return []

    try:
        data = resp.json()
    except Exception:
        return []

    # tolerate common shapes and return a list
    if isinstance(data, dict):
        for key in ("foods", "food", "foods_result"):
            if key in data:
                val = data[key]
                return val if isinstance(val, list) else [val]
        for v in data.values():
            if isinstance(v, list):
                return v
        return []
    if isinstance(data, list):
        return data
    return []

@tool
def get_reccomended_daily_calorie_intake(
    age: int = 30,
    is_male: bool = True,
    activity_level: str = "sedentary",
    height_cm: float = 175.0,
    weight_kg: float = 70.0
) -> int:
    """
    Get recommended daily calorie intake
    Args:
        age (int, optional): Age of the individual (default: 30)
        is_male (bool, optional): Gender of the individual (default: True)
        activity_level (str, optional): Activity level (default: 'sedentary')
        height_cm (float, optional): Height in centimeters (default: 175.0)
        weight_kg (float, optional): Weight in kilograms (default: 70.0)
    Returns:
        int: Recommended daily calorie intake
    """
    # Simple estimation based on Mifflin-St Jeor Equation and activity factor
    # Calculate BMR using Mifflin-St Jeor Equation
    if is_male:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

    # Activity factor mapping
    activity_factors = {
        "sedentary": 1.2,        # little or no exercise
        "light": 1.375,          # light exercise/sports 1-3 days/week
        "moderate": 1.55,        # moderate exercise/sports 3-5 days/week
        "active": 1.725,         # hard exercise/sports 6-7 days a week
        "very active": 1.9       # very hard exercise/sports & physical job
    }

    factor = activity_factors.get(activity_level.lower(), 1.2)  # default to sedentary if invalid
    daily_calories = int(bmr * factor)

    return daily_calories


@tool
def get_macronutrient_distribution(
    goal: str = "maintain",
) -> dict:
    """
    Get recommended macronutrient distribution based on fitness goal or diet preference.
    
    Args:
        goal (str, optional): Fitness goal or diet type. Options include:
            'lose', 'maintain', 'gain', 
            'keto', 'low-carb', 'high-protein', 
            'balanced', 'endurance', 'strength'
            (default: 'maintain')
    
    Returns:
        dict: Recommended macronutrient distribution percentages
    """
    distributions = {
        "lose": {"protein": 40, "carbs": 30, "fats": 30},
        "maintain": {"protein": 30, "carbs": 40, "fats": 30},
        "gain": {"protein": 25, "carbs": 50, "fats": 25},
        "keto": {"protein": 20, "carbs": 5, "fats": 75},
        "low-carb": {"protein": 30, "carbs": 20, "fats": 50},
        "high-protein": {"protein": 40, "carbs": 35, "fats": 25},
        "balanced": {"protein": 30, "carbs": 40, "fats": 30},
        "endurance": {"protein": 20, "carbs": 55, "fats": 25},
        "strength": {"protein": 35, "carbs": 40, "fats": 25},
    }
    
    return distributions.get(goal.lower(), distributions["maintain"])

@tool
def search_openfoodfacts(
    query: str,
    max_results: int = 5,
    page: int = 1,
    language: str = "en",
) -> list:
    """
    Search OpenFoodFacts for products matching `query` and return nutrition data and metadata.

    Args:
        query (str): Search terms (product name, brand, UPC, etc.)
        max_results (int): Number of results per page to return (default: 5)
        page (int): Page number to request (default: 1)
        language (str): Preferred language code (used when available)

    Returns:
        list: List of product dicts containing keys like `name`, `brand`, `upc`,
              `categories`, `nutriments`, `image`, `ingredients_text`, `url`, and more.

    Raises:
        NutritionAPIError: If the OpenFoodFacts request fails or returns invalid JSON.
    """
    url = "https://world.openfoodfacts.org/cgi/search.pl"
    headers = {"User-Agent": "SnapTop/1.0 (contact: dev@snaptop.example)"}
    params = {
        "search_terms": query,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": max_results,
        "page": page,
        # language/locale fields may be honored by the API when available
        "lc": language,
    }

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=10)
    except Exception as e:
        raise NutritionAPIError(f"OpenFoodFacts request error: {e}")

    if resp.status_code != 200:
        raise NutritionAPIError(
            f"OpenFoodFacts API error {resp.status_code}: {resp.text}"
        )

    try:
        data = resp.json()
    except Exception as e:
        raise NutritionAPIError(f"Error parsing OpenFoodFacts JSON: {e}")

    products = data.get("products", [])
    results = []
    for p in products:
        code = p.get("code")
        results.append({
            "name": p.get("product_name") or p.get(f"product_name_{language}") or p.get("generic_name"),
            "brand": p.get("brands"),
            "upc": code,
            "categories": p.get("categories_tags") or p.get("categories"),
            "categories_hierarchy": p.get("categories_hierarchy"),
            "nutriments": p.get("nutriments"),
            "nutrient_levels": p.get("nutrient_levels"),
            "image": p.get("image_small_url") or p.get("image_url"),
            "ingredients_text": p.get("ingredients_text"),
            "ingredients": p.get("ingredients"),
            "labels": p.get("labels"),
            "stores": p.get("stores"),
            "countries": p.get("countries_tags") or p.get("countries"),
            "serving_size": p.get("serving_size"),
            "packaging": p.get("packaging"),
            "nova_group": p.get("nova_group"),
            "ecoscore_grade": p.get("ecoscore_grade"),
            "url": p.get("url") or (f"https://world.openfoodfacts.org/product/{code}" if code else None),
        })

    return results


# Example usage:
if __name__ == "__main__":
    import sys
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "apple"
    fat_secret_api_result = get_nutrition.invoke({"query": query})
    openfoodfacts_result = search_openfoodfacts.invoke({"query": query, "max_results": 3})
    print(f"Fat secret API {fat_secret_api_result}")
    print(f"OpenFoodFacts API {openfoodfacts_result}")