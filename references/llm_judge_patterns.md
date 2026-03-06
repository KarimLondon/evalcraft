# LLM-as-Judge Implementation Patterns

**Proven patterns for using LLMs to evaluate AI outputs**

---

## Core Concept

Instead of using traditional metrics (BLEU, ROUGE, etc.), use a strong LLM to grade outputs based on your rubric.

**Why this works:**
- LLM judges often correlate better with human judgment than traditional metrics
- Can evaluate subjective qualities (tone, helpfulness, clarity)
- Flexible - works across different use cases
- Fast to implement compared to building custom metrics

---

## The Basic Pattern

### Judge Prompt Structure

```
You are an expert evaluator for [domain].

Evaluate the following response using these criteria:

[RUBRIC CATEGORIES AND SCALES]

[REFERENCE EXAMPLES]

User Query: {query}
Assistant Response: {response}

Provide scores for each criterion and justification.
```

### Example Judge Prompt

```
You are an expert evaluator for customer support chatbots.

Evaluate the following response on these criteria:

1. Correctness (1-5): Is the information factually accurate?
   - 5: All facts correct
   - 3: Core facts right, some details wrong
   - 1: Completely wrong

2. Completeness (1-5): Does it fully address the query?
   - 5: Addresses all parts with detail
   - 3: Addresses main question, misses secondary points
   - 1: Doesn't address the query

3. Tone (1-5): Does it match our friendly, helpful brand voice?
   - 5: Perfectly friendly and empathetic
   - 3: Neutral, functional
   - 1: Cold or dismissive

Reference Examples:
[Correctness - Score 5]: "Our return policy allows returns within 30 days..."
[Correctness - Score 3]: "You can return items within 30 days. Check our website..."
[Correctness - Score 1]: "We don't accept returns."

User Query: {query}
Assistant Response: {response}

Provide scores and brief justification for each criterion.
```

---

## Critical Implementation Details

### 1. Temperature = 0 (Deterministic Scoring)

**Always use temperature=0 for judge calls.**

```python
# ✅ Correct
judge_response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    temperature=0,  # Deterministic
    max_tokens=2048,
    messages=[...]
)

# ❌ Wrong
judge_response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    temperature=0.7,  # Non-deterministic - scores will vary
    max_tokens=2048,
    messages=[...]
)
```

**Why:** Evaluation should be consistent. Same input → same score.

### 2. Use a Stronger Model as Judge

**Don't judge your product with the same model.**

| Product Model | Judge Model |
|--------------|-------------|
| GPT-3.5 Turbo | GPT-4 or Claude 3.5 Sonnet |
| Claude 3 Haiku | Claude 3.5 Sonnet or Opus |
| GPT-4 | GPT-4 Turbo or Claude 3 Opus |
| Open-source (Llama, etc.) | Any frontier model |

**Why:** Models can't effectively judge their own outputs. Use a more capable model.

### 3. Include Chain-of-Thought Reasoning

**Ask the judge to explain before scoring.**

```
Before providing scores, explain your reasoning for each criterion.

Reasoning:
[Judge explains thinking]

Scores:
- Correctness: 4/5
- Completeness: 5/5
- Tone: 4/5
```

**Why:**
- Improves accuracy (judge thinks through evaluation)
- Makes debugging easier (you can see why it scored something)
- Helps calibrate against human judgment

### 4. Structured Output Format

**Request scores in parseable format.**

**Option 1: JSON output**
```
Provide your evaluation in this JSON format:
{
  "correctness": {
    "score": 4,
    "reasoning": "..."
  },
  "completeness": {
    "score": 5,
    "reasoning": "..."
  },
  "tone": {
    "score": 4,
    "reasoning": "..."
  }
}
```

**Option 2: Markdown format**
```
## Correctness: 4/5
Reasoning: [explanation]

## Completeness: 5/5
Reasoning: [explanation]

## Tone: 4/5
Reasoning: [explanation]
```

**Parsing tip:** JSON is easier to parse programmatically, but markdown is more reliable with some models.

---

## Advanced Patterns

### Pattern 1: Holistic vs. Per-Category Judging

**Holistic (Single Call)** - One judge call evaluates all categories
- **Pros:** Faster, cheaper, sees full context
- **Cons:** Can get overwhelmed with many categories
- **Best for:** ≤4 categories

**Per-Category (Multiple Calls)** - Separate judge call per category
- **Pros:** More focused, better for complex rubrics
- **Cons:** Slower, more expensive, loses cross-category context
- **Best for:** >4 categories

**Adaptive approach:**
```python
if len(rubric_categories) <= 4:
    # Single holistic judge call
    score = judge_holistic(query, response, rubric)
else:
    # Multiple focused judge calls
    scores = {cat: judge_category(query, response, cat, rubric[cat])
              for cat in rubric_categories}
```

### Pattern 2: Comparative Judging

Instead of scoring individually, compare two outputs.

**Use case:** A/B testing prompt changes

**Judge prompt:**
```
Which response is better for this query?

Query: {query}
Response A: {response_a}
Response B: {response_b}

Which is better on:
- Correctness
- Completeness
- Tone

Provide reasoning and declare a winner.
```

**Why:** Often easier for judges to compare than to score absolutely.

### Pattern 3: Multi-Judge Ensemble

Use multiple judge calls and aggregate scores.

```python
def ensemble_judge(query, response, rubric, num_judges=3):
    scores = []
    for i in range(num_judges):
        score = judge_single(query, response, rubric)
        scores.append(score)

    # Aggregate (e.g., median or mean)
    return {
        cat: np.median([s[cat] for s in scores])
        for cat in rubric.keys()
    }
```

**Pros:** More robust, reduces noise
**Cons:** 3x the cost
**Best for:** High-stakes decisions, production monitoring

### Pattern 4: Self-Consistency Check

Ask judge to score twice, check if scores match.

```python
score_1 = judge(query, response, rubric, temperature=0)
score_2 = judge(query, response, rubric, temperature=0)

if score_1 != score_2:
    # Judge is inconsistent - flag for human review
    flag_for_review(query, response, score_1, score_2)
```

**Why:** Catch edge cases where judge is uncertain.

### Pattern 5: Confidence Scoring

Ask judge to provide confidence level with scores.

```
For each criterion, provide:
- Score (1-5)
- Confidence (low/medium/high)
- Reasoning

Low confidence scores should be reviewed by humans.
```

**Why:** Identifies cases that need human validation.

---

## Calibration Against Human Scores

**LLM judges need calibration.** Don't trust blindly.

### Calibration Process

1. **Collect human-scored examples** (50-100 cases)
2. **Run LLM judge on same examples**
3. **Calculate correlation**
4. **If correlation < 0.7, refine judge prompt**
5. **Repeat until calibrated**

### Measuring Agreement

```python
from scipy.stats import pearsonr, spearmanr

human_scores = [4, 5, 3, 4, 2, ...]
llm_scores = [4, 4, 3, 5, 2, ...]

# Pearson correlation (for continuous scores)
correlation, p_value = pearsonr(human_scores, llm_scores)
print(f"Correlation: {correlation:.2f}")

# Spearman correlation (for ranked scores, more robust)
correlation, p_value = spearmanr(human_scores, llm_scores)
print(f"Spearman: {correlation:.2f}")

# Target: > 0.7 correlation
```

### Common Calibration Issues and Fixes

| Issue | Fix |
|-------|-----|
| Judge too lenient (scores too high) | Add more score 1-2 reference examples |
| Judge too strict (scores too low) | Add more score 4-5 reference examples |
| Inconsistent on edge cases | Add borderline examples (scores 2-4) |
| Misses specific issues | Make rubric more specific, add task examples |
| Ignores certain categories | Put important categories first in prompt |

---

## Pitfall Avoidance

### Pitfall 1: Judging Too Many Dimensions

**Problem:** One judge call tries to evaluate 8+ categories
**Result:** Overwhelmed judge, poor scores, missed details

**Solution:**
- If ≤4 categories: Single judge call
- If 5-6 categories: Consider splitting
- If >6 categories: Definitely split into multiple calls

### Pitfall 2: Not Using Reference Examples

**Problem:** Rubric has abstract scales without examples
**Result:** Judge scores inconsistently, doesn't match human judgment

**Solution:** Always include reference examples in judge prompt

### Pitfall 3: Vague Rubric Language

**Problem:** "Rate helpfulness on 1-5" without defining what each score means
**Result:** Judge interprets differently than you intend

**Solution:** Define every scale level explicitly

### Pitfall 4: Ignoring Judge Reasoning

**Problem:** Only parse scores, ignore explanations
**Result:** Can't debug why certain cases score poorly

**Solution:** Save judge reasoning with scores, review for calibration

### Pitfall 5: No Human Validation

**Problem:** Fully automated judging with no human oversight
**Result:** Broken eval system nobody notices

**Solution:**
- Human review 1% of judge outputs daily
- Flag low-confidence or outlier scores for review
- Recalibrate quarterly

---

## Code Implementation Example

### Complete Judge Implementation

```python
import os
import json
from anthropic import Anthropic

def create_judge_prompt(query, response, rubric):
    """Generate LLM-as-judge prompt."""

    prompt = "You are an expert evaluator.\n\n"
    prompt += "Evaluate the following response using these criteria:\n\n"

    # Add rubric categories
    for i, (category, details) in enumerate(rubric.items(), 1):
        prompt += f"{i}. {category.title()} (1-5): {details['description']}\n"
        prompt += f"   Scale: {details['scale']}\n\n"

    # Add reference examples
    prompt += "Reference Examples:\n"
    for category, details in rubric.items():
        if 'reference_examples' in details:
            for score, example in details['reference_examples'].items():
                prompt += f"[{category.title()} - Score {score}]: \"{example}\"\n"

    # Add query and response
    prompt += f"\n\nUser Query: {query}\n"
    prompt += f"Assistant Response: {response}\n\n"

    # Request structured output
    prompt += """Provide your evaluation in JSON format:
{
  "category_name": {
    "score": <1-5>,
    "reasoning": "<explanation>"
  },
  ...
}"""

    return prompt

def judge_response(query, response, rubric, model="claude-3-5-sonnet-20241022"):
    """Run LLM-as-judge evaluation."""

    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    judge_prompt = create_judge_prompt(query, response, rubric)

    # Call judge with temperature=0
    judge_response = client.messages.create(
        model=model,
        temperature=0,  # Deterministic scoring
        max_tokens=2048,
        messages=[
            {"role": "user", "content": judge_prompt}
        ]
    )

    # Parse response
    judge_text = judge_response.content[0].text

    try:
        scores = json.loads(judge_text)
    except json.JSONDecodeError:
        # Fallback: extract scores from text
        scores = parse_scores_from_text(judge_text, rubric)

    return scores

def parse_scores_from_text(text, rubric):
    """Fallback parser if JSON fails."""
    import re

    scores = {}
    for category in rubric.keys():
        # Look for "category: X/5" or "category: X"
        pattern = rf"{category}.*?(\d)/5"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            scores[category] = {
                "score": int(match.group(1)),
                "reasoning": "Extracted from text"
            }

    return scores

# Example usage
rubric = {
    "correctness": {
        "description": "Is the information factually accurate?",
        "scale": "1 (completely wrong) to 5 (fully correct)",
        "pass_threshold": 4.0,
        "reference_examples": {
            5: "Our return policy allows returns within 30 days...",
            3: "You can return items within 30 days.",
            1: "We don't accept returns."
        }
    },
    "completeness": {
        "description": "Does it fully address the query?",
        "scale": "1 (doesn't address) to 5 (fully addresses all parts)",
        "pass_threshold": 4.0
    }
}

query = "What's your return policy?"
response = "You can return most items within 30 days. Visit our returns page for details."

scores = judge_response(query, response, rubric)
print(json.dumps(scores, indent=2))
```

---

## Best Practices Summary

✅ **DO:**
- Use temperature=0 for all judge calls
- Use a stronger model as judge than your product model
- Include chain-of-thought reasoning
- Provide concrete reference examples
- Calibrate against human scores regularly
- Save judge reasoning with scores
- Split complex rubrics (>4 categories) into multiple calls

❌ **DON'T:**
- Use the same model as judge and product
- Judge too many dimensions in one call (>6 categories)
- Skip reference examples
- Use temperature > 0 for judges
- Fully automate without human validation
- Ignore judge reasoning
- Trust scores without calibration

---

**LLM-as-judge is powerful but requires careful implementation. Follow these patterns for reliable evaluation.**
