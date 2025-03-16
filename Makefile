#!make

.HELP: build  ## Build docker image
build:
	docker build -t fastapi-playground .

.HELP: run  ## Run FastAPI server
run:
	docker run -it --rm -p 8000:8000 -v $$(PWD)/src:/app:ro fastapi-playground

.HELP: test  ## Test
test:
	docker run -it --rm -p 8000:8000 -v $$(PWD)/tests:/tests:ro -v $$(PWD)/src:/app:ro fastapi-playground -m pytest /tests

.HELP: ping  ## Run ping example (health check)
ping:
	docker run -it --rm -p 8000:8000 -v $$(PWD)/src:/app:ro fastapi-playground ping.py

.HELP: help  ## Display this message
help:
	@grep -E \
		'^.HELP: .*?## .*$$' $(MAKEFILE_LIST) | \
		sort | \
		awk 'BEGIN {FS = ".HELP: |## "}; {printf "\033[36m%-19s\033[0m %s\n", $$2, $$3}'
