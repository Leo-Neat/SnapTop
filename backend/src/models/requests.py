"""Request models for API endpoints."""

from pydantic import BaseModel, Field

from backend.src.models.recipe import Ingredient, NutritionProfile
from backend.src.models.user import UserProfile


class GenerateRecipeRequest(BaseModel):
    """Request to generate a new recipe."""

    description: str = Field(..., description="Recipe description from user")
    complexity: str | None = Field(
        None, description="Recipe complexity: easy, medium, hard"
    )
    target_macros: NutritionProfile | None = Field(
        None, description="Target nutritional macros"
    )
    available_ingredients: list[Ingredient] | None = Field(
        None, description="Ingredients user has available"
    )


class GenerateWeeklyMealsRequest(BaseModel):
    """Request to generate a weekly meal plan."""

    user_profile: UserProfile = Field(..., description="User profile and preferences")


class RegenerateRecipeRequest(BaseModel):
    """Request to regenerate an existing recipe."""

    recipe_id: str = Field(..., description="Recipe ID to regenerate")
    regeneration_reason: str | None = Field(
        None, description="Reason for regeneration"
    )


class ModifyRecipeRequest(BaseModel):
    """Request to modify an existing recipe."""

    recipe_id: str = Field(..., description="Recipe ID to modify")
    modification_instructions: str = Field(
        ..., description="Instructions for modification"
    )


class GetShoppingListRequest(BaseModel):
    """Request to get a shopping list for a meal plan."""

    meal_plan_id: str = Field(..., description="Meal plan ID")
    pantry_items: list[Ingredient] | None = Field(
        None, description="Items already in pantry"
    )
