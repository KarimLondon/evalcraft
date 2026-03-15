# Publishing EvalCraft to GitHub

**Quick guide to get your project on GitHub**

---

## Step 1: Initialize Git Repo

```bash
cd /Users/karimezzouek/Documents/evalcraft-github

# Initialize git
git init

# Add all files
git add .

# First commit
git commit -m "Initial commit: EvalCraft - AI Evaluation Framework Builder

- Claude Code skill for generating eval rubrics
- AI-powered rubric generation from prompt + outcomes
- LLM-as-judge code generator
- Interactive HTML reports
- Complete examples and documentation
- Phase 2 roadmap (Web UI)"
```

---

## Step 2: Create GitHub Repo

**Option A: Via GitHub Website**
1. Go to https://github.com/new
2. Repository name: `evalcraft`
3. Description: `AI Evaluation Framework Builder for Product Managers - Generate custom rubrics and LLM-as-judge code`
4. Public (for portfolio showcase)
5. **DON'T** initialize with README (we already have one)
6. Click "Create repository"

**Option B: Via GitHub CLI**
```bash
# Install gh CLI if needed: brew install gh

gh auth login
gh repo create evalcraft --public --source=. \
  --description="AI Evaluation Framework Builder for Product Managers" \
  --remote=origin

git push -u origin main
```

---

## Step 3: Push to GitHub

```bash
# Add remote (use URL from GitHub)
git remote add origin https://github.com/YOUR_USERNAME/evalcraft.git

# Push
git branch -M main
git push -u origin main
```

---

## Step 4: Add Repository Topics

On GitHub repo page → Settings → Topics:
- `ai-evaluation`
- `llm-as-judge`
- `product-management`
- `claude-api`
- `evaluation-framework`
- `ai-agents`
- `python`
- `portfolio`

---

## Step 5: Create Release (v1.0.0)

**Option A: Via GitHub Website**
1. Go to Releases → Create a new release
2. Tag: `v1.0.0`
3. Title: `EvalCraft v1.0.0 - Claude Skill MVP`
4. Description:
```
   ## EvalCraft v1.0.0 - Phase 1 Complete

   First release of EvalCraft, an AI evaluation framework builder for PMs.

   ### Features
   - 🎯 Outcome-driven rubric generation
   - 🤖 AI-powered category recommendations
   - 📊 LLM-as-judge code generation
   - 🔍 Interactive HTML reports
   - ♻️ Iterative refinement support

   ### What's Included
   - Claude Code skill (`/evalcraft`)
   - Python scripts for standalone use
   - Complete documentation and examples
   - Phase 2 roadmap (Web UI)

   ### Getting Started
   See [README.md](README.md) for installation and usage.

   ### Example
   See `examples/fitness_coach_complete/` for full working example.
```

**Option B: Via GitHub CLI**
```bash
gh release create v1.0.0 \
  --title "EvalCraft v1.0.0 - Claude Skill MVP" \
  --notes "First release - Phase 1 complete. See README for details."
```

---

## Step 6: Enhance README (Add Visual Elements)

### Add Badge at Top
```markdown
![Status](https://img.shields.io/badge/status-active-success.svg)
![Phase](https://img.shields.io/badge/phase-1%20complete-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
```

### Add Screenshots (When Available)
1. Run evaluation with API credits
2. Take screenshot of HTML report
3. Save to `docs/images/dashboard-screenshot.png`
4. Update README to show image:
```markdown
   ![Results Dashboard](docs/images/dashboard-screenshot.png)
```

### Add Demo GIF (Optional)
1. Record terminal session with [asciinema](https://asciinema.org)
2. Or screen recording → GIF with [Gifski](https://gif.ski)
3. Add to README

---

## Step 7: Create Project Website (Optional)

**Option A: GitHub Pages**
```bash
# Create docs site
mkdir -p docs/_site
# Add index.html based on README
git add docs
git commit -m "Add GitHub Pages site"
git push

# Enable in Settings → Pages → Source: docs/
```

**Option B: Simple Landing Page**
Use [readme.so](https://readme.so) or similar to create visual README

---

## Step 8: Add to Portfolio/LinkedIn

### LinkedIn Post Template:
```
🚀 Just built EvalCraft - an AI evaluation framework builder!

The problem: PMs building AI products don't know how to write evals.
They ship agents without measuring performance.

The solution: EvalCraft automates eval creation by:
✅ Analyzing agent prompts + product outcomes
✅ Generating custom rubrics (4-6 categories)
✅ Creating executable LLM-as-judge code
✅ Producing interactive HTML reports

Built with Claude API and implemented as both:
- Claude Code skill (Phase 1 ✅)
- Web UI (Phase 2 roadmap)

Demonstrates:
🎯 Product thinking (solves real PM pain point)
🤖 AI agent orchestration
📊 Full-stack implementation
♻️ Iterative design

Check it out: https://github.com/YOUR_USERNAME/evalcraft

#AI #ProductManagement #LLM #Portfolio #ClaudeAI
```

### Portfolio Page:
```markdown
# EvalCraft - AI Evaluation Framework Builder

**Role:** Solo Developer & Product Designer
**Timeline:** March 2026 (2 weeks)
**Tech:** Python, Claude API, LLM-as-judge

## Problem
Product Managers building AI products lack tools to create
evaluation frameworks, resulting in unvalidated AI agents.

## Solution
Built EvalCraft - an AI-powered tool that generates custom
evaluation rubrics and executable code from agent prompts
and product outcomes.

## Key Features
- Outcome-driven rubric generation
- LLM-as-judge automation (temperature=0)
- Interactive HTML reports with traces
- Iterative refinement support

## Impact
- Reduces eval setup time from days to minutes
- Embeds best practices from eval research
- Generates production-ready Python code
- Complete end-to-end workflow

## Technical Highlights
- Claude API integration for rubric generation
- Code generation with template injection
- 34KB standalone evaluation scripts
- Interactive HTML reports with filtering

[View on GitHub](https://github.com/YOUR_USERNAME/evalcraft) |
[Live Demo](link-when-phase-2-done)
```

---

## Step 9: Star & Fork (Build Community)

After publishing:
1. Share in relevant communities:
  - r/LanguageTechnology
  - r/MachineLearning (Sunday megathread)
  - Anthropic Discord
  - AI Twitter
  - LinkedIn

2. Ask for feedback:
  - "Would love feedback on my eval tool for PMs"
  - Link to Issues for suggestions

3. Respond to issues/PRs promptly

---

## Step 10: Maintenance Plan

### Weekly (First Month):
- [ ] Check issues/PRs
- [ ] Update README based on questions
- [ ] Add more examples if requested

### Monthly:
- [ ] Review dependencies (security updates)
- [ ] Add requested features to Phase 2 roadmap
- [ ] Update documentation

### When Phase 2 Complete:
- [ ] Create v2.0.0 release
- [ ] Update README with Web UI info
- [ ] Add deployment guide
- [ ] Create demo video
- [ ] Update portfolio with new screenshots

---

## Checklist Before Publishing

- [x] README complete with examples
- [x] LICENSE added (MIT)
- [x] .gitignore configured
- [x] Requirements.txt included
- [x] Examples working
- [x] Documentation clear
- [x] Syntax errors fixed
- [ ] Screenshots added (after eval runs)
- [ ] Demo video created (optional)
- [ ] Links updated (replace YOUR_USERNAME)

---

## After Publishing

**Celebrate!** 🎉 You've built a complete, production-ready AI tool!

**Next:**
1. Get feedback from 5 PMs
2. Iterate based on feedback
3. Plan Phase 2 kick-off
4. Add to resume/portfolio
5. Share on social media

**Your GitHub repo will showcase:**
✅ Product thinking (real PM problem)
✅ AI engineering (Claude API, LLM-as-judge)
✅ Full-stack skills (Python, code generation, reports)
✅ Documentation quality (comprehensive README, guides)
✅ Project management (phased approach, roadmap)

---

**Ready to ship!** 🚀
