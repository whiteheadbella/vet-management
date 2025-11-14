# Quick Deploy Script for Pet Adoption System (Windows PowerShell)
# Run this script to deploy using Docker

Write-Host "🚀 Pet Adoption System - Quick Deploy" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is installed
try {
    docker --version | Out-Null
    Write-Host "✅ Docker is installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not installed. Please install Docker Desktop first." -ForegroundColor Red
    Write-Host "   Download from: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Build and start services
Write-Host "📦 Building Docker images..." -ForegroundColor Yellow
docker-compose build

Write-Host ""
Write-Host "🚀 Starting all services..." -ForegroundColor Yellow
docker-compose up -d

Write-Host ""
Write-Host "⏳ Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Initialize databases
Write-Host ""
Write-Host "🗄️ Initializing databases..." -ForegroundColor Yellow
docker-compose exec -T adoption-system python init_databases.py

Write-Host ""
Write-Host "🐾 Populating pets..." -ForegroundColor Yellow
docker-compose exec -T shelter-system python populate_pets.py

Write-Host ""
Write-Host "🏥 Populating veterinary records..." -ForegroundColor Yellow
docker-compose exec -T veterinary-system python populate_vet_records.py

Write-Host ""
Write-Host "✅ Deployment Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Access your systems:" -ForegroundColor Cyan
Write-Host "   Adoption System:    http://localhost:5000" -ForegroundColor White
Write-Host "   Shelter System:     http://localhost:5001" -ForegroundColor White
Write-Host "   Veterinary System:  http://localhost:5002" -ForegroundColor White
Write-Host ""
Write-Host "📊 View logs:" -ForegroundColor Cyan
Write-Host "   docker-compose logs -f" -ForegroundColor White
Write-Host ""
Write-Host "🛑 Stop services:" -ForegroundColor Cyan
Write-Host "   docker-compose down" -ForegroundColor White
Write-Host ""
