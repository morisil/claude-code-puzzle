#!/usr/bin/env python3
"""
Batch Test Runner for Polish Reasoning Language Experiment
Coordinates the execution of all 20 test runs (5 puzzles × 4 languages)
"""

import json
import os

def prepare_test_matrix():
    """Prepare the test matrix showing all 20 tests."""
    puzzles = [1, 2, 3, 4, 5]
    languages = {
        'en': 'English',
        'pl': 'Polish',
        'zh-CN': 'Simplified Chinese',
        'zh-TW': 'Traditional Chinese'
    }

    test_matrix = []
    test_id = 1

    for puzzle_id in puzzles:
        for lang_code, lang_name in languages.items():
            test_matrix.append({
                'test_id': test_id,
                'puzzle_id': puzzle_id,
                'language_code': lang_code,
                'language_name': lang_name,
                'prompt_file': f"/home/user/claude-code-puzzle/batch_test_prompts/puzzle_{puzzle_id}_{lang_code}.txt",
                'response_file': f"/home/user/claude-code-puzzle/batch_test_responses/puzzle_{puzzle_id}_{lang_code}_response.txt",
                'status': 'pending'
            })
            test_id += 1

    return test_matrix

def save_test_matrix(matrix, filename):
    """Save test matrix to JSON."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(matrix, f, indent=2, ensure_ascii=False)

def generate_subagent_commands(matrix):
    """Generate commands for running subagents."""
    # Group by puzzle for batch execution
    by_puzzle = {}
    for test in matrix:
        puzzle_id = test['puzzle_id']
        if puzzle_id not in by_puzzle:
            by_puzzle[puzzle_id] = []
        by_puzzle[puzzle_id].append(test)

    print("=" * 80)
    print("BATCH TEST EXECUTION PLAN")
    print("=" * 80)
    print()
    print(f"Total tests: {len(matrix)}")
    print(f"Puzzles: 5")
    print(f"Languages per puzzle: 4")
    print()

    print("=" * 80)
    print("EXECUTION STRATEGY")
    print("=" * 80)
    print()
    print("We will run tests in 5 batches (one per puzzle).")
    print("Each batch runs 4 subagents in parallel (one per language).")
    print()

    for puzzle_id in sorted(by_puzzle.keys()):
        tests = by_puzzle[puzzle_id]
        print(f"\n{'='*80}")
        print(f"BATCH {puzzle_id}: Puzzle {puzzle_id} - All Languages")
        print(f"{'='*80}")

        for test in tests:
            print(f"\nTest {test['test_id']}: {test['language_name']}")
            print(f"  Prompt: {test['prompt_file']}")
            print(f"  Response: {test['response_file']}")

def main():
    """Main execution function."""
    # Create output directory
    os.makedirs("/home/user/claude-code-puzzle/batch_test_responses", exist_ok=True)

    # Prepare test matrix
    matrix = prepare_test_matrix()

    # Save matrix
    matrix_file = "/home/user/claude-code-puzzle/test_matrix.json"
    save_test_matrix(matrix, matrix_file)

    print(f"Test matrix saved to: {matrix_file}")
    print()

    # Generate execution plan
    generate_subagent_commands(matrix)

    print("\n\n" + "=" * 80)
    print("READY TO EXECUTE")
    print("=" * 80)
    print()
    print("Test matrix prepared. Ready to run 20 tests in 5 batches.")
    print()
    print("Next step: The main assistant will launch subagents in batches.")

if __name__ == "__main__":
    main()
