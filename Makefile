.PHONY: format fix lint clean dev test

# Python lint/format/fix only on changed and tracked Python files from main (exclude deleted)
CHANGED_PY_FILES=$(shell git diff --name-only main...HEAD | grep '\.py$$' | xargs -r git ls-files --error-unmatch 2>/dev/null | xargs)

format:
ifneq ($(strip $(CHANGED_PY_FILES)),)
	ruff format $(CHANGED_PY_FILES)
else
	@echo "No changed Python files to format."
endif

fix:
ifneq ($(strip $(CHANGED_PY_FILES)),)
	ruff check --fix $(CHANGED_PY_FILES)
else
	@echo "No changed Python files to fix."
endif

lint: format fix
ifneq ($(strip $(CHANGED_PY_FILES)),)
	ruff check $(CHANGED_PY_FILES)
else
	@echo "No changed Python files to lint."
endif

dev:
	@echo "Starting development environment..."
	docker-compose up --build

test:
	pytest backend/src/tests/

clean:
	@echo "Cleaning up generated files and caches..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true