import requests
from langchain.tools import tool
from backend.src.common.utils import get_gcp_secret
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



# Example usage:
if __name__ == "__main__":
    import sys
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "apple"
    result = get_nutrition.invoke({"query": query})
    print(result)
