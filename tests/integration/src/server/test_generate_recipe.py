import grpc
import sys
from src.mealprep.proto import (
    mealprep_service_pb2_grpc,
    mealprep_service_pb2,
    recipe_pb2,
)


def test_generate_recipe():
    channel = grpc.insecure_channel("localhost:50051")
    stub = mealprep_service_pb2_grpc.MealPrepServiceStub(channel)

    # Build a test request
    request = mealprep_service_pb2.GenerateRecipeRequest(
        description="I want a healthy vegetarian dinner using quinoa and greek yogurt.",
        complexity="easy",
        # Optionally add macros
        target_macros=recipe_pb2.NutritionProfile(
            calories=500,
            protein_grams=20,
        ),
        available_ingredients=[
            recipe_pb2.Ingredient(name="quinoa", quantity=1, unit="cup"),
            recipe_pb2.Ingredient(name="greek yogurt", quantity=0.5, unit="cup"),
        ],
    )

    print("Sending GenerateRecipe request...")
    try:
        response = stub.GenerateRecipe(request)
        print("Received Recipe response:")
        print(response)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)


if __name__ == "__main__":
    test_generate_recipe()
