# SnapTop - AI Meal Prep System

An intelligent meal planning system that generates personalized recipes, weekly meal plans, nutritional analysis, and shopping lists using AI agents powered by LangGraph and Google Cloud.

## 🌟 Features

- **AI Recipe Generation**: Create custom recipes based on dietary preferences, available ingredients, and nutritional goals
- **Multi-Agent Architecture**: Specialized AI agents for meal planning, nutrition analysis, recipe creation, and validation
- **Nutritional Tracking**: Automatic calculation of macros and nutritional information for entire recipes
- **Recipe Image Generation**: AI-generated images for every recipe
- **Modern Web Interface**: Clean, responsive UI built with React and TypeScript
- **REST API**: FastAPI backend with automatic OpenAPI documentation

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Documentation](#documentation)
- [Development](#development)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)

## 🚀 Quick Start

### Using Docker Compose (Recommended)

The easiest way to run the entire application:

```bash
# Clone the repository
git clone <repo-url>
cd snaptop

# Set up environment variables
cp .env.example .env
# Edit .env and add your API keys

# Start all services
docker-compose up --build

# Or use the Makefile
make dev
```

**Access the application:**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs (Interactive Swagger UI)

### Local Development

See [QUICKSTART.md](./QUICKSTART.md) for detailed instructions on running locally without Docker.

## 🏗️ Architecture

### Project Structure

```
snaptop/
├── backend/                 # Python FastAPI backend
│   ├── src/
│   │   ├── models/         # Pydantic data models
│   │   ├── server/         # FastAPI server
│   │   ├── agents/         # AI agents (Chef, Planner, etc.)
│   │   ├── langgraph_tools/# LangGraph tools and utilities
│   │   └── common/         # Shared utilities
│   ├── Dockerfile
│   └── README.md           # Backend-specific documentation
├── frontend/               # React + TypeScript frontend
│   ├── src/
│   │   ├── RecipeForm.tsx
│   │   ├── RecipeDisplay.tsx
│   │   └── grpcClient.ts   # API client (renamed, now uses REST)
│   ├── package.json
│   └── README.md           # Frontend-specific documentation
├── bigquery/               # BigQuery schemas and scripts
├── docker-compose.yml      # Multi-service orchestration
├── Makefile               # Development commands
├── pyproject.toml         # Python dependencies
├── QUICKSTART.md          # Quick start guide
└── MIGRATION.md           # gRPC → FastAPI migration guide
```

### Technology Stack

**Backend:**
- Python 3.12+
- FastAPI - Modern web framework
- Pydantic - Data validation
- LangGraph - AI agent orchestration
- LangChain - LLM integration
- Google Cloud (Vertex AI, BigQuery, Secret Manager)

**Frontend:**
- React 18
- TypeScript
- Vite - Build tool
- Tailwind CSS - Styling

**Infrastructure:**
- Docker & Docker Compose
- uv - Fast Python package manager

### AI Agents

The system uses specialized AI agents:

1. **Chef Agent**: Generates recipes using web search and nutrition APIs
2. **Meal Planner**: Creates weekly meal plans based on user preferences (TODO)
3. **Nutritionist**: Allocates macro targets per meal (TODO)
4. **Validator**: Checks recipes against constraints and user preferences (TODO)

## 📚 Documentation

- **[QUICKSTART.md](./QUICKSTART.md)** - Get up and running quickly
- **[backend/README.md](./backend/README.md)** - Backend development guide
- **[frontend/README.md](./frontend/README.md)** - Frontend development guide
- **[MIGRATION.md](./MIGRATION.md)** - Migration from gRPC to FastAPI

## 🛠️ Development

### Prerequisites

- **Docker & Docker Compose** (for containerized development)
- **Python 3.12+** (for local backend development)
- **Node.js 18+** (for local frontend development)
- **uv** (Python package manager) - `pip install uv`

### Development Commands

```bash
# Code quality (Python)
make format          # Format Python code
make fix            # Auto-fix linting issues
make lint           # Run full lint check

# Development
make dev            # Start all services with Docker Compose
make test           # Run tests
make clean          # Clean up generated files and caches
```

### Running Services Individually

**Backend:**
```bash
cd snaptop
uv sync                          # Install dependencies
uv run python -m backend.src.server.fastapi_server
# Server runs on http://localhost:8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
# App runs on http://localhost:3000
```

### Environment Variables

Create a `.env` file in the project root:

```bash
# Google Cloud
GOOGLE_CLOUD_PROJECT=your-project-id

# API Keys (stored in GCP Secret Manager)
# Add other necessary environment variables
```

## 📖 API Documentation

### REST Endpoints

The FastAPI backend provides the following endpoints:

**Recipe Generation:**
- `POST /api/recipes/generate` - Generate a new recipe ✅
  - Input: Recipe description, complexity, nutrition targets, available ingredients
  - Output: Complete recipe with ingredients, instructions, nutrition, and AI-generated image

**Meal Planning:** (TODO - Currently stubs)
- `POST /api/meals/generate-weekly` - Generate weekly meal plan
- `POST /api/recipes/regenerate` - Regenerate an existing recipe
- `POST /api/recipes/modify` - Modify an existing recipe
- `POST /api/shopping-list/generate` - Generate shopping list

**Interactive Documentation:**
Visit http://localhost:8000/docs for the full interactive API documentation (Swagger UI).

### Example API Request

```bash
curl -X POST "http://localhost:8000/api/recipes/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "A healthy pasta dish with chicken and vegetables",
    "complexity": "medium",
    "target_macros": {
      "calories": 500,
      "protein_grams": 35,
      "carbs_grams": 45,
      "fat_grams": 15
    }
  }'
```

## 🧪 Testing

Run the test suite:

```bash
# Using make
make test

# Or directly with pytest
pytest backend/src/tests/
```

## 🔧 Troubleshooting

### Services Not Starting

```bash
# Check if ports are in use
lsof -i :3000,8000

# View service logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Rebuild containers
docker-compose build --no-cache
docker-compose up
```

### Backend Errors

- Check backend logs: `docker-compose logs -f backend`
- Verify `.env` file has correct GCP credentials
- Ensure all required environment variables are set

### Frontend Not Connecting

- Verify backend is running: `curl http://localhost:8000/`
- Check browser console for errors
- Ensure both services are on the same Docker network

## 🗺️ Roadmap

- [x] Recipe generation with AI
- [x] FastAPI REST API
- [x] AI-generated recipe images
- [x] Nutrition calculation per serving
- [ ] Weekly meal planning
- [ ] Shopping list generation
- [ ] User profile management
- [ ] Recipe modification and regeneration
- [ ] BigQuery data persistence
- [ ] Recipe search and filtering

## 📄 License

ISC

## 🤝 Contributing

See [QUICKSTART.md](./QUICKSTART.md) for development setup instructions.

## 📞 Support

For issues and questions:
- Review the [QUICKSTART.md](./QUICKSTART.md) guide
- Check the [MIGRATION.md](./MIGRATION.md) if you're familiar with the old gRPC version
- Review API docs at http://localhost:8000/docs

---

**Note:** This project was recently migrated from gRPC to FastAPI. See [MIGRATION.md](./MIGRATION.md) for details on the architectural changes.
