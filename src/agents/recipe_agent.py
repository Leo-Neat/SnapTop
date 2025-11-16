from src.langgraph_tools.nutrition import get_nutrition
from src.langgraph_tools.recipe_search import fetch_url_content, search_tool
from langchain.agents import create_agent
from src.common.llms import get_gemini_flash

# System prompt for the agent
system_prompt = (
    "You are a highly skilled chef specializing in adapting recipes to meet clients' dietary restrictions and preferences. "
    "When creating a recipe, use the recipe search tool for inspiration and to learn about cooking methods, but do not copy recipes directly. "
    "You can use the fetch URL tool to dive deeper into any of the recipes you found for inspiration, extracting details or clarifying cooking steps. "
    "Use the nutrition search tool to look up nutrition information for each individual ingredient, not for entire recipes. "
    "Sum the nutrition values for all ingredients to provide accurate macros for the final recipe. "
    "Your output must include: a set of ingredients (with quantities and units), clear step-by-step instructions, and a nutritional breakdown (macros: protein, carbs, fat, calories) for the whole recipe. "
    "Always cite sources for inspiration in the citations field. "
    "If a user requests substitutions or has dietary restrictions, adapt the recipe accordingly and explain your choices in the instructions. "
    "Format your output so it can be parsed into the Recipe proto message."
)

# Choose Gemini model (flash, pro, ultra)
llm = get_gemini_flash(system_prompt=system_prompt)
# llm = get_gemini_pro(system_prompt=system_prompt)
# llm = get_gemini_ultra(system_prompt=system_prompt)

recipe_toolkit = [search_tool, fetch_url_content, get_nutrition]

agent = create_agent(tools=recipe_toolkit, model=llm, debug=True)

result = agent.invoke(
    {
        "messages": [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": "Create a high protein vegan recipe for a post-workout grain bowl.",
            },
        ]
    }
)

print(result)
