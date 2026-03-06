#!/usr/bin/env python3
"""
Evaluation Code Generator for EvalCraft

This script generates executable Python evaluation code by:
1. Loading rubric.json
2. Injecting rubric into eval_code_template.py
3. Generating evaluate.py and requirements.txt

Output:
- evaluate.py: Standalone evaluation script with embedded rubric
- requirements.txt: Python dependencies
- .env.example: API key template

Usage:
    python generate_eval_code.py \
        --rubric ~/Documents/eval_projects/my_project/rubric.json \
        --output-dir ~/Documents/eval_projects/my_project/
"""

import os
import sys
import json
import argparse
from pathlib import Path

def load_rubric(rubric_path):
    """Load rubric from JSON file."""

    rubric_file = Path(rubric_path)

    if not rubric_file.exists():
        print(f"❌ Rubric file not found: {rubric_path}")
        sys.exit(1)

    try:
        with open(rubric_file) as f:
            rubric = json.load(f)

        # Validate rubric structure
        required_keys = ['categories', 'project_name']
        for key in required_keys:
            if key not in rubric:
                print(f"❌ Rubric missing required key: {key}")
                sys.exit(1)

        return rubric

    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in rubric file: {e}")
        sys.exit(1)

def format_rubric_python(rubric):
    """
    Convert rubric JSON to Python dictionary code.

    Args:
        rubric: Rubric dictionary

    Returns:
        Python code string defining RUBRIC variable
    """

    # Start with project metadata
    code = f'PROJECT_NAME = "{rubric["project_name"]}"\n'

    # Add agent prompt if available
    if 'agent_prompt' in rubric:
        # Escape quotes in prompt
        prompt = rubric['agent_prompt'].replace('"', '\\"').replace('\n', '\\n')
        code += f'AGENT_PROMPT = """{prompt}"""\n\n'

    # Build RUBRIC dictionary
    code += "RUBRIC = {\n"

    for cat_name, cat_details in rubric['categories'].items():
        code += f'    "{cat_name}": {{\n'
        code += f'        "description": "{cat_details["description"]}",\n'
        code += f'        "weight": {cat_details.get("weight", 1.0)},\n'
        code += f'        "pass_threshold": {cat_details["pass_threshold"]},\n'

        # Add scale
        code += '        "scale": {\n'
        for score, definition in cat_details.get('scale', {}).items():
            # Escape quotes
            definition_escaped = definition.replace('"', '\\"')
            code += f'            {score}: "{definition_escaped}",\n'
        code += '        },\n'

        # Add reference examples
        code += '        "reference_examples": {\n'
        for score, example in cat_details.get('reference_examples', {}).items():
            # Escape quotes and newlines
            example_escaped = example.replace('"', '\\"').replace('\n', '\\n')
            code += f'            {score}: "{example_escaped}",\n'
        code += '        }\n'

        code += '    },\n'

    code += '}\n\n'

    # Add pass logic configuration
    code += f'USE_ALL_MUST_PASS = True  # All categories must pass\n'
    code += f'OVERALL_THRESHOLD = 4.0  # Used if USE_ALL_MUST_PASS is False\n'

    return code

def generate_eval_code(rubric, output_dir):
    """
    Generate evaluation code from template and rubric.

    Args:
        rubric: Rubric dictionary
        output_dir: Directory to save generated files
    """

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Load template
    script_dir = Path(__file__).parent.parent
    template_path = script_dir / "templates" / "eval_code_template.py"

    if not template_path.exists():
        print(f"❌ Template not found: {template_path}")
        sys.exit(1)

    with open(template_path) as f:
        template = f.read()

    # Generate rubric Python code
    rubric_code = format_rubric_python(rubric)

    # Find injection markers
    start_marker = "# INJECTED: RUBRIC_CONFIG_START"
    end_marker = "# INJECTED: RUBRIC_CONFIG_END"

    if start_marker in template and end_marker in template:
        # Replace section between markers
        start_idx = template.find(start_marker)
        end_idx = template.find(end_marker) + len(end_marker)

        # Extract before and after sections
        before = template[:start_idx]
        after = template[end_idx:]

        # Construct new code
        generated_code = before + start_marker + "\n" + rubric_code + end_marker + after

    else:
        print("⚠️ Warning: Template missing injection markers")
        print("   Using template as-is (rubric not injected)")
        generated_code = template

    # Save evaluate.py
    eval_path = output_path / "evaluate.py"
    with open(eval_path, "w") as f:
        f.write(generated_code)

    # Make executable
    os.chmod(eval_path, 0o755)

    print(f"✅ Generated: {eval_path}")

    return eval_path

def generate_requirements(output_dir):
    """Generate requirements.txt file."""

    output_path = Path(output_dir)

    requirements = """# EvalCraft Evaluation Dependencies

anthropic>=0.39.0
pandas>=2.0.0
python-dotenv>=1.0.0
"""

    req_path = output_path / "requirements.txt"
    with open(req_path, "w") as f:
        f.write(requirements)

    print(f"✅ Generated: {req_path}")

    return req_path

def generate_env_example(output_dir):
    """Generate .env.example file."""

    output_path = Path(output_dir)

    env_example = """# Claude API Key for LLM-as-judge evaluation
# Get your key from: https://console.anthropic.com

ANTHROPIC_API_KEY=your_anthropic_api_key_here
"""

    env_path = output_path / ".env.example"
    with open(env_path, "w") as f:
        f.write(env_example)

    print(f"✅ Generated: {env_path}")

    return env_path

def main():
    """Main entry point."""

    parser = argparse.ArgumentParser(
        description="Generate evaluation code from rubric",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--rubric",
        required=True,
        help="Path to rubric.json file"
    )

    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory to save generated files"
    )

    args = parser.parse_args()

    print("🔧 EvalCraft Code Generator\n")

    # Load rubric
    print(f"📂 Loading rubric from: {args.rubric}")
    rubric = load_rubric(args.rubric)
    print(f"   ✅ Loaded rubric with {len(rubric['categories'])} categories\n")

    # Generate evaluation code
    print("🔨 Generating evaluation code...")
    eval_path = generate_eval_code(rubric, args.output_dir)

    # Generate supporting files
    print("\n📦 Generating supporting files...")
    req_path = generate_requirements(args.output_dir)
    env_path = generate_env_example(args.output_dir)

    print("\n" + "="*60)
    print("✅ EVALUATION FRAMEWORK GENERATED!")
    print("="*60)

    print(f"\n📁 Files created in: {args.output_dir}/")
    print(f"   - evaluate.py (main evaluation script)")
    print(f"   - requirements.txt (Python dependencies)")
    print(f"   - .env.example (API key template)")

    print(f"\n🚀 Next Steps:")
    print(f"\n1. Install dependencies:")
    print(f"   cd {args.output_dir}")
    print(f"   pip install -r requirements.txt")

    print(f"\n2. Set your Claude API key:")
    print(f"   cp .env.example .env")
    print(f"   # Edit .env and add your ANTHROPIC_API_KEY")

    print(f"\n3. Run evaluation:")
    print(f"   python evaluate.py --input test_dataset.csv")

    print(f"\n💡 The evaluation code includes:")
    print(f"   - Your custom rubric embedded")
    print(f"   - LLM-as-judge implementation (temperature=0)")
    print(f"   - Result aggregation and reporting")
    print(f"   - Interactive HTML report generation")

    print(f"\n📖 Customize by editing evaluate.py:")
    print(f"   - RUBRIC dictionary (categories, thresholds)")
    print(f"   - Judge prompts (create_judge_prompt function)")
    print(f"   - Pass logic (USE_ALL_MUST_PASS, OVERALL_THRESHOLD)")

if __name__ == "__main__":
    main()
