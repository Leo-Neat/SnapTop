import React, { useState } from 'react';
import { GenerateRecipeRequest, Ingredient, NutritionProfile } from './types';

interface RecipeFormProps {
  onSubmit: (request: GenerateRecipeRequest) => void;
  isLoading: boolean;
}

const RecipeForm: React.FC<RecipeFormProps> = ({ onSubmit, isLoading }) => {
  const [description, setDescription] = useState('');
  const [complexity, setComplexity] = useState('');
  const [showAdvanced, setShowAdvanced] = useState(false);

  // Nutrition fields
  const [calories, setCalories] = useState('');
  const [protein, setProtein] = useState('');
  const [carbs, setCarbs] = useState('');
  const [fat, setFat] = useState('');

  // Ingredients
  const [ingredientName, setIngredientName] = useState('');
  const [ingredientQty, setIngredientQty] = useState('');
  const [ingredientUnit, setIngredientUnit] = useState('');
  const [ingredients, setIngredients] = useState<Ingredient[]>([]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const request: GenerateRecipeRequest = {
      description,
    };

    if (complexity) {
      request.complexity = complexity;
    }

    if (calories || protein || carbs || fat) {
      request.target_macros = {} as NutritionProfile;
      if (calories) request.target_macros.calories = parseInt(calories);
      if (protein) request.target_macros.proteinGrams = parseFloat(protein);
      if (carbs) request.target_macros.carbsGrams = parseFloat(carbs);
      if (fat) request.target_macros.fatGrams = parseFloat(fat);
    }

    if (ingredients.length > 0) {
      request.available_ingredients = ingredients;
    }

    onSubmit(request);
  };

  const addIngredient = () => {
    if (ingredientName && ingredientQty) {
      setIngredients([
        ...ingredients,
        {
          name: ingredientName,
          quantity: parseFloat(ingredientQty),
          unit: ingredientUnit,
        },
      ]);
      setIngredientName('');
      setIngredientQty('');
      setIngredientUnit('');
    }
  };

  const removeIngredient = (index: number) => {
    setIngredients(ingredients.filter((_, i) => i !== index));
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-6">
      <div className="w-full max-w-2xl">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Recipe Generator</h1>
          <p className="text-gray-600">Tell us what you'd like to cook</p>
        </div>

        <form onSubmit={handleSubmit} className="bg-white rounded-2xl shadow-lg p-8 space-y-6">
          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
              What would you like to make? *
            </label>
            <textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              required
              rows={3}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
              placeholder="e.g., A healthy pasta dish with chicken and vegetables"
            />
          </div>

          <div>
            <label htmlFor="complexity" className="block text-sm font-medium text-gray-700 mb-2">
              Complexity
            </label>
            <select
              id="complexity"
              value={complexity}
              onChange={(e) => setComplexity(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
            >
              <option value="">Any</option>
              <option value="easy">Easy</option>
              <option value="medium">Medium</option>
              <option value="hard">Hard</option>
            </select>
          </div>

          <button
            type="button"
            onClick={() => setShowAdvanced(!showAdvanced)}
            className="text-blue-600 hover:text-blue-700 text-sm font-medium"
          >
            {showAdvanced ? '− Hide' : '+ Show'} Advanced Options
          </button>

          {showAdvanced && (
            <div className="space-y-6 p-6 bg-gray-50 rounded-lg">
              <div>
                <h3 className="text-sm font-semibold text-gray-900 mb-4">Target Nutrition (Optional)</h3>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm text-gray-700 mb-1">Calories</label>
                    <input
                      type="number"
                      value={calories}
                      onChange={(e) => setCalories(e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm text-gray-700 mb-1">Protein (g)</label>
                    <input
                      type="number"
                      step="0.1"
                      value={protein}
                      onChange={(e) => setProtein(e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="30"
                    />
                  </div>
                  <div>
                    <label className="block text-sm text-gray-700 mb-1">Carbs (g)</label>
                    <input
                      type="number"
                      step="0.1"
                      value={carbs}
                      onChange={(e) => setCarbs(e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="50"
                    />
                  </div>
                  <div>
                    <label className="block text-sm text-gray-700 mb-1">Fat (g)</label>
                    <input
                      type="number"
                      step="0.1"
                      value={fat}
                      onChange={(e) => setFat(e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="15"
                    />
                  </div>
                </div>
              </div>

              <div>
                <h3 className="text-sm font-semibold text-gray-900 mb-4">Available Ingredients (Optional)</h3>
                <div className="flex gap-2 mb-3">
                  <input
                    type="text"
                    value={ingredientName}
                    onChange={(e) => setIngredientName(e.target.value)}
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Ingredient name"
                  />
                  <input
                    type="number"
                    step="0.1"
                    value={ingredientQty}
                    onChange={(e) => setIngredientQty(e.target.value)}
                    className="w-24 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Qty"
                  />
                  <input
                    type="text"
                    value={ingredientUnit}
                    onChange={(e) => setIngredientUnit(e.target.value)}
                    className="w-24 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Unit"
                  />
                  <button
                    type="button"
                    onClick={addIngredient}
                    className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition font-medium"
                  >
                    Add
                  </button>
                </div>

                {ingredients.length > 0 && (
                  <div className="space-y-2">
                    {ingredients.map((ing, index) => (
                      <div key={index} className="flex justify-between items-center bg-white px-3 py-2 rounded-lg">
                        <span className="text-sm text-gray-700">
                          {ing.quantity} {ing.unit} {ing.name}
                        </span>
                        <button
                          type="button"
                          onClick={() => removeIngredient(index)}
                          className="text-red-600 hover:text-red-700 text-sm font-medium"
                        >
                          Remove
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}

          <button
            type="submit"
            disabled={isLoading || !description}
            className="w-full py-4 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold rounded-lg transition shadow-lg hover:shadow-xl disabled:cursor-not-allowed"
          >
            {isLoading ? 'Generating...' : 'Generate Recipe'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default RecipeForm;
