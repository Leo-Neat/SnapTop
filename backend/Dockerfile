FROM python:3.12-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files first to leverage caching
COPY pyproject.toml uv.lock ./

# Install dependencies (cached if no change)
RUN uv sync --frozen

# Copy app code
COPY backend/ ./backend/
COPY bigquery/ ./bigquery/

# Environment setup
EXPOSE 8000

# Run FastAPI server with uvicorn
CMD ["uv", "run", "python", "-m", "backend.src.server.fastapi_server"]

