[![Docker Automated build](https://img.shields.io/docker/image-size/andgineer/fastapi)](https://hub.docker.com/r/andgineer/fastapi)
[![Docker Automated build](https://img.shields.io/docker/image-size/andgineer/fastapi)](https://hub.docker.com/r/andgineer/fastapi)

# FastAPI Docker Container

Lightweight Alpine-based [Docker Container](https://hub.docker.com/r/andgineer/fastapi)
with FastAPI and MongoDB support.

## Features

- FastAPI for high-performance API development
- MongoDB integration
- OpenSSL for secure communications
- [uv](https://github.com/astral-sh/uv) package manager for optimized dependency management
- Alpine Linux base for minimal image size

## Quick Start

```bash
docker run -it --rm -v $PWD/example:/app:ro andgineer/fastapi ping.py
```

## Run FastAPI server

```bash
docker run -it --rm -v $PWD/example:/app:ro -p 8000:8000 andgineer/fastapi -m uvicorn singularity:app  --host 0.0.0.0
```

Voila! Your FastAPI server is up and running at http://localhost:8000/
