# Recipe Generator - Quick Start Guide

This guide will help you get the Recipe Generator web application up and running.

## What's Included

- **Frontend**: Modern React + TypeScript web app with Tailwind CSS
- **Backend**: Python gRPC server with AI recipe generation
- **Proxy**: Envoy proxy for gRPC-web translation

## Prerequisites

- Docker and Docker Compose
- (Optional) Python 3.12+ and Node.js 18+ for local development

## Quick Start with Docker Compose (Recommended)

This is the easiest way to get everything running - all services in containers!

### 1. Set Up Environment

Make sure you have a `.env` file in the project root with your API keys and GCP credentials:

```bash
# Example .env (adjust as needed)
GOOGLE_CLOUD_PROJECT=your-project-id
# Add other necessary environment variables
```

### 2. Build and Start All Services

From the project root:

```bash
docker-compose build
docker-compose up
```

This will start:
- **Backend**: Python gRPC server on port 50051
- **Envoy**: gRPC-web proxy on port 8080
- **Frontend**: React dev server on port 3000

### 3. Access the Application

Open your browser and navigate to:
```
http://localhost:3000
```

### 4. View Logs

To see logs from all services:
```bash
docker-compose logs -f
```

To see logs from a specific service:
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f envoy
```

### 5. Stop Services

```bash
docker-compose down
```

## Alternative: Manual Local Development

If you prefer to run services locally without Docker:

### 1. Start the Backend

```bash
# Set up Python environment
python3 -m venv .venv
source .venv/bin/activate
pip install uv
uv sync

# Export PYTHONPATH
export PYTHONPATH="$(pwd):$(pwd)/backend/generated:$PYTHONPATH"

# Run the server
python -m backend.src.server.grpc_server
```

### 2. Start Envoy Proxy

```bash
cd frontend
docker build -f Dockerfile.envoy -t recipe-envoy .
docker run -d -p 8080:8080 -p 9901:9901 --add-host=host.docker.internal:host-gateway recipe-envoy
```

### 3. Start Frontend Dev Server

```bash
cd frontend
npm install
npm run dev
```

### 4. Access the Application

Open your browser and navigate to:
```
http://localhost:3000
```

## Using the Application

1. **Enter Recipe Description**: Describe what you'd like to make (e.g., "A healthy pasta dish with chicken")

2. **Set Complexity** (Optional): Choose Easy, Medium, or Hard

3. **Advanced Options** (Optional):
   - Set target nutrition values (calories, protein, carbs, fat)
   - Specify available ingredients you want to use

4. **Generate Recipe**: Click the "Generate Recipe" button

5. **View Recipe**: The AI-generated recipe will display with:
   - Recipe title and description
   - Ingredients list
   - Step-by-step instructions
   - Nutrition information
   - Prep and cook times

6. **Generate More**: Click "Generate Another Recipe" to go back and create more recipes

## Troubleshooting

### Services Not Starting
- Make sure Docker is running: `docker ps`
- Check if ports are already in use: `lsof -i :3000,8080,50051` (or `netstat -tuln`)
- View service logs: `docker-compose logs -f [service-name]`
- Rebuild containers: `docker-compose build --no-cache`

### Backend Errors
- Check backend logs: `docker-compose logs -f backend`
- Ensure `.env` file has correct GCP credentials
- Verify all required environment variables are set
- Restart backend: `docker-compose restart backend`

### Frontend Not Connecting
- Ensure all services are running: `docker-compose ps`
- Check frontend logs: `docker-compose logs -f frontend`
- Verify Envoy is running: `docker-compose logs -f envoy`
- Check browser console for errors
- Try rebuilding: `docker-compose build frontend && docker-compose up`

### Network Issues
- All services run on the same Docker network (`recipe-network`)
- Verify network exists: `docker network ls | grep recipe`
- Check service connectivity: `docker-compose exec frontend ping backend`

## Ports

- **3000**: Frontend development server
- **8080**: Envoy gRPC-web proxy
- **9901**: Envoy admin interface
- **50051**: Backend gRPC server

## Next Steps

- Customize the UI in `frontend/src/`
- Modify the recipe agent in `backend/src/agents/recipe_agent.py`
- Add more gRPC endpoints in `backend/src/server/grpc_server.py`

For more details, see:
- Frontend README: `frontend/README.md`
- Backend documentation: `backend/`
