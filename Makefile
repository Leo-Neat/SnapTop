


PROTO_DIR=proto
PY_OUT=src/mealprep/proto
PYDANTIC_OUT=src/mealprep/pydantic_models.py
PYTHON=python3

protos: $(PROTO_DIR)/*.proto
	mkdir -p $(PY_OUT)
	$(PYTHON) -m grpc_tools.protoc \
		-I$(PROTO_DIR) \
		--python_out=$(PY_OUT) \
		--grpc_python_out=$(PY_OUT) \
		$(PROTO_DIR)/user.proto \
		$(PROTO_DIR)/recipe.proto \
		$(PROTO_DIR)/shopping.proto \
		$(PROTO_DIR)/meal_plan.proto

# Generate Pydantic models from all .proto files using protobuf-to-pydantic plugin
pydantic-models: protos
	for file in $(PROTO_DIR)/*.proto; do \
		$(PYTHON) -m grpc_tools.protoc -I$(PROTO_DIR) --protobuf-to-pydantic_out=$(PY_OUT) $$file; \
	done

clean:
	rm -rf $(PY_OUT)
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