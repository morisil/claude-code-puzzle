#!/usr/bin/env python3
"""
Subagent-Based Test Runner for Hard Puzzle Study
Runs each of the 50 tests in a separate subagent to avoid context pollution

This script generates the test execution instructions that the main assistant
will use to launch individual subagents for each test.
"""

import json
import os

def load_test_matrix(matrix_file):
    """Load the test matrix."""
    with open(matrix_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_subagent_prompts(matrix):
    """Generate individual prompts for each subagent test."""
    prompts = []

    for test in matrix:
        test_id = test['test_id']
        puzzle_id = test['puzzle_id']
        lang_code = test['language_code']
        lang_name = test['language_name']
        prompt_file = test['prompt_file']
        response_file = test['response_file']

        # Read the puzzle prompt
        with open(prompt_file, 'r', encoding='utf-8') as f:
            puzzle_prompt = f.read()

        # Create subagent task prompt
        subagent_prompt = f"""You are solving Test {test_id}: Puzzle {puzzle_id} in {lang_name}.

This is a constraint satisfaction puzzle. Read the prompt carefully and solve it systematically.

===== PUZZLE PROMPT =====
{puzzle_prompt}

===== END PUZZLE PROMPT =====

INSTRUCTIONS FOR YOU:
1. Read and understand all constraints carefully
2. Solve the puzzle step by step
3. Show your reasoning process
4. Verify your solution against all constraints
5. Present your final answer clearly

Your response will be saved to: {response_file}

BEGIN SOLVING NOW."""

        prompts.append({
            'test_id': test_id,
            'puzzle_id': puzzle_id,
            'language_code': lang_code,
            'language_name': lang_name,
            'response_file': response_file,
            'prompt': subagent_prompt
        })

    return prompts

def save_prompts_for_execution(prompts, output_dir):
    """Save prompts to individual files for execution."""
    os.makedirs(output_dir, exist_ok=True)

    for prompt_data in prompts:
        test_id = prompt_data['test_id']
        filename = f"{output_dir}/test_{test_id}_prompt.txt"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(prompt_data['prompt'])

    print(f"Saved {len(prompts)} subagent prompts to {output_dir}")

def generate_execution_metadata(prompts, output_file):
    """Generate metadata for test execution."""
    metadata = {
        'total_tests': len(prompts),
        'tests': [
            {
                'test_id': p['test_id'],
                'puzzle_id': p['puzzle_id'],
                'language_code': p['language_code'],
                'language_name': p['language_name'],
                'response_file': p['response_file']
            }
            for p in prompts
        ]
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print(f"Saved execution metadata to {output_file}")

def main():
    """Main function."""
    matrix_file = "/home/user/claude-code-puzzle/hard_test_matrix.json"
    prompts_dir = "/home/user/claude-code-puzzle/subagent_prompts"
    metadata_file = "/home/user/claude-code-puzzle/hard_test_execution_metadata.json"

    print("="*80)
    print("HARD PUZZLE STUDY - SUBAGENT TEST RUNNER")
    print("="*80)
    print()

    # Load test matrix
    matrix = load_test_matrix(matrix_file)
    print(f"Loaded {len(matrix)} tests from matrix")
    print()

    # Generate subagent prompts
    print("Generating subagent prompts...")
    prompts = generate_subagent_prompts(matrix)
    print(f"Generated {len(prompts)} subagent prompts")
    print()

    # Save prompts
    save_prompts_for_execution(prompts, prompts_dir)
    print()

    # Save metadata
    generate_execution_metadata(prompts, metadata_file)
    print()

    print("="*80)
    print("READY FOR EXECUTION")
    print("="*80)
    print()
    print(f"Total tests to run: {len(prompts)}")
    print(f"Each test will run in a separate subagent")
    print()
    print("The main assistant will now launch subagents to execute all 50 tests.")
    print("This ensures no context window pollution between tests.")

if __name__ == "__main__":
    main()
