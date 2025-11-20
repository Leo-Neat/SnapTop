"""Recipe-related Pydantic models."""

from pydantic import BaseModel, Field


class Ingredient(BaseModel):
    """Recipe ingredient with quantity and unit."""

    name: str = Field(..., description="Ingredient name")
    quantity: float = Field(..., description="Quantity of ingredient")
    unit: str = Field(..., description="Unit of measurement")
    notes: str | None = Field(None, description="Optional notes about the ingredient")


class InstructionSection(BaseModel):
    """Grouped cooking instructions."""

    section_name: str = Field(..., description="Name of the instruction section")
    steps: list[str] = Field(..., description="List of instruction steps")


class NutritionProfile(BaseModel):
    """Nutritional information for the entire recipe (all servings combined)."""

    calories: int | None = Field(None, description="Total calories for entire recipe")
    protein_grams: float | None = Field(None, description="Total protein in grams for entire recipe")
    carbs_grams: float | None = Field(None, description="Total carbohydrates in grams for entire recipe")
    fat_grams: float | None = Field(None, description="Total fat in grams for entire recipe")
    fiber_grams: float | None = Field(None, description="Total fiber in grams for entire recipe")
    sugar_grams: float | None = Field(None, description="Total sugar in grams for entire recipe")
    sodium_mg: float | None = Field(None, description="Total sodium in milligrams for entire recipe")


class Recipe(BaseModel):
    """Complete recipe with all details."""

    recipe_id: str = Field(..., description="Unique identifier for the recipe")
    title: str = Field(..., description="Recipe title")
    description: str = Field(..., description="Recipe description")
    ingredients: list[Ingredient] = Field(..., description="List of ingredients")
    instructions: list[InstructionSection] = Field(..., description="Cooking instructions")
    prep_time_minutes: int = Field(..., description="Preparation time in minutes")
    cook_time_minutes: int = Field(..., description="Cooking time in minutes")
    nutrition: NutritionProfile | None = Field(None, description="Nutritional information for entire recipe (all servings)")
    servings: int = Field(..., description="Number of servings")
    serving_size: str | None = Field(None, description="Description of serving size")
    citations: list[str] | None = Field(None, description="Recipe sources and citations")
    image_base64: str | None = Field(None, description="Base64 encoded recipe image")
