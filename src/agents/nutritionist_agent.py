# A nutrtion agent that takes in a set of people, their demographics and activity levels and any dietary restrictions.
# It also takes in a number of days and meals per day between breakfast, lunch, dinner, snack and dessert.
# It outputs a structured macronutrtient set and seving sizes for each meal over the number of days specified.
# For example 4 days 3 meals per day, might output a rule for dinner 1 that can be used 3 times and a rule for dinner 2 which can be used once.
from src.langgraph_tools.nutrition import get_macronutrient_distribution, get_reccomended_daily_calorie_intake
from langchain.agents import create_agent
from src.common.llms import get_gemini_flash
import json



# System prompt for the nutritionist agent
system_prompt = (
    "You are a certified nutritionist tasked with creating a single, shared meal plan for all provided individuals, "
    "based on their demographics, activity levels, and dietary restrictions. Minimize the number of unique recipes required by reusing meals across days and people whenever possible. "
    "You will use the nutrition tools provided to calculate daily caloric needs and macronutrient distributions. "
    "Your output must include a structured meal plan with serving sizes for each meal over the specified number of days. "
    "Ensure that the meal plans are balanced, nutritious, and tailored to the specific needs of each individual. "
    "DO NOT PROVIDE FOODS OR RECIPES, just the meal plan structure and macronutrient breakdowns. "
    "\n\n"
    "Your output MUST be a valid JSON object matching the following structure, which can be parsed into the MealPlan proto:\n"
    "{\n"
    "  \"meal_plan_id\": \"string\",\n"
    "  \"user_id\": \"string\",\n"
    "  \"meals\": [\n"
    "    {\n"
    "      \"meal_id\": \"string\",\n"
    "      \"title\": \"string\",\n"
    "      \"recipe_id\": \"string (optional)\",\n"
    "      \"target_calories_per_serving\": int,\n"
    "      \"servings\": int,\n"
    "      \"macro_percentages\": {\n"
    "        \"protein_percent\": float,\n"
    "        \"carb_percent\": float,\n"
    "        \"fat_percent\": float\n"
    "      },\n"
    "      \"dates\": [\n"
    "        \"YYYY-MM-DDTHH:MM:SSZ\"\n"
    "      ],\n"
    "      \"meal_type\": \"BREAKFAST|LUNCH|DINNER|DESSERT|SNACK\"\n"
    "    }\n"
    "  ]\n"
    "}\n"
    "\nExample Output:\n"
    "{\n"
    "  \"meal_plan_id\": \"plan123\",\n"
    "  \"user_id\": \"user456\",\n"
    "  \"meals\": [\n"
    "    {\n"
    "      \"meal_id\": \"meal1\",\n"
    "      \"title\": \"Breakfast Day 1\",\n"
    "      \"target_calories_per_serving\": 350,\n"
    "      \"servings\": 2,\n"
    "      \"macro_percentages\": {\n"
    "        \"protein_percent\": 20.0,\n"
    "        \"carb_percent\": 60.0,\n"
    "        \"fat_percent\": 20.0\n"
    "      },\n"
    "      \"dates\": [\n"
    "        \"2025-11-10T08:00:00Z\",\n"
    "        \"2025-11-11T08:00:00Z\"\n"
    "      ],\n"
    "      \"meal_type\": \"BREAKFAST\"\n"
    "    },\n"
    "    {\n"
    "      \"meal_id\": \"meal2\",\n"
    "      \"title\": \"Lunch Day 1\",\n"
    "      \"target_calories_per_serving\": 500,\n"
    "      \"servings\": 2,\n"
    "      \"macro_percentages\": {\n"
    "        \"protein_percent\": 25.0,\n"
    "        \"carb_percent\": 55.0,\n"
    "        \"fat_percent\": 20.0\n"
    "      },\n"
    "      \"dates\": [\n"
    "        \"2025-11-10T12:00:00Z\"\n"
    "      ],\n"
    "      \"meal_type\": \"LUNCH\"\n"
    "    }\n"
    "  ]\n"
    "}\n"
)

llm = get_gemini_flash()


nutritionist_toolkit = [get_reccomended_daily_calorie_intake, get_macronutrient_distribution]
agent = create_agent(tools=nutritionist_toolkit, model=llm, debug=True)




import json
if __name__ == "__main__":
    result = agent.invoke(
        {
            "messages": [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": (
                        "Create a 4-day meal plan for 2 individuals:\n"
                        " Person 1: 30-year-old female , 65kg, 165cm, moderate activity level, vegetarian.\n"
                        " Person 2: 40-year-old male, 80kg, 180cm, light activity level, gluten-free.\n"
                        " The meal plan should include breakfast, lunch, dinner, and snacks for each day."
                    ),
                },
            ]
        }
    )
    print("Raw agent output:")
    print(result['messages'][-1].content)
    imputed_output = result['messages'][-1].content
    try:
        meal_plan = json.loads(imputed_output)
        print("Parsed Meal Plan JSON:")
        print(json.dumps(meal_plan, indent=2))
    except json.JSONDecodeError as e:
        print("Failed to parse JSON from agent output:", e)