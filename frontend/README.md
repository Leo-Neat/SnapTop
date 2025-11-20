# SnapTop Frontend

A modern web application for AI-powered recipe generation, built with React, TypeScript, and Tailwind CSS.

## Features

- 🎨 Clean, modern UI with Tailwind CSS
- 📝 Recipe generation form with advanced options
- 🎯 Nutrition targeting (calories, protein, carbs, fat) per serving
- 🥕 Ingredient availability specification
- 📖 Beautiful recipe display with step-by-step instructions
- 🖼️ AI-generated recipe images
- 📊 Automatic per-serving nutrition calculation

## Tech Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first styling
- **Fetch API** - Backend communication via REST

## Quick Start

### Option 1: Docker Compose (Recommended)

Run the entire stack from the project root:

```bash
docker-compose up --build
```

The frontend will be available at http://localhost:3000

### Option 2: Local Development

Run the frontend locally while the backend runs in Docker:

#### 1. Start the Backend

```bash
# From project root
docker-compose up backend
```

#### 2. Install Dependencies

```bash
# From frontend directory
npm install
```

#### 3. Start the Dev Server

```bash
npm run dev
```

The application will be available at http://localhost:3000

## Project Structure

```
frontend/
├── src/
│   ├── App.tsx              # Main application component
│   ├── RecipeForm.tsx       # Recipe generation form with inputs
│   ├── RecipeDisplay.tsx    # Recipe display component
│   ├── grpcClient.ts        # API client (REST, not gRPC anymore)
│   ├── types.ts             # TypeScript type definitions
│   ├── main.tsx             # Application entry point
│   └── index.css            # Global styles with Tailwind
├── public/                  # Static assets
├── vite.config.ts          # Vite configuration
├── tailwind.config.js      # Tailwind CSS configuration
├── tsconfig.json           # TypeScript configuration
├── package.json            # Dependencies and scripts
└── README.md               # This file
```

## Available Scripts

```bash
npm run dev        # Start development server (http://localhost:3000)
npm run build      # Build for production
npm run preview    # Preview production build
```

## How It Works

### Data Flow

1. **User Input**: User fills out the recipe generation form
   - Recipe description (required)
   - Complexity level (optional: easy, medium, hard)
   - Target nutrition per serving (optional)
   - Available ingredients (optional)

2. **API Request**: Form data is sent to the FastAPI backend
   - Endpoint: `POST http://localhost:8000/api/recipes/generate`
   - Format: JSON with snake_case fields

3. **Backend Processing**: The backend's AI agent generates the recipe
   - Searches for recipe inspiration
   - Calculates nutrition for entire recipe
   - Generates an AI image

4. **Response Handling**: Frontend receives and transforms the data
   - Converts snake_case to camelCase
   - Calculates per-serving nutrition (divides by servings)
   - Displays the recipe with image

5. **Recipe Display**: Beautiful presentation of the recipe
   - Recipe title and description
   - AI-generated image
   - Prep/cook times and servings
   - Ingredients list
   - Nutrition facts (per serving)
   - Step-by-step instructions
   - Citations/sources

### Component Architecture

```
App.tsx
├── RecipeForm (onSubmit → generateRecipe)
│   ├── Basic inputs (description, complexity)
│   └── Advanced options
│       ├── Target nutrition inputs
│       └── Available ingredients manager
└── RecipeDisplay (recipe, onBack)
    ├── Recipe header (title, description)
    ├── Recipe image
    ├── Meta info (times, servings)
    ├── Two-column layout
    │   ├── Ingredients list
    │   └── Nutrition facts (calculated per serving)
    └── Instructions by section
```

## API Integration

### API Client (`grpcClient.ts`)

The `grpcClient.ts` file handles all communication with the backend:

**Request Format:**
```typescript
{
  description: string;           // Required
  complexity?: string;           // Optional: "easy" | "medium" | "hard"
  target_macros?: {             // Optional, per serving
    calories?: number;
    protein_grams?: number;
    carbs_grams?: number;
    fat_grams?: number;
  };
  available_ingredients?: Array<{
    name: string;
    quantity: number;
    unit: string;
  }>;
}
```

**Response Format:**
```typescript
{
  recipe_id: string;
  title: string;
  description: string;
  ingredients: Array<Ingredient>;
  instructions: Array<InstructionSection>;
  prep_time_minutes: number;
  cook_time_minutes: number;
  nutrition: NutritionProfile;    // Total for entire recipe
  servings: number;
  serving_size?: string;
  citations?: string[];
  image_base64?: string;          // Base64 PNG image
}
```

### Nutrition Calculation

The backend returns nutrition for the **entire recipe**. The frontend calculates per-serving values:

```typescript
// Display per-serving nutrition
const perServingCalories = Math.round(recipe.nutrition.calories / recipe.servings);
```

## Development

### Type Safety

All data models are defined in `types.ts`:
- `Recipe` - Complete recipe with all fields
- `Ingredient` - Individual ingredient
- `NutritionProfile` - Nutritional information
- `InstructionSection` - Grouped cooking steps
- `GenerateRecipeRequest` - API request payload

### Styling

The app uses Tailwind CSS with a custom configuration:

**Color Scheme:**
- Primary: Blue (`blue-600`, `blue-700`)
- Background: White and light gray
- Text: Gray scale for hierarchy

**Responsive Design:**
- Mobile-first approach
- Grid layouts for ingredient/nutrition display
- Responsive navigation and forms

### State Management

Simple React state using `useState`:
- `recipe` - Currently displayed recipe
- `loading` - Request in progress
- `error` - Error message if any
- Form state for all inputs

## Troubleshooting

### Backend Connection Issues

**Problem:** "Failed to fetch" or connection errors

**Solutions:**
1. Verify backend is running:
   ```bash
   curl http://localhost:8000/
   ```
2. Check Docker network if using containers
3. Review browser console for CORS errors
4. Ensure backend is on port 8000

### Recipe Not Generating

**Problem:** Form submits but no recipe appears

**Solutions:**
1. Check browser console for errors
2. Verify backend logs:
   ```bash
   docker-compose logs -f backend
   ```
3. Test API directly:
   ```bash
   curl -X POST http://localhost:8000/api/recipes/generate \
     -H "Content-Type: application/json" \
     -d '{"description": "pasta with chicken"}'
   ```

### Image Not Displaying

**Problem:** Recipe displays but no image

**Solutions:**
1. Check if `imageBase64` is in the response
2. Verify the base64 string is valid
3. Check browser console for image load errors
4. Backend may have failed to generate image (check logs)

### Build Errors

**Problem:** `npm run build` fails

**Solutions:**
1. Delete `node_modules` and reinstall:
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```
2. Check TypeScript errors:
   ```bash
   npm run build 2>&1 | grep "error TS"
   ```
3. Ensure all types are correctly defined

## Production Build

Build for production:

```bash
npm run build
```

The optimized files will be in the `dist/` directory.

### Deployment Options

- **Static Hosting**: Deploy to Vercel, Netlify, or AWS S3
- **Docker**: Use the production container
- **CDN**: Serve from any CDN with static file support

**Environment Configuration:**

For production, update the API endpoint in `grpcClient.ts`:

```typescript
const API_ENDPOINT = process.env.VITE_API_URL || 'http://localhost:8000/api/recipes/generate';
```

Then set the environment variable during build:
```bash
VITE_API_URL=https://your-api.com npm run build
```

## Related Documentation

- [Main README](../README.md) - Project overview
- [Backend README](../backend/README.md) - Backend development
- [QUICKSTART](../QUICKSTART.md) - Quick start guide
- [API Docs](http://localhost:8000/docs) - Interactive API documentation (when running)

## License

ISC
