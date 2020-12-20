# Project level Build rule defined here.


# Useful exported target
#	- gen_proto 			Compile all protos and generate the corresponding code. 
#	- fmt | format 			Format all code
#   - clean					Clean all generated code



# Root directory
DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

# API protos definitions
API_PROTOS = $(wildcard $(DIR)/proto/api/*.proto)

# Create API proto directory
gen_api_proto_dir:
	@ mkdir -p $(DIR)/web/proto

# Call protoc command to generate code
gen_proto: gen_api_proto_dir
	@ protoc \
	--go_out=$(DIR)/web/proto \
	--go_opt=paths=source_relative \
	--go-grpc_out=$(DIR)/web/proto \
	--go-grpc_opt=paths=source_relative \
	--proto_path=$(DIR)/proto \
	$(API_PROTOS)

# Clean generated proto code
clean_proto:
	@ rm -rf ${DIR}/web/proto

# Clean all
clean: clean_proto

# Format go source files
fmt_go:
	@ gofmt -w -s $(DIR)/web

# Format proto source files
fmt_proto:
	@ clang-format -style='Google' -i $(API_PROTOS)

# Format all
format: fmt_go fmt_proto

# Alias of format
fmt: format