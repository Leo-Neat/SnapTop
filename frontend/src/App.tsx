import { useState } from 'react';
import RecipeForm from './RecipeForm';
import RecipeDisplay from './RecipeDisplay';
import { Recipe, GenerateRecipeRequest } from './types';
import { generateRecipe } from './grpcClient';

function App() {
  const [recipe, setRecipe] = useState<Recipe | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleGenerateRecipe = async (request: GenerateRecipeRequest) => {
    setIsLoading(true);
    setError(null);

    try {
      const generatedRecipe = await generateRecipe(request);
      setRecipe(generatedRecipe);
    } catch (err) {
      setError('Failed to generate recipe. Please try again.');
      console.error('Error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleBack = () => {
    setRecipe(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {error && (
        <div className="fixed top-4 right-4 bg-red-500 text-white px-6 py-3 rounded-lg shadow-lg">
          {error}
        </div>
      )}

      {recipe ? (
        <RecipeDisplay recipe={recipe} onBack={handleBack} />
      ) : (
        <RecipeForm onSubmit={handleGenerateRecipe} isLoading={isLoading} />
      )}
    </div>
  );
}

export default App;
