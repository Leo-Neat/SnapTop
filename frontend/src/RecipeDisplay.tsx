import React from 'react';
import { Recipe } from './types';

interface RecipeDisplayProps {
  recipe: Recipe;
  onBack: () => void;
}

const RecipeDisplay: React.FC<RecipeDisplayProps> = ({ recipe, onBack }) => {
  return (
    <div className="min-h-screen p-6 pb-20">
      <div className="max-w-4xl mx-auto">
        <button
          onClick={onBack}
          className="mb-6 px-6 py-3 bg-white hover:bg-gray-50 text-gray-700 font-medium rounded-lg shadow transition flex items-center gap-2"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Generate Another Recipe
        </button>

        <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
          {/* Header */}
          <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white p-8">
            <h1 className="text-4xl font-bold mb-3">{recipe.title}</h1>
            {recipe.description && (
              <p className="text-blue-100 text-lg">{recipe.description}</p>
            )}
          </div>

          {/* Recipe Image */}
          {recipe.imageBase64 && (
            <div className="w-full">
              <img
                src={`data:image/png;base64,${recipe.imageBase64}`}
                alt={recipe.title}
                className="w-full h-96 object-cover"
              />
            </div>
          )}

          {/* Meta Info */}
          <div className="grid grid-cols-3 gap-4 p-6 bg-gray-50 border-b">
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">{recipe.prepTimeMinutes}</div>
              <div className="text-sm text-gray-600">Prep Time (min)</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">{recipe.cookTimeMinutes}</div>
              <div className="text-sm text-gray-600">Cook Time (min)</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">{recipe.servings}</div>
              <div className="text-sm text-gray-600">Servings</div>
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-8 p-8">
            {/* Ingredients */}
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
                Ingredients
              </h2>
              <ul className="space-y-3">
                {recipe.ingredients.map((ingredient, index) => (
                  <li key={index} className="flex items-start gap-3 text-gray-700">
                    <span className="text-blue-600 mt-1">•</span>
                    <span>
                      <span className="font-semibold">
                        {ingredient.quantity} {ingredient.unit}
                      </span>{' '}
                      {ingredient.name}
                      {ingredient.notes && (
                        <span className="text-gray-500 text-sm"> ({ingredient.notes})</span>
                      )}
                    </span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Nutrition */}
            {recipe.nutrition && (
              <div>
                <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                  <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                  Nutrition Facts
                </h2>
                <p className="text-xs text-gray-500 mb-3">Per serving</p>
                <div className="bg-gray-50 rounded-lg p-4 space-y-2">
                  {recipe.nutrition.calories !== undefined && (
                    <div className="flex justify-between">
                      <span className="text-gray-600">Calories</span>
                      <span className="font-semibold text-gray-900">{Math.round(recipe.nutrition.calories / recipe.servings)}</span>
                    </div>
                  )}
                  {recipe.nutrition.proteinGrams !== undefined && (
                    <div className="flex justify-between">
                      <span className="text-gray-600">Protein</span>
                      <span className="font-semibold text-gray-900">{Math.round(recipe.nutrition.proteinGrams / recipe.servings)}g</span>
                    </div>
                  )}
                  {recipe.nutrition.carbsGrams !== undefined && (
                    <div className="flex justify-between">
                      <span className="text-gray-600">Carbohydrates</span>
                      <span className="font-semibold text-gray-900">{Math.round(recipe.nutrition.carbsGrams / recipe.servings)}g</span>
                    </div>
                  )}
                  {recipe.nutrition.fatGrams !== undefined && (
                    <div className="flex justify-between">
                      <span className="text-gray-600">Fat</span>
                      <span className="font-semibold text-gray-900">{Math.round(recipe.nutrition.fatGrams / recipe.servings)}g</span>
                    </div>
                  )}
                  {recipe.nutrition.fiberGrams !== undefined && (
                    <div className="flex justify-between">
                      <span className="text-gray-600">Fiber</span>
                      <span className="font-semibold text-gray-900">{Math.round(recipe.nutrition.fiberGrams / recipe.servings)}g</span>
                    </div>
                  )}
                  {recipe.nutrition.sugarGrams !== undefined && (
                    <div className="flex justify-between">
                      <span className="text-gray-600">Sugar</span>
                      <span className="font-semibold text-gray-900">{Math.round(recipe.nutrition.sugarGrams / recipe.servings)}g</span>
                    </div>
                  )}
                  {recipe.nutrition.sodiumMg !== undefined && (
                    <div className="flex justify-between">
                      <span className="text-gray-600">Sodium</span>
                      <span className="font-semibold text-gray-900">{Math.round(recipe.nutrition.sodiumMg / recipe.servings)}mg</span>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>

          {/* Instructions */}
          <div className="p-8 pt-0">
            <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
              <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
              Instructions
            </h2>
            <div className="space-y-6">
              {recipe.instructions.map((section, sectionIndex) => (
                <div key={sectionIndex}>
                  {section.sectionName && (
                    <h3 className="text-xl font-semibold text-gray-800 mb-3">
                      {section.sectionName}
                    </h3>
                  )}
                  <ol className="space-y-4">
                    {section.steps.map((step, stepIndex) => (
                      <li key={stepIndex} className="flex gap-4">
                        <span className="flex-shrink-0 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-semibold text-sm">
                          {stepIndex + 1}
                        </span>
                        <p className="text-gray-700 pt-1">{step}</p>
                      </li>
                    ))}
                  </ol>
                </div>
              ))}
            </div>
          </div>

          {/* Citations */}
          {recipe.citations && recipe.citations.length > 0 && (
            <div className="p-8 pt-0">
              <h3 className="text-sm font-semibold text-gray-600 mb-2">Sources</h3>
              <ul className="space-y-1">
                {recipe.citations.map((citation, index) => (
                  <li key={index} className="text-sm text-gray-500">
                    {citation}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default RecipeDisplay;
