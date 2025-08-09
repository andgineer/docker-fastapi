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

# Multi-service stack with docker-compose
.HELP: stack-up  ## Start stack (FastAPI + MongoDB + Redis)
stack-up:
	docker-compose up -d

.HELP: stack-down  ## Stop stack
stack-down:
	docker-compose down

.HELP: stack-logs  ## Show logs from all services
stack-logs:
	docker-compose logs -f

.HELP: stack-build  ## Build and start stack
stack-build:
	docker-compose up -d --build

.HELP: stack-test  ## Run tests in stack environment
stack-test:
	docker-compose exec app pytest /tests

.HELP: stack-init-db  ## Initialize database with sample data
stack-init-db:
	./deploy-stack/init-db.sh

.HELP: help  ## Display this message
help:
	@grep -E \
		'^.HELP: .*?## .*$$' $(MAKEFILE_LIST) | \
		sort | \
		awk 'BEGIN {FS = ".HELP: |## "}; {printf "\033[36m%-19s\033[0m %s\n", $$2, $$3}'
