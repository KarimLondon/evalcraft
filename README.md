# EvalCraft 🎯

**AI Evaluation Framework Builder for Product Managers**

EvalCraft helps PMs design evaluation frameworks for AI agents by generating custom rubrics, executable LLM-as-judge code, and interactive reports—no ML expertise required.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Claude API](https://img.shields.io/badge/Claude-API-orange.svg)](https://www.anthropic.com)

---

## 🎥 Demo

**Example:** Fitness coach agent → Custom 6-category rubric → Evaluation code → Interactive HTML report

---

## 🚀 Problem & Solution

### Problem
Product Managers may struggle to know where or how to write evaluations for their AI products. In the absense of any evals, some may even ship agents without measuring performance or knowing if they behave as expected.

### Solution
EvalCraft support Product Managers in creating evals by:
1. Analyzing your agent prompt + product outcomes
2. Working with you to create custom rubrics (4-6 categories with scoring scales)
3. Creating executable Python code (LLM-as-judge)
4. Running evaluations with interactive HTML reports
5. Supporting iteration based on results

---

## ✨ Features

- **🎯 Outcome-Driven**: Rubrics aligned with your product goals, not generic metrics
- **🤖 AI-Powered**: Claude generates custom eval categories and reference examples
- **📊 LLM-as-Judge**: Automated scoring with temperature=0 for consistency
- **🔍 Interactive Reports**: HTML dashboards with detailed traces and filtering
- **📐 Confusion Matrix Metrics**: Add a `label` column to your dataset and get precision, recall, F1, and accuracy automatically — ideal for classification agents
- **🧭 Classification Detection**: EvalCraft spots when your agent is a classifier and proactively suggests the right metrics, even before you have labels
- **♻️ Iterative**: Refine rubrics based on results
- **📦 Portable**: Standalone Python scripts you can customize and integrate

---

## 🏗️ Architecture

### Phase 1: Claude Code Skill (✅ Complete)

```
Input: Agent prompt + Product outcomes + (Optional) Labeled data
  ↓
Rubric Generation (Claude API analyzes → recommends categories)
  ↓
Code Generation (Embeds rubric → creates evaluate.py)
  ↓
Evaluation Execution (LLM-as-judge scores all test cases)
  ↓
Output: Rubric + Python code + Interactive HTML report
```

### Phase 2: Web UI (🚧 Planned)
- Visual rubric builder
- Real-time evaluation dashboard
- Team collaboration features

---

## 📦 Installation

### Prerequisites
- Python 3.9+
- Claude API key ([get one here](https://console.anthropic.com))
- Claude Code CLI (for skill version)

### Option 1: Use as Claude Code Skill

```bash
# Clone the repo
git clone https://github.com/KarimLondon/evalcraft.git

# Copy the skill folder into Claude Code's skills directory
cp -r evalcraft ~/.claude/skills/evalcraft

# Restart Claude Code, then invoke:
# /evalcraft
```

> **Requires:** [Claude Code CLI](https://claude.ai/claude-code) — the skill is invoked directly inside a Claude Code session.

### Option 2: Use Scripts Directly

```bash
# Clone repo
git clone https://github.com/KarimLondon/evalcraft.git
cd evalcraft

# Install dependencies
pip install -r requirements.txt

# Set API key
export ANTHROPIC_API_KEY=your_key_here

# Generate rubric
python scripts/generate_rubric.py \
  --agent-prompt "Your agent prompt here" \
  --outcomes '["Outcome 1", "Outcome 2"]' \
  --output-dir ./my_eval

# Generate evaluation code
python scripts/generate_eval_code.py \
  --rubric ./my_eval/rubric.json \
  --output-dir ./my_eval

# Run evaluation
cd ./my_eval
python evaluate.py --input test_dataset.csv
```

---

## 💡 Quick Start Example

### 1. Define Your Agent

```python
prompt = """You are a customer support assistant for an e-commerce company.
Handle returns, shipping, and product questions."""

outcomes = ["Reduce support tickets by 30%", "Improve customer satisfaction"]
```

### 2. Generate Rubric

EvalCraft creates:
- **Correctness** (≥4.0) - Factually accurate info
- **Completeness** (≥4.0) - Addresses all query parts
- **Deflection Potential** (≥4.0) - Prevents ticket escalation
- **Clarity** (≥3.5) - Easy to understand
- **Tone** (≥3.5) - Friendly and helpful

Each with 1-5 scales and concrete reference examples.

### 3. Run Evaluation

```bash
# Basic run
python evaluate.py --input test_cases.csv

# With ground truth labels (unlocks confusion matrix metrics)
# Add a 'label' column to your CSV with values: pass/fail, yes/no, 1/0, positive/negative
python evaluate.py --input test_cases_labeled.csv
```

### 4. View Results

Interactive HTML report opens in browser:
- Overall: 73% pass rate (11/15 cases)
- Deflection: 3.8/5.0 ⚠️ (needs improvement)
- Correctness: 4.2/5.0 ✅
- Click any case to see judge reasoning

If labeled data was provided, confusion matrix metrics appear automatically:
- Precision: 81% | Recall: 75% | F1: 0.779 | Accuracy: 80%

---

## 📊 Example Output

### Generated Rubric (Markdown)
```markdown
# Customer Support Bot - Evaluation Rubric

## 1. Correctness
**Description:** Is the information factually accurate?
**Pass Threshold:** ≥4.0/5.0

**Score 5:** "Our return policy allows returns within 30 days..."
**Score 3:** "You can return items within 30 days."
**Score 1:** "We don't accept returns." (Wrong!)
```

### Generated Code (Python)
```python
RUBRIC = {
    "correctness": {
        "description": "Is the information factually accurate?",
        "pass_threshold": 4.0,
        "weight": 2.0,  # Critical category
        "reference_examples": {...}
    },
    # ... more categories
}

# LLM-as-judge implementation with temperature=0
def evaluate_response(query, response):
    judge_prompt = create_judge_prompt(query, response, RUBRIC)
    scores = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        temperature=0,  # Deterministic scoring
        messages=[{"role": "user", "content": judge_prompt}]
    )
    return parse_scores(scores)
```

### Results Dashboard (HTML)
![Results Dashboard](docs/images/dashboard-screenshot.png) ← *Coming soon*

---

## 🎯 Use Cases

### ✅ Customer Support Bots
- Measure: Correctness, Deflection, Empathy, Resolution
- Outcome: Reduce tickets, improve CSAT

### ✅ Code Generation Tools
- Measure: Correctness, Quality, Safety, Documentation
- Outcome: Working code, best practices

### ✅ Content Generation
- Measure: Accuracy, Tone, Engagement, Brand consistency
- Outcome: Quality content, brand alignment

### ✅ RAG Systems
- Measure: Retrieval accuracy, Grounding, Hallucination avoidance
- Outcome: Factual, cited responses

### ✅ Classification & Moderation Agents
- Measure: Precision, Recall, F1 (via ground truth labels), plus LLM rubric scores
- Outcome: Accurate triage, routing, spam/content filtering with measurable error rates

---

## 🧪 Example: Fitness Coach Agent

**Input:**
```
Prompt: "You are a fitness and nutrition coach..."
Outcomes: ["Help people live healthier lives and achieve fitness goals"]
```

**Generated Rubric (6 categories):**
1. Personalization (≥4.0, 2x weight) - Accounts for user stats/goals
2. Safety (≥4.5, 2x weight) - No dangerous advice
3. Accuracy (≥4.0, 2x weight) - Correct calculations
4. Completeness (≥4.0, 1.5x weight) - All plan components
5. Practicality (≥3.5, 1.5x weight) - Realistic to follow
6. Tone (≥3.5) - Encouraging, supportive

**Test Results (10 cases):**
- Overall: 70% pass rate
- Safety: 4.8/5.0 ✅ (critical for fitness)
- Personalization: 4.1/5.0 ✅
- Identified issues: Some plans too generic, missing medical disclaimers

**See:** [examples/fitness_coach/](examples/fitness_coach/) for full output

---

## 🏆 Best Practices Embedded

EvalCraft implements research from:
- **Hamel Husain & Shreya Shankar** (AI Evals for Engineers & PMs)
- **Aakash Gupta** (Product Growth - AI Evals)
- Industry LLM-as-judge patterns

**Key principles:**
- ✅ Binary pass/fail thresholds (even with 1-5 scales)
- ✅ Product-specific evals over generic metrics
- ✅ Concrete reference examples for calibration
- ✅ Temperature=0 for judges (deterministic)
- ✅ Stronger model as judge (Sonnet judges your product)
- ✅ Don't optimize for high pass rates (70% can be better than 100%)

---

## 📂 Project Structure

```
evalcraft/
├── SKILL.md                          # Claude Code skill orchestrator
├── README.md                         # This file
├── LICENSE                           # MIT License
├── requirements.txt                  # Python dependencies
├── scripts/
│   ├── generate_rubric.py            # AI-powered rubric generation
│   └── generate_eval_code.py         # Code generator
├── templates/
│   ├── rubric_template.md            # Rubric structure
│   └── eval_code_template.py         # Python eval framework
├── references/
│   ├── eval_best_practices.md        # Synthesized knowledge
│   ├── rubric_building_guide.md      # Step-by-step guide
│   └── llm_judge_patterns.md         # LLM-as-judge patterns
├── examples/
│   ├── fitness_coach/                # Complete example
│   ├── customer_support/             # Another example
│   └── sample_dataset.csv            # Dataset format
├── docs/
│   ├── images/                       # Screenshots
│   └── ARCHITECTURE.md               # Technical details
└── PHASE2_RESUMPTION_GUIDE.md        # Web UI roadmap
```

---

## 🛠️ Development

### Running Tests

```bash
# Test rubric generation
python scripts/generate_rubric.py \
  --agent-prompt "Test prompt" \
  --outcomes '["Test outcome"]' \
  --output-dir ./test_output

# Test code generation
python scripts/generate_eval_code.py \
  --rubric ./test_output/rubric.json \
  --output-dir ./test_output

# Test evaluation
cd ./test_output
python evaluate.py --input ../examples/sample_dataset.csv
```

### Contributing

Contributions welcome! Please:
1. Fork the repo
2. Create a feature branch
3. Add tests if applicable
4. Submit PR with clear description

---

## 📈 Roadmap

### Phase 1: Claude Skill ✅ (Complete)
- [x] Rubric generation from prompt + outcomes
- [x] LLM-as-judge code generation
- [x] Evaluation execution
- [x] Interactive HTML reports
- [x] Iteration support
- [x] Classification task detection + confusion matrix metrics (precision, recall, F1, accuracy)

### Phase 2: Web UI 🚧 (Planned)
- [ ] Visual rubric builder
- [ ] Drag-and-drop test data upload
- [ ] Real-time evaluation dashboard
- [ ] Rubric version comparison
- [ ] Team collaboration
- [ ] Hosted version (SaaS)

See [PHASE2_RESUMPTION_GUIDE.md](./PHASE2_RESUMPTION_GUIDE.md) for details.

### Future Ideas 💡
- Integration with Braintrust, LangSmith
- Pre-built rubric templates (20+ use cases)
- Automated regression testing (run on every prompt change)
- Multi-model judge comparison (Claude vs GPT-4)
- Slack/email notifications

---

## 💰 Cost

**Very affordable:**
- 10 test cases: ~$0.20
- 100 test cases: ~$2.00
- Rubric generation: ~$0.05 per rubric

*Based on Claude Sonnet 4.5 pricing (March 2026)*

---

## 🤝 Acknowledgments

Built with:
- [Claude API](https://www.anthropic.com) (LLM-as-judge + rubric generation)
- [Claude Code](https://claude.com/claude-code) (skill framework)

Inspired by:
- Hamel Husain & Shreya Shankar's eval research
- Aakash Gupta's PM-focused eval frameworks
- Braintrust, LangSmith, Promptfoo

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

## 👤 Author

**Karim Ezzouek**

Building AI products and tooling for PMs.

- Portfolio: [your-portfolio-link]
- LinkedIn: [your-linkedin]
- Twitter: [@your-handle]

---

## ⭐ Support

If EvalCraft helps you build better AI products:
- Star this repo ⭐
- Share with other PMs
- [Open an issue](https://github.com/KarimLondon/evalcraft/issues) with feedback

---

**Built to solve a real PM problem. Designed for ease of use. Ready for production.** 🚀
