[![Build Status](https://github.com/andgineer/docker-fastapi/workflows/CI/badge.svg)](https://github.com/andgineer/docker-fastapi/actions)

# FastAPI Docker-based Playground

- Lightweight Alpine-based container with FastAPI for high-performance API development
- MongoDB integration
- OpenSSL for secure communications
- [uv](https://github.com/astral-sh/uv) package manager for optimized dependency management
- Alpine Linux base for minimal image size
- Nothing installed locally, everything is in the container

## Build

Place all necessary requirements in `requirements.txt` file.

    make build

## Run FastAPI server

What will run is set in `Dockerfile`'s `CMD` command

    make run

Voila! Your FastAPI server is up and running at http://localhost:8000/
And Swagger UI is available at http://localhost:8000/docs

## Run ping example (health check)

    make ping
