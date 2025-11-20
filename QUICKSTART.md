# SnapTop Quick Start Guide

Get the SnapTop AI Recipe Generator up and running in minutes.

## What You're Running

- **Backend**: FastAPI server with AI recipe generation (port 8000)
- **Frontend**: React web application (port 3000)

## Prerequisites

Choose one:
- **Docker & Docker Compose** (easiest, recommended)
- **Python 3.12+ & Node.js 18+** (for local development)

## Quick Start (Docker)

### 1. Set Up Environment

Create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your credentials
GOOGLE_CLOUD_PROJECT=your-project-id
```

### 2. Start Everything

```bash
# Start all services
docker-compose up --build

# Or use the Makefile
make dev
```

That's it! The application is now running.

### 3. Access the Application

Open your browser:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 4. Generate Your First Recipe

1. Go to http://localhost:3000
2. Enter a recipe description (e.g., "healthy chicken pasta")
3. Optionally set complexity and nutrition targets
4. Click "Generate Recipe"
5. Wait for the AI to create your recipe!

### 5. Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## Local Development (Without Docker)

### Backend

```bash
# Install Python dependencies
pip install uv
uv sync

# Run the FastAPI server
uv run python -m backend.src.server.fastapi_server
```

Backend runs on http://localhost:8000

### Frontend

```bash
# Install Node dependencies
cd frontend
npm install

# Run the dev server
npm run dev
```

Frontend runs on http://localhost:3000

## Using the Application

### Basic Recipe Generation

1. **Description**: Enter what you want to make
   - Example: "A healthy pasta dish with chicken"

2. **Complexity** (Optional): Choose difficulty level
   - Easy, Medium, or Hard

3. **Click Generate**: Wait for the AI to work its magic!

### Advanced Options

Click "Show Advanced Options" to specify:

**Target Nutrition (per serving):**
- Calories: e.g., 500
- Protein: e.g., 35g
- Carbs: e.g., 45g
- Fat: e.g., 15g

**Available Ingredients:**
- Add ingredients you have on hand
- The AI will try to incorporate them

## Troubleshooting

### Services Not Starting

**Check if ports are in use:**
```bash
lsof -i :3000,8000
```

**View service logs:**
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

**Rebuild from scratch:**
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### Backend Errors

**Check backend is running:**
```bash
curl http://localhost:8000/
```

**View detailed backend logs:**
```bash
docker-compose logs -f backend
```

**Common issues:**
- Missing `.env` file → Create one with your GCP credentials
- Invalid API keys → Check your `.env` configuration
- Port 8000 in use → Stop other services or change the port

### Frontend Not Connecting

**Check browser console:**
- Press F12 in your browser
- Look for errors in the Console tab
- Check Network tab for failed requests

**Verify backend is accessible:**
```bash
curl http://localhost:8000/
```

**Common issues:**
- Backend not running → Start the backend first
- CORS errors → Check backend CORS configuration
- Port 3000 in use → Change the port in vite.config.ts

### Recipe Generation Fails

**Test the API directly:**
```bash
curl -X POST http://localhost:8000/api/recipes/generate \
  -H "Content-Type: application/json" \
  -d '{
    "description": "pasta with chicken",
    "complexity": "easy"
  }'
```

**Check for errors:**
- Review backend logs: `docker-compose logs -f backend`
- Verify GCP credentials are correct
- Ensure all required API keys are in `.env`

## Environment Variables

Create a `.env` file in the project root:

```bash
# Required
GOOGLE_CLOUD_PROJECT=your-gcp-project-id

# Optional (if not using GCP Secret Manager)
GOOGLE_SEARCH_API_KEY=your-api-key
FATSECRET_API_KEY=your-api-key
```

## Ports

- **3000**: Frontend (React app)
- **8000**: Backend (FastAPI server)

## Next Steps

**Explore the API:**
- Visit http://localhost:8000/docs for interactive API documentation
- Try different endpoints and request parameters

**Customize:**
- Modify the UI in `frontend/src/`
- Adjust the AI agent in `backend/src/agents/recipe_agent.py`
- Add new API endpoints in `backend/src/server/fastapi_server.py`

**Learn More:**
- [Main README](./README.md) - Project overview and architecture
- [Backend README](./backend/README.md) - Backend development guide
- [Frontend README](./frontend/README.md) - Frontend development guide
- [Migration Guide](./MIGRATION.md) - gRPC to FastAPI migration details

## Development Commands

```bash
# Start all services
make dev

# Format Python code
make format

# Lint Python code
make lint

# Run tests
make test

# Clean up
make clean
```

## Getting Help

**Documentation:**
- Check [README.md](./README.md) for detailed information
- Review [API docs](http://localhost:8000/docs) for endpoint details
- See [MIGRATION.md](./MIGRATION.md) if you used the old gRPC version

**Debugging:**
- Enable debug logging in the backend
- Check browser console for frontend errors
- Review Docker logs for service issues

---

**Happy Cooking! 🍳**
