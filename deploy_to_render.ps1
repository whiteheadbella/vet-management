# PowerShell Script for Render Deployment Setup

Write-Host "`n🚀 Render.com Deployment Helper" -ForegroundColor Cyan
Write-Host "================================`n" -ForegroundColor Cyan

# Check if git is initialized
if (-not (Test-Path .git)) {
    Write-Host "❌ Git not initialized. Initializing now..." -ForegroundColor Yellow
    git init
    Write-Host "✅ Git initialized`n" -ForegroundColor Green
}

# Check for GitHub remote
$hasRemote = git remote | Select-String -Pattern "origin" -Quiet
if (-not $hasRemote) {
    Write-Host ""
    $repoUrl = Read-Host "Enter your GitHub repository URL (e.g., https://github.com/username/vet-management.git)"
    git remote add origin $repoUrl
    Write-Host "✅ GitHub remote added`n" -ForegroundColor Green
}

# Add all files
Write-Host "📦 Adding all files to git..." -ForegroundColor Cyan
git add .

# Commit
Write-Host ""
$commitMsg = Read-Host "Enter commit message (press Enter for 'Deploy to Render')"
if ([string]::IsNullOrWhiteSpace($commitMsg)) {
    $commitMsg = "Deploy to Render"
}
git commit -m $commitMsg

# Push to GitHub
Write-Host "`n⬆️  Pushing to GitHub..." -ForegroundColor Cyan
git branch -M main
git push -u origin main

Write-Host "`n✅ Code pushed to GitHub!`n" -ForegroundColor Green

# Display next steps
Write-Host "📋 Next Steps:" -ForegroundColor Cyan
Write-Host "==============" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Go to https://render.com" -ForegroundColor White
Write-Host "2. Sign in and click 'New +' → 'Web Service'" -ForegroundColor White
Write-Host "3. Connect your repository`n" -ForegroundColor White

Write-Host "4. Create SERVICE 1 - Adoption System:" -ForegroundColor Yellow
Write-Host "   Name: pet-adoption-system"
Write-Host "   Build: pip install -r requirements.txt"
Write-Host "   Start: python adoption_system/app.py`n"

Write-Host "5. Create SERVICE 2 - Shelter System:" -ForegroundColor Yellow
Write-Host "   Name: shelter-system"
Write-Host "   Build: pip install -r requirements.txt"
Write-Host "   Start: python shelter_system/app.py`n"

Write-Host "6. Create SERVICE 3 - Veterinary System:" -ForegroundColor Yellow
Write-Host "   Name: veterinary-system"
Write-Host "   Build: pip install -r requirements.txt"
Write-Host "   Start: python veterinary_system/app.py`n"

Write-Host "7. After deployment, update these Environment Variables for each service:" -ForegroundColor Cyan
Write-Host "   FLASK_ENV=production"
Write-Host "   SECRET_KEY=your-secret-key-here"
Write-Host "   SHELTER_SYSTEM_URL=https://shelter-system.onrender.com"
Write-Host "   VETERINARY_SYSTEM_URL=https://veterinary-system.onrender.com"
Write-Host "   ADOPTION_SYSTEM_URL=https://pet-adoption-system.onrender.com`n"

Write-Host "8. Initialize databases in each service Shell:" -ForegroundColor Cyan
Write-Host "   python init_databases.py"
Write-Host "   python populate_pets.py`n"

Write-Host "🎉 Done! Check RENDER_DEPLOYMENT_GUIDE.md for detailed instructions`n" -ForegroundColor Green

# Offer to open Render
$openRender = Read-Host "Would you like to open Render.com now? (y/n)"
if ($openRender -eq 'y') {
    Start-Process "https://render.com"
}
