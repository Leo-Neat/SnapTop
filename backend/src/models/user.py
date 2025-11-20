"""User-related Pydantic models."""

from enum import Enum
from pydantic import BaseModel, Field


class ProfileType(str, Enum):
    """Dietary profile types."""

    OMNIVORE = "OMNIVORE"
    VEGAN = "VEGAN"
    VEGETARIAN = "VEGETARIAN"
    PESCATARIAN = "PESCATARIAN"
    PALEO = "PALEO"
    KETO = "KETO"
    GLUTEN_FREE = "GLUTEN_FREE"


class Allergen(str, Enum):
    """Common allergens."""

    NUTS = "NUTS"
    DAIRY = "DAIRY"
    EGGS = "EGGS"
    SHELLFISH = "SHELLFISH"
    SOY = "SOY"
    WHEAT = "WHEAT"


class KitchenTool(str, Enum):
    """Available kitchen equipment."""

    OVEN = "OVEN"
    STOVE = "STOVE"
    AIR_FRYER = "AIR_FRYER"
    MICROWAVE = "MICROWAVE"
    INSTANT_POT = "INSTANT_POT"
    BLENDER = "BLENDER"
    FOOD_PROCESSOR = "FOOD_PROCESSOR"
    SLOW_COOKER = "SLOW_COOKER"
    GRILL = "GRILL"


class MealType(str, Enum):
    """Meal types."""

    BREAKFAST = "BREAKFAST"
    LUNCH = "LUNCH"
    DINNER = "DINNER"
    SNACK = "SNACK"
    DESSERT = "DESSERT"


class DietaryProfile(BaseModel):
    """Diet type and allergen information."""

    profiles: list[ProfileType] = Field(
        default_factory=list, description="Dietary profiles"
    )
    allergens: list[Allergen] = Field(
        default_factory=list, description="Allergens to avoid"
    )


class PantryItem(BaseModel):
    """Available ingredient in pantry."""

    name: str = Field(..., description="Item name")
    quantity: float = Field(..., description="Quantity available")
    unit: str = Field(..., description="Unit of measurement")
    notes: str | None = Field(None, description="Optional notes")


class MacroSplit(BaseModel):
    """Macronutrient percentages."""

    carbs_percent: float = Field(..., description="Percentage of calories from carbs")
    fat_percent: float = Field(..., description="Percentage of calories from fat")
    protein_percent: float = Field(
        ..., description="Percentage of calories from protein"
    )


class MealTypeRequest(BaseModel):
    """Meal type preferences for planning."""

    type: MealType = Field(..., description="Type of meal")
    recipes_per_week: int = Field(..., description="Number of recipes per week")
    servings_per_recipe: int = Field(..., description="Servings per recipe")


class MealPlanningParams(BaseModel):
    """Meal planning configuration."""

    meal_requests: list[MealTypeRequest] = Field(
        ..., description="Meal type requests"
    )
    daily_calorie_target: int = Field(..., description="Daily calorie target")
    macro_targets: MacroSplit | None = Field(None, description="Macro targets")


class UserProfile(BaseModel):
    """User profile with preferences and constraints."""

    user_id: str = Field(..., description="Unique user identifier")
    dietary_profile: DietaryProfile = Field(..., description="Dietary preferences")
    dietary_preferences: str | None = Field(
        None, description="Additional dietary preferences"
    )
    dietary_dislikes: str | None = Field(None, description="Foods to avoid")
    kitchen_tools: list[KitchenTool] = Field(
        default_factory=list, description="Available kitchen tools"
    )
    pantry: list[PantryItem] = Field(
        default_factory=list, description="Available pantry items"
    )
    grocery_stores: list[str] = Field(
        default_factory=list, description="Preferred grocery stores"
    )
    meal_params: MealPlanningParams | None = Field(
        None, description="Meal planning parameters"
    )
