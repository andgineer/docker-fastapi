import logging
import os
from contextlib import asynccontextmanager
from typing import Any, Dict

import redis.asyncio as redis
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for database connections
mongodb_client: AsyncIOMotorClient = None
redis_client: redis.Redis = None
database = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global mongodb_client, redis_client, database

    # MongoDB connection
    mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017/fastapi_db")
    mongodb_client = AsyncIOMotorClient(mongodb_url)
    database = mongodb_client.get_default_database()

    # Redis connection
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    redis_client = redis.from_url(redis_url, decode_responses=True)

    logger.info("Connected to databases")
    yield

    # Shutdown
    if mongodb_client:
        mongodb_client.close()
    if redis_client:
        await redis_client.close()
    logger.info("Disconnected from databases")


app = FastAPI(
    title=os.getenv("PROJECT_NAME", "FastAPI Playground"),
    version=os.getenv("VERSION", "1.0.0"),
    lifespan=lifespan,
)


@app.get("/")
async def read_root():
    return {"Hello": "World", "status": "running"}


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    health_status = {"status": "healthy", "services": {}}

    # Check MongoDB
    try:
        await mongodb_client.admin.command("ping")
        health_status["services"]["mongodb"] = "healthy"
    except Exception as e:
        health_status["services"]["mongodb"] = f"unhealthy: {str(e)}"
        health_status["status"] = "degraded"

    # Check Redis
    try:
        await redis_client.ping()
        health_status["services"]["redis"] = "healthy"
    except Exception as e:
        health_status["services"]["redis"] = f"unhealthy: {str(e)}"
        health_status["status"] = "degraded"

    return health_status


@app.get("/users")
async def get_users():
    """Get all users from MongoDB"""
    try:
        users = await database.users.find().to_list(length=100)
        # Convert ObjectId to string for JSON serialization
        for user in users:
            user["_id"] = str(user["_id"])
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/cache/{key}")
async def set_cache(key: str, value: Dict[str, Any]):
    """Set a value in Redis cache"""
    try:
        import json

        await redis_client.set(key, json.dumps(value), ex=3600)  # Expire in 1 hour
        return {"message": f"Cached {key} successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/cache/{key}")
async def get_cache(key: str):
    """Get a value from Redis cache"""
    try:
        import json

        value = await redis_client.get(key)
        if value is None:
            raise HTTPException(status_code=404, detail="Key not found")
        return {"key": key, "value": json.loads(value)}
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON in cache")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
