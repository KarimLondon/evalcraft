# Rubric Building Guide

**A step-by-step guide for creating effective evaluation rubrics**

---

## Step 1: Define User Scenarios

**Start with the user, not the AI.**

What are the top 10 scenarios your users will encounter?

### Example: Customer Support Chatbot
1. User asks about return policy
2. User asks about shipping times
3. User asks about product specifications
4. User asks about account issues
5. User asks unclear questions
6. User asks about order status
7. User requests cancellation
8. User reports damaged item
9. User asks about warranty
10. User asks multiple questions at once

### Example: Code Generation Tool
1. User requests a simple function
2. User requests a complex algorithm
3. User requests refactoring
4. User requests bug fixes
5. User requests tests
6. User requests documentation
7. User provides ambiguous requirements
8. User asks for optimization
9. User requests integration code
10. User asks for error handling

**Write these down. These become your test cases.**

---

## Step 2: Map Scenarios to Product Outcomes

Connect each scenario to your product goals.

### Example: Support Bot with Goal "Reduce tickets by 30%"

| Scenario | Success Looks Like | Eval Category |
|----------|-------------------|---------------|
| Return policy question | Complete answer with link → no human ticket | Completeness, Deflection |
| Unclear question | Clarifying questions OR best-effort answer | Helpfulness |
| Multiple questions | Addresses all parts | Completeness |
| Account issue | Correct escalation path | Correctness |

**This is how you ensure product-specific evals, not generic ones.**

---

## Step 3: Select 4-6 Rubric Categories

### Common Categories by Domain

**Customer Support:**
- Correctness (factual accuracy)
- Completeness (addresses all parts)
- Clarity (easy to understand)
- Tone (brand voice match)
- Deflection Potential (prevents escalation)

**Code Generation:**
- Correctness (works as intended)
- Code Quality (follows style, readable)
- Efficiency (performance considerations)
- Safety (error handling, security)
- Documentation (comments, docstrings)

**Content Generation:**
- Accuracy (factually correct)
- Tone (matches brand/audience)
- Engagement (compelling, interesting)
- Structure (well-organized)
- Conciseness (no unnecessary length)

**RAG / Search Systems:**
- Retrieval Accuracy (found right docs)
- Grounding (cites sources correctly)
- Completeness (uses all relevant info)
- Hallucination Avoidance (doesn't make up facts)

### How Many Categories?

- **Too few (1-2):** Miss important dimensions
- **Just right (4-6):** Comprehensive but manageable
- **Too many (7+):** Overwhelming for judges, hard to calibrate

---

## Step 4: Define Success Criteria

For each category, define what success looks like.

### Bad Success Criteria (Vague)
❌ "The response is helpful"
❌ "The code works"
❌ "The tone is good"

### Good Success Criteria (Specific)
✅ "The response contains the correct return window (30 days) and includes the return portal link"
✅ "The code passes all test cases, follows project style guide, and includes error handling"
✅ "The tone is friendly and professional, uses brand voice guidelines (conversational, not formal)"

**Make it specific. Measurable. Unambiguous.**

---

## Step 5: Create the 1-5 Scale Definitions

For each category, define what each score level means.

### Template Structure

**Category: [Name]**
**Description:** [What this measures]
**Pass Threshold:** [Minimum score to pass, e.g., 4.0]

**Scale:**
- **5 - Excellent:** [Specific criteria]
- **4 - Good:** [Specific criteria]
- **3 - Acceptable:** [Specific criteria]
- **2 - Poor:** [Specific criteria]
- **1 - Failing:** [Specific criteria]

### Example: Correctness for Customer Support

**Category: Correctness**
**Description:** Is the information factually accurate?
**Pass Threshold:** 4.0

**Scale:**
- **5 - Excellent:** All information is factually correct. Policies, dates, numbers, and procedures are accurate.
- **4 - Good:** Information is mostly correct with minor inaccuracies that don't affect the core answer (e.g., slightly off timeframe).
- **3 - Acceptable:** Core information is correct but missing some details or has minor errors.
- **2 - Poor:** Contains significant factual errors that could mislead the user.
- **1 - Failing:** Completely incorrect or provides wrong information that could harm the user.

---

## Step 6: Create Reference Examples

**This is the most important step. Don't skip it.**

For each category, create concrete examples showing what scores 1, 3, and 5 look like.

### Example: Correctness Reference Examples

**User Query:** "What's your return policy?"

**Score 5 (Excellent):**
```
Our return policy allows returns within 30 days of purchase for most items.
To start a return, visit returns.company.com and enter your order number.
You'll receive a full refund to your original payment method within 5-7
business days after we receive the item.

Note: Personalized items and final sale items cannot be returned.
```
*Why 5: All facts correct (30 days, refund timeline, exclusions), includes actionable link*

**Score 3 (Acceptable):**
```
You can return items within 30 days. Check our website for the return process.
```
*Why 3: Core fact correct (30 days) but missing important details (how to return, refund timeline)*

**Score 1 (Failing):**
```
We don't accept returns. All sales are final.
```
*Why 1: Completely incorrect—contradicts actual policy*

### Why Reference Examples Matter

1. **Calibrate human annotators** - Everyone grades consistently
2. **Calibrate LLM judges** - Include in judge prompts
3. **Document edge cases** - Show what borderline looks like
4. **Make rubric concrete** - No room for interpretation

---

## Step 7: Set Pass/Fail Thresholds

Even with 1-5 scales, convert to binary pass/fail.

### Recommended Thresholds

**Strict (high-stakes domains):**
- All categories must be ≥ 4.5
- Use for: Medical advice, legal, financial, safety-critical

**Standard (most products):**
- Critical categories (Correctness, Safety) ≥ 4.0
- Nice-to-have categories (Tone, Efficiency) ≥ 3.5
- Use for: Customer support, content generation, most tools

**Lenient (early development):**
- All categories ≥ 3.0
- Use for: Prototypes, rapid iteration, exploratory phase

### Overall Pass Logic

**Option 1: All categories must pass (AND logic)**
```
pass_threshold = {
    "correctness": 4.0,
    "completeness": 4.0,
    "tone": 3.5
}
overall_pass = all(scores[cat] >= threshold for cat, threshold in pass_threshold.items())
```

**Option 2: Average must pass (weighted average)**
```
weights = {
    "correctness": 2.0,  # Double weight
    "completeness": 1.5,
    "tone": 1.0
}
weighted_avg = sum(scores[cat] * weights[cat] for cat in categories) / sum(weights.values())
overall_pass = weighted_avg >= 4.0
```

**Recommended: Option 1 (all must pass) for production readiness**

---

## Step 8: Test Inter-Rater Reliability

Have 2-3 people independently grade the same 10 outputs using your rubric.

### Calculate Agreement

**Simple method:**
```
agreement_rate = (number of matching scores) / (total scores)

Example:
Rater 1: [4, 5, 3, 4, 5, 2, 5, 4, 3, 5]
Rater 2: [4, 4, 3, 4, 5, 2, 5, 3, 3, 5]

Matches: 8/10 = 80% agreement
```

**Target:** ≥70% exact agreement, ≥90% within 1 point

### If Agreement is Low

**Common issues and fixes:**

1. **Vague scale definitions** → Make each level more specific
2. **Missing reference examples** → Add more examples
3. **Ambiguous category** → Split into two categories or clarify description
4. **Raters need training** → Review examples together, discuss disagreements

**Iterate until multiple evaluators give similar scores.**

---

## Step 9: Version and Iterate

Rubrics evolve as you learn more about failure modes.

### Version Control Pattern

```
rubric_v1.json - Initial rubric (4 categories)
rubric_v2.json - Added "Safety" category after production incidents
rubric_v3.json - Refined "Completeness" scale after low inter-rater reliability
```

### When to Update Your Rubric

- **New failure mode discovered** in production
- **Inter-rater reliability drops** below 70%
- **Product outcomes change** (new goals)
- **LLM judge calibration issues** (scores don't match human judgment)

---

## Complete Example: E-commerce Support Bot

### Product Context
- **Goal:** Reduce support tickets by 30%
- **Agent:** Customer support chatbot for e-commerce site
- **Common queries:** Returns, shipping, products, accounts

### Rubric

**Categories: 5 (Correctness, Completeness, Deflection, Clarity, Tone)**

---

#### Category 1: Correctness
**Description:** Is the information factually accurate based on our policies?
**Pass Threshold:** 4.0

**Scale:**
- 5: All facts correct (policies, timelines, procedures)
- 4: Mostly correct, minor details off
- 3: Core facts right, some details wrong
- 2: Significant factual errors
- 1: Completely wrong information

**Reference Examples:**
- Score 5: "Returns accepted within 30 days. Visit returns.site.com. Refund in 5-7 days."
- Score 3: "Returns accepted within 30 days. Contact support for return process." (Missing self-service link)
- Score 1: "No returns accepted." (Factually wrong)

---

#### Category 2: Completeness
**Description:** Does it fully address all parts of the user's query?
**Pass Threshold:** 4.0

**Scale:**
- 5: Addresses every part of query with sufficient detail
- 4: Addresses all parts, some could be more detailed
- 3: Addresses main question but misses secondary points
- 2: Partially addresses query, key points missing
- 1: Doesn't address the query

**Reference Examples:**
- Score 5: (For "How do I return a damaged item?") Explains return process + emphasizes damage documentation + mentions refund timeline
- Score 3: (Same query) Explains return process only, misses damage-specific steps
- Score 1: (Same query) Generic response about returns, doesn't mention damage case

---

#### Category 3: Deflection Potential
**Description:** Will this response prevent the user from creating a support ticket?
**Pass Threshold:** 4.0

**Scale:**
- 5: Completely self-service, no escalation needed
- 4: Mostly self-service, minor follow-up possible
- 3: Partially self-service, might need human help
- 2: Likely requires human escalation
- 1: Forces escalation or doesn't help at all

**Reference Examples:**
- Score 5: Includes direct link, step-by-step instructions, troubleshooting tips
- Score 3: Explains process but user must search for link or contact support
- Score 1: "Please contact our support team for help."

---

#### Category 4: Clarity
**Description:** Is the response easy to understand for the average customer?
**Pass Threshold:** 3.5

**Scale:**
- 5: Crystal clear, simple language, well-structured
- 4: Clear but could be more concise or better structured
- 3: Understandable but requires some effort
- 2: Confusing, unclear, or overly complex
- 1: Incomprehensible or contradictory

**Reference Examples:**
- Score 5: Numbered steps, short sentences, no jargon
- Score 3: Long paragraph format, some complex terms
- Score 1: Contradictory statements, run-on sentences, unclear structure

---

#### Category 5: Tone
**Description:** Does the response match our brand voice (friendly, helpful, empathetic)?
**Pass Threshold:** 3.5

**Scale:**
- 5: Perfectly friendly and empathetic, natural conversation
- 4: Friendly but slightly formal or generic
- 3: Neutral, functional but not warm
- 2: Cold, robotic, or overly formal
- 1: Rude, dismissive, or inappropriate

**Reference Examples:**
- Score 5: "I'm sorry to hear about the issue! Let me help you get this resolved quickly."
- Score 3: "Please follow the return process outlined below."
- Score 1: "Returns must be initiated according to policy."

---

### Pass Logic
```
pass_thresholds = {
    "correctness": 4.0,      # Critical
    "completeness": 4.0,     # Critical
    "deflection": 4.0,       # Critical for goal
    "clarity": 3.5,          # Important
    "tone": 3.5              # Nice-to-have
}

overall_pass = all(scores[cat] >= thresh for cat, thresh in pass_thresholds.items())
```

---

## Checklist: Is Your Rubric Ready?

- [ ] 4-6 categories aligned with product outcomes
- [ ] Each category has clear description
- [ ] 1-5 scale defined for each category
- [ ] Reference examples for scores 1, 3, 5 for each category
- [ ] Pass/fail thresholds set
- [ ] Tested with 2-3 human raters (≥70% agreement)
- [ ] Concrete, specific, measurable (no vague language)

---

**Your rubric is the foundation of your entire eval system. Invest time here.**
