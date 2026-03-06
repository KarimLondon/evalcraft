# Customer Support Bot - Evaluation Rubric

**Agent Purpose:** E-commerce customer support chatbot that handles returns, shipping, products, and account queries
**Product Outcomes:** Reduce support tickets by 30%, improve customer satisfaction
**Generated:** 2026-03-06

---

## Evaluation Categories

This rubric defines how we evaluate AI agent outputs. Each category has a 1-5 scale with reference examples.

### 1. Correctness

**Description:** Is the information factually accurate based on company policies?

**What This Measures:** Whether the agent provides accurate information about returns, shipping, products, and policies without hallucinating or misrepresenting facts.

**Pass Threshold:** ≥ 4.0/5.0

**Scoring Scale:**

| Score | Level | Definition |
|-------|-------|------------|
| 5 | Excellent | All information is factually correct - policies, dates, numbers, procedures are accurate |
| 4 | Good | Mostly correct with minor details slightly off (e.g., timeframe off by 1-2 days) |
| 3 | Acceptable | Core information correct but missing some accuracy in details |
| 2 | Poor | Contains significant factual errors that could mislead the customer |
| 1 | Failing | Completely incorrect or provides wrong information that could harm customer |

**Reference Examples:**

**Score 5 (Excellent):**
```
Our return policy allows returns within 30 days of purchase for most items.
To start a return, visit returns.company.com and enter your order number.
You'll receive a full refund to your original payment method within 5-7
business days after we receive the item. Please note that personalized
items and final sale items cannot be returned.
```
*Why this scores 5:* All facts are accurate (30-day window, return process, refund timeline, exclusions). Includes actionable link.

**Score 3 (Acceptable):**
```
You can return items within 30 days. Please contact our support team
for instructions on how to process your return.
```
*Why this scores 3:* Core fact correct (30 days) but forces customer to contact support instead of providing self-service option. Missing refund timeline.

**Score 1 (Failing):**
```
I'm sorry, but we don't accept returns. All sales are final.
```
*Why this scores 1:* Completely incorrect - contradicts actual return policy. Would prevent legitimate returns.

---

### 2. Completeness

**Description:** Does the response fully address all parts of the customer's query?

**What This Measures:** Whether the agent provides comprehensive answers without leaving gaps that would require follow-up questions.

**Pass Threshold:** ≥ 4.0/5.0

**Scoring Scale:**

| Score | Level | Definition |
|-------|-------|------------|
| 5 | Excellent | Addresses every part of query with sufficient detail. Anticipates related questions. |
| 4 | Good | Addresses all explicit parts of query, could provide more detail on some points |
| 3 | Acceptable | Addresses main question but misses secondary points or related concerns |
| 2 | Poor | Partially addresses query with key points missing |
| 1 | Failing | Doesn't address the actual query or misses the main point entirely |

**Reference Examples:**

**Score 5 (Excellent):**
*Query: "How do I return a damaged item?"*
```
I'm sorry to hear your item arrived damaged! Here's how to return it:

1. Visit returns.company.com and enter your order number
2. Select "Damaged Item" as the reason - this will prioritize your case
3. Upload photos of the damage (helps us improve packaging)
4. You'll get a prepaid return label via email within 1 hour
5. Drop off at any USPS location

You'll receive a full refund within 3-5 business days after we receive it.
If you need a replacement instead of a refund, please let me know!
```
*Why this scores 5:* Addresses return process, emphasizes damage-specific steps, mentions documentation, provides timeline, offers alternative (replacement).

**Score 3 (Acceptable):**
*Query: "How do I return a damaged item?"*
```
To return an item, visit our returns page and follow the instructions.
You'll get a refund once we receive it.
```
*Why this scores 3:* Addresses returns but doesn't acknowledge damage aspect, misses damage-specific guidance, no timeline details.

**Score 1 (Failing):**
*Query: "How do I return a damaged item?"*
```
Please check our shipping policy on the website.
```
*Why this scores 1:* Doesn't address returns at all, redirects to wrong policy (shipping vs returns).

---

### 3. Deflection Potential

**Description:** Will this response prevent the customer from creating a support ticket or escalating to a human agent?

**What This Measures:** The agent's ability to provide self-service solutions that fully resolve customer needs without requiring further assistance.

**Pass Threshold:** ≥ 4.0/5.0

**Scoring Scale:**

| Score | Level | Definition |
|-------|-------|------------|
| 5 | Excellent | Completely self-service - customer can resolve issue independently with no escalation needed |
| 4 | Good | Mostly self-service, minor follow-up questions possible but main issue resolved |
| 3 | Acceptable | Partially self-service, customer might need additional help for edge cases |
| 2 | Poor | Likely requires human escalation to fully resolve |
| 1 | Failing | Forces escalation or provides no actionable path forward |

**Reference Examples:**

**Score 5 (Excellent):**
```
Here's your order status:
• Order #12345 shipped on March 3rd via UPS
• Tracking number: 1Z999AA10123456784
• Expected delivery: March 6th by 8pm
• Track it here: https://track.ups.com/12345

If it doesn't arrive by March 6th, let me know and I'll help investigate!
```
*Why this scores 5:* Provides complete information, direct tracking link, sets expectations, offers follow-up path. Fully self-service.

**Score 3 (Acceptable):**
```
Your order has shipped. Please check your email for tracking information,
or contact us if you need help tracking it.
```
*Why this scores 3:* Provides basic info but forces customer to search email or contact support. Not fully self-service.

**Score 1 (Failing):**
```
Please contact our support team for order status updates.
```
*Why this scores 1:* Forces escalation to human support for something that could be self-service.

---

### 4. Clarity

**Description:** Is the response easy to understand for the average customer?

**What This Measures:** Whether the agent communicates clearly using simple language, good structure, and appropriate formatting.

**Pass Threshold:** ≥ 3.5/5.0

**Scoring Scale:**

| Score | Level | Definition |
|-------|-------|------------|
| 5 | Excellent | Crystal clear, simple language, well-structured (numbered steps, bullets), no jargon |
| 4 | Good | Clear but could be more concise or better structured |
| 3 | Acceptable | Understandable but requires some effort, could be simpler |
| 2 | Poor | Confusing, unclear, or overly complex language |
| 1 | Failing | Incomprehensible, contradictory, or impossible to follow |

**Reference Examples:**

**Score 5 (Excellent):**
```
To update your shipping address:

1. Log into your account at company.com
2. Click "Orders" in the menu
3. Find your order and click "Edit Shipping Address"
4. Enter the new address and click "Save"

Note: You can only change the address before the order ships.
Need help? I'm here!
```
*Why this scores 5:* Numbered steps, simple language, clear structure, includes caveat, friendly tone.

**Score 3 (Acceptable):**
```
You can update your shipping address by logging into your account and
going to the orders section where you'll find an option to edit the
address but this is only possible if the order hasn't shipped yet.
```
*Why this scores 3:* Contains all needed info but single run-on sentence, no structure, harder to parse.

**Score 1 (Failing):**
```
Address modifications can be facilitated through the account management
portal, contingent upon fulfillment center processing status parameters.
```
*Why this scores 1:* Overly complex language, jargon-heavy, unclear what customer should do.

---

### 5. Tone

**Description:** Does the response match our brand voice (friendly, helpful, empathetic)?

**What This Measures:** Whether the agent communicates in a warm, approachable way that makes customers feel heard and supported.

**Pass Threshold:** ≥ 3.5/5.0

**Scoring Scale:**

| Score | Level | Definition |
|-------|-------|------------|
| 5 | Excellent | Perfectly friendly and empathetic, natural conversation, acknowledges customer feelings |
| 4 | Good | Friendly but slightly generic or formal, could be warmer |
| 3 | Acceptable | Neutral, functional but not warm, feels automated |
| 2 | Poor | Cold, robotic, or overly formal. No personality. |
| 1 | Failing | Rude, dismissive, or inappropriate tone |

**Reference Examples:**

**Score 5 (Excellent):**
```
I'm so sorry to hear your order arrived damaged! That's definitely not
the experience we want for you. Let me help you get this resolved right
away - you shouldn't have to wait any longer for your item.
```
*Why this scores 5:* Acknowledges problem, shows empathy ("so sorry"), takes ownership ("Let me help"), sets positive expectation.

**Score 3 (Acceptable):**
```
Please follow the return process outlined in our policy to return the
damaged item. You will receive a refund.
```
*Why this scores 3:* Functional but no warmth, doesn't acknowledge customer frustration, feels automated.

**Score 1 (Failing):**
```
Returns for damaged items must be initiated according to policy 3.4.2.
Failure to comply may result in refund denial.
```
*Why this scores 1:* Cold, threatening tone, policy-speak instead of helpful language, no empathy.

---

## Overall Evaluation Logic

**Pass Criteria:**

An output passes evaluation if:
- **ALL categories** meet their individual pass thresholds (AND logic)

**Category Weights:**
- **Correctness:** 2.0x (Critical - wrong info is worse than poor tone)
- **Completeness:** 2.0x (Critical - incomplete answers force escalation)
- **Deflection Potential:** 2.0x (Critical - directly impacts ticket reduction goal)
- **Clarity:** 1.0x (Important but not critical)
- **Tone:** 1.0x (Nice-to-have for customer satisfaction)

---

## How to Use This Rubric

### For Human Evaluation:
1. Read the customer query and bot response
2. For each category, compare the response to reference examples
3. Assign a score (1-5) based on the scale definitions
4. Check if the score meets the pass threshold
5. Record overall pass/fail

### For LLM-as-Judge:
- This rubric is embedded in the evaluation code
- Reference examples are included in judge prompts
- Scores are parsed automatically
- Results aggregated by category

### For Iteration:
- Review lowest-scoring categories in results
- Identify patterns in failures (e.g., "Always misses damage-specific steps")
- Refine agent prompt to address gaps
- Update rubric if product outcomes change

---

## Customization

This rubric is designed for an e-commerce support bot with a ticket reduction goal. You can:
- Add categories (e.g., "Safety" if handling sensitive data)
- Adjust pass thresholds based on your quality standards
- Update reference examples to match your products/policies
- Modify weights if different categories matter more for your outcomes

To regenerate after changes, use `/evalcraft` or manually edit `rubric.json` and regenerate the evaluation code.

---

**This rubric measures what matters for reducing support tickets and improving customer satisfaction. Use results to iteratively improve your agent.**
