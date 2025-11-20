"""Pydantic models for the SnapTop API."""

from backend.src.models.recipe import (
    Ingredient,
    InstructionSection,
    NutritionProfile,
    Recipe,
)
from backend.src.models.user import (
    Allergen,
    DietaryProfile,
    KitchenTool,
    MacroSplit,
    MealPlanningParams,
    MealType,
    MealTypeRequest,
    PantryItem,
    ProfileType,
    UserProfile,
)
from backend.src.models.meal_plan import (
    DatesForPerson,
    MacroPercentages,
    MealPlan,
    RecipeSkeleton,
)
from backend.src.models.shopping import ShoppingItem, ShoppingList
from backend.src.models.requests import (
    GenerateRecipeRequest,
    GenerateWeeklyMealsRequest,
    ModifyRecipeRequest,
    RegenerateRecipeRequest,
    GetShoppingListRequest,
)

__all__ = [
    # Recipe models
    "Ingredient",
    "InstructionSection",
    "NutritionProfile",
    "Recipe",
    # User models
    "Allergen",
    "DietaryProfile",
    "KitchenTool",
    "MacroSplit",
    "MealPlanningParams",
    "MealType",
    "MealTypeRequest",
    "PantryItem",
    "ProfileType",
    "UserProfile",
    # Meal plan models
    "DatesForPerson",
    "MacroPercentages",
    "MealPlan",
    "RecipeSkeleton",
    # Shopping models
    "ShoppingItem",
    "ShoppingList",
    # Request models
    "GenerateRecipeRequest",
    "GenerateWeeklyMealsRequest",
    "ModifyRecipeRequest",
    "RegenerateRecipeRequest",
    "GetShoppingListRequest",
]
