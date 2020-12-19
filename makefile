BLACK        := $(shell tput -Txterm setaf 0)
RED          := $(shell tput -Txterm setaf 1)
GREEN        := $(shell tput -Txterm setaf 2)
YELLOW       := $(shell tput -Txterm setaf 3)
LIGHTPURPLE  := $(shell tput -Txterm setaf 4)
PURPLE       := $(shell tput -Txterm setaf 5)
BLUE         := $(shell tput -Txterm setaf 6)
WHITE        := $(shell tput -Txterm setaf 7)

RESET := $(shell tput -Txterm sgr0)

# Root directory
DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

# API protos definitions
API_PROTOS = $(wildcard $(DIR)/proto/api/*.proto)

gen_api_proto_dir:
	@ mkdir -p $(DIR)/web/proto

gen_proto: gen_api_proto_dir
	@ echo "${GREEN}[Info]: Updating proto${RESET}"
	@ protoc \
	--go_out=$(DIR)/web/proto \
	--go_opt=paths=source_relative \
	--go-grpc_out=$(DIR)/web/proto \
	--go-grpc_opt=paths=source_relative \
	--proto_path=$(DIR)/proto \
	$(API_PROTOS) || (echo "${RED}[Error]: Updating failed${RESET}"; exit 1)
	@ echo "${GREEN}[Info]: Updating finished${RESET}"

clean_proto:
	@ rm -rf ${DIR}/web/proto

clean: clean_proto