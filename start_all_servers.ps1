# Start All Servers Script
# This will open 3 PowerShell windows, one for each system

Write-Host "`nStarting Pet Adoption System..." -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan

$projectPath = $PSScriptRoot

Write-Host "`nProject location: $projectPath" -ForegroundColor Yellow

Write-Host "`nStarting Adoption System (Port 5000)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectPath'; Write-Host 'Adoption System - Port 5000' -ForegroundColor Green; python adoption_system/app.py"

Start-Sleep -Seconds 3

Write-Host "Starting Shelter System (Port 5001)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectPath'; Write-Host 'Shelter System - Port 5001' -ForegroundColor Green; python shelter_system/app.py"

Start-Sleep -Seconds 3

Write-Host "Starting Veterinary System (Port 5002)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectPath'; Write-Host 'Veterinary System - Port 5002' -ForegroundColor Green; python veterinary_system/app.py"

Write-Host "`nWaiting for all servers to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host "`nAll servers started!" -ForegroundColor Green
Write-Host "`nAccess your systems:" -ForegroundColor Cyan
Write-Host "   Adoption System:    http://localhost:5000" -ForegroundColor White
Write-Host "   Shelter System:     http://localhost:5001" -ForegroundColor White
Write-Host "   Veterinary System:  http://localhost:5002" -ForegroundColor White

Write-Host "`nOpening Adoption System in browser..." -ForegroundColor Yellow
Start-Sleep -Seconds 2
Start-Process "http://localhost:5000"

Write-Host "`nTo stop all servers:" -ForegroundColor Yellow
Write-Host "   Close the 3 PowerShell windows" -ForegroundColor White
Write-Host "   OR run: Get-Process python | Stop-Process -Force" -ForegroundColor White

Write-Host "`nHappy browsing!" -ForegroundColor Green
Write-Host ""
