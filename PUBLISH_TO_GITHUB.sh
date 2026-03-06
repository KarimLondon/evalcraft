#!/bin/bash
# Script to publish EvalCraft to GitHub
# Run this from the evalcraft-github directory

set -e  # Exit on error

echo "🚀 Publishing EvalCraft to GitHub"
echo "=================================="
echo ""

# Check we're in the right directory
if [ ! -f "README.md" ]; then
    echo "❌ Error: README.md not found"
    echo "Please run this script from the evalcraft-github directory"
    exit 1
fi

echo "✅ In correct directory"
echo ""

# Initialize git if not already done
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    echo "✅ Git initialized"
else
    echo "✅ Git already initialized"
fi
echo ""

# Add all files
echo "📝 Staging all files..."
git add .
echo "✅ Files staged"
echo ""

# Create initial commit
if git rev-parse HEAD >/dev/null 2>&1; then
    echo "✅ Commits already exist"
else
    echo "💾 Creating initial commit..."
    git commit -m "Initial commit: EvalCraft v1.0.0 - AI Evaluation Framework Builder

- Claude Code skill for generating eval rubrics
- AI-powered rubric generation from prompt + outcomes
- LLM-as-judge code generator
- Interactive HTML reports
- Complete examples and documentation
- Phase 2 roadmap (Web UI)

Built to solve: PMs building AI products don't know how to write evals"
    echo "✅ Initial commit created"
fi
echo ""

# Set main branch
echo "🌿 Setting main branch..."
git branch -M main
echo "✅ Branch set to main"
echo ""

# Add remote (replace YOUR_USERNAME with actual username)
GITHUB_USER="KarimLondon"
REPO_NAME="evalcraft"

echo "🔗 Adding remote origin..."
if git remote | grep -q "^origin$"; then
    echo "   Removing existing origin..."
    git remote remove origin
fi

git remote add origin "https://github.com/${GITHUB_USER}/${REPO_NAME}.git"
echo "✅ Remote added: https://github.com/${GITHUB_USER}/${REPO_NAME}"
echo ""

echo "📋 Next Steps:"
echo "=============="
echo ""
echo "1. Create GitHub repo (if not exists):"
echo "   Go to: https://github.com/new"
echo "   Name: ${REPO_NAME}"
echo "   Description: AI Evaluation Framework Builder for Product Managers"
echo "   Public: Yes"
echo "   Don't initialize with README"
echo ""
echo "2. Push to GitHub:"
echo "   Run: git push -u origin main"
echo ""
echo "   (You'll be prompted for GitHub credentials)"
echo ""
echo "3. If you get authentication error:"
echo "   Create Personal Access Token:"
echo "   https://github.com/settings/tokens/new"
echo "   Scopes: repo (all)"
echo "   Use token as password when pushing"
echo ""
echo "🎉 Repository prepared! Run 'git push -u origin main' to publish"
