import { Recipe, GenerateRecipeRequest } from './types';

// For now, we'll use a simple fetch-based approach to communicate with the gRPC backend
// through an Envoy proxy that translates HTTP/JSON to gRPC

const GRPC_ENDPOINT = 'http://localhost:8080/mealprep.proto.MealPrepService/GenerateRecipe';

export async function generateRecipe(request: GenerateRecipeRequest): Promise<Recipe> {
  try {
    // Convert our request to the format expected by the gRPC service
    const grpcRequest: any = {
      description: request.description,
    };

    if (request.complexity) {
      grpcRequest.complexity = request.complexity;
    }

    if (request.target_macros) {
      grpcRequest.target_macros = {
        calories: request.target_macros.calories || 0,
        proteinGrams: request.target_macros.proteinGrams || 0,
        carbsGrams: request.target_macros.carbsGrams || 0,
        fatGrams: request.target_macros.fatGrams || 0,
        fiberGrams: request.target_macros.fiberGrams || 0,
        sugarGrams: request.target_macros.sugarGrams || 0,
        sodiumMg: request.target_macros.sodiumMg || 0,
      };
    }

    if (request.available_ingredients && request.available_ingredients.length > 0) {
      grpcRequest.available_ingredients = request.available_ingredients.map(ing => ({
        name: ing.name,
        quantity: ing.quantity,
        unit: ing.unit || '',
        notes: ing.notes || '',
      }));
    }

    const response = await fetch(GRPC_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(grpcRequest),
    });

    console.log('Response status:', response.status);
    console.log('Response headers:', Object.fromEntries(response.headers.entries()));

    const responseText = await response.text();
    console.log('Response body:', responseText);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}, body: ${responseText}`);
    }

    if (!responseText) {
      throw new Error('Empty response from server');
    }

    const recipe = JSON.parse(responseText);
    return recipe as Recipe;
  } catch (error) {
    console.error('Error generating recipe:', error);
    throw error;
  }
}
