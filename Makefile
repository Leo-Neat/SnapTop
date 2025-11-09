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
