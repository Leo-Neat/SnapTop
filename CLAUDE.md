# CLAUDE.md - AI Assistant Guide for SnapTop

This document provides comprehensive guidance for AI assistants working with the SnapTop codebase. It covers architecture, conventions, workflows, and critical knowledge needed to effectively contribute to this project.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Codebase Structure](#codebase-structure)
3. [Development Setup & Workflows](#development-setup--workflows)
4. [Architecture & Design Patterns](#architecture--design-patterns)
5. [Code Conventions](#code-conventions)
6. [Common Tasks](#common-tasks)
7. [Critical Knowledge & Gotchas](#critical-knowledge--gotchas)
8. [External Integrations](#external-integrations)
9. [Testing & Quality](#testing--quality)
10. [Deployment & Infrastructure](#deployment--infrastructure)

---

## Project Overview

### What is SnapTop?

SnapTop is an AI-powered meal planning system that generates personalized recipes, weekly meal plans, nutritional analysis, and shopping lists. It uses multi-agent architecture powered by LangGraph and Google Cloud services.

### Core Features

- **Recipe Generation**: AI-created recipes based on dietary preferences, ingredients, and nutrition targets
- **Multi-Agent System**: Specialized agents for different tasks (Chef, Nutritionist, Planner)
- **Nutritional Analysis**: Automatic macro/micronutrient calculation via FatSecret API
- **Recipe Images**: AI-generated food photography using Google Imagen
- **Modern Stack**: FastAPI backend + React/TypeScript frontend

### Technology Stack

**Backend:**
- Python 3.12+ with FastAPI
- LangGraph + LangChain for AI agents
- Pydantic for data validation
- Google Cloud (Vertex AI, Secret Manager, BigQuery)
- OAuth2 for API authentication

**Frontend:**
- React 18 + TypeScript
- Vite build tool
- Tailwind CSS
- Simple useState-based state management

**Infrastructure:**
- Docker + Docker Compose
- uv (Python package manager)
- BigQuery (schemas defined, not actively used yet)

### Project Status

**Production Ready:**
- Recipe generation endpoint (`/api/recipes/generate`)
- Recipe agent with web search, nutrition lookup, and image generation
- Frontend recipe form and display

**In Development:**
- Meal planning functionality (nutritionist agent exists but not wired)
- Shopping list generation (stub endpoint)
- Recipe modification (not implemented)
- BigQuery persistence layer (schemas exist, not used)

---

## Codebase Structure

### Directory Layout

```
SnapTop/
├── backend/
│   ├── src/
│   │   ├── agents/              # LangGraph AI agents
│   │   │   ├── recipe_agent.py          # Recipe generation agent ✅
│   │   │   └── nutritionist_agent.py    # Meal planning agent 🚧
│   │   ├── common/              # Shared utilities
│   │   │   ├── llms.py                  # Gemini model wrappers
│   │   │   ├── utils.py                 # GCP helpers (Secret Manager, etc.)
│   │   │   └── img_generation_models.py # Imagen wrappers
│   │   ├── langgraph_tools/     # Agent tools (LangChain compatible)
│   │   │   ├── nutrition.py             # FatSecret + OpenFoodFacts APIs
│   │   │   ├── recipe_search.py         # Google Custom Search
│   │   │   └── generate_recipe_image.py # AI image generation
│   │   ├── models/              # Pydantic data models
│   │   │   ├── __init__.py              # Exports all models
│   │   │   ├── recipe.py                # Recipe, Ingredient, NutritionProfile
│   │   │   ├── user.py                  # UserProfile, DietaryProfile, enums
│   │   │   ├── meal_plan.py             # MealPlan, RecipeSkeleton
│   │   │   ├── shopping.py              # ShoppingList, ShoppingItem
│   │   │   └── requests.py              # API request models
│   │   └── server/              # FastAPI server
│   │       └── fastapi_server.py        # Main API server
│   ├── Dockerfile
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── App.tsx              # Main app component (state container)
│   │   ├── RecipeForm.tsx       # Recipe input form
│   │   ├── RecipeDisplay.tsx    # Recipe viewer component
│   │   ├── grpcClient.ts        # REST API client (misnamed, uses fetch)
│   │   ├── types.ts             # TypeScript type definitions
│   │   ├── main.tsx             # React entry point
│   │   └── index.css            # Tailwind CSS setup
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   └── README.md
├── bigquery/                    # Database schemas (not actively used yet)
│   ├── recipes.sql
│   ├── users.sql
│   ├── meal_plans.sql
│   ├── agent_logs.sql
│   └── create_bigquery_tables.py
├── .github/
│   └── copilot-instructions.md  # AI assistant guidelines (slightly outdated)
├── pyproject.toml               # Python dependencies (uv)
├── uv.lock                      # Locked dependencies
├── docker-compose.yml           # Multi-service orchestration
├── Makefile                     # Development commands
├── .env.example                 # Environment template
├── README.md                    # Main documentation
├── QUICKSTART.md                # Quick start guide
└── MIGRATION.md                 # gRPC to FastAPI migration notes
```

### Key Files to Know

| File | Purpose | When to Modify |
|------|---------|----------------|
| `backend/src/server/fastapi_server.py` | All API endpoints | Adding/modifying API routes |
| `backend/src/models/recipe.py` | Recipe data models | Changing recipe structure |
| `backend/src/agents/recipe_agent.py` | Recipe generation logic | Improving recipe quality |
| `frontend/src/grpcClient.ts` | API client | Adding new API calls |
| `frontend/src/types.ts` | TypeScript types | Adding/changing data structures |
| `pyproject.toml` | Python dependencies | Adding Python packages |
| `frontend/package.json` | Frontend dependencies | Adding npm packages |
| `docker-compose.yml` | Service orchestration | Changing ports, environment |
| `.env` | Secrets and config | Never commit; use `.env.example` |

---

## Development Setup & Workflows

### Initial Setup

```bash
# Clone repository
git clone <repo-url>
cd SnapTop

# Set up environment
cp .env.example .env
# Edit .env and add GCP project ID

# Start all services (easiest method)
docker-compose up --build
# OR
make dev
```

**Services:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Package Management

**Backend (uv):**
```bash
# Install dependencies
uv sync

# Add new dependency
uv add package-name

# Run Python scripts
uv run python -m backend.src.server.fastapi_server

# Update dependencies
uv lock --upgrade
```

**Frontend (npm):**
```bash
cd frontend

# Install dependencies
npm install

# Add new dependency
npm install package-name

# Run dev server
npm run dev

# Build for production
npm run build
```

### Development Commands (Makefile)

```bash
make format    # Format changed Python files (ruff)
make fix       # Auto-fix linting issues
make lint      # Full lint check (format + fix + check)
make dev       # Start docker-compose
make test      # Run pytest
make clean     # Remove __pycache__, .pyc, etc.
```

**Note:** Linting is git-aware and only processes files changed from main branch.

### Running Services Individually

**Backend only:**
```bash
uv sync
uv run python -m backend.src.server.fastapi_server
# Runs on http://localhost:8000
```

**Frontend only:**
```bash
cd frontend
npm install
npm run dev
# Runs on http://localhost:3000
```

### Docker Workflow

```bash
# Start all services
docker-compose up --build

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Rebuild specific service
docker-compose build backend
docker-compose up backend

# Stop all services
docker-compose down

# Clean up volumes
docker-compose down -v
```

### Git Workflow

**Branch Strategy:**
- Feature branches start with `claude/`
- Main branch for production-ready code
- Always create PRs for review

**Committing Code:**
```bash
# Check status
git status

# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: add recipe modification endpoint"

# Push to remote
git push -u origin <branch-name>
```

**Commit Message Conventions:**
- `feat:` New features
- `fix:` Bug fixes
- `refactor:` Code restructuring
- `docs:` Documentation changes
- `test:` Test additions/changes
- `chore:` Maintenance tasks

---

## Architecture & Design Patterns

### Backend Architecture

#### FastAPI Server Pattern

**Location:** `backend/src/server/fastapi_server.py`

**Standard Endpoint Pattern:**
```python
@app.post("/api/resource/action", response_model=ResponseModel)
async def endpoint_name(request: RequestModel) -> ResponseModel:
    """
    Endpoint description for auto-generated docs.

    Args:
        request: Request model with required fields

    Returns:
        ResponseModel: Detailed response description
    """
    logger.info(f"Endpoint called with: {request.field}")

    try:
        # Business logic here
        result = process_request(request)
        return result
    except Exception as e:
        logger.error(f"Error in endpoint: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Descriptive error message: {str(e)}"
        )
```

**Current Endpoints:**

| Endpoint | Status | Method | Purpose |
|----------|--------|--------|---------|
| `/api/recipes/generate` | ✅ Production | POST | Generate new recipe |
| `/api/meals/generate-weekly` | 🚧 Stub | POST | Generate weekly meal plan |
| `/api/recipes/regenerate` | ❌ Not Implemented | POST | Regenerate existing recipe |
| `/api/recipes/modify` | ❌ Not Implemented | POST | Modify existing recipe |
| `/api/shopping-list/generate` | ❌ Not Implemented | POST | Generate shopping list |

#### LangGraph Agent Architecture

**Core Components:**
1. **System Prompt**: Defines agent role, constraints, output format
2. **LLM**: Gemini model (Flash for speed, Pro for quality)
3. **Tools**: LangChain-compatible functions for external data/actions
4. **Response Format**: Pydantic model ensures structured output
5. **Debug Mode**: Always enabled for observability

**Recipe Agent Flow:**

```python
# 1. Define system prompt
system_prompt = """
You are a highly skilled chef creating recipes.
Use recipe search tool for inspiration.
Use nutrition search tool for each ingredient.
Sum nutrition values for ALL ingredients.
CRITICAL: Nutrition must be for ENTIRE recipe, not per serving.
Output valid JSON matching Recipe schema.
"""

# 2. Get LLM with system prompt
llm = get_gemini_flash(system_prompt=system_prompt)

# 3. Create agent with tools and structured output
agent = create_agent(
    tools=[search_tool, fetch_url_content, get_nutrition],
    model=llm,
    debug=True,
    response_format=Recipe  # Pydantic model
)

# 4. Invoke agent
result = agent.invoke({
    "messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
})

# 5. Extract validated result
recipe = result["structured_response"]  # Already validated Pydantic model
```

**Agent Tool Pattern:**

```python
from langchain.tools import tool

@tool
def tool_name(param: str) -> dict:
    """
    Tool description that the LLM will see.
    Be very explicit about what this tool does and when to use it.

    Args:
        param: Parameter description

    Returns:
        dict: Return value description
    """
    try:
        # Implementation
        result = external_api_call(param)
        return result
    except Exception as e:
        logger.error(f"Tool error: {e}", exc_info=True)
        return {"error": str(e)}
```

### Frontend Architecture

#### Component Hierarchy

```
App.tsx (state container)
├── RecipeForm.tsx (input form)
│   ├── Basic inputs (description, complexity)
│   └── Advanced options (collapsible)
│       ├── Nutrition targets
│       └── Available ingredients
└── RecipeDisplay.tsx (recipe viewer)
    ├── Header (title, description, image)
    ├── Meta info (times, servings)
    ├── Grid layout
    │   ├── Ingredients list
    │   └── Nutrition facts (per serving)
    └── Instructions (sectioned, numbered)
```

#### State Management Pattern

**Simple useState in App.tsx:**
```typescript
function App() {
  const [recipe, setRecipe] = useState<Recipe | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (request: GenerateRecipeRequest) => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await generateRecipe(request);
      setRecipe(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return recipe
    ? <RecipeDisplay recipe={recipe} onBack={() => setRecipe(null)} />
    : <RecipeForm onSubmit={handleSubmit} isLoading={isLoading} />;
}
```

**No global state library needed** - simple prop drilling suffices for current complexity.

#### API Integration Pattern

**Case Conversion Layer:**

The frontend handles case conversion between JavaScript (camelCase) and Python (snake_case):

```typescript
// Request: camelCase → snake_case
const apiRequest = {
  description: request.description,
  complexity: request.complexity,
  target_macros: request.targetMacros ? {
    calories: request.targetMacros.calories,
    protein_grams: request.targetMacros.proteinGrams,
    carbs_grams: request.targetMacros.carbsGrams,
    fat_grams: request.targetMacros.fatGrams,
    // ... other fields
  } : undefined,
};

// Response: snake_case → camelCase
const recipe: Recipe = {
  recipeId: data.recipe_id,
  prepTimeMinutes: data.prep_time_minutes,
  cookTimeMinutes: data.cook_time_minutes,
  nutrition: {
    calories: data.nutrition.calories,
    proteinGrams: data.nutrition.protein_grams,
    carbsGrams: data.nutrition.carbs_grams,
    // ... other fields
  },
};
```

---

## Code Conventions

### Python Style Guide

**Naming Conventions:**
- `snake_case`: Functions, variables, module names
- `PascalCase`: Classes, Pydantic models, enums
- `UPPER_CASE`: Constants, enum values

**Type Hints (Modern Python 3.12+):**
```python
# Use built-in types (no typing imports needed)
def function(items: list[str], count: int | None = None) -> dict[str, int]:
    """Always include docstrings."""
    return {"count": len(items)}

# Pydantic models with Field descriptions
class Recipe(BaseModel):
    """Recipe data model."""

    recipe_id: str = Field(..., description="Unique identifier")
    title: str = Field(..., description="Recipe name")
    optional_field: str | None = Field(None, description="Optional value")
    servings: int = Field(default=4, description="Number of servings")
```

**Pydantic Best Practices:**
```python
from pydantic import BaseModel, Field

class MyModel(BaseModel):
    """Always include class docstring."""

    # Required fields use ... (ellipsis)
    required_field: str = Field(..., description="Clear description")

    # Optional fields use None default
    optional_field: str | None = Field(None, description="May be null")

    # Default values
    with_default: int = Field(default=10, description="Has default")

    # Nested models
    nested: OtherModel | None = Field(None, description="Nested object")

    # Arrays
    items: list[str] = Field(default_factory=list, description="List of items")
```

**Logging Pattern:**
```python
import logging

logger = logging.getLogger(__name__)

# Info logging
logger.info(f"Processing request: {request.id}")

# Error logging with traceback
try:
    result = dangerous_operation()
except Exception as e:
    logger.error(f"Operation failed: {e}", exc_info=True)
    raise
```

**GCP Secret Access:**
```python
from backend.src.common.utils import get_gcp_secret

# Always use Secret Manager for credentials
api_key = get_gcp_secret("secret-name", version="latest")
```

**Tool Definition Pattern:**
```python
from langchain.tools import tool

@tool
def my_tool(query: str, max_results: int = 10) -> dict:
    """
    Clear description for the LLM about what this tool does.

    The LLM will see this docstring, so be explicit about:
    - What the tool does
    - When to use it
    - What parameters mean
    - What the return value contains

    Args:
        query: What to search for
        max_results: Maximum number of results to return

    Returns:
        dict: Dictionary containing results and metadata
    """
    # Implementation
    return {"results": [...]}
```

**Caching Pattern for Tokens/Credentials:**
```python
# Module-level cache
_TOKEN_CACHE: str | None = None
_TOKEN_EXPIRY: int = 0

def get_token() -> str:
    """Get token with automatic refresh."""
    global _TOKEN_CACHE, _TOKEN_EXPIRY

    current_time = int(time.time())

    # Return cached token if still valid
    if _TOKEN_CACHE and _TOKEN_EXPIRY > current_time + 10:
        return _TOKEN_CACHE

    # Refresh token
    _TOKEN_CACHE = fetch_new_token()
    _TOKEN_EXPIRY = current_time + 3600

    return _TOKEN_CACHE
```

### TypeScript Style Guide

**Naming Conventions:**
- `camelCase`: Variables, functions, properties
- `PascalCase`: Interfaces, types, components
- `UPPER_CASE`: Constants

**Type Definitions:**
```typescript
// Interfaces for data structures
export interface Recipe {
  recipeId: string;
  title: string;
  description: string;
  // ... required fields first

  citations?: string[];  // Optional fields with ?
}

// Props interfaces
interface ComponentProps {
  recipe: Recipe;
  onSubmit: (data: Recipe) => void;
  isLoading?: boolean;
}

// Use const for enums when possible
const RecipeComplexity = {
  SIMPLE: 'simple',
  MEDIUM: 'medium',
  COMPLEX: 'complex',
} as const;

type ComplexityType = typeof RecipeComplexity[keyof typeof RecipeComplexity];
```

**Component Pattern:**
```typescript
import React, { useState } from 'react';
import { Recipe } from './types';

interface RecipeDisplayProps {
  recipe: Recipe;
  onBack: () => void;
}

const RecipeDisplay: React.FC<RecipeDisplayProps> = ({ recipe, onBack }) => {
  const [expanded, setExpanded] = useState(false);

  const handleClick = () => {
    setExpanded(!expanded);
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold">{recipe.title}</h1>
      {/* Component JSX */}
    </div>
  );
};

export default RecipeDisplay;
```

**API Client Pattern:**
```typescript
const API_BASE = 'http://localhost:8000';

export async function apiCall(request: RequestType): Promise<ResponseType> {
  try {
    const response = await fetch(`${API_BASE}/endpoint`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || `HTTP ${response.status}`);
    }

    const data = await response.json();
    return transformResponse(data);
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
}
```

**Tailwind CSS Conventions:**
```typescript
// Utility-first approach
className="w-full px-4 py-3 border border-gray-300 rounded-lg
           focus:ring-2 focus:ring-blue-500 transition"

// Responsive breakpoints
className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"

// Conditional classes
className={`btn ${isLoading ? 'opacity-50 cursor-not-allowed' : 'hover:bg-blue-700'}`}

// Color scheme: Blue primary, Gray neutral
className="bg-blue-600 hover:bg-blue-700 text-white"
className="bg-gray-100 border-gray-300 text-gray-700"
```

---

## Common Tasks

### Adding a New API Endpoint

**1. Define Pydantic Models (if needed):**

```python
# backend/src/models/requests.py
class NewFeatureRequest(BaseModel):
    """Request model for new feature."""

    field1: str = Field(..., description="Required field")
    field2: int | None = Field(None, description="Optional field")
```

```python
# backend/src/models/response.py (or appropriate model file)
class NewFeatureResponse(BaseModel):
    """Response model for new feature."""

    result: str = Field(..., description="Result data")
    metadata: dict = Field(default_factory=dict, description="Additional info")
```

**2. Export Models:**

```python
# backend/src/models/__init__.py
from .requests import NewFeatureRequest
from .response import NewFeatureResponse

__all__ = ["NewFeatureRequest", "NewFeatureResponse", ...]
```

**3. Add Endpoint:**

```python
# backend/src/server/fastapi_server.py
from backend.src.models import NewFeatureRequest, NewFeatureResponse

@app.post("/api/feature/action", response_model=NewFeatureResponse)
async def new_endpoint(request: NewFeatureRequest) -> NewFeatureResponse:
    """
    Endpoint description for API docs.

    Args:
        request: Input parameters

    Returns:
        NewFeatureResponse: Result data
    """
    logger.info(f"New endpoint called: {request.field1}")

    try:
        # Business logic
        result = process(request)
        return NewFeatureResponse(result=result)
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
```

**4. Add TypeScript Types:**

```typescript
// frontend/src/types.ts
export interface NewFeatureRequest {
  field1: string;
  field2?: number;
}

export interface NewFeatureResponse {
  result: string;
  metadata: Record<string, any>;
}
```

**5. Add API Client Function:**

```typescript
// frontend/src/grpcClient.ts
export async function callNewFeature(
  request: NewFeatureRequest
): Promise<NewFeatureResponse> {
  const apiRequest = {
    field1: request.field1,
    field2: request.field2,
  };

  const response = await fetch(`${API_BASE}/api/feature/action`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(apiRequest),
  });

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }

  const data = await response.json();
  return {
    result: data.result,
    metadata: data.metadata,
  };
}
```

**6. Use in Component:**

```typescript
// frontend/src/SomeComponent.tsx
import { callNewFeature } from './grpcClient';

const handleSubmit = async () => {
  try {
    const result = await callNewFeature({ field1: 'value' });
    console.log(result);
  } catch (error) {
    console.error('Error:', error);
  }
};
```

### Creating a New LangGraph Agent

**1. Create Agent File:**

```python
# backend/src/agents/new_agent.py
import logging
from langchain_core.messages import SystemMessage
from langchain.agents import create_agent
from backend.src.common.llms import get_gemini_flash
from backend.src.models import OutputModel

logger = logging.getLogger(__name__)

def create_new_agent():
    """Create and return the new agent."""

    system_prompt = """
    You are a specialized agent for [purpose].

    Guidelines:
    1. [Guideline 1]
    2. [Guideline 2]

    Output format: JSON matching OutputModel schema
    """

    # Get LLM
    llm = get_gemini_flash(system_prompt=system_prompt)

    # Create agent with tools
    agent = create_agent(
        tools=[tool1, tool2],
        model=llm,
        debug=True,
        response_format=OutputModel
    )

    return agent

def run_new_agent(user_input: str) -> OutputModel:
    """Run the agent with user input."""

    agent = create_new_agent()

    result = agent.invoke({
        "messages": [
            {"role": "user", "content": user_input}
        ]
    })

    return result["structured_response"]
```

**2. Create Agent Tools (if needed):**

```python
# backend/src/langgraph_tools/new_tool.py
from langchain.tools import tool
import logging

logger = logging.getLogger(__name__)

@tool
def new_tool(query: str) -> dict:
    """
    Tool description for the LLM.

    Args:
        query: What to search for

    Returns:
        dict: Results
    """
    try:
        # Implementation
        result = external_api_call(query)
        return result
    except Exception as e:
        logger.error(f"Tool error: {e}", exc_info=True)
        return {"error": str(e)}
```

**3. Wire to API Endpoint:**

```python
# backend/src/server/fastapi_server.py
from backend.src.agents.new_agent import run_new_agent

@app.post("/api/new-agent/execute")
async def execute_new_agent(request: NewAgentRequest) -> NewAgentResponse:
    """Execute the new agent."""

    try:
        result = run_new_agent(request.input)
        return result
    except Exception as e:
        logger.error(f"Agent error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
```

### Adding a New Python Dependency

```bash
# Add package
uv add package-name

# Add dev dependency
uv add --dev package-name

# Update lock file
uv lock

# Sync environment
uv sync
```

Update Docker image (if using docker-compose):
```bash
docker-compose build backend
docker-compose up backend
```

### Adding a New Frontend Dependency

```bash
cd frontend

# Add package
npm install package-name

# Add dev dependency
npm install --save-dev package-name
```

Update type definitions if needed:
```bash
npm install --save-dev @types/package-name
```

### Running Tests

```bash
# Run all tests
make test
# OR
pytest backend/src/tests/

# Run specific test file
pytest backend/src/tests/test_file.py

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=backend/src
```

**Test File Pattern:**

```python
# backend/src/tests/test_feature.py
import pytest
from backend.src.models import Recipe

def test_recipe_creation():
    """Test recipe model creation."""
    recipe = Recipe(
        recipe_id="test-123",
        title="Test Recipe",
        # ... required fields
    )
    assert recipe.title == "Test Recipe"

def test_api_endpoint():
    """Test API endpoint."""
    # Test implementation
    pass
```

---

## Critical Knowledge & Gotchas

### 🔴 CRITICAL: Nutrition Calculation Convention

**The Single Most Important Thing to Know:**

Backend agents calculate nutrition for the **ENTIRE recipe** (all servings combined), not per serving. The frontend divides by serving count to display per-serving values.

```python
# Backend Agent Output
Recipe(
    servings=4,
    nutrition=NutritionProfile(
        calories=2000,      # Total for ALL 4 servings
        protein_grams=140,  # Total for ALL 4 servings
        # ...
    )
)
```

```typescript
// Frontend Display
{Math.round(recipe.nutrition.calories / recipe.servings)}
// Shows: 500 calories per serving
```

**Why This Matters:**
- Agents must sum nutrition from ALL ingredients
- System prompts explicitly instruct agents on this
- Frontend calculations depend on this convention
- Violating this breaks nutrition display

**Agent System Prompt Must Include:**
```python
"IMPORTANT: The nutrition facts must be for the ENTIRE recipe (total for ALL servings), NOT per serving."
```

### Migration Context: gRPC → FastAPI

**Recently Completed Migration:**
- Old: gRPC + Envoy proxy
- New: FastAPI REST API
- Migration date: Recent (Q4 2024)

**Legacy Artifacts:**
- `frontend/src/grpcClient.ts` - **MISNAMED** (actually uses REST/fetch, not gRPC)
- `vite.config.ts` has unused gRPC proxy config
- Some documentation may reference gRPC

**What This Means:**
- If you see "gRPC" in code/docs, it's likely outdated
- The actual API is REST (JSON over HTTP)
- File names may be misleading (grpcClient.ts)

### Incomplete Features & TODOs

**Production Ready (✅):**
- Recipe generation endpoint
- Recipe agent with all tools
- Frontend form and display
- Image generation

**Partially Implemented (🚧):**
- Nutritionist agent exists but not wired to API
- `/api/meals/generate-weekly` returns stub data
- BigQuery schemas exist but persistence not implemented

**Not Implemented (❌):**
- `/api/recipes/regenerate` - returns 501
- `/api/recipes/modify` - returns 501
- `/api/shopping-list/generate` - returns 501
- Validation agent doesn't exist
- Recipe search/filtering
- User profile management

**When Working on These:**
1. Check if models already exist in `backend/src/models/`
2. Check if agents are partially implemented
3. Update status in README.md roadmap
4. Wire agents to API endpoints
5. Test thoroughly before marking complete

### Environment & Secrets

**DO:**
- Use `.env` file for local development
- Store secrets in GCP Secret Manager for production
- Use `get_gcp_secret()` helper function
- Add new secrets to `.env.example` (without values)

**DON'T:**
- Commit `.env` file
- Hardcode API keys in code
- Use print() for secrets (use logger)

**Required Secrets:**
```bash
# .env
GOOGLE_CLOUD_PROJECT=your-project-id

# GCP Secret Manager (access via get_gcp_secret())
# - google-cloud-api-key: Google Custom Search API key
# - recipe-search-id: Google Custom Search Engine ID
# - fat-secret-api-id: FatSecret OAuth credentials (JSON)
```

### Common Pitfalls

**1. Import Paths:**
```python
# ✅ Correct
from backend.src.models import Recipe
from backend.src.common.utils import get_gcp_secret

# ❌ Wrong
from models import Recipe  # Relative imports can break
```

**2. Docker Volume Mounting:**
- Frontend `node_modules` uses named volume
- Don't commit `frontend/node_modules` to git
- If packages aren't installing, rebuild: `docker-compose build --no-cache frontend`

**3. Port Conflicts:**
```bash
# If ports 3000 or 8000 are in use:
lsof -i :3000
lsof -i :8000

# Kill process or change ports in docker-compose.yml
```

**4. GCP Credentials:**
- Docker compose mounts `~/.config/gcloud/application_default_credentials.json`
- If missing, run: `gcloud auth application-default login`

**5. Case Conversion:**
- Python uses `snake_case` (protein_grams)
- TypeScript uses `camelCase` (proteinGrams)
- **ALWAYS** convert at API boundary in `grpcClient.ts`

---

## External Integrations

### Google Cloud Platform

**1. Vertex AI (LLM & Image Generation)**

**Models Available:**
- `gemini-2.0-flash-exp`: Fast, cost-effective (default for agents)
- `gemini-1.5-pro`: Higher quality, slower, more expensive
- `gemini-2.0-flash-lite`: Lightweight option
- `imagen-3.0-fast-generate-001`: Fast image generation (default)
- `imagen-3.0-generate-001`: Higher quality images

**Usage:**
```python
from backend.src.common.llms import get_gemini_flash, get_gemini_pro
from backend.src.common.img_generation_models import get_imagen_fast

# Get LLM
llm = get_gemini_flash(system_prompt="You are a chef...")

# Get image model
img_model = get_imagen_fast()
response = img_model.generate_images(
    prompt="Professional food photography...",
    aspect_ratio="1:1"
)
```

**Configuration:**
```python
import vertexai
vertexai.init(project=project_id, location="us-central1")
```

**2. Secret Manager**

**Purpose:** Store API keys and credentials securely

**Secrets:**
- `google-cloud-api-key`: Google Custom Search API
- `recipe-search-id`: Custom Search Engine ID
- `fat-secret-api-id`: FatSecret OAuth (JSON with client_id/client_secret)

**Usage:**
```python
from backend.src.common.utils import get_gcp_secret

api_key = get_gcp_secret("secret-name", version="latest")
credentials_json = get_gcp_secret("fat-secret-api-id", version="latest")
creds = json.loads(credentials_json)
```

**3. BigQuery (Schema Defined, Not Actively Used)**

**Dataset:** `mealprep`
**Tables:** `recipes`, `users`, `meal_plans`, `agent_logs`

**Schema Files:** `bigquery/*.sql`

**Usage (when implemented):**
```python
from google.cloud import bigquery

client = bigquery.Client(project=project_id)
table_id = f"{project_id}.mealprep.recipes"

# Insert recipe
errors = client.insert_rows_json(table_id, [recipe_dict])
```

### Nutrition APIs

**1. FatSecret Platform API (Primary)**

**Purpose:** Get nutrition info for ingredients

**Authentication:** OAuth2 Client Credentials flow

**Tool:** `get_nutrition(query: str) -> dict`

**Response Handling:**
```python
# Tolerant parsing - handles multiple response shapes
# Response can be:
# - {"foods": {"food": [...]}}  # Multiple results
# - {"foods": {"food": {...}}}  # Single result
# - {"foods": {}}               # No results
```

**Caching:**
```python
# OAuth token cached in memory
_FATSECRET_TOKEN = None
_FATSECRET_TOKEN_EXP = 0

# Token refreshed automatically when expired
# Reduces Secret Manager calls
```

**2. OpenFoodFacts (Defined, Not Used by Agents)**

**Purpose:** Alternative nutrition database

**Tool:** `search_openfoodfacts(query, max_results, page) -> list`

**Status:** Available but not currently used by recipe agent

### Search & Web APIs

**Google Custom Search API**

**Purpose:** Recipe search and inspiration

**Tool:** `search_tool` (LangChain Tool wrapper)

**Configuration:**
```python
from langchain_google_community import GoogleSearchAPIWrapper

search = GoogleSearchAPIWrapper(
    google_api_key=api_key,
    google_cse_id=cse_id,
    k=10  # Max results
)

# Tool returns top 3 results
```

**Usage by Agent:**
```python
# Agent uses tool to find recipes
search_tool.run("healthy pasta recipes")
# Returns: [{"title": "...", "link": "...", "snippet": "..."}, ...]
```

**Web Scraping (WebBaseLoader)**

**Purpose:** Fetch content from recipe URLs

**Tool:** `fetch_url_content(url: str) -> str`

**Usage:**
```python
from langchain_community.document_loaders import WebBaseLoader

@tool
def fetch_url_content(url: str) -> str:
    """Fetch and parse web page content."""
    loader = WebBaseLoader(url)
    docs = loader.load()
    return docs[0].page_content if docs else ""
```

**Agent Workflow:**
1. Search for recipes with `search_tool`
2. Pick promising URLs
3. Fetch content with `fetch_url_content`
4. Extract recipe ideas from content

---

## Testing & Quality

### Test Structure

**Location:** `backend/src/tests/`

**Configuration:** `pyproject.toml`
```toml
[tool.pytest.ini_options]
testpaths = ["backend/src/tests"]
pythonpath = [".", "src"]
```

**Current Status:**
- Test directory exists
- No test files currently present
- TODO: Add comprehensive test coverage

### Writing Tests

**Unit Test Pattern:**
```python
# backend/src/tests/test_models.py
import pytest
from backend.src.models import Recipe, Ingredient

def test_recipe_model():
    """Test Recipe model creation and validation."""
    recipe = Recipe(
        recipe_id="test-123",
        title="Test Recipe",
        description="A test recipe",
        ingredients=[],
        instructions=[],
        servings=4
    )

    assert recipe.title == "Test Recipe"
    assert recipe.servings == 4

def test_ingredient_validation():
    """Test Ingredient model validation."""
    with pytest.raises(ValueError):
        Ingredient(
            name="",  # Should fail - empty name
            quantity=1.0,
            unit="cup"
        )
```

**API Test Pattern:**
```python
# backend/src/tests/test_api.py
from fastapi.testclient import TestClient
from backend.src.server.fastapi_server import app

client = TestClient(app)

def test_generate_recipe_endpoint():
    """Test recipe generation endpoint."""
    response = client.post(
        "/api/recipes/generate",
        json={
            "description": "pasta dish",
            "complexity": "medium"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "recipe_id" in data
    assert "title" in data
```

**Agent Test Pattern:**
```python
# backend/src/tests/test_agents.py
import pytest
from backend.src.agents.recipe_agent import run_recipe_agent

@pytest.mark.slow  # Mark expensive API calls
def test_recipe_agent():
    """Test recipe agent generation."""
    result = run_recipe_agent(
        description="healthy pasta",
        complexity="medium"
    )

    assert result.title
    assert len(result.ingredients) > 0
    assert result.nutrition is not None
```

### Code Quality Tools

**Ruff (Linter & Formatter):**
```bash
# Format code
make format

# Fix linting issues
make fix

# Check (no changes)
make lint
```

**Git-Aware Linting:**
```makefile
# Only formats files changed from main
git diff --name-only --diff-filter=ACM main | grep '\.py$$'
```

### Code Review Checklist

**Before Committing:**
- [ ] Run `make lint` - all checks pass
- [ ] Run `make test` - all tests pass
- [ ] Add/update docstrings for new functions
- [ ] Add type hints to all parameters and return values
- [ ] Update models in both Python and TypeScript
- [ ] Test API endpoints with Swagger UI (`/docs`)
- [ ] Check error handling - no silent failures
- [ ] Update `.env.example` if new env vars added
- [ ] Update this CLAUDE.md if patterns changed

**API Changes:**
- [ ] Update Pydantic models
- [ ] Update TypeScript types
- [ ] Update API client in `grpcClient.ts`
- [ ] Test case conversion (snake_case ↔ camelCase)
- [ ] Update API documentation (docstrings)

**Agent Changes:**
- [ ] Test agent standalone before API integration
- [ ] Verify structured output matches Pydantic model
- [ ] Check system prompt clarity
- [ ] Test tool calls individually
- [ ] Verify debug output is useful

**Frontend Changes:**
- [ ] Test on mobile (responsive design)
- [ ] Check loading states
- [ ] Check error states
- [ ] Verify Tailwind classes work
- [ ] Check browser console for errors

---

## Deployment & Infrastructure

### Docker Configuration

**Backend Dockerfile:**
```dockerfile
FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-cache

# Copy application code
COPY backend/ ./backend/

# Run server
CMD ["uv", "run", "python", "-m", "backend.src.server.fastapi_server"]
```

**Frontend Setup (docker-compose):**
```yaml
frontend:
  image: node:20-slim
  working_dir: /app
  volumes:
    - ./frontend:/app
    - frontend_node_modules:/app/node_modules  # Named volume
  command: sh -c "npm install && npm run dev -- --host"
```

### Environment Variables

**Required:**
```bash
GOOGLE_CLOUD_PROJECT=your-project-id
```

**Optional (if not using Secret Manager):**
```bash
GOOGLE_SEARCH_API_KEY=xxx
GOOGLE_SEARCH_ENGINE_ID=xxx
FATSECRET_CLIENT_ID=xxx
FATSECRET_CLIENT_SECRET=xxx
```

### Ports

| Service | Port | Purpose |
|---------|------|---------|
| Frontend | 3000 | Vite dev server |
| Backend | 8000 | FastAPI server |

### GCP Setup

**Required Services:**
- Vertex AI API (enabled)
- Secret Manager API (enabled)
- BigQuery API (enabled)

**Authentication:**
```bash
# Local development
gcloud auth application-default login

# Docker (credentials mounted)
~/.config/gcloud/application_default_credentials.json:/app/gcp-credentials.json
```

**Project Structure:**
```
GCP Project: recipellm (or your project)
├── Secret Manager
│   ├── google-cloud-api-key
│   ├── recipe-search-id
│   └── fat-secret-api-id
├── Vertex AI
│   ├── Gemini models
│   └── Imagen models
└── BigQuery
    └── Dataset: mealprep
        ├── recipes
        ├── users
        ├── meal_plans
        └── agent_logs
```

### Makefile Commands Reference

```bash
make format    # Format Python code with ruff (git-aware)
make fix       # Auto-fix linting issues with ruff
make lint      # Full lint check (format + fix + check)
make dev       # Start docker-compose (all services)
make test      # Run pytest test suite
make clean     # Remove Python cache files
```

---

## Additional Resources

### Documentation Files

- **README.md**: Project overview and quick start
- **QUICKSTART.md**: Detailed setup instructions
- **MIGRATION.md**: gRPC to FastAPI migration notes
- **backend/README.md**: Backend-specific documentation
- **frontend/README.md**: Frontend-specific documentation
- **.github/copilot-instructions.md**: AI assistant guidelines (slightly outdated)

### API Documentation

- **Swagger UI**: http://localhost:8000/docs (interactive)
- **ReDoc**: http://localhost:8000/redoc (alternative)
- **OpenAPI Schema**: http://localhost:8000/openapi.json

### Key Dependencies Documentation

**Backend:**
- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/)
- [LangChain](https://python.langchain.com/)
- [LangGraph](https://langchain-ai.github.io/langgraph/)
- [Vertex AI](https://cloud.google.com/vertex-ai/docs)

**Frontend:**
- [React](https://react.dev/)
- [TypeScript](https://www.typescriptlang.org/)
- [Vite](https://vitejs.dev/)
- [Tailwind CSS](https://tailwindcss.com/)

---

## Version History

**Current Version:** 0.1.0

**Recent Changes:**
- Migrated from gRPC to FastAPI (Q4 2024)
- Added recipe generation with image support
- Implemented nutritionist agent (not yet wired)
- Added Docker Compose orchestration
- Switched to uv package manager

**TODO / Roadmap:**
- Wire nutritionist agent to API
- Implement recipe modification
- Implement shopping list generation
- Add BigQuery persistence
- Create validation agent
- Add user profile management
- Add recipe search/filtering

---

## Quick Reference

### File Naming
- Python: `snake_case.py`
- TypeScript: `PascalCase.tsx` (components), `camelCase.ts` (utilities)
- CSS: `kebab-case.css`

### Import Patterns
```python
# Python
from backend.src.models import Recipe
from backend.src.common.utils import get_gcp_secret
```

```typescript
// TypeScript
import { Recipe } from './types';
import { generateRecipe } from './grpcClient';
```

### Running Services
```bash
# All services
make dev

# Backend only
uv run python -m backend.src.server.fastapi_server

# Frontend only
cd frontend && npm run dev
```

### Common URLs
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

**Last Updated:** 2025-01-23

**Maintained By:** Development Team

**Questions?** Check the documentation files in the repository root, or consult the API documentation at `/docs`.
