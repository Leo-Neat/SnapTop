export interface Ingredient {
  name: string;
  quantity: number;
  unit: string;
  notes?: string;
}

export interface NutritionProfile {
  calories?: number;
  proteinGrams?: number;
  carbsGrams?: number;
  fatGrams?: number;
  fiberGrams?: number;
  sugarGrams?: number;
  sodiumMg?: number;
}

export interface InstructionSection {
  sectionName: string;
  steps: string[];
}

export interface Recipe {
  recipeId: string;
  title: string;
  description: string;
  ingredients: Ingredient[];
  instructions: InstructionSection[];
  prepTimeMinutes: number;
  cookTimeMinutes: number;
  nutrition?: NutritionProfile;
  servings: number;
  servingSize?: string;
  citations?: string[];
}

export interface GenerateRecipeRequest {
  description: string;
  complexity?: string;
  target_macros?: NutritionProfile;
  available_ingredients?: Ingredient[];
}
