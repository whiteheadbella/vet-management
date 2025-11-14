# Local Network Deploy Script (Windows PowerShell)
# Run this script to deploy on your local network for in-person presentations

Write-Host "🏠 Pet Adoption System - Local Network Deployment" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

# Get local IP address
$ipAddress = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -notlike "*Loopback*" -and $_.IPAddress -like "192.168.*"}).IPAddress

if (-not $ipAddress) {
    $ipAddress = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -notlike "*Loopback*"}).IPAddress | Select-Object -First 1
}

Write-Host "📍 Your local IP address: $ipAddress" -ForegroundColor Green
Write-Host ""

# Configure firewall
Write-Host "🔥 Configuring Windows Firewall..." -ForegroundColor Yellow
try {
    New-NetFirewallRule -DisplayName "Pet Adoption System" -Direction Inbound -LocalPort 5000-5002 -Protocol TCP -Action Allow -ErrorAction SilentlyContinue
    Write-Host "✅ Firewall rules added" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Could not add firewall rules. You may need to run as Administrator." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🚀 Starting services..." -ForegroundColor Yellow
Write-Host ""

# Start services in separate windows
Write-Host "Starting Adoption System (Port 5000)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; python adoption_system/app.py"

Start-Sleep -Seconds 3

Write-Host "Starting Shelter System (Port 5001)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; python shelter_system/app.py"

Start-Sleep -Seconds 3

Write-Host "Starting Veterinary System (Port 5002)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; python veterinary_system/app.py"

Write-Host ""
Write-Host "⏳ Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host ""
Write-Host "✅ All Services Started!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Access from this computer:" -ForegroundColor Cyan
Write-Host "   Adoption System:    http://localhost:5000" -ForegroundColor White
Write-Host "   Shelter System:     http://localhost:5001" -ForegroundColor White
Write-Host "   Veterinary System:  http://localhost:5002" -ForegroundColor White
Write-Host ""
Write-Host "📱 Access from other devices on your network:" -ForegroundColor Cyan
Write-Host "   Adoption System:    http://${ipAddress}:5000" -ForegroundColor White
Write-Host "   Shelter System:     http://${ipAddress}:5001" -ForegroundColor White
Write-Host "   Veterinary System:  http://${ipAddress}:5002" -ForegroundColor White
Write-Host ""
Write-Host "📱 Generate QR codes for these URLs for easy mobile access!" -ForegroundColor Yellow
Write-Host "   Use: https://www.qr-code-generator.com/" -ForegroundColor White
Write-Host ""
Write-Host "🛑 To stop all services, close the PowerShell windows or run:" -ForegroundColor Cyan
Write-Host "   Get-Process python | Stop-Process" -ForegroundColor White
Write-Host ""
