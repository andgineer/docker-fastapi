#!/usr/bin/env python3
"""MongoDB initialization script for FastAPI playground"""

from datetime import datetime, timezone

import pymongo

# Connect to MongoDB
client: pymongo.MongoClient = pymongo.MongoClient("mongodb://admin:password@localhost:27017/")
db = client["fastapi_db"]

# Create collections with indexes
users_collection = db["users"]
users_collection.create_index("email", unique=True)
users_collection.create_index("created_at")

items_collection = db["items"]
items_collection.create_index("name")
items_collection.create_index("owner_id")
items_collection.create_index("created_at")

# Insert sample data
sample_user = {
    "email": "user@example.com",
    "name": "Sample User",
    "created_at": datetime.now(tz=timezone.utc),
}
users_collection.insert_one(sample_user)

sample_item = {
    "name": "Sample Item",
    "description": "This is a sample item",
    "owner_id": "user@example.com",
    "created_at": datetime.now(tz=timezone.utc),
}
items_collection.insert_one(sample_item)

print("Database initialized successfully")
client.close()
