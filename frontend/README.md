# Recipe Generator Frontend

A modern, minimalist web application for generating recipes using AI, built with React, TypeScript, and Tailwind CSS.

## Features

- Clean, modern UI with Tailwind CSS
- Recipe generation form with optional advanced settings
- Nutrition targeting (calories, protein, carbs, fat)
- Ingredient availability specification
- Beautiful recipe display with step-by-step instructions
- Back button to generate more recipes

## Tech Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling
- **gRPC-web** - Backend communication via Envoy proxy

## Prerequisites

- Docker and Docker Compose (recommended)
- OR Node.js 18+ and npm (for local development)

## Quick Start

### Option 1: Using Docker Compose (Recommended)

The easiest way to run the entire stack (backend, Envoy, and frontend):

```bash
# From project root
docker-compose up
```

This starts:
- Backend gRPC server on port 50051
- Envoy proxy on port 8080
- Frontend dev server on port 3000

The application will be available at `http://localhost:3000`

### Option 2: Local Development

If you want to run the frontend locally while other services are in Docker:

#### 1. Start Backend and Envoy

```bash
# From project root
docker-compose up backend envoy
```

#### 2. Install Dependencies

```bash
# From frontend directory
npm install
```

#### 3. Start the Frontend Dev Server

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

### Option 3: Manual Setup (All Local)

For full local development without Docker Compose:

#### 1. Start the Backend

```bash
cd ../
python -m backend.src.server.grpc_server
```

#### 2. Start the Envoy Proxy

```bash
# From frontend directory
docker build -f Dockerfile.envoy -t recipe-envoy .
docker run -d -p 8080:8080 -p 9901:9901 --add-host=host.docker.internal:host-gateway recipe-envoy
```

The Envoy proxy will be available at:
- gRPC-web endpoint: `http://localhost:8080`
- Admin interface: `http://localhost:9901`

#### 3. Start the Frontend Dev Server

```bash
npm install
npm run dev
```

The application will be available at `http://localhost:3000`

## Development

### Project Structure

```
frontend/
├── src/
│   ├── App.tsx              # Main application component
│   ├── RecipeForm.tsx       # Recipe generation form
│   ├── RecipeDisplay.tsx    # Recipe display component
│   ├── grpcClient.ts        # gRPC client communication
│   ├── types.ts             # TypeScript type definitions
│   ├── main.tsx             # Application entry point
│   └── index.css            # Global styles with Tailwind
├── envoy.yaml               # Envoy proxy configuration
├── Dockerfile.envoy         # Envoy Docker image
├── vite.config.ts           # Vite configuration
├── tailwind.config.js       # Tailwind CSS configuration
└── package.json             # Dependencies and scripts
```

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

## How It Works

1. **User Input**: User fills out the recipe generation form with description, complexity, nutrition targets, and available ingredients
2. **Vite Proxy**: The frontend sends a request to `/grpc/*` which Vite proxies to the Envoy container
3. **Envoy Proxy**: Envoy translates the gRPC-web request to standard gRPC and forwards it to the backend container on port 50051
4. **Backend**: The gRPC server processes the request using the recipe agent and returns a Recipe proto
5. **Response**: Envoy translates the response back to gRPC-web and returns it through the proxy chain
6. **Display**: The frontend displays the recipe in a beautiful, easy-to-read format

**Docker Network Flow** (when using Docker Compose):
- Browser → `localhost:3000` → Frontend container
- Frontend → Vite proxy (`/grpc/*`) → Envoy container (`envoy:8080`)
- Envoy → Backend container (`backend:50051`)
- All containers communicate on the `recipe-network` Docker network

## Troubleshooting

### CORS Errors

If you see CORS errors, make sure the Envoy proxy is running and configured correctly. The `envoy.yaml` file includes CORS configuration.

### Connection Refused or 500 Errors

When using Docker Compose:
- Ensure all services are running: `docker-compose ps`
- Check service logs: `docker-compose logs -f frontend`, `docker-compose logs -f envoy`, `docker-compose logs -f backend`
- Verify network connectivity: `docker-compose exec frontend ping envoy`
- Restart services: `docker-compose restart`

When running locally:
- Ensure the backend gRPC server is running on port 50051
- Ensure the Envoy proxy is running on port 8080
- Check that Docker can access `host.docker.internal` (Linux users may need different setup)

### Recipe Not Generating

- Check the browser console for errors
- Verify the backend is running and accessible
- Check Envoy admin interface at `http://localhost:9901` for connection status
- Review backend logs for errors: `docker-compose logs -f backend`

### Vite Proxy Errors

If you see `ENOTFOUND envoy` or similar errors:
- When using Docker Compose, restart the containers: `docker-compose down && docker-compose up`
- Ensure the `vite.config.ts` proxy target is set to `http://envoy:8080` (Docker) or `http://localhost:8080` (local)
- Check that all services are on the same Docker network

## Production Build

To build for production:

```bash
npm run build
```

The built files will be in the `dist/` directory. You can serve them with any static file server or deploy to platforms like Vercel, Netlify, or AWS S3.

## License

ISC
