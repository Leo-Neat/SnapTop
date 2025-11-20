
# SnapTop - AI Meal Prep System

## Project Overview
SnapTop is a multi-agent meal planning system designed to generate personalized weekly meal plans, recipes, nutritional analysis, and shopping lists. It features:
- Modular agent architecture (planner, nutritionist, chef, validator)
- FastAPI REST API with Pydantic models
- Persistent storage in Google Cloud BigQuery
- Human-in-the-loop approval and modification at every stage

## Monorepo Structure

```
snaptop/
├── backend/
│   ├── src/
│   │   ├── models/          # Pydantic data models
│   │   ├── server/          # FastAPI server
│   │   ├── agents/          # AI agents
│   │   └── langgraph_tools/ # LangGraph tools
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── RecipeForm.tsx
│   │   ├── RecipeDisplay.tsx
│   │   └── grpcClient.ts    # API client
│   └── package.json
├── bigquery/                # BigQuery schemas
├── Makefile
├── docker-compose.yml
└── pyproject.toml
```

- `backend/`: Python FastAPI backend with AI agents
- `frontend/`: React + TypeScript frontend
- `bigquery/`: BigQuery table schemas and creation scripts
- `Makefile`: Linting, formatting, and development commands

## Quick Start

### Using Docker Compose (Recommended)

```bash
# Start all services
docker-compose up --build

# Or use the Makefile
make dev
```

Services will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (interactive Swagger UI)

### Local Development

#### Backend

```bash
# Install uv if you don't have it
pip install uv

# Install dependencies
uv sync

# Run the server
uv run python -m backend.src.server.fastapi_server
```

Backend runs on http://localhost:8000

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on http://localhost:3000

## API Endpoints

- `POST /api/recipes/generate` - Generate a new recipe (✅ working)
- `POST /api/meals/generate-weekly` - Generate weekly meal plan (stub)
- `POST /api/recipes/regenerate` - Regenerate a recipe (stub)
- `POST /api/recipes/modify` - Modify a recipe (stub)
- `POST /api/shopping-list/generate` - Generate shopping list (stub)

See http://localhost:8000/docs for full interactive API documentation.

## Development

### Code Quality

```bash
# Format Python code
make format

# Fix Python linting issues
make fix

# Run full lint check
make lint
```

### Testing

```bash
make test
```

## Migration from gRPC

This project was recently migrated from gRPC to FastAPI. See [MIGRATION.md](./MIGRATION.md) for details.

## More Information

- Backend implementation: `backend/README.md`
- Frontend implementation: `frontend/README.md`
- Migration guide: `MIGRATION.md`
- BigQuery schemas: `bigquery/`

