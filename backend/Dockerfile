FROM python:3.12-slim AS builder

WORKDIR /app

# Install uv and build dependencies
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
RUN apt-get update && apt-get install -y --no-install-recommends \
    protobuf-compiler && rm -rf /var/lib/apt/lists/*

# Copy dependency files first to leverage caching
COPY pyproject.toml uv.lock ./

# Install dependencies (cached if no change)
RUN uv sync --frozen

# Copy proto files and generate code
COPY proto/ ./proto/

RUN mkdir -p backend/generated && \
    touch backend/generated/__init__.py && \
    uv run python -m grpc_tools.protoc \
        -Iproto \
        --python_out=backend/generated \
        --grpc_python_out=backend/generated \
        proto/*.proto && \
    uv run python -m protobuf_to_pydantic \
        --input proto \
        --output backend/generated

# --- Runtime image ---
FROM python:3.12-slim

WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files and sync environment
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

# Copy generated proto files from builder
COPY --from=builder /app/backend/generated /app/backend/generated

# Copy app code last (changes often)
COPY backend/ ./backend/
COPY bigquery/ ./bigquery/

# Environment setup
EXPOSE 50051

# Explicitly set PYTHONPATH when running the command
CMD ["sh", "-c", "PYTHONPATH=/app:/app/backend/generated exec uv run python -m backend.src.server.grpc_server"]

