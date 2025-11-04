#!/usr/bin/env python3
"""
Test Matrix Preparation for Hard Puzzle Study
Creates 50 test matrix entries (10 puzzles × 5 languages)
"""

import json
import os

def prepare_hard_test_matrix():
    """Prepare the test matrix showing all 50 tests."""
    puzzles = list(range(1, 11))  # 10 puzzles
    languages = {
        'en': 'English',
        'pl': 'Polish',
        'zh-CN': 'Simplified Chinese',
        'zh-TW': 'Traditional Chinese',
        'ko': 'Korean'
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
                'prompt_file': f"/home/user/claude-code-puzzle/hard_test_prompts/puzzle_{puzzle_id}_{lang_code}.txt",
                'response_file': f"/home/user/claude-code-puzzle/hard_test_responses/puzzle_{puzzle_id}_{lang_code}_response.txt",
                'status': 'pending'
            })
            test_id += 1

    return test_matrix

def save_test_matrix(matrix, filename):
    """Save test matrix to JSON."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(matrix, f, indent=2, ensure_ascii=False)

def main():
    """Main execution function."""
    # Create output directory
    os.makedirs("/home/user/claude-code-puzzle/hard_test_responses", exist_ok=True)

    # Prepare test matrix
    matrix = prepare_hard_test_matrix()

    # Save matrix
    matrix_file = "/home/user/claude-code-puzzle/hard_test_matrix.json"
    save_test_matrix(matrix, matrix_file)

    print(f"Test matrix saved to: {matrix_file}")
    print(f"\nTotal tests: {len(matrix)}")
    print(f"Puzzles: 10")
    print(f"Languages per puzzle: 5")
    print(f"\nLanguages: English, Polish, Simplified Chinese, Traditional Chinese, Korean")
    print(f"\nEach puzzle has 7 people, 7 time slots, and 10-12 constraints")
    print(f"This is a harder version of the original study")

if __name__ == "__main__":
    main()
