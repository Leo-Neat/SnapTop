# Migration from gRPC to FastAPI

## Summary

The SnapTop application has been converted from gRPC + Protobuf to FastAPI + Pydantic + JSON. This simplifies the architecture by removing the need for:
- Protocol Buffer definitions and code generation
- Envoy proxy for gRPC-Web translation
- Complex build processes for proto files

## What Changed

### Backend
- **Server**: Replaced `grpc_server.py` with `fastapi_server.py`
- **Models**: Created Pydantic models in `backend/src/models/` to replace proto definitions
- **Port**: Changed from `50051` to `8000`
- **Protocol**: REST API with JSON instead of gRPC

### Frontend
- **Client**: Updated `grpcClient.ts` to use fetch API against REST endpoints
- **Endpoint**: Changed from `http://localhost:8080` (Envoy) to `http://localhost:8000` (FastAPI)
- **Protocol**: Simple HTTP/JSON instead of gRPC-Web

### Removed
- `/proto` directory - Proto definitions
- `/backend/generated` - Generated protobuf Python code
- `/frontend/generated` - Generated protobuf JavaScript code
- `/frontend/envoy.yaml` - Envoy proxy configuration
- `/frontend/Dockerfile.envoy` - Envoy container
- Envoy service from `docker-compose.yml`

### Updated
- `pyproject.toml` - Removed gRPC dependencies, added FastAPI and Uvicorn
- `package.json` - Removed grpc-web and google-protobuf
- `Makefile` - Removed proto generation targets
- `docker-compose.yml` - Removed envoy service, updated backend port

## API Endpoints

### FastAPI Server (Port 8000)

**Generate Recipe**
- `POST /api/recipes/generate`
- Request: `GenerateRecipeRequest`
- Response: `Recipe`
- Status: ✅ Fully implemented

**Generate Weekly Meals** (TODO)
- `POST /api/meals/generate-weekly`
- Request: `GenerateWeeklyMealsRequest`
- Response: `MealPlan`
- Status: ⚠️ Stub only

**Regenerate Recipe** (TODO)
- `POST /api/recipes/regenerate`
- Request: `RegenerateRecipeRequest`
- Response: `Recipe`
- Status: ⚠️ Not implemented

**Modify Recipe** (TODO)
- `POST /api/recipes/modify`
- Request: `ModifyRecipeRequest`
- Response: `Recipe`
- Status: ⚠️ Not implemented

**Get Shopping List** (TODO)
- `POST /api/shopping-list/generate`
- Request: `GetShoppingListRequest`
- Response: `ShoppingList`
- Status: ⚠️ Not implemented

## How to Run

### Using Docker Compose (Recommended)

```bash
# Start all services (backend + frontend)
docker-compose up --build

# Or use the Makefile
make dev
```

The services will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs (FastAPI auto-generated Swagger UI)

### Running Locally

**Backend:**
```bash
# Install dependencies
uv sync

# Run the server
uv run python -m backend.src.server.fastapi_server
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Benefits of FastAPI Migration

1. **Simpler Architecture**: No need for Envoy proxy or proto compilation
2. **Better Developer Experience**: Auto-generated API docs at `/docs`
3. **Easier Debugging**: JSON is human-readable, standard HTTP tools work
4. **Faster Iteration**: No proto generation step in build process
5. **Type Safety**: Pydantic provides runtime validation + Python type hints
6. **Modern Stack**: FastAPI is the current Python API framework standard

## Backward Compatibility

This is a breaking change. The old gRPC endpoints are no longer available. If you need the old gRPC server, it's still available at `backend/src/server/grpc_server.py` but is no longer maintained.
