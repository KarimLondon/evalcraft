#!/usr/bin/env python3
"""
Rubric Generator for EvalCraft

This script generates a custom evaluation rubric based on:
1. Agent prompt (what the agent does)
2. Product outcomes (what success looks like)
3. Best practices from eval knowledge base

Output:
- rubric.md: Human-readable rubric with reference examples
- rubric.json: Machine-readable rubric for code generation

Usage:
    python generate_rubric.py \
        --agent-prompt "You are a customer support assistant..." \
        --outcomes '["Reduce support tickets", "Improve CSAT"]' \
        --output-dir ~/Documents/eval_projects/my_project/
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

try:
    from anthropic import Anthropic
    from dotenv import load_dotenv
except ImportError:
    print("❌ Missing dependencies. Install: pip install anthropic python-dotenv")
    sys.exit(1)

load_dotenv()

# Model for rubric generation
RUBRIC_MODEL = "claude-3-5-sonnet-20241022"

def load_best_practices():
    """Load eval best practices from knowledge base."""
    # Path to best practices reference
    script_dir = Path(__file__).parent.parent
    best_practices_path = script_dir / "references" / "eval_best_practices.md"

    if best_practices_path.exists():
        with open(best_practices_path) as f:
            return f.read()
    else:
        # Fallback principles if file not found
        return """
        Core Eval Principles:
        - Use 4-6 categories aligned with product outcomes
        - Provide concrete reference examples (scores 1, 3, 5)
        - Binary pass/fail thresholds (even with 1-5 scales)
        - Product-specific evals, not generic metrics
        """

def generate_rubric(agent_prompt, outcomes, best_practices):
    """
    Generate custom rubric using Claude API.

    Args:
        agent_prompt: The AI agent's system instructions
        outcomes: List of product outcomes/goals
        best_practices: Eval best practices text

    Returns:
        Dictionary with rubric structure
    """

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("\n❌ ANTHROPIC_API_KEY not found")
        print("\nPlease set your Claude API key:")
        print("    export ANTHROPIC_API_KEY=your_key_here")
        print("Or create a .env file with: ANTHROPIC_API_KEY=your_key_here\n")
        sys.exit(1)

    client = Anthropic(api_key=api_key)

    # Prepare outcomes as bullet points
    outcomes_text = "\n".join(f"- {outcome}" for outcome in outcomes)

    # Create rubric generation prompt
    prompt = f"""You are an expert at designing evaluation rubrics for AI agents.

# Task
Create a custom evaluation rubric for an AI agent based on its purpose and product outcomes.

# Agent Prompt
{agent_prompt}

# Product Outcomes (what success looks like)
{outcomes_text}

# Evaluation Best Practices
{best_practices[:2000]}  # Truncate if too long

# Instructions
Generate a rubric with 4-6 evaluation categories that:
1. **Align with product outcomes** - Categories should directly measure whether outcomes are achieved
2. **Are specific to this use case** - Not generic metrics
3. **Have clear 1-5 scoring scales** - Define what each score level means
4. **Include reference examples** - Provide concrete examples for scores 1, 3, and 5

For each category, provide:
- Category name (one word: correctness, completeness, tone, etc.)
- Description (what this measures)
- Pass threshold (recommended: 4.0 for critical, 3.5 for nice-to-have)
- Scale definitions (what scores 1-5 mean)
- Reference examples (concrete examples showing scores 1, 3, 5)

# Output Format
Return JSON in this exact structure:
{{
  "project_name": "Suggested project name based on agent purpose",
  "agent_purpose": "One sentence summarizing what the agent does",
  "product_outcomes": ["outcome1", "outcome2"],
  "categories": {{
    "category_name": {{
      "description": "What this measures",
      "pass_threshold": 4.0,
      "weight": 1.0 or 2.0 (use 2.0 for critical categories aligned with outcomes),
      "scale": {{
        "5": "Definition of excellent (score 5)",
        "4": "Definition of good (score 4)",
        "3": "Definition of acceptable (score 3)",
        "2": "Definition of poor (score 2)",
        "1": "Definition of failing (score 1)"
      }},
      "reference_examples": {{
        "5": "Concrete example showing score 5 quality",
        "3": "Concrete example showing score 3 quality",
        "1": "Concrete example showing score 1 quality"
      }},
      "reference_reasoning": {{
        "5": "Why this example scores 5",
        "3": "Why this example scores 3",
        "1": "Why this example scores 1"
      }}
    }}
  }}
}}

Think step by step:
1. What does this agent do? (determine domain)
2. What are the key outcomes? (determine what matters)
3. What categories best measure those outcomes? (4-6 categories)
4. What would excellent/acceptable/failing look like for each? (scales and examples)

Return ONLY valid JSON, no other text.
"""

    print("🤖 Generating custom rubric with Claude API...")
    print(f"   Model: {RUBRIC_MODEL}")
    print(f"   Analyzing agent prompt and {len(outcomes)} outcomes...\n")

    try:
        response = client.messages.create(
            model=RUBRIC_MODEL,
            max_tokens=8192,  # Rubrics can be long
            temperature=1.0,  # Some creativity for examples
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        rubric_text = response.content[0].text

        # Extract JSON from response
        if "```json" in rubric_text:
            start = rubric_text.find("```json") + 7
            end = rubric_text.find("```", start)
            json_str = rubric_text[start:end].strip()
            rubric = json.loads(json_str)
        else:
            # Try parsing entire response
            rubric = json.loads(rubric_text)

        return rubric

    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse rubric JSON: {e}")
        print(f"\nResponse received:\n{rubric_text[:500]}...\n")
        sys.exit(1)

    except Exception as e:
        print(f"❌ Error generating rubric: {e}")
        sys.exit(1)

def format_rubric_markdown(rubric):
    """
    Format rubric as markdown for human readability.

    Args:
        rubric: Rubric dictionary

    Returns:
        Formatted markdown string
    """

    md = f"# {rubric['project_name']} - Evaluation Rubric\n\n"
    md += f"**Agent Purpose:** {rubric['agent_purpose']}\n"
    md += f"**Product Outcomes:** {', '.join(rubric['product_outcomes'])}\n"
    md += f"**Generated:** {datetime.now().strftime('%Y-%m-%d')}\n\n"
    md += "---\n\n"

    md += "## Evaluation Categories\n\n"
    md += "This rubric defines how we evaluate AI agent outputs. Each category has a 1-5 scale with reference examples.\n\n"

    # Add each category
    for idx, (cat_name, cat_details) in enumerate(rubric['categories'].items(), 1):
        md += f"### {idx}. {cat_name.title()}\n\n"
        md += f"**Description:** {cat_details['description']}\n\n"
        md += f"**Pass Threshold:** ≥ {cat_details['pass_threshold']}/5.0\n\n"

        # Scoring scale table
        md += "**Scoring Scale:**\n\n"
        md += "| Score | Level | Definition |\n"
        md += "|-------|-------|------------|\n"

        levels = {5: "Excellent", 4: "Good", 3: "Acceptable", 2: "Poor", 1: "Failing"}
        for score in [5, 4, 3, 2, 1]:
            if str(score) in cat_details['scale']:
                md += f"| {score} | {levels[score]} | {cat_details['scale'][str(score)]} |\n"

        md += "\n**Reference Examples:**\n\n"

        # Add reference examples
        for score in ['5', '3', '1']:
            if score in cat_details.get('reference_examples', {}):
                md += f"**Score {score} ({'Excellent' if score=='5' else 'Acceptable' if score=='3' else 'Failing'}):**\n"
                md += "```\n"
                md += cat_details['reference_examples'][score]
                md += "\n```\n"

                if score in cat_details.get('reference_reasoning', {}):
                    md += f"*Why this scores {score}:* {cat_details['reference_reasoning'][score]}\n\n"

        md += "---\n\n"

    # Overall evaluation logic
    md += "## Overall Evaluation Logic\n\n"
    md += "**Pass Criteria:**\n\n"
    md += "An output passes evaluation if **ALL categories** meet their individual pass thresholds (AND logic).\n\n"

    md += "**Category Weights:**\n"
    for cat_name, cat_details in rubric['categories'].items():
        weight = cat_details.get('weight', 1.0)
        is_critical = " (Critical)" if weight > 1.0 else ""
        md += f"- **{cat_name.title()}:** {weight}x{is_critical}\n"

    md += "\n---\n\n"

    # Usage instructions
    md += "## How to Use This Rubric\n\n"
    md += "### For Human Evaluation:\n"
    md += "1. Read the query and response\n"
    md += "2. For each category, compare response to reference examples\n"
    md += "3. Assign a score (1-5) based on scale definitions\n"
    md += "4. Check if score meets pass threshold\n"
    md += "5. Record overall pass/fail\n\n"

    md += "### For LLM-as-Judge:\n"
    md += "- This rubric is embedded in evaluation code\n"
    md += "- Reference examples included in judge prompts\n"
    md += "- Scores parsed automatically\n"
    md += "- Results aggregated by category\n\n"

    md += "### For Iteration:\n"
    md += "- Review lowest-scoring categories\n"
    md += "- Identify patterns in failures\n"
    md += "- Refine agent prompt to address gaps\n"
    md += "- Update rubric if outcomes change\n\n"

    md += "---\n\n"
    md += "**This rubric measures what matters for your product outcomes. Review failed cases to identify improvement opportunities.**\n"

    return md

def save_rubric(rubric, output_dir):
    """
    Save rubric in both markdown and JSON formats.

    Args:
        rubric: Rubric dictionary
        output_dir: Directory to save files
    """

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Save markdown
    md = format_rubric_markdown(rubric)
    md_path = output_path / "rubric.md"
    with open(md_path, "w") as f:
        f.write(md)

    # Save JSON
    json_path = output_path / "rubric.json"
    with open(json_path, "w") as f:
        json.dump(rubric, f, indent=2)

    print(f"✅ Rubric generated successfully!")
    print(f"   📄 Markdown: {md_path}")
    print(f"   📄 JSON: {json_path}\n")

    return md_path, json_path

def main():
    """Main entry point."""

    parser = argparse.ArgumentParser(
        description="Generate custom evaluation rubric for AI agent",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--agent-prompt",
        required=True,
        help="Agent system instructions or prompt"
    )

    parser.add_argument(
        "--outcomes",
        required=True,
        help="Product outcomes as JSON list (e.g., '[\"Reduce tickets\", \"Improve CSAT\"]')"
    )

    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory to save rubric files"
    )

    args = parser.parse_args()

    # Parse outcomes
    try:
        outcomes = json.loads(args.outcomes)
        if not isinstance(outcomes, list):
            print("❌ Outcomes must be a JSON list")
            sys.exit(1)
    except json.JSONDecodeError:
        print("❌ Invalid JSON for outcomes")
        sys.exit(1)

    # Load best practices
    best_practices = load_best_practices()

    # Generate rubric
    rubric = generate_rubric(args.agent_prompt, outcomes, best_practices)

    # Save rubric
    save_rubric(rubric, args.output_dir)

    # Print summary
    print("📊 Rubric Summary:")
    print(f"   Project: {rubric['project_name']}")
    print(f"   Categories: {len(rubric['categories'])}")
    for cat_name, cat_details in rubric['categories'].items():
        print(f"      - {cat_name.title()} (threshold: ≥{cat_details['pass_threshold']})")

if __name__ == "__main__":
    main()
