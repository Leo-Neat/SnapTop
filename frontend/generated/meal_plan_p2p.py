# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.3.1](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 5.29.5
# Pydantic Version: 2.12.4
import typing
from datetime import datetime
from enum import IntEnum

from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel, ConfigDict, Field


class MealType(IntEnum):
    MEAL_TYPE_UNSPECIFIED = 0
    BREAKFAST = 1
    LUNCH = 2
    DINNER = 3
    DESSERT = 4
    SNACK = 5


class MacroPercentages(BaseModel):
    protein_percent: float = Field(default=0.0)
    carb_percent: float = Field(default=0.0)
    fat_percent: float = Field(default=0.0)


class RecipeSkeleton(BaseModel):
    model_config = ConfigDict(validate_default=True)
    skeleton_id: str = Field(default="")
    title: str = Field(default="")
    recipe_id: typing.Optional[str] = Field(default="")
    target_calories_per_serving: int = Field(default=0)
    servings: int = Field(default=0)
    macro_percentages: MacroPercentages = Field(default_factory=MacroPercentages)
    dates: "typing.Dict[str, DatesForPerson]" = Field(
        default_factory=dict
    )  # person_id -> DatesForPerson
    meal_type: MealType = Field(default=0)


class MealPlan(BaseModel):
    meal_plan_id: str = Field(default="")
    user_id: str = Field(default="")
    recipes: typing.List[RecipeSkeleton] = Field(default_factory=list)


class DatesForPerson(BaseModel):
    dates: typing.List[datetime] = Field(default_factory=list)
