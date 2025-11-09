import json
from langchain.tools import tool
from src.langgraph_tools.get_nutrition import get_nutrition
from src.langgraph_tools.google_search import search_tool, fetch_url_content
from langchain.agents import create_agent
from langchain_google_vertexai import ChatVertexAI
import google.generativeai as genai
from src.langgraph_tools.gcp_secrets import get_gcp_secret



genai.configure(api_key="AIzaSyCfx8Th15NccJF7F64GDeR_HBI_4nPOTm4")

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

llm = ChatVertexAI(model_name="gemini-2.5-flash", project="recipellm", system_message=system_prompt)

recipe_toolkit = [search_tool, fetch_url_content, get_nutrition]

agent = create_agent(tools=recipe_toolkit, model=llm, debug=True)

result = agent.invoke({
    "messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Create a high protein vegan recipe for a post-workout grain bowl."}
    ]
})

print(result)