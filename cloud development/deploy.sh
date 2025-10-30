#!/bin/bash
cd ~/cloud-project

echo "Pulling latest Docker images..."
docker compose pull

echo "Rebuilding containers..."
docker compose up -d --build

echo "Cleaning old images..."
docker image prune -f

echo "Deployment complete!"
