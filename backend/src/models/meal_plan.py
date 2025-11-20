"""Meal plan-related Pydantic models."""

from datetime import datetime
from pydantic import BaseModel, Field

from backend.src.models.user import MealType


class MacroPercentages(BaseModel):
    """Macronutrient percentages."""

    protein_percent: float = Field(..., description="Percentage of calories from protein")
    carb_percent: float = Field(..., description="Percentage of calories from carbs")
    fat_percent: float = Field(..., description="Percentage of calories from fat")


class DatesForPerson(BaseModel):
    """Dates scheduled for a person."""

    dates: list[datetime] = Field(..., description="List of dates")


class RecipeSkeleton(BaseModel):
    """Recipe placeholder in meal plan."""

    skeleton_id: str = Field(..., description="Unique skeleton identifier")
    title: str = Field(..., description="Recipe title")
    recipe_id: str | None = Field(None, description="Associated recipe ID if generated")
    target_calories_per_serving: int = Field(
        ..., description="Target calories per serving"
    )
    servings: int = Field(..., description="Number of servings")
    macro_percentages: MacroPercentages = Field(..., description="Macro percentages")
    dates: dict[str, DatesForPerson] = Field(
        default_factory=dict, description="person_id -> dates scheduled"
    )
    meal_type: MealType = Field(..., description="Type of meal")


class MealPlan(BaseModel):
    """Weekly meal plan."""

    meal_plan_id: str = Field(..., description="Unique meal plan identifier")
    user_id: str = Field(..., description="User ID this plan belongs to")
    recipes: list[RecipeSkeleton] = Field(
        default_factory=list, description="Recipe skeletons in the plan"
    )
