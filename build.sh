#!/bin/bash

# Simple Docker Build Script
# Builds the Flask API image locally and runs it

set -e

# Change to project root directory (assuming script is in root)
cd "$(dirname "$0")"

echo "Building Docker image locally..."

# Stop and remove existing container if it exists
echo "Cleaning up existing container..."
docker stop flask-api-container 2>/dev/null || true
docker rm flask-api-container 2>/dev/null || true

# Build Docker image
echo "Building flask-api image..."
docker build -t flask-api:latest .

echo "Build completed successfully!"
echo "Local image: flask-api:latest"
echo ""

# Ensure data directory and db.json exist
mkdir -p data
if [ ! -f data/db.json ]; then
    echo "Creating initial data/db.json..."
    touch data/db.json
fi

# Run the container with port mapping and bind mount for db.json persistence
echo "Starting flask-api container with bind mount for data/db.json..."
docker run -d --name flask-api-container \
    -p 5000:5000 \
    -v "$(pwd)/data/db.json:/app/db.json" \
    flask-api:latest

echo "Container started successfully!"
echo "Container name: flask-api-container"
echo "API available at: http://localhost:5000"
echo ""
echo "To check logs:"
echo "  docker logs flask-api-container"
echo ""
echo "To follow logs in real-time:"
echo "  docker logs -f flask-api-container"
echo ""
echo "To stop the container:"
echo "  docker stop flask-api-container"