# AI Evaluation Best Practices

**Synthesized from industry research and PM eval knowledge base**

---

## Core Principles

### 1. The Three Types of Evals (All Required)

**Offline Evals (Pre-Launch)**
- Testing before the feature ships
- Tells you if the feature is ready for production
- Run eval suite against test cases to establish baselines

**Online Evals (Post-Launch)**
- Monitoring after launch in production
- Tells you if the feature is working with real users
- Includes system metrics, quality metrics, and business metrics

**Human Evals (Ongoing)**
- Spot-checking quality with real human reviewers
- Tells you if users actually like the output
- Sample 1% of production traffic daily for manual review

*Skip any of these and your feature will fail.*

---

## Rubric Design

### Start With Product Outcomes, Not Metrics

**Key Question:** What does success look like for your product?

Example outcomes and their eval categories:
- **Reduce support tickets** → Deflection Potential, Completeness, Clarity
- **Improve code quality** → Correctness, Style Adherence, Efficiency
- **Increase engagement** → Tone, Relevance, Conciseness

### Rubric Structure (4-6 Categories)

**Good rubric categories:**
1. **Correctness** - Is the answer factually correct?
2. **Completeness** - Does it address all parts of the query?
3. **Clarity** - Is it easy to understand?
4. **Tone** - Does it match brand voice?
5. **Safety** - Does it avoid harmful content?
6. **Efficiency** - Is it concise without being terse?

**Each category needs:**
- 1-5 scale with clear definitions for each level
- Concrete reference examples (scores 1, 3, 5)
- Binary pass/fail threshold (e.g., ≥4.0 to pass)

### Reference Examples Are Critical

**Bad example (too abstract):**
- Score 3: "Response is helpful"

**Good example (concrete):**
- Score 5: "Our return policy allows returns within 30 days of purchase. Visit returns.company.com to start your return. You'll receive a full refund within 5-7 business days."
- Score 3: "You can return items within 30 days. Check our website for details."
- Score 1: "We don't accept returns." (Factually wrong)

### Test Your Rubric for Inter-Rater Reliability

Have 2-3 people independently grade the same 10 outputs. If they disagree on scores, your rubric is ambiguous—refine it.

---

## LLM-as-Judge Implementation

### Core Pattern

Use a stronger LLM (e.g., Claude 3.5 Sonnet or GPT-4) to grade your product's outputs.

**Judge prompt must include:**
1. The rubric (scoring criteria)
2. Reference examples (what scores 1, 3, 5 look like)
3. The input query
4. The output to evaluate

### Critical Best Practices

**1. Use Temperature=0 for Judges**
- Deterministic scoring is essential
- You want consistent evaluation, not creative variation

**2. Use a Stronger Model as Judge**
- Don't use the same model as judge and product
- Example: If your product uses GPT-3.5, use GPT-4 as judge

**3. Don't Judge Too Many Dimensions at Once**
- If ≤4 categories: One holistic judge call
- If >4 categories: Separate judge calls per category
- Prevents overwhelmed responses

**4. Calibrate Your Judge Against Human Scores**
- Regularly compare judge scores to human scores
- Adjust prompts if correlation is poor
- Never fully automate without validation

**5. Include Chain-of-Thought Reasoning**
- Ask judge to "explain your reasoning before scoring"
- Makes debugging easier
- Improves score accuracy

---

## Labels and Scoring

### Prefer Binary Labels Over Likert Scales

**Problem with Likert (1-5):**
- Difference between 3 and 4 is subjective
- Hard to calibrate human annotators
- Hard to calibrate LLM judges

**Binary solution:**
- Even with 1-5 rubrics, convert to pass/fail
- Set clear threshold (e.g., ≥4.0 = pass)
- Makes decisions unambiguous

### Don't Optimize for High Pass Rates

**If you're passing 100% of evals, you're not challenging your system enough.**

A 70% pass rate might indicate more meaningful evaluation than 100%. Focus on evals that catch real issues, not ones that make metrics look good.

---

## Dataset Creation

### Prefer Real Data Over Synthetic

**Best practice hierarchy:**
1. **Real labeled data** - Actual user queries with ground truth
2. **Real unlabeled data + manual annotation** - Annotate as you eval
3. **Synthetic data from weaker models** - Use GPT-3.5 to generate failures for GPT-4 eval
4. **Synthetic data from strong models** - Last resort (tends to be out-of-distribution)

### Start With Error Analysis

**Before building evals:**
1. Manually review 50-100 real user traces
2. Identify the most common failure modes
3. Categorize failures
4. Reach "theoretical saturation" (no new failure types)

Many issues will be straightforward bugs you can fix immediately—no eval infrastructure needed.

### Dataset Size

- **Minimum:** 50-100 test cases with at least 20-30 failure cases
- **Ideal:** 200+ cases with diverse failure modes
- **Production sampling:** 1% of daily traffic for ongoing eval

---

## Metrics Framework

### Choose Metrics Based on Use Case

| Use Case | Primary Metrics |
|----------|----------------|
| Retrieving documents (RAG) | Precision, Recall, F1, NDCG |
| Generating text similar to reference | BERTScore |
| Task-specific (code, support, etc.) | Custom task metrics |
| Measuring quality holistically | LLM-as-judge |

### Most Products Need Multiple Metrics

Don't rely on just one metric. Example for customer support bot:
- **Retrieval metrics:** Does it find the right knowledge base article?
- **Generation metrics:** Is the response well-formed?
- **Task metrics:** Does it include required links? Correct policy info?
- **LLM-as-judge:** Overall helpfulness and tone

---

## Production Monitoring (Three Layers)

### Layer 1: System Metrics
- Latency (p50, p95, p99)
- Error rates
- Token usage / API costs
- Timeout rates

### Layer 2: Quality Metrics
- Average LLM judge scores (on sampled traffic)
- Human feedback scores (thumbs up/down)
- Task success rate
- Hallucination rate

### Layer 3: Business Metrics
- Feature adoption rate
- User retention
- Customer satisfaction (CSAT/NPS)
- Support ticket deflection
- Revenue impact

**You need all three layers:**
- System metrics without quality metrics = blind to bad outputs
- Quality metrics without business metrics = no idea if it matters

---

## Common Pitfalls to Avoid

### 1. Stacking Abstractions
**Problem:** AI agent creates rubric AND judges outputs
**Risk:** High scores hide flaws behind automation
**Solution:** Human validation of rubric before automating

### 2. Using Same Model for Product and Judge
**Problem:** Model can't effectively judge its own outputs
**Solution:** Use stronger model as judge

### 3. Not Calibrating Judges
**Problem:** Judge scores diverge from human judgment
**Solution:** Regularly compare to human scores and refine prompts

### 4. Outsourcing Annotation
**Problem:** Annotators don't understand domain nuances
**Solution:** Domain experts must do annotation

### 5. Evaluating Only Happy Paths
**Problem:** Edge cases and failures aren't tested
**Solution:** Use "unhappy paths" approach—define what bad looks like first

### 6. Ignoring Context Window Effects
**Problem:** Quality degrades as context fills ("lost in the middle")
**Solution:** Test at different context lengths matching production usage

### 7. Not Testing Prompt Sensitivity
**Problem:** Small prompt changes break everything
**Solution:** Test multiple prompt variations users might type

---

## The Feedback Loop

**Production monitoring should feed back into your eval dataset:**

1. User reports issue → Add to eval dataset
2. Low judge scores in production → Investigate and add test cases
3. New failure mode discovered → Update rubric
4. Rubric updated → Regenerate eval code
5. Run updated evals → Verify fix → Deploy

This creates a virtuous cycle where evals improve over time.

---

## Key Takeaways for PMs

1. **Evals are the new PRDs** - Well-crafted eval prompts become living product requirements
2. **PMs should own evals** - You understand outcomes, customers, and business value
3. **Expect 60-80% of dev time on evals** - This is part of development, not a separate line item
4. **Start simple, iterate** - Better to have basic evals running than perfect evals planned
5. **Don't ship without evals** - The cost of blind deployment is too high

---

*This guide synthesizes best practices from:*
- *Hamel Husain & Shreya Shankar (AI Evals for Engineers & PMs)*
- *Aakash Gupta (Product Growth)*
- *Industry experience with LLM-as-judge patterns*
