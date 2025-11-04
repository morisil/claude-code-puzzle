#!/usr/bin/env python3
"""
Generate batch launch instructions for subagent tests
"""

import json

# Load metadata
with open('/home/user/claude-code-puzzle/hard_test_execution_metadata.json', 'r') as f:
    metadata = json.load(f)

tests = metadata['tests']

# Group into batches of 10
batch_size = 10
batches = [tests[i:i+batch_size] for i in range(0, len(tests), batch_size)]

print(f"Total tests: {len(tests)}")
print(f"Number of batches: {len(batches)}")
print(f"Batch size: {batch_size}")
print()

for batch_num, batch in enumerate(batches, 1):
    print(f"=== BATCH {batch_num} ===")
    print(f"Tests {batch[0]['test_id']} to {batch[-1]['test_id']}")
    print()

    for test in batch:
        prompt_file = f"/home/user/claude-code-puzzle/subagent_prompts/test_{test['test_id']}_prompt.txt"

        # Read the prompt
        with open(prompt_file, 'r', encoding='utf-8') as f:
            prompt = f.read()

        print(f"Test {test['test_id']}: Puzzle {test['puzzle_id']} - {test['language_name']}")
        print(f"  Response file: {test['response_file']}")
    print()
