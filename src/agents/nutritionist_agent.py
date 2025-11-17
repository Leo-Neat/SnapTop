# A nutrtion agent that takes in a set of people, their demographics and activity levels and any dietary restrictions.
# It also takes in a number of days and meals per day between breakfast, lunch, dinner, snack and dessert.
# It outputs a structured macronutrtient set and seving sizes for each meal over the number of days specified.
# For example 4 days 3 meals per day, might output a rule for dinner 1 that can be used 3 times and a rule for dinner 2 which can be used once.
from src.langgraph_tools.nutrition import (
    get_macronutrient_distribution,
    get_reccomended_daily_calorie_intake,
)
from langchain.agents import create_agent
from src.common.llms import get_gemini_flash
from src.mealprep.proto.meal_plan_p2p import MealPlan


# System prompt for the nutritionist agent
system_prompt = (
    "You are a certified nutritionist tasked with creating a single, shared meal plan for all provided individuals, "
    "based on their demographics, activity levels, and dietary restrictions. Minimize the number of unique recipes required by reusing meals across days and people whenever possible. "
    "You will use the nutrition tools provided to calculate daily caloric needs and macronutrient distributions. "
    "Your output must be a valid JSON object matching the MealPlan schema. Dates must be ISO8601 strings or RFC3339 timestamps. "
    "If you make a mistake, you will be asked to fix it."
)

llm = get_gemini_flash()


nutritionist_toolkit = [
    get_reccomended_daily_calorie_intake,
    get_macronutrient_distribution,
]
agent = create_agent(
    tools=nutritionist_toolkit, model=llm, debug=True, response_format=MealPlan
)


if __name__ == "__main__":
    user_query = (
        "Create a 4-day meal plan for 2 individuals:\n"
        " Person 1: 30-year-old female , 65kg, 165cm, moderate activity level, vegetarian.\n"
        " Person 2: 40-year-old male, 80kg, 180cm, light activity level, gluten-free.\n"
        " The meal plan should include breakfast, lunch, dinner, and snacks for each day."
    )
    result = agent.invoke(
        {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query},
            ]
        }
    )
    meal_plan = result["structured_response"]  # structured object, already validated
    print("✅ Structured MealPlan object:")
    print(meal_plan.model_dump_json(indent=2))
