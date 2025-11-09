
PROTO_DIR=proto
PY_OUT=src/mealprep/proto

PYTHON=python3

protos: $(PROTO_DIR)/*.proto
	mkdir -p $(PY_OUT)
	$(PYTHON) -m grpc_tools.protoc \
		-I$(PROTO_DIR) \
		--python_out=$(PY_OUT) \
		--grpc_python_out=$(PY_OUT) \
		$(PROTO_DIR)/user.proto \
		$(PROTO_DIR)/recipe.proto \
		$(PROTO_DIR)/shopping.proto

clean:
	rm -rf $(PY_OUT)

# Python lint/format only on changed files from main
CHANGED_PY_FILES=$(shell git diff --name-only main...HEAD | grep '\.py$$' | xargs)

lint:
ifdef CHANGED_PY_FILES
	ruff check $(CHANGED_PY_FILES)
else
	echo "No changed Python files to lint."
endif

format:
ifdef CHANGED_PY_FILES
	ruff format $(CHANGED_PY_FILES)
else
	echo "No changed Python files to format."
endif

fix:
ifdef CHANGED_PY_FILES
	ruff check --fix $(CHANGED_PY_FILES)
else
	echo "No changed Python files to fix."
endif