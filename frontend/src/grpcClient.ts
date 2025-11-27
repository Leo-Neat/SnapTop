import { Recipe, GenerateRecipeRequest, AuthResponse, GoogleAuthRequest, FacebookAuthRequest } from './types';

// FastAPI backend endpoints
const API_BASE = 'http://localhost:8000';
const API_ENDPOINT = `${API_BASE}/api/recipes/generate`;

export async function generateRecipe(request: GenerateRecipeRequest): Promise<Recipe> {
  try {
    // Convert camelCase to snake_case for backend
    const apiRequest: any = {
      description: request.description,
    };

    if (request.complexity) {
      apiRequest.complexity = request.complexity;
    }

    if (request.target_macros) {
      apiRequest.target_macros = {
        calories: request.target_macros.calories,
        protein_grams: request.target_macros.proteinGrams,
        carbs_grams: request.target_macros.carbsGrams,
        fat_grams: request.target_macros.fatGrams,
        fiber_grams: request.target_macros.fiberGrams,
        sugar_grams: request.target_macros.sugarGrams,
        sodium_mg: request.target_macros.sodiumMg,
      };
    }

    if (request.available_ingredients && request.available_ingredients.length > 0) {
      apiRequest.available_ingredients = request.available_ingredients;
    }

    const response = await fetch(API_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(apiRequest),
    });

    console.log('Response status:', response.status);

    if (!response.ok) {
      const errorText = await response.text();
      console.error('Error response:', errorText);
      throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
    }

    const responseData = await response.json();
    console.log('Recipe generated:', responseData.title);

    // Convert snake_case response to camelCase for frontend
    const recipe: Recipe = {
      recipeId: responseData.recipe_id,
      title: responseData.title,
      description: responseData.description,
      ingredients: responseData.ingredients,
      instructions: responseData.instructions.map((section: any) => ({
        sectionName: section.section_name,
        steps: section.steps,
      })),
      prepTimeMinutes: responseData.prep_time_minutes,
      cookTimeMinutes: responseData.cook_time_minutes,
      nutrition: responseData.nutrition ? {
        calories: responseData.nutrition.calories,
        proteinGrams: responseData.nutrition.protein_grams,
        carbsGrams: responseData.nutrition.carbs_grams,
        fatGrams: responseData.nutrition.fat_grams,
        fiberGrams: responseData.nutrition.fiber_grams,
        sugarGrams: responseData.nutrition.sugar_grams,
        sodiumMg: responseData.nutrition.sodium_mg,
      } : undefined,
      servings: responseData.servings,
      servingSize: responseData.serving_size,
      citations: responseData.citations,
      imageBase64: responseData.image_base64,
    };

    return recipe;
  } catch (error) {
    console.error('Error generating recipe:', error);
    throw error;
  }
}

export async function authenticateWithGoogle(credential: string): Promise<AuthResponse> {
  try {
    const response = await fetch(`${API_BASE}/api/auth/google`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ credential }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Authentication failed: ${errorText}`);
    }

    const data = await response.json();

    // Convert snake_case to camelCase
    return {
      user: {
        userId: data.user.user_id,
        email: data.user.email,
        name: data.user.name,
        picture: data.user.picture,
        provider: data.user.provider,
      },
      token: {
        accessToken: data.token.access_token,
        tokenType: data.token.token_type,
      },
    };
  } catch (error) {
    console.error('Google authentication error:', error);
    throw error;
  }
}

export async function authenticateWithFacebook(accessToken: string, userId: string): Promise<AuthResponse> {
  try {
    const response = await fetch(`${API_BASE}/api/auth/facebook`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        access_token: accessToken,
        user_id: userId,
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Authentication failed: ${errorText}`);
    }

    const data = await response.json();

    // Convert snake_case to camelCase
    return {
      user: {
        userId: data.user.user_id,
        email: data.user.email,
        name: data.user.name,
        picture: data.user.picture,
        provider: data.user.provider,
      },
      token: {
        accessToken: data.token.access_token,
        tokenType: data.token.token_type,
      },
    };
  } catch (error) {
    console.error('Facebook authentication error:', error);
    throw error;
  }
}
