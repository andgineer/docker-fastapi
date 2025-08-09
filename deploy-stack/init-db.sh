#!/bin/bash
# Database initialization script

echo "Waiting for MongoDB to be ready..."
until docker-compose exec mongo mongosh --eval "print('MongoDB is ready')" > /dev/null 2>&1; do
    echo "Waiting for MongoDB..."
    sleep 2
done

echo "Initializing database..."
docker-compose exec -T mongo mongosh fastapi_db --eval "
// Create collections with indexes
db.users.createIndex({ 'email': 1 }, { unique: true });
db.users.createIndex({ 'created_at': 1 });

db.items.createIndex({ 'name': 1 });
db.items.createIndex({ 'owner_id': 1 });
db.items.createIndex({ 'created_at': 1 });

// Insert sample data
db.users.insertOne({
    email: 'user@example.com',
    name: 'Sample User',
    created_at: new Date()
});

db.items.insertOne({
    name: 'Sample Item',
    description: 'This is a sample item',
    owner_id: 'user@example.com',
    created_at: new Date()
});

print('Database initialized successfully');
"

echo "Database initialization completed!"
