#!/bin/bash
# GitHub + Render.com Deployment Script

echo "🌐 Pet Adoption System - GitHub + Render Deployment"
echo "==================================================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    echo ""
fi

# Add all files
echo "📝 Adding files to Git..."
git add .

# Commit
echo "💾 Committing changes..."
read -p "Enter commit message (default: 'Deploy Pet Adoption System'): " commit_msg
commit_msg=${commit_msg:-"Deploy Pet Adoption System"}
git commit -m "$commit_msg"

echo ""
echo "🔗 Next Steps:"
echo ""
echo "1. Create a GitHub repository:"
echo "   - Go to https://github.com/new"
echo "   - Repository name: pet-adoption-system"
echo "   - Keep it public (or private if you prefer)"
echo "   - Don't initialize with README"
echo "   - Click 'Create repository'"
echo ""
echo "2. Push your code:"
read -p "Enter your GitHub username: " github_user
read -p "Enter repository name (default: pet-adoption-system): " repo_name
repo_name=${repo_name:-"pet-adoption-system"}

echo ""
echo "📤 Setting up remote and pushing..."
git branch -M main
git remote add origin "https://github.com/$github_user/$repo_name.git"
git push -u origin main

echo ""
echo "✅ Code pushed to GitHub!"
echo ""
echo "🌐 Deploy on Render.com:"
echo ""
echo "1. Go to https://render.com and sign up (free)"
echo "2. Click 'New +' → 'Blueprint'"
echo "3. Connect your GitHub repository: $github_user/$repo_name"
echo "4. Render will detect render.yaml and create 3 services automatically"
echo "5. Click 'Apply' and wait 5-10 minutes"
echo "6. You'll get 3 live URLs!"
echo ""
echo "Your services will be deployed at:"
echo "   - https://pet-adoption-system.onrender.com"
echo "   - https://pet-shelter-system.onrender.com"
echo "   - https://pet-veterinary-system.onrender.com"
echo ""
echo "🎉 Deployment guide complete!"
echo ""
