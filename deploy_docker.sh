#!/bin/bash
# Quick Deploy Script for Pet Adoption System

echo "🚀 Pet Adoption System - Quick Deploy"
echo "======================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker Desktop first."
    echo "   Download from: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker is installed"
echo ""

# Build and start services
echo "📦 Building Docker images..."
docker-compose build

echo ""
echo "🚀 Starting all services..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to start..."
sleep 10

# Initialize databases
echo ""
echo "🗄️ Initializing databases..."
docker-compose exec -T adoption-system python init_databases.py

echo ""
echo "🐾 Populating pets..."
docker-compose exec -T shelter-system python populate_pets.py

echo ""
echo "🏥 Populating veterinary records..."
docker-compose exec -T veterinary-system python populate_vet_records.py

echo ""
echo "✅ Deployment Complete!"
echo ""
echo "🌐 Access your systems:"
echo "   Adoption System:    http://localhost:5000"
echo "   Shelter System:     http://localhost:5001"
echo "   Veterinary System:  http://localhost:5002"
echo ""
echo "📊 View logs:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 Stop services:"
echo "   docker-compose down"
echo ""
