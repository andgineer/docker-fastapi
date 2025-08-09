import json
import logging
import os
from contextlib import asynccontextmanager
from typing import Any

import redis.asyncio as redis
from fastapi import Depends, FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseManager:
    def __init__(self) -> None:
        self.mongodb_client: AsyncIOMotorClient | None = None
        self.redis_client: redis.Redis | None = None
        self.database: Any = None

    async def connect(self) -> None:
        # MongoDB connection
        mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017/fastapi_db")
        self.mongodb_client = AsyncIOMotorClient(mongodb_url)
        self.database = self.mongodb_client.get_default_database()

        # Redis connection
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.redis_client = redis.from_url(redis_url, decode_responses=True)

        logger.info("Connected to databases")

    async def disconnect(self) -> None:
        if self.mongodb_client:
            self.mongodb_client.close()
        if self.redis_client:
            await self.redis_client.close()
        logger.info("Disconnected from databases")


db_manager = DatabaseManager()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Startup
    await db_manager.connect()
    yield
    # Shutdown
    await db_manager.disconnect()


def get_db_manager() -> DatabaseManager:
    return db_manager


# Module-level dependency to satisfy B008 linter warning
db_dependency = Depends(get_db_manager)

app = FastAPI(
    title=os.getenv("PROJECT_NAME", "FastAPI Playground"),
    version=os.getenv("VERSION", "1.0.0"),
    lifespan=lifespan,
)


@app.get("/")
async def read_root():
    return {"Hello": "World", "status": "running"}


@app.get("/health")
async def health_check(db: DatabaseManager = db_dependency):
    """Health check endpoint for monitoring"""
    health_status: dict[str, Any] = {"status": "healthy", "services": {}}

    # Check MongoDB
    if db.mongodb_client is None:
        health_status["services"]["mongodb"] = "unhealthy: not connected"
        health_status["status"] = "degraded"
    else:
        try:
            await db.mongodb_client.admin.command("ping")
            health_status["services"]["mongodb"] = "healthy"
        except PyMongoError as e:
            health_status["services"]["mongodb"] = f"unhealthy: {str(e)}"
            health_status["status"] = "degraded"

    # Check Redis
    if db.redis_client is None:
        health_status["services"]["redis"] = "unhealthy: not connected"
        health_status["status"] = "degraded"
    else:
        try:
            await db.redis_client.ping()
            health_status["services"]["redis"] = "healthy"
        except redis.RedisError as e:
            health_status["services"]["redis"] = f"unhealthy: {str(e)}"
            health_status["status"] = "degraded"

    return health_status


@app.get("/users")
async def get_users(db: DatabaseManager = db_dependency):
    """Get all users from MongoDB"""
    if db.database is None:
        raise HTTPException(status_code=503, detail="Database not connected")

    try:
        users = await db.database.users.find().to_list(length=100)
        # Convert ObjectId to string for JSON serialization
        for user in users:
            user["_id"] = str(user["_id"])
        return {"users": users}
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/cache/{key}")
async def set_cache(key: str, value: dict[str, Any], db: DatabaseManager = db_dependency):
    """Set a value in Redis cache"""
    if db.redis_client is None:
        raise HTTPException(status_code=503, detail="Redis not connected")

    try:
        await db.redis_client.set(key, json.dumps(value), ex=3600)  # Expire in 1 hour
        return {"message": f"Cached {key} successfully"}
    except redis.RedisError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/cache/{key}")
async def get_cache(key: str, db: DatabaseManager = db_dependency):
    """Get a value from Redis cache"""
    if db.redis_client is None:
        raise HTTPException(status_code=503, detail="Redis not connected")

    try:
        value = await db.redis_client.get(key)
        if value is None:
            raise HTTPException(status_code=404, detail="Key not found")
        return {"key": key, "value": json.loads(value)}
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail="Invalid JSON in cache") from e
    except redis.RedisError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
