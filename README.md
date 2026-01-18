[![Build Status](https://github.com/andgineer/docker-fastapi/workflows/CI/badge.svg)](https://github.com/andgineer/docker-fastapi/actions)

# Lightweight FastAPI docker-compose Playground with MongoDB, and Redis on Alpine Linux

- Lightweight Alpine-based docker compose setup for high-performance FastAPI development
- MongoDB integration
- OpenSSL for secure communications
- [uv](https://github.com/astral-sh/uv) package manager for optimized dependency management
- Alpine Linux base for minimal image size
- Nothing installed locally, everything is in the container

## Build

Place all necessary requirements in the `requirements.txt` file.

    make build

## Run FastAPI server

What will run is set in `Dockerfile`'s `CMD` command

    make run

Voilà! Your FastAPI server is up and running at http://localhost:8000/
Swagger UI is available at http://localhost:8000/docs

## Run ping example (health check)

    make ping

## Multi-Service Stack

For a full-featured development environment with MongoDB, Redis, and Nginx:

### Quick Start

1. Start the complete stack:
   ```bash
   make stack-up
   ```

2. Initialize database with sample data:
   ```bash
   make stack-init-db
   ```

3. Access the application:
   - FastAPI: http://localhost:8000/
   - API documentation: http://localhost:8000/docs
   - Health check: http://localhost:8000/health
   - Sample endpoints: http://localhost:8000/users, http://localhost:8000/cache/test

### Stack Commands

- `make stack-up` - Start all services (FastAPI + MongoDB + Redis)
- `make stack-down` - Stop all services
- `make stack-logs` - View logs from all services
- `make stack-build` - Rebuild and start services
- `make stack-test` - Run tests with database connections
- `make stack-init-db` - Initialize MongoDB with sample data

### Services

- **FastAPI app** - Main application with database connectivity (`src/app_full.py`)
- **MongoDB** - Document database on port 27017
- **Redis** - Cache and session storage on port 6379
- **Nginx** - Reverse proxy (production mode: `docker-compose --profile production up`)

### Configuration

Copy `env.example` to `.env` and customize environment variables as needed.

### Database Access

**Default MongoDB credentials:**
- Username: `admin`
- Password: `password`
- Database: `fastapi_db`
- Connection URL: `mongodb://admin:password@localhost:27017/fastapi_db?authSource=admin`

**Direct MongoDB access:**
```bash
# Connect to MongoDB shell
docker-compose exec mongo mongosh -u admin -p password --authenticationDatabase admin

# Or with connection string
docker-compose exec mongo mongosh "mongodb://admin:password@localhost:27017/fastapi_db?authSource=admin"
```

**Redis access:**
```bash
# Connect to Redis CLI
docker-compose exec redis redis-cli
```
