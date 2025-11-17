# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.3.1](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 5.29.5
# Pydantic Version: 2.12.4
import typing

from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel, Field


class ShoppingItem(BaseModel):
    ingredient_name: str = Field(default="")
    total_quantity: float = Field(default=0.0)
    unit: str = Field(default="")
    needed_for_recipes: typing.List[str] = Field(default_factory=list)


class ShoppingList(BaseModel):
    meal_plan_id: str = Field(default="")
    items: typing.List[ShoppingItem] = Field(default_factory=list)
    generated_at: int = Field(default=0)
