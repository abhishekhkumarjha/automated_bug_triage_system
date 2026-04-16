#!/bin/bash

# Automated Bug Triage System - Deployment Script

set -e

echo "🚀 Starting deployment of Automated Bug Triage System..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p model
mkdir -p data
mkdir -p logs

# Set permissions
chmod +x main.py
chmod +x train_with_large_dataset.py

# Build and start the application
echo "🔨 Building Docker image..."
docker-compose build

echo "🚀 Starting application..."
docker-compose up -d

# Wait for the application to start
echo "⏳ Waiting for application to start..."
sleep 10

# Check if the application is running
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Application is running successfully!"
    echo "🌐 API is available at: http://localhost:8000"
    echo "📚 API Documentation: http://localhost:8000/docs"
    echo "🏥 Health Check: http://localhost:8000/health"
else
    echo "❌ Application failed to start. Check logs with: docker-compose logs bug-triage-api"
    exit 1
fi

echo "🎉 Deployment completed successfully!"
