import grpc
from concurrent import futures
from src.mealprep.proto import mealprep_service_pb2_grpc
from src.mealprep.proto import meal_plan_pb2, recipe_pb2, shopping_pb2, user_pb2
from src.mealprep.proto.meal_plan_p2p import MealPlan
from src.mealprep.proto.recipe_p2p import Recipe
from src.mealprep.proto.shopping_p2p import ShoppingList
from src.mealprep.proto.user_p2p import UserProfile
import logging
from src.agents.recipe_agent import agent, system_prompt

class MealPrepServiceServicer(mealprep_service_pb2_grpc.MealPrepServiceServicer):
    def GenerateWeeklyMeals(self, request, context):
        # TODO: Wire to nutritionist agent and planner
        meal_plan = meal_plan_pb2.MealPlan()
        meal_plan.meal_plan_id = "dummy_id"
        meal_plan.user_id = request.user_profile.user_id
        # ...populate recipes...
        yield meal_plan

    def RegenerateRecipe(self, request, context):
        # TODO: Wire to chef agent
        recipe = recipe_pb2.Recipe()
        recipe.recipe_id = request.recipe_id
        # ...populate other fields...
        return recipe

    def ModifyRecipe(self, request, context):
        # TODO: Wire to chef agent with modification instructions
        recipe = recipe_pb2.Recipe()
        recipe.recipe_id = request.recipe_id
        # ...populate other fields...
        return recipe

    def GetShoppingList(self, request, context):
        # TODO: Wire to shopping list agent
        shopping_list = shopping_pb2.ShoppingList()
        shopping_list.meal_plan_id = request.weekly_meal_plan_id
        # ...populate items...
        return shopping_list

    def GenerateRecipe(self, request, context):
        # Wire to recipe agent
   

        # Build a single prompt string from all request fields
        prompt_lines = []
        prompt_lines.append(f"Recipe request: {request.description}")

        if request.complexity:
            prompt_lines.append(f"Desired complexity: {request.complexity}")

        if request.HasField("target_macros"):
            macros = request.target_macros
            macro_parts = []
            if macros.calories:
                macro_parts.append(f"calories={macros.calories}")
            if macros.protein_grams:
                macro_parts.append(f"protein={macros.protein_grams}g")
            if macros.carbs_grams:
                macro_parts.append(f"carbs={macros.carbs_grams}g")
            if macros.fat_grams:
                macro_parts.append(f"fat={macros.fat_grams}g")
            if macros.fiber_grams:
                macro_parts.append(f"fiber={macros.fiber_grams}g")
            if macros.sugar_grams:
                macro_parts.append(f"sugar={macros.sugar_grams}g")
            if macros.sodium_mg:
                macro_parts.append(f"sodium={macros.sodium_mg}mg")
            if macro_parts:
                prompt_lines.append("Target macros: " + ", ".join(macro_parts))

        if request.available_ingredients:
            ing_list = []
            for ing in request.available_ingredients:
                ing_desc = f"{ing.quantity} {ing.unit} {ing.name}" if ing.unit else f"{ing.quantity} {ing.name}"
                if ing.notes:
                    ing_desc += f" ({ing.notes})"
                ing_list.append(ing_desc)
            prompt_lines.append("Available ingredients: " + ", ".join(ing_list))

        prompt = "\n".join(prompt_lines)

        # Compose agent input as in main()
        agent_input = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ]
        }
        result = agent.invoke(agent_input)
        recipe_obj = result["structured_response"]
        # Convert Pydantic Recipe to proto
        recipe_proto = recipe_obj.to_proto() if hasattr(recipe_obj, "to_proto") else recipe_pb2.Recipe(**recipe_obj.model_dump())
        return recipe_proto


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    mealprep_service_pb2_grpc.add_MealPrepServiceServicer_to_server(
        MealPrepServiceServicer(), server
    )
    server.add_insecure_port('[::]:50051')
    logging.info("Starting gRPC server on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve()
