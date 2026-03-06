# {{PROJECT_NAME}} - Evaluation Rubric

**Agent Purpose:** {{AGENT_PURPOSE}}
**Product Outcomes:** {{PRODUCT_OUTCOMES}}
**Generated:** {{TIMESTAMP}}

---

## Evaluation Categories

This rubric defines how we evaluate AI agent outputs. Each category has a 1-5 scale with reference examples.

{{#each CATEGORIES}}
### {{index}}. {{category_name}}

**Description:** {{description}}

**What This Measures:** {{what_it_measures}}

**Pass Threshold:** ≥ {{pass_threshold}}/5.0

**Scoring Scale:**

| Score | Level | Definition |
|-------|-------|------------|
| 5 | Excellent | {{scale_5_definition}} |
| 4 | Good | {{scale_4_definition}} |
| 3 | Acceptable | {{scale_3_definition}} |
| 2 | Poor | {{scale_2_definition}} |
| 1 | Failing | {{scale_1_definition}} |

**Reference Examples:**

**Score 5 (Excellent):**
```
{{reference_example_5}}
```
*Why this scores 5:* {{reference_example_5_reasoning}}

**Score 3 (Acceptable):**
```
{{reference_example_3}}
```
*Why this scores 3:* {{reference_example_3_reasoning}}

**Score 1 (Failing):**
```
{{reference_example_1}}
```
*Why this scores 1:* {{reference_example_1_reasoning}}

---

{{/each}}

## Overall Evaluation Logic

**Pass Criteria:**

An output passes evaluation if:
{{#if USE_ALL_MUST_PASS}}
- **ALL categories** meet their individual pass thresholds (AND logic)
{{else}}
- **Weighted average** across all categories ≥ {{OVERALL_THRESHOLD}}
{{/if}}

**Category Weights:**
{{#each CATEGORY_WEIGHTS}}
- {{category_name}}: {{weight}}x {{#if is_critical}}(Critical){{/if}}
{{/each}}

---

## How to Use This Rubric

### For Human Evaluation:
1. Read the query and response
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
- Review lowest-scoring categories
- Identify patterns in failures
- Refine agent prompt to address gaps
- Update rubric if outcomes change

---

## Customization

This rubric is generated based on your specific use case. You can:
- Add/remove categories
- Adjust pass thresholds
- Update reference examples
- Modify scoring definitions
- Change category weights

To regenerate after changes, use `/evalcraft` or manually edit `rubric.json` and regenerate the evaluation code.

---

**This rubric measures what matters for your product outcomes. Review failed cases to identify improvement opportunities.**
