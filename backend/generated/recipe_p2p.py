# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.3.1](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 5.29.5
# Pydantic Version: 2.12.4
import typing

from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel, Field


class Ingredient(BaseModel):
    name: str = Field(default="")
    quantity: float = Field(default=0.0)
    unit: str = Field(default="")
    notes: str = Field(default="")


class InstructionSection(BaseModel):
    section_name: str = Field(default="")
    steps: typing.List[str] = Field(default_factory=list)


class NutritionProfile(BaseModel):
    calories: int = Field(default=0)
    protein_grams: float = Field(default=0.0)
    carbs_grams: float = Field(default=0.0)
    fat_grams: float = Field(default=0.0)
    fiber_grams: float = Field(default=0.0)
    sugar_grams: float = Field(default=0.0)
    sodium_mg: float = Field(default=0.0)


class Recipe(BaseModel):
    recipe_id: str = Field(default="")
    title: str = Field(default="")
    description: str = Field(default="")
    ingredients: typing.List[Ingredient] = Field(default_factory=list)
    instructions: typing.List[InstructionSection] = Field(default_factory=list)
    prep_time_minutes: int = Field(default=0)
    cook_time_minutes: int = Field(default=0)
    nutrition: NutritionProfile = Field(default_factory=NutritionProfile)
    servings: int = Field(default=0)
    serving_size: str = Field(default="")
    citations: typing.List[str] = Field(default_factory=list)
