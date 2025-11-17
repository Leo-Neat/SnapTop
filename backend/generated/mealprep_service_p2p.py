# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.3.1](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 5.29.5
# Pydantic Version: 2.12.4
import typing

from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel, Field

from .recipe_p2p import Ingredient, NutritionProfile
from .user_p2p import PantryItem, UserProfile


class GenerateRecipeRequest(BaseModel):
    description: str = Field(default="")
    target_macros: NutritionProfile = Field(
        default_factory=NutritionProfile
    )  # optional
    available_ingredients: typing.List[Ingredient] = Field(
        default_factory=list
    )  # optional
    complexity: str = Field(
        default=""
    )  # optional, e.g. "easy", "medium", "hard" or a freeform description


class WeeklyMealRequest(BaseModel):  #  Add fields as needed for weekly meal planning
    pass


class GenerateWeeklyMealsRequest(BaseModel):
    user_profile: UserProfile = Field(default_factory=UserProfile)
    weekly_meal_request: WeeklyMealRequest = Field(default_factory=WeeklyMealRequest)


class WeeklyMealPlanProgress(BaseModel):  #  Add fields for streaming progress updates
    pass


class RegenerateRecipeRequest(BaseModel):
    recipe_id: str = Field(default="")
    regeneration_reason: str = Field(default="")


class ModifyRecipeRequest(BaseModel):
    recipe_id: str = Field(default="")
    modification_instructions: str = Field(default="")


class GetShoppingListRequest(BaseModel):
    weekly_meal_plan_id: str = Field(default="")
    pantry: typing.List[PantryItem] = Field(default_factory=list)
