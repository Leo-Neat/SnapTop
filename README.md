# AI Meal Prep System

## Overview
This repo implements a multi-agent meal planning system using LangGraph, LangChain, and Google Cloud. It generates personalized weekly meal plans, recipes, nutritional analysis, and shopping lists. The backend exposes a gRPC API for a web frontend, with all persistent data stored in Google Cloud BigQuery.

## Architecture
- **Agents:**
  - Meal Planner: Proposes meal ideas based on user profile and requirements.
  - Nutritionist: Allocates macro targets per meal, ensuring weekly goals are met.
  - Chef: Generates recipes using web search, FatSecret nutrition API, and fetches web content for inspiration.
  - Validator: Checks recipes against user constraints, equipment, macros, and clarity. Feedback loops to Chef.
- **State Management:**
  - LangGraph maintains state across workflow stages and human checkpoints.
  - Intermediate agent outputs are stored for rollback/debugging.
- **API Endpoints (gRPC):**
  - `GenerateWeeklyMeals`, `RegenerateRecipe`, `ModifyRecipe`, `GetShoppingList`.
  - All endpoints stream progress and support human-in-the-loop modifications.

## Key Directories & Files
- `src/mealprep/proto/`: Protocol Buffer schemas for user, recipe, and shopping list messages.
- `src/langgraph_tools/`: Modular tools for agents (nutrition, search, fetch, GCP secrets).
- `src/agents/`: Agent implementations (e.g., `recipe_agent.py`).
- `src/server/`: gRPC server implementation.
- `bigquery/`: Table schemas and creation scripts for Google BigQuery.
- `Makefile`: Build and proto code generation commands.
- `pyproject.toml`: Python dependencies for uv/PEP 621.

## Setup & Developer Workflow


### 0. Python Path Setup
- Before running any code, export the root directory of this repo **and** the proto output directory to your PYTHONPATH to ensure imports work:
  ```bash
  export PYTHONPATH="$(pwd):$(pwd)/src/mealprep/proto:$PYTHONPATH"
  ```
- To avoid repeating this step, add the following line to your `~/.bashrc` or `~/.zshrc`:
  ```bash
  export PYTHONPATH="/path/to/your/repo:/path/to/your/repo/src/mealprep/proto:$PYTHONPATH"
  ```
  Replace `/path/to/your/repo` with the absolute path to this repository.

### 1. Environment Setup
- Install [uv](https://github.com/astral-sh/uv):
  ```bash
  pip install uv
  # or follow uv docs for your platform
  ```
- Create a Python virtual environment (recommended):
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 2. Install Dependencies
- Install all project dependencies using uv:
  ```bash
  uv pip install -r requirements.txt
  # or if using pyproject.toml:
  uv pip install
  ```

### 3. Build & Code Generation
- If your virtual environment is not active, prefix Makefile commands with `uv run`:
  ```bash
  uv run make protos
  uv run make pydantic-models
  uv run make lint
  uv run make format
  uv run make fix
  ```
- If your venv is active, you can use `make ...` directly:
  ```bash
  make protos
  make pydantic-models
  make lint
  make format
  make fix
  ```

### 4. Code Quality
- Lint changed Python files:
  ```bash
  make lint
  ```
- Format changed Python files:
  ```bash
  make format
  ```
- Auto-fix linting issues:
  ```bash
  make fix
  ```

### 5. Running Agents & Tools
- Run agents/tools (example):
  ```bash
  uv run src/agents/recipe_agent.py
  ```

### 6. Running the gRPC Server Locally

To start the MealPrep gRPC server locally:

1. Ensure your Python environment is activated and dependencies are installed (see Setup above).
2. Export your PYTHONPATH as described above.
3. Run the server:
   ```bash
   uv run src/server/grpc_server.py
   # or, if your venv is active:
   python src/server/grpc_server.py
   ```
4. The server will start on port 50051 by default.

You can connect to it using any gRPC client, using the proto definitions in `src/mealprep/proto/`.

### 7. Cloud Credentials
- Set up GCP credentials and Secret Manager for API keys as described in the cloud integration section.

## Tooling & Cloud Integration
- **Nutrition Tool:** Uses FatSecret API, credentials managed via GCP Secret Manager.
- **Recipe Search Tool:** Uses Google Custom Search API, API key managed via GCP Secret Manager.
- **Fetch URL Tool:** Retrieves and parses web content for recipe inspiration.
- **GCP Secret Manager:** All sensitive API keys and credentials are fetched securely at runtime.

## Example: Running the Recipe Agent
```python
from src.agents.recipe_agent import agent
result = agent.invoke({
    "messages": [
        {"role": "system", "content": "You are a highly skilled chef..."},
        {"role": "user", "content": "Create a new recipe for chocolate cake but use chickpeas. Show me the nutrition info of the new recipe"}
    ]
})
print(result)
```

## Protocol Buffer Schemas
See `src/mealprep/proto/` for full schemas. Example (Recipe):
```proto
message Recipe {
  string recipe_id = 1;
  string title = 2;
  string description = 3;
  repeated Ingredient ingredients = 4;
  repeated InstructionSection instructions = 5;
  int32 prep_time_minutes = 6;
  int32 cook_time_minutes = 7;
  NutritionProfile nutrition = 8;
  int32 servings = 9;
  string serving_size = 10;
  repeated string citations = 11;
}
```

## BigQuery Table Creation
See `bigquery/` for table schemas and a Python script to create tables from SQL files using the Google Cloud BigQuery API.

## Testing & Integration Tests
- Run all integration tests: `pytest tests/integration`
- Example integration tests:
  - `tests/integration/src/langgraph_tools/get_nutrition_integration_test.py`: Validates FatSecret nutrition API tool (see `src/langgraph_tools/nutrition.py`)
  - `tests/integration/src/langgraph_tools/recipe_search_integration_test.py`: Validates recipe search and web content fetching
  - `tests/integration/src/common/llm_integration_test.py`: Validates Gemini LLM integration

## Security & Compliance
- All API keys and credentials are managed via GCP Secret Manager
- User data is encrypted at rest in BigQuery
- gRPC uses TLS for secure communication
- PII and dietary/health data handled per compliance requirements

## Conventions
- Recipes must cite sources and match user dietary/equipment constraints
- Macro targets must be met within tolerance
- Human-in-the-loop: Users can approve, modify, or regenerate meal plans/recipes at any stage

## TODO List
- [ ] Implement gRPC API server
  - Create Python gRPC server with endpoints: GenerateWeeklyMeals, RegenerateRecipe, ModifyRecipe, GetShoppingList. Use proto definitions in proto/ and ensure streaming and human-in-the-loop support.
- [ ] Wire agents to API endpoints
  - Connect LangGraph agents (planner, nutritionist, chef, validator) to gRPC API logic. Ensure agent outputs are correctly mapped to proto messages and BigQuery storage.
- [ ] BigQuery integration for persistence
  - Implement logic to store and retrieve users, recipes, meal plans, and agent logs in BigQuery. Use schemas in bigquery/ and ensure encryption and versioning.
- [ ] Human-in-the-loop approval flow
  - Implement user approval/modification checkpoints in agent workflow. Ensure API streams progress and allows user intervention at each stage.
- [ ] Agent feedback and validation loop
  - Ensure validation failures return actionable feedback and trigger recipe regeneration. Log agent decisions for debugging.
- [ ] API authentication and security
  - Add authentication for API endpoints, enforce TLS, and handle PII per compliance requirements.
- [ ] End-to-end test suite
  - Create integration tests for API endpoints, agent workflows, and BigQuery persistence. Validate functional requirements and error handling.
- [ ] Explore deep agent architecture for Chef agent
  - Research and prototype a deep agent (multi-step, multi-tool, reasoning) for the Chef role to improve recipe generation and adaptation.
- [ ] Implement Nutritionist, Validator, and Meal Planner agents
  - Build dedicated agents for nutrition allocation, recipe validation, and meal planning. Integrate with LangGraph and ensure modularity.

---
## Running the gRPC Server Locally

To start the MealPrep gRPC server locally:

1. Ensure your Python environment is activated and dependencies are installed (see Setup above).
2. Export your PYTHONPATH as described above.
3. Run the server:
  ```bash
  uv run src/server/grpc_server.py
  # or, if your venv is active:
  python src/server/grpc_server.py
  ```
4. The server will start on port 50051 by default.

You can connect to it using any gRPC client, using the proto definitions in `proto/`.
### 0. Python Path Setup
- Before running any code, export the root directory of this repo to your PYTHONPATH to ensure imports work:
  ```bash
  export PYTHONPATH="$(pwd):$PYTHONPATH"
  ```
- To avoid repeating this step, add the following line to your `~/.bashrc` or `~/.zshrc`:
  ```bash
  export PYTHONPATH="/path/to/your/repo:$PYTHONPATH"
  ```
  Replace `/path/to/your/repo` with the absolute path to this repository.
# AI Meal Prep System

## TODO List
- [ ] Implement gRPC API server
  - Create Python gRPC server with endpoints: GenerateWeeklyMeals, RegenerateRecipe, ModifyRecipe, GetShoppingList. Use proto definitions in proto/ and ensure streaming and human-in-the-loop support.
- [ ] Wire agents to API endpoints
  - Connect LangGraph agents (planner, nutritionist, chef, validator) to gRPC API logic. Ensure agent outputs are correctly mapped to proto messages and BigQuery storage.
- [ ] BigQuery integration for persistence
  - Implement logic to store and retrieve users, recipes, meal plans, and agent logs in BigQuery. Use schemas in bigquery/ and ensure encryption and versioning.
- [ ] Human-in-the-loop approval flow
  - Implement user approval/modification checkpoints in agent workflow. Ensure API streams progress and allows user intervention at each stage.
- [ ] Agent feedback and validation loop
  - Ensure validation failures return actionable feedback and trigger recipe regeneration. Log agent decisions for debugging.
- [ ] API authentication and security
  - Add authentication for API endpoints, enforce TLS, and handle PII per compliance requirements.
- [ ] End-to-end test suite
  - Create integration tests for API endpoints, agent workflows, and BigQuery persistence. Validate functional requirements and error handling.
- [ ] Explore deep agent architecture for Chef agent
  - Research and prototype a deep agent (multi-step, multi-tool, reasoning) for the Chef role to improve recipe generation and adaptation.
- [ ] Implement Nutritionist, Validator, and Meal Planner agents
  - Build dedicated agents for nutrition allocation, recipe validation, and meal planning. Integrate with LangGraph and ensure modularity.

## Overview
This repo implements a multi-agent meal planning system using LangGraph, LangChain, and Google Cloud. It generates personalized weekly meal plans, recipes, nutritional analysis, and shopping lists. The backend exposes a gRPC API for a web frontend, with all persistent data stored in Google Cloud BigQuery.

## Architecture
- **Agents:**
  - Meal Planner: Proposes meal ideas based on user profile and requirements.
  - Nutritionist: Allocates macro targets per meal, ensuring weekly goals are met.
  - Chef: Generates recipes using web search, FatSecret nutrition API, and fetches web content for inspiration.
  - Validator: Checks recipes against user constraints, equipment, macros, and clarity. Feedback loops to Chef.
- **State Management:**
  - LangGraph maintains state across workflow stages and human checkpoints.
  - Intermediate agent outputs are stored for rollback/debugging.
- **API Endpoints (gRPC):**
  - `GenerateWeeklyMeals`, `RegenerateRecipe`, `ModifyRecipe`, `GetShoppingList`.
  - All endpoints stream progress and support human-in-the-loop modifications.

## Key Directories & Files
- `proto/`: Protocol Buffer schemas for user, recipe, and shopping list messages.
- `src/langgraph_tools/`: Modular tools for agents (nutrition, search, fetch, GCP secrets).
- `src/agents/`: Agent implementations (e.g., `recipe_agent.py`).
- `bigquery/`: Table schemas and creation scripts for Google BigQuery.
- `Makefile`: Build and proto code generation commands.
- `pyproject.toml`: Python dependencies for uv/PEP 621.

## Tooling & Cloud Integration
- **Nutrition Tool:** Uses FatSecret API, credentials managed via GCP Secret Manager.
- **Recipe Search Tool:** Uses Google Custom Search API, API key managed via GCP Secret Manager.
- **Fetch URL Tool:** Retrieves and parses web content for recipe inspiration.
- **GCP Secret Manager:** All sensitive API keys and credentials are fetched securely at runtime.

## Example: Running the Recipe Agent
```python
from src.agents.recipe_agent import agent
result = agent.invoke({
    "messages": [
        {"role": "system", "content": "You are a highly skilled chef..."},
        {"role": "user", "content": "Create a new recipe for chocolate cake but use chickpeas. Show me the nutrition info of the new recipe"}
    ]
})
print(result)
```

## Protocol Buffer Schemas
See `proto/` for full schemas. Example (Recipe):
```proto
message Recipe {
  string recipe_id = 1;
  string title = 2;
  string description = 3;
  repeated Ingredient ingredients = 4;
  repeated InstructionSection instructions = 5;
  int32 prep_time_minutes = 6;
  int32 cook_time_minutes = 7;
  NutritionProfile nutrition = 8;
  int32 servings = 9;
  string serving_size = 10;
  repeated string citations = 11;
}
```

## BigQuery Table Creation
See `bigquery/` for table schemas and a Python script to create tables from SQL files using the Google Cloud BigQuery API.

## Setup & Developer Workflow

### 1. Environment Setup
- Install [uv](https://github.com/astral-sh/uv):
  ```bash
  pip install uv
  # or follow uv docs for your platform
  ```
- Create a Python virtual environment (recommended):
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 2. Install Dependencies
- Install all project dependencies using uv:
  ```bash
  uv pip install -r requirements.txt
  # or if using pyproject.toml:
  uv pip install
  ```


### 3. Build & Code Generation
- If your virtual environment is not active, prefix Makefile commands with `uv run`:
  ```bash
  uv run make protos
  uv run make pydantic-models
  uv run make lint
  uv run make format
  uv run make fix
  ```
- If your venv is active, you can use `make ...` directly:
  ```bash
  make protos
  make pydantic-models
  make lint
  make format
  make fix
  ```

### 4. Code Quality
- Lint changed Python files:
  ```bash
  make lint
  ```
- Format changed Python files:
  ```bash
  make format
  ```
- Auto-fix linting issues:
  ```bash
  make fix
  ```

### 5. Running Agents & Tools
- Run agents/tools (example):
  ```bash
  uv run src/agents/recipe_agent.py
  ```

### 6. Cloud Credentials
- Set up GCP credentials and Secret Manager for API keys as described in the cloud integration section.

## Testing & Integration Tests
- Run all integration tests: `pytest tests/integration`
- Example integration tests:
  - `tests/integration/src/langgraph_tools/get_nutrition_integration_test.py`: Validates FatSecret nutrition API tool (see `src/langgraph_tools/nutrition.py`)
  - `tests/integration/src/langgraph_tools/recipe_search_integration_test.py`: Validates recipe search and web content fetching
  - `tests/integration/src/common/llm_integration_test.py`: Validates Gemini LLM integration

## Security & Compliance
- All API keys and credentials are managed via GCP Secret Manager
- User data is encrypted at rest in BigQuery
- gRPC uses TLS for secure communication
- PII and dietary/health data handled per compliance requirements

## Conventions
- Recipes must cite sources and match user dietary/equipment constraints
- Macro targets must be met within tolerance
- Human-in-the-loop: Users can approve, modify, or regenerate meal plans/recipes at any stage

---
For more details, see code comments and individual module documentation.


