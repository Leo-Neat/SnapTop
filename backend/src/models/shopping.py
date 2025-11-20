"""Shopping list-related Pydantic models."""

from pydantic import BaseModel, Field


class ShoppingItem(BaseModel):
    """Individual shopping list item."""

    ingredient_name: str = Field(..., description="Name of the ingredient")
    total_quantity: float = Field(
        ..., description="Aggregated quantity across recipes"
    )
    unit: str = Field(..., description="Unit of measurement")
    needed_for_recipes: list[str] = Field(
        default_factory=list, description="Recipe IDs that need this ingredient"
    )


class ShoppingList(BaseModel):
    """Shopping list for a meal plan."""

    meal_plan_id: str = Field(..., description="Associated meal plan ID")
    items: list[ShoppingItem] = Field(
        default_factory=list, description="Shopping items"
    )
    generated_at: int = Field(..., description="Unix timestamp of generation")
