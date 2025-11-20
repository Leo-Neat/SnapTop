# Backend README

## Overview
This backend implements a multi-agent meal planning system using LangGraph, LangChain, and Google Cloud. It generates personalized weekly meal plans, recipes, nutritional analysis, and shopping lists. The backend exposes a REST API via FastAPI for a web frontend, with all persistent data stored in Google Cloud BigQuery.

## Architecture
- **Agents:**
  - Meal Planner: Proposes meal ideas based on user profile and requirements
  - Nutritionist: Allocates macro targets per meal, ensuring weekly goals are met
  - Chef: Generates recipes using web search, FatSecret nutrition API, and fetches web content for inspiration
  - Validator: Checks recipes against user constraints, equipment, macros, and clarity with feedback loops to Chef
- **State Management:**
  - LangGraph maintains state across workflow stages and human checkpoints
  - Intermediate agent outputs are stored for rollback/debugging
- **API Endpoints (FastAPI REST):**
  - `POST /api/recipes/generate` - Generate recipe (✅ fully working)
  - `POST /api/meals/generate-weekly` - Generate weekly meal plan (stub)
  - `POST /api/recipes/regenerate` - Regenerate recipe (stub)
  - `POST /api/recipes/modify` - Modify recipe (stub)
  - `POST /api/shopping-list/generate` - Generate shopping list (stub)
  - Interactive API docs available at http://localhost:8000/docs

## Key Directories & Files
- `backend/src/models/`: Pydantic data models for recipes, users, meal plans, shopping lists
- `backend/src/server/`: FastAPI server implementation
- `backend/src/langgraph_tools/`: Modular tools for agents (nutrition, search, fetch, GCP secrets)
- `backend/src/agents/`: Agent implementations (e.g., `recipe_agent.py`)
- `backend/src/common/`: Shared backend utilities
- `bigquery/`: Table schemas and creation scripts for Google BigQuery
- `Makefile`: Linting, formatting, and development commands
- `pyproject.toml`: Python dependencies for uv/PEP 621

## Setup & Developer Workflow

### 1. Environment Setup
Install [uv](https://github.com/astral-sh/uv):
```bash
pip install uv
```

Create a Python virtual environment (recommended):
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies
Install all project dependencies using uv:
```bash
uv sync
```

### 3. Code Quality
Lint changed Python files:
```bash
make lint
```

Format changed Python files:
```bash
make format
```

Auto-fix linting issues:
```bash
make fix
```

### 4. Running Agents & Tools
Run agents/tools (example):
```bash
uv run backend/src/agents/recipe_agent.py
```

### 5. Running the FastAPI Server

#### Option A: Using Docker (Recommended)

The easiest way to run the backend is with Docker Compose:

```bash
# From project root
docker-compose up --build

# Or just the backend
docker-compose up backend
```

The backend will start on port 8000. API docs: http://localhost:8000/docs

#### Option B: Running Locally

To start the FastAPI server locally for development:

1. Ensure your Python environment is activated and dependencies are installed
2. Run the server:
   ```bash
   uv run python -m backend.src.server.fastapi_server
   # or, if your venv is active:
   python -m backend.src.server.fastapi_server
   ```
3. The server will start on port 8000 by default
4. Access API docs at http://localhost:8000/docs

### 6. Cloud Credentials
Set up GCP credentials and Secret Manager for API keys. Ensure you have a `.env` file with:
```bash
GOOGLE_CLOUD_PROJECT=your-project-id
```

## Tooling & Cloud Integration
- **Nutrition Tool:** Uses FatSecret API, credentials managed via GCP Secret Manager
- **Recipe Search Tool:** Uses Google Custom Search API, API key managed via GCP Secret Manager
- **Fetch URL Tool:** Retrieves and parses web content for recipe inspiration
- **Image Generation:** Uses AI to generate recipe images
- **GCP Secret Manager:** All sensitive API keys and credentials are fetched securely at runtime

## Example: Running the Recipe Agent
```python
from backend.src.agents.recipe_agent import agent, system_prompt

result = agent.invoke({
    "messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Create a healthy pasta dish with chicken"}
    ]
})
recipe = result["structured_response"]
print(recipe.model_dump_json(indent=2))
```

## Pydantic Models
All data models are defined using Pydantic in `backend/src/models/`:
- `Recipe`: Full recipe with ingredients, instructions, nutrition
- `UserProfile`: User preferences, dietary restrictions, kitchen equipment
- `MealPlan`: Weekly meal planning structure
- `ShoppingList`: Aggregated shopping items

Example Recipe model:
```python
class Recipe(BaseModel):
    recipe_id: str
    title: str
    description: str
    ingredients: list[Ingredient]
    instructions: list[InstructionSection]
    prep_time_minutes: int
    cook_time_minutes: int
    nutrition: NutritionProfile | None
    servings: int
    serving_size: str | None
    citations: list[str] | None
    image_base64: str | None
```

## BigQuery Table Creation
See `bigquery/` for table schemas and a Python script to create tables from SQL files using the Google Cloud BigQuery API.

## Testing & Integration Tests
Run all integration tests:
```bash
pytest backend/src/tests/
```

Example integration tests:
- `tests/integration/langgraph_tools/get_nutrition_integration_test.py`: Validates FatSecret nutrition API tool
- `tests/integration/langgraph_tools/recipe_search_integration_test.py`: Validates recipe search and web content fetching
- `tests/integration/common/llm_integration_test.py`: Validates Gemini LLM integration

## Security & Compliance
- All API keys and credentials are managed via GCP Secret Manager
- User data is encrypted at rest in BigQuery
- HTTPS/TLS for secure communication
- PII and dietary/health data handled per compliance requirements

## Migration from gRPC

This project was recently migrated from gRPC to FastAPI. See [MIGRATION.md](../MIGRATION.md) for details about the conversion.
