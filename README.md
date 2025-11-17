
# AI Meal Prep System

## Project Overview
SnapTop is a multi-agent meal planning system designed to generate personalized weekly meal plans, recipes, nutritional analysis, and shopping lists. It features:
- Modular agent architecture (planner, nutritionist, chef, validator)
- gRPC API for frontend integration
- Persistent storage in Google Cloud BigQuery
- Human-in-the-loop approval and modification at every stage

## Monorepo Structure

```
snaptop/
├── backend/
│   ├── src/
│   ├── generated/
│   └── README.md
├── frontend/
│   ├── src/
│   ├── generated/
│   └── README.md
├── protos/
│   └── api/v1/
├── bigquery/
├── Makefile
├── README.md
```

- `backend/`: Python backend, agents, gRPC server, codegen outputs
- `frontend/`: Frontend code and generated proto models
- `protos/api/v1/`: Protocol Buffer schemas for API messages
- `bigquery/`: BigQuery table schemas and creation scripts
- `Makefile`: Build and codegen automation

## Quick Start & Project Setup

### 1. Clone the Repository
```bash
git clone <repo-url>
cd snaptop
```

### 2. Python Path Setup
To ensure all imports work, add the following to your shell rc file (`~/.bashrc` or `~/.zshrc`):
```bash
export PYTHONPATH="/absolute/path/to/snaptop:/absolute/path/to/snaptop/backend/generated:/absolute/path/to/snaptop/frontend/generated:$PYTHONPATH"
```
Replace `/absolute/path/to/snaptop` with the full path to your repo.
After editing, reload your shell:
```bash
source ~/.bashrc   # or source ~/.zshrc
```

### 3. Python Environment Setup
Install [uv](https://github.com/astral-sh/uv) and create a virtual environment:
```bash
pip install uv
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
uv pip install -r requirements.txt
# or if using pyproject.toml:
uv pip install
```

### 5. Build & Code Generation
Generate proto and Pydantic code for backend and frontend:
```bash
make protos
make pydantic-models
```

### 6. Run the Backend gRPC Server
Start the backend server (ensure your venv is active and PYTHONPATH is set):
```bash
uv run backend/src/server/grpc_server.py
# or
python backend/src/server/grpc_server.py
```
The server runs on port 50051 by default. Proto definitions are in `protos/api/v1/`.

### 7. Frontend Setup
See `frontend/README.md` for frontend instructions and codegen usage.

### 8. BigQuery Setup
See `bigquery/` for table schemas and setup scripts.

## More Information
- Backend implementation details: `backend/README.md`
- Frontend implementation details: `frontend/README.md`
- Protocol Buffers: `protos/api/v1/`
- BigQuery schemas: `bigquery/`
- Build/codegen: `Makefile`

