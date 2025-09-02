#!/bin/bash

# AI Mortgage Advisor - Git Commit and Push Script
# This script will commit all changes and push to the remote repository

echo "🏦 AI Mortgage Advisor - Git Setup and Push"
echo "============================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
else
    echo "✅ Git repository already initialized"
fi

# Check if remote origin exists
if ! git remote | grep -q "origin"; then
    echo "🌐 Adding remote origin..."
    echo "Please enter your GitHub username:"
    read -r github_username
    
    echo "Please enter your repository name (default: ai-mortgage-advisor):"
    read -r repo_name
    repo_name=${repo_name:-ai-mortgage-advisor}
    
    git remote add origin "https://github.com/$github_username/$repo_name.git"
    echo "✅ Remote origin added: https://github.com/$github_username/$repo_name.git"
else
    echo "✅ Remote origin already exists"
fi

# Add all files
echo "📦 Adding all files to git..."
git add .

# Check if there are changes to commit
if git diff --cached --quiet; then
    echo "ℹ️  No changes to commit"
else
    echo "💾 Creating commit..."
    git commit -m "Initial commit: AI Mortgage Advisor System

- Complete AI mortgage advisor system with 30+ UK lenders
- Vector database with LanceDB for semantic search
- OpenAI GPT-4 integration for intelligent responses
- Streamlit web interface for user interaction
- Comprehensive documentation and guides
- Automated update and maintenance scripts
- Professional project structure with proper licensing

Features:
- Instant access to mortgage criteria
- AI-powered question answering
- Regular criteria updates
- Professional documentation
- Scalable architecture"

    echo "✅ Commit created successfully"
fi

# Push to remote repository
echo "🚀 Pushing to remote repository..."
git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo "🎉 Successfully pushed to GitHub!"
    echo "🌐 Your repository is now available at:"
    git remote get-url origin
    echo ""
    echo "📚 Next steps:"
    echo "1. Visit your GitHub repository"
    echo "2. Review the uploaded files"
    echo "3. Update repository description if needed"
    echo "4. Set up branch protection rules"
    echo "5. Invite collaborators if needed"
else
    echo "❌ Failed to push to GitHub"
    echo "Please check your GitHub credentials and try again"
fi

echo ""
echo "✨ Git setup complete!"



