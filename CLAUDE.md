# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

All development is done through Docker containers using the provided Makefile:

### Single Container Mode
- `make build` - Build the Docker image
- `make run` - Run the FastAPI server at http://localhost:8000 (Swagger UI at /docs)
- `make test` - Run pytest tests inside Docker container
- `make ping` - Run health check script

### Multi-Service Stack Mode
- `make stack-up` - Start full stack (FastAPI + MongoDB + Redis)
- `make stack-down` - Stop stack
- `make stack-logs` - Show logs from all services
- `make stack-build` - Build and start stack
- `make stack-test` - Run tests in stack environment
- `make stack-init-db` - Initialize database with sample data

### General
- `make help` - Display all available commands

The project uses no local Python installation - everything runs in containers.

## Architecture

This is a containerized FastAPI playground built on Alpine Linux for minimal footprint:

### Container Architecture
- Base: `andgineer/lean-python` (Alpine-based with uv package manager)
- Source code mounted as read-only volume from `src/` to `/app`
- Tests mounted from `tests/` to `/tests`
- Main application: `singularity.py` with FastAPI app
- Entry point: uvicorn server on port 8000

### Code Structure
- `src/singularity.py` - Simple FastAPI application with root endpoint
- `src/app_full.py` - Full-featured app with MongoDB and Redis connections
- `src/ping.py` - Simple health check utility
- `tests/test_singularity.py` - FastAPI test client tests
- `tests/conftest.py` - Test configuration that adds src/ and app/ to Python path

### Multi-Service Stack
The `docker-compose.yml` provides a complete development environment:
- **FastAPI app** - Runs `app_full.py` with database connectivity
- **MongoDB** - Document database with initialization scripts
- **Redis** - Cache and session storage
- **Nginx** - Reverse proxy (production profile)

Configuration files:
- `env.example` - Environment variables template
- `deploy-stack/init-db.sh` - Database initialization script
- `deploy-stack/nginx.conf` - Nginx reverse proxy configuration

### Dependencies
Uses `requirements.txt` with FastAPI, uvicorn, MongoDB (pymongo/motor), Redis, testing (pytest, httpx), and various utilities. Installed via uv package manager for speed.

## Testing

Tests use FastAPI's TestClient and are containerized. The conftest.py handles path setup to import modules from both `src/` and `app/` directories for container compatibility. Use `make stack-test` for testing with database services.
