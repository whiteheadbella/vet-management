# System Health Check Script

Write-Host "🔍 Pet Adoption System - Health Check" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

$systems = @(
    @{Name="Adoption System"; URL="http://localhost:5000"; Port=5000},
    @{Name="Shelter System"; URL="http://localhost:5001"; Port=5001},
    @{Name="Veterinary System"; URL="http://localhost:5002"; Port=5002}
)

$allHealthy = $true

foreach ($system in $systems) {
    Write-Host "Checking $($system.Name)..." -ForegroundColor Yellow
    
    # Check if port is listening
    $portOpen = Test-NetConnection -ComputerName localhost -Port $system.Port -WarningAction SilentlyContinue
    
    if ($portOpen.TcpTestSucceeded) {
        Write-Host "  ✅ Port $($system.Port) is open" -ForegroundColor Green
        
        # Try to access the URL
        try {
            $response = Invoke-WebRequest -Uri $system.URL -TimeoutSec 5 -UseBasicParsing
            Write-Host "  ✅ Service responding (Status: $($response.StatusCode))" -ForegroundColor Green
            Write-Host "  🌐 Access at: $($system.URL)" -ForegroundColor Cyan
        } catch {
            Write-Host "  ⚠️ Port open but service not responding" -ForegroundColor Yellow
            $allHealthy = $false
        }
    } else {
        Write-Host "  ❌ Port $($system.Port) is not open - service not running" -ForegroundColor Red
        $allHealthy = $false
    }
    Write-Host ""
}

# Test API endpoints
Write-Host "Testing API Endpoints..." -ForegroundColor Yellow
Write-Host ""

$apiTests = @(
    @{Name="Get Pets"; URL="http://localhost:5001/api/pets/"},
    @{Name="Get Health Record"; URL="http://localhost:5002/api/health/1"},
    @{Name="Get Vets"; URL="http://localhost:5002/api/vets"}
)

foreach ($test in $apiTests) {
    Write-Host "  Testing: $($test.Name)..." -NoNewline
    try {
        $response = Invoke-RestMethod -Uri $test.URL -TimeoutSec 5 -ErrorAction Stop
        Write-Host " ✅" -ForegroundColor Green
    } catch {
        Write-Host " ❌" -ForegroundColor Red
        $allHealthy = $false
    }
}

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan

if ($allHealthy) {
    Write-Host "🎉 All systems are healthy!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Ready for presentation! 🚀" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Open http://localhost:5000 in your browser" -ForegroundColor White
    Write-Host "  2. Browse pets and test features" -ForegroundColor White
    Write-Host "  3. Use Postman to test APIs" -ForegroundColor White
} else {
    Write-Host "⚠️ Some systems are not healthy" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Try:" -ForegroundColor Cyan
    Write-Host "  • Run .\deploy_docker.ps1 or .\deploy_local.ps1" -ForegroundColor White
    Write-Host "  • Check if services are running" -ForegroundColor White
    Write-Host "  • Review logs for errors" -ForegroundColor White
}

Write-Host ""
