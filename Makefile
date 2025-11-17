


PROTO_DIR=proto
PY_OUT=src/mealprep/proto
PYDANTIC_OUT=src/mealprep/pydantic_models.py

PYTHON=python3

.DEFAULT_GOAL := pydantic-models


BACKEND_GEN=backend/generated
FRONTEND_GEN=frontend/generated

protos: $(PROTO_DIR)/*.proto
	mkdir -p $(BACKEND_GEN)
	mkdir -p $(FRONTEND_GEN)
	$(PYTHON) -m grpc_tools.protoc \
		-I$(PROTO_DIR) \
		--python_out=$(BACKEND_GEN) \
		--grpc_python_out=$(BACKEND_GEN) \
		$(PROTO_DIR)/user.proto \
		$(PROTO_DIR)/recipe.proto \
		$(PROTO_DIR)/shopping.proto \
		$(PROTO_DIR)/meal_plan.proto \
		$(PROTO_DIR)/mealprep_service.proto
	$(PYTHON) -m grpc_tools.protoc \
		-I$(PROTO_DIR) \
		--python_out=$(FRONTEND_GEN) \
		--grpc_python_out=$(FRONTEND_GEN) \
		$(PROTO_DIR)/user.proto \
		$(PROTO_DIR)/recipe.proto \
		$(PROTO_DIR)/shopping.proto \
		$(PROTO_DIR)/meal_plan.proto \
		$(PROTO_DIR)/mealprep_service.proto

# Generate Pydantic models from all .proto files using protobuf-to-pydantic plugin
PYDANTIC_BACKEND=$(BACKEND_GEN)
PYDANTIC_FRONTEND=$(FRONTEND_GEN)

pydantic-models: protos
	for file in $(PROTO_DIR)/*.proto; do \
		$(PYTHON) -m grpc_tools.protoc -I$(PROTO_DIR) --protobuf-to-pydantic_out=$(PYDANTIC_BACKEND) $$file; \
		$(PYTHON) -m grpc_tools.protoc -I$(PROTO_DIR) --protobuf-to-pydantic_out=$(PYDANTIC_FRONTEND) $$file; \
	done

clean:
	rm -rf $(PY_OUT)
	rm -rf $(BACKEND_GEN)
	rm -rf $(FRONTEND_GEN)
	rm -f $(PYDANTIC_OUT)

# Python lint/format/fix only on changed and tracked Python files from main (exclude deleted)
CHANGED_PY_FILES=$(shell git diff --name-only main...HEAD | grep '\.py$$' | xargs -r git ls-files --error-unmatch 2>/dev/null | xargs)



format:
ifneq ($(strip $(CHANGED_PY_FILES)),)
	ruff format $(CHANGED_PY_FILES)
else
	echo "No changed Python files to format."
endif


fix:
ifneq ($(strip $(CHANGED_PY_FILES)),)
	ruff check --fix $(CHANGED_PY_FILES)
else
	echo "No changed Python files to fix."
endif

lint: format fix
ifneq ($(strip $(CHANGED_PY_FILES)),)
	ruff check $(CHANGED_PY_FILES)
else
	echo "No changed Python files to lint."
endif