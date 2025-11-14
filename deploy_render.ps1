# GitHub + Render.com Deployment Script (Windows PowerShell)

Write-Host "🌐 Pet Adoption System - GitHub + Render Deployment" -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "📦 Initializing Git repository..." -ForegroundColor Yellow
    git init
    Write-Host ""
}

# Add all files
Write-Host "📝 Adding files to Git..." -ForegroundColor Yellow
git add .

# Commit
Write-Host "💾 Committing changes..." -ForegroundColor Yellow
$commitMsg = Read-Host "Enter commit message (press Enter for default: 'Deploy Pet Adoption System')"
if ([string]::IsNullOrWhiteSpace($commitMsg)) {
    $commitMsg = "Deploy Pet Adoption System"
}
git commit -m $commitMsg

Write-Host ""
Write-Host "🔗 Next Steps:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Create a GitHub repository:" -ForegroundColor Yellow
Write-Host "   - Go to https://github.com/new" -ForegroundColor White
Write-Host "   - Repository name: pet-adoption-system" -ForegroundColor White
Write-Host "   - Keep it public (or private if you prefer)" -ForegroundColor White
Write-Host "   - Don't initialize with README" -ForegroundColor White
Write-Host "   - Click 'Create repository'" -ForegroundColor White
Write-Host ""

$githubUser = Read-Host "Enter your GitHub username"
$repoName = Read-Host "Enter repository name (press Enter for default: pet-adoption-system)"
if ([string]::IsNullOrWhiteSpace($repoName)) {
    $repoName = "pet-adoption-system"
}

Write-Host ""
Write-Host "📤 Setting up remote and pushing..." -ForegroundColor Yellow
git branch -M main
git remote remove origin 2>$null
git remote add origin "https://github.com/$githubUser/$repoName.git"

Write-Host ""
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
Write-Host "You may need to authenticate with GitHub" -ForegroundColor Cyan
git push -u origin main

Write-Host ""
Write-Host "✅ Code pushed to GitHub!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Deploy on Render.com:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Go to https://render.com and sign up (free)" -ForegroundColor White
Write-Host "2. Click 'New +' → 'Blueprint'" -ForegroundColor White
Write-Host "3. Connect your GitHub repository: $githubUser/$repoName" -ForegroundColor White
Write-Host "4. Render will detect render.yaml and create 3 services automatically" -ForegroundColor White
Write-Host "5. Click 'Apply' and wait 5-10 minutes" -ForegroundColor White
Write-Host "6. You'll get 3 live URLs!" -ForegroundColor White
Write-Host ""
Write-Host "Your services will be deployed at:" -ForegroundColor Green
Write-Host "   - https://pet-adoption-system.onrender.com" -ForegroundColor White
Write-Host "   - https://pet-shelter-system.onrender.com" -ForegroundColor White
Write-Host "   - https://pet-veterinary-system.onrender.com" -ForegroundColor White
Write-Host ""
Write-Host "🎉 Deployment guide complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Press any key to open Render.com in your browser..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
Start-Process "https://render.com"
