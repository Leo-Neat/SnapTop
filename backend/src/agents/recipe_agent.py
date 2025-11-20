from backend.src.langgraph_tools.nutrition import get_nutrition
from backend.src.langgraph_tools.recipe_search import fetch_url_content, search_tool
from langchain.agents import create_agent
from backend.src.common.llms import get_gemini_flash
from backend.src.models.recipe import Recipe

# System prompt for the agent
system_prompt = (
    "You are a highly skilled chef specializing in adapting recipes to meet clients' dietary restrictions and preferences. "
    "When creating a recipe, use the recipe search tool for inspiration and to learn about cooking methods, but do not copy recipes directly. "
    "You can use the fetch URL tool to dive deeper into any of the recipes you found for inspiration, extracting details or clarifying cooking steps. "
    "Use the nutrition search tool to look up nutrition information for each individual ingredient, not for entire recipes. "
    "Sum the nutrition values for all ingredients to provide accurate macros for the final recipe. "
    "Your output must be a valid JSON object matching the Recipe schema. "
    "Always cite sources for inspiration in the citations field. "
    "If a user requests substitutions or has dietary restrictions, adapt the recipe accordingly and explain your choices in the instructions. "
    "Format your output so it can be parsed into the Recipe proto message. "
    "If you make a mistake, you will be asked to fix it."
)

# Choose Gemini model (flash, pro, ultra)
llm = get_gemini_flash(system_prompt=system_prompt)
# llm = get_gemini_pro(system_prompt=system_prompt)
# llm = get_gemini_ultra(system_prompt=system_prompt)

recipe_toolkit = [search_tool, fetch_url_content, get_nutrition]

agent = create_agent(
    tools=recipe_toolkit, model=llm, debug=True, response_format=Recipe
)


if __name__ == "__main__":
    result = agent.invoke(
        {
            "messages": [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": "I have a gluten alergy, and at my home I have granola, flour, quinoa, pizza sauce, greek yogurt, and some apples. What can I make for dinner? And I can go shopping if needed, but am on a budget.",
                },
            ]
        }
    )
    recipe = result["structured_response"]  # structured object, already validated
    print("✅ Structured Recipe object:")
    print(recipe.model_dump_json(indent=2))
