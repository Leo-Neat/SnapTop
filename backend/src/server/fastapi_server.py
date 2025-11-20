"""FastAPI server for SnapTop meal prep service."""

import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from backend.src.models import (
    GenerateRecipeRequest,
    GenerateWeeklyMealsRequest,
    ModifyRecipeRequest,
    RegenerateRecipeRequest,
    GetShoppingListRequest,
    Recipe,
    MealPlan,
    ShoppingList,
)
from backend.src.agents.recipe_agent import agent, system_prompt
from backend.src.langgraph_tools.generate_recipe_image import generate_recipe_image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="SnapTop Meal Prep API",
    description="AI-powered meal planning and recipe generation service",
    version="1.0.0",
)

# Configure CORS to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "healthy", "service": "SnapTop Meal Prep API"}


@app.post("/api/recipes/generate", response_model=Recipe)
async def generate_recipe(request: GenerateRecipeRequest) -> Recipe:
    """
    Generate a new recipe based on user description and preferences.

    Args:
        request: Recipe generation request with description, complexity, macros, etc.

    Returns:
        Recipe: Generated recipe with ingredients, instructions, nutrition, and image
    """
    logger.info(f"GenerateRecipe called with description: {request.description}")

    # Build a single prompt string from all request fields
    prompt_lines = []
    prompt_lines.append(f"Recipe request: {request.description}")

    if request.complexity:
        prompt_lines.append(f"Desired complexity: {request.complexity}")

    if request.target_macros:
        macros = request.target_macros
        macro_parts = []
        if macros.calories:
            macro_parts.append(f"calories={macros.calories}")
        if macros.protein_grams:
            macro_parts.append(f"protein={macros.protein_grams}g")
        if macros.carbs_grams:
            macro_parts.append(f"carbs={macros.carbs_grams}g")
        if macros.fat_grams:
            macro_parts.append(f"fat={macros.fat_grams}g")
        if macros.fiber_grams:
            macro_parts.append(f"fiber={macros.fiber_grams}g")
        if macros.sugar_grams:
            macro_parts.append(f"sugar={macros.sugar_grams}g")
        if macros.sodium_mg:
            macro_parts.append(f"sodium={macros.sodium_mg}mg")
        if macro_parts:
            prompt_lines.append("Target macros per serving: " + ", ".join(macro_parts))
            prompt_lines.append("(Remember: nutrition facts in your response should be for the ENTIRE recipe, not per serving)")

    if request.available_ingredients:
        ing_list = []
        for ing in request.available_ingredients:
            ing_desc = (
                f"{ing.quantity} {ing.unit} {ing.name}"
                if ing.unit
                else f"{ing.quantity} {ing.name}"
            )
            if ing.notes:
                ing_desc += f" ({ing.notes})"
            ing_list.append(ing_desc)
        prompt_lines.append("Available ingredients: " + ", ".join(ing_list))

    prompt = "\n".join(prompt_lines)
    logger.info(f"Generated prompt: {prompt}")

    try:
        # Invoke the recipe agent
        agent_input = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ]
        }
        logger.info("Invoking agent...")
        result = agent.invoke(agent_input)
        logger.info(f"Agent result: {result}")

        recipe_obj = result["structured_response"]
        logger.info(f"Recipe object: {recipe_obj}")

        # Convert to our Pydantic model if needed
        if not isinstance(recipe_obj, Recipe):
            recipe_data = recipe_obj.model_dump() if hasattr(recipe_obj, "model_dump") else recipe_obj
            recipe_obj = Recipe(**recipe_data)

        # Generate recipe image using title and description
        try:
            logger.info(f"Generating image for recipe: {recipe_obj.title}")
            image_description = f"{recipe_obj.title}. {recipe_obj.description}"
            image_base64 = generate_recipe_image.invoke(
                {"recipe_description": image_description}
            )
            recipe_obj.image_base64 = image_base64
            logger.info(f"Image generated successfully (length: {len(image_base64)})")
        except Exception as img_error:
            logger.warning(f"Failed to generate image: {img_error}", exc_info=True)
            # Continue without image if generation fails

        logger.info(f"Returning recipe: {recipe_obj.title}")
        return recipe_obj

    except Exception as e:
        logger.error(f"Error in generate_recipe: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Error generating recipe: {str(e)}"
        )


@app.post("/api/meals/generate-weekly", response_model=MealPlan)
async def generate_weekly_meals(request: GenerateWeeklyMealsRequest) -> MealPlan:
    """
    Generate a weekly meal plan based on user profile and preferences.

    Args:
        request: Weekly meal generation request with user profile

    Returns:
        MealPlan: Generated weekly meal plan

    Note:
        This endpoint is currently a stub and needs to be wired to the
        nutritionist agent and planner.
    """
    # TODO: Wire to nutritionist agent and planner
    logger.info(f"GenerateWeeklyMeals called for user: {request.user_profile.user_id}")

    meal_plan = MealPlan(
        meal_plan_id="dummy_id",
        user_id=request.user_profile.user_id,
        recipes=[],
    )
    return meal_plan


@app.post("/api/recipes/regenerate", response_model=Recipe)
async def regenerate_recipe(request: RegenerateRecipeRequest) -> Recipe:
    """
    Regenerate an existing recipe with new parameters.

    Args:
        request: Recipe regeneration request with recipe ID and reason

    Returns:
        Recipe: Regenerated recipe

    Note:
        This endpoint is currently a stub and needs to be wired to the chef agent.
    """
    # TODO: Wire to chef agent
    logger.info(f"RegenerateRecipe called for recipe: {request.recipe_id}")

    raise HTTPException(
        status_code=501, detail="Recipe regeneration not yet implemented"
    )


@app.post("/api/recipes/modify", response_model=Recipe)
async def modify_recipe(request: ModifyRecipeRequest) -> Recipe:
    """
    Modify an existing recipe based on instructions.

    Args:
        request: Recipe modification request with recipe ID and instructions

    Returns:
        Recipe: Modified recipe

    Note:
        This endpoint is currently a stub and needs to be wired to the chef agent.
    """
    # TODO: Wire to chef agent with modification instructions
    logger.info(
        f"ModifyRecipe called for recipe: {request.recipe_id} "
        f"with instructions: {request.modification_instructions}"
    )

    raise HTTPException(
        status_code=501, detail="Recipe modification not yet implemented"
    )


@app.post("/api/shopping-list/generate", response_model=ShoppingList)
async def get_shopping_list(request: GetShoppingListRequest) -> ShoppingList:
    """
    Generate a shopping list for a meal plan.

    Args:
        request: Shopping list request with meal plan ID and pantry items

    Returns:
        ShoppingList: Generated shopping list

    Note:
        This endpoint is currently a stub and needs to be wired to the
        shopping list agent.
    """
    # TODO: Wire to shopping list agent
    logger.info(f"GetShoppingList called for meal plan: {request.meal_plan_id}")

    raise HTTPException(
        status_code=501, detail="Shopping list generation not yet implemented"
    )


def serve():
    """Start the FastAPI server."""
    uvicorn.run(
        "backend.src.server.fastapi_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )


if __name__ == "__main__":
    serve()
