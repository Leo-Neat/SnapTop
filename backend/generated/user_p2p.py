# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.3.1](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 5.29.5
# Pydantic Version: 2.12.4
import typing
from enum import IntEnum

from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel, ConfigDict, Field


class Allergen(IntEnum):
    NUTS = 0
    DAIRY = 1
    EGGS = 2


class KitchenTool(IntEnum):
    OVEN = 0
    STOVE = 1
    AIR_FRYER = 2
    MICROWAVE = 3
    INSTANT_POT = 4
    BLENDER = 5
    NUTRIBULLET = 6
    IMMERSION_BLENDER = 7
    VACUUM_SEALER = 8
    HAND_MIXER = 9
    STAND_MIXER = 10


class DietaryProfile(BaseModel):
    class ProfileType(IntEnum):
        OMNIVORE = 0
        VEGAN = 1
        VEGETARIAN = 2
        PESCATARIAN = 3
        PALEO = 4
        KETO = 5
        GLUTEN_FREE = 6

    model_config = ConfigDict(validate_default=True)
    profiles: typing.List[ProfileType] = Field(default_factory=list)
    allergens: typing.List[Allergen] = Field(default_factory=list)


class PantryItem(BaseModel):
    name: str = Field(default="")
    quantity: float = Field(default=0.0)
    unit: str = Field(default="")
    notes: str = Field(default="")


class MealTypeRequest(BaseModel):
    class MealType(IntEnum):
        BREAKFAST = 0
        LUNCH = 1
        DINNER = 2
        SNACK = 3
        DESSERT = 4

    model_config = ConfigDict(validate_default=True)
    type: MealType = Field(default=0)
    recipes_per_week: int = Field(default=0)
    servings_per_recipe: int = Field(default=0)


class MacroSplit(BaseModel):
    carbs_percent: float = Field(default=0.0)
    fat_percent: float = Field(default=0.0)
    protein_percent: float = Field(default=0.0)


class MealPlanningParams(BaseModel):
    meal_requests: typing.List[MealTypeRequest] = Field(default_factory=list)
    daily_calorie_target: int = Field(default=0)
    macro_targets: MacroSplit = Field(default_factory=MacroSplit)


class UserProfile(BaseModel):
    model_config = ConfigDict(validate_default=True)
    user_id: str = Field(default="")
    dietary_profile: DietaryProfile = Field(default_factory=DietaryProfile)
    dietary_preferences: str = Field(default="")
    dietary_dislikes: str = Field(default="")
    kitchen_tools: typing.List[KitchenTool] = Field(default_factory=list)
    pantry: typing.List[PantryItem] = Field(default_factory=list)
    grocery_stores: typing.List[str] = Field(default_factory=list)
    meal_params: MealPlanningParams = Field(default_factory=MealPlanningParams)
