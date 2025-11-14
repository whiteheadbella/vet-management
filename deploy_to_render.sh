#!/bin/bash

# Automated Render Deployment Setup Script
# Run this after creating your Render account and services

echo "🚀 Render.com Deployment Helper"
echo "================================"
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "❌ Git not initialized. Initializing now..."
    git init
fi

# Check for GitHub remote
if ! git remote | grep -q origin; then
    echo ""
    read -p "Enter your GitHub repository URL (e.g., https://github.com/username/vet-management.git): " REPO_URL
    git remote add origin "$REPO_URL"
    echo "✅ GitHub remote added"
fi

# Add all files
echo ""
echo "📦 Adding all files to git..."
git add .

# Commit
echo ""
read -p "Enter commit message (default: 'Deploy to Render'): " COMMIT_MSG
COMMIT_MSG=${COMMIT_MSG:-"Deploy to Render"}
git commit -m "$COMMIT_MSG"

# Push to GitHub
echo ""
echo "⬆️  Pushing to GitHub..."
git push -u origin main

echo ""
echo "✅ Code pushed to GitHub!"
echo ""
echo "📋 Next Steps:"
echo "=============="
echo ""
echo "1. Go to https://render.com"
echo "2. Sign in and click 'New +' → 'Web Service'"
echo "3. Connect your repository"
echo ""
echo "4. Create SERVICE 1 - Adoption System:"
echo "   Name: pet-adoption-system"
echo "   Build: pip install -r requirements.txt"
echo "   Start: python adoption_system/app.py"
echo ""
echo "5. Create SERVICE 2 - Shelter System:"
echo "   Name: shelter-system"
echo "   Build: pip install -r requirements.txt"
echo "   Start: python shelter_system/app.py"
echo ""
echo "6. Create SERVICE 3 - Veterinary System:"
echo "   Name: veterinary-system"
echo "   Build: pip install -r requirements.txt"
echo "   Start: python veterinary_system/app.py"
echo ""
echo "7. After deployment, note your URLs and update config.py"
echo ""
echo "🎉 Done! Check RENDER_DEPLOYMENT_GUIDE.md for detailed instructions"
