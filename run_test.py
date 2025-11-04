#!/usr/bin/env python3
"""
Test harness for validating the ONERULER findings about Polish reasoning efficiency.
Tests Claude Sonnet 4.5 with the same logic puzzle in 4 different languages.
"""

import json
import os
from datetime import datetime

# Test configurations
LANGUAGES = {
    "English": {
        "code": "en",
        "file_section": "english",
        "description": "English Version"
    },
    "Polish": {
        "code": "pl",
        "file_section": "polish",
        "description": "Polish Version (Wersja Polska)"
    },
    "Chinese": {
        "code": "zh-CN",
        "file_section": "chinese",
        "description": "Chinese Version (Simplified) (中文简体版)"
    },
    "Traditional Chinese": {
        "code": "zh-TW",
        "file_section": "traditional_chinese",
        "description": "Traditional Chinese Version (繁體中文版)"
    }
}

# Expected correct answer
CORRECT_SOLUTION = {
    "9:00": "Anderson",
    "10:30": "Chen",
    "1:00": "Evans",
    "2:30": "Dubois",
    "4:00": "Brown"
}

BONUS_ANSWER = "Brown"

def extract_puzzle_text(language):
    """Extract the puzzle text for a specific language from the markdown file."""
    with open('/home/user/claude-code-puzzle/polish_reasoning_test.md', 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the section for this language
    sections = content.split('---')

    if language == "English":
        # English is the first version
        for section in sections:
            if "### English Version" in section:
                return section.strip()
    elif language == "Polish":
        for section in sections:
            if "### Polish Version" in section or "Wersja Polska" in section:
                return section.strip()
    elif language == "Chinese":
        for section in sections:
            if "### Chinese Version (Simplified)" in section or "中文简体版" in section:
                return section.strip()
    elif language == "Traditional Chinese":
        for section in sections:
            if "### Traditional Chinese Version" in section or "繁體中文版" in section:
                return section.strip()

    return None

def create_test_prompt(language):
    """Create the prompt for the subagent in the specified language."""
    puzzle_text = extract_puzzle_text(language)

    prompt = f"""You are being tested on complex logical reasoning. Please solve the following puzzle carefully and systematically.

{puzzle_text}

IMPORTANT INSTRUCTIONS:
1. Show your complete reasoning process step by step
2. Track each constraint carefully
3. Verify your final answer against ALL constraints
4. Answer both the main question AND the additional challenge
5. Present your final answer in a clear format

Please proceed with solving the puzzle."""

    return prompt

def score_response(response_text, language):
    """Score the response based on the evaluation criteria."""
    score = {
        "language": language,
        "correctness": 0,  # 40 points
        "reasoning_quality": 0,  # 20 points
        "constraint_tracking": 0,  # 20 points
        "verification": 0,  # 20 points
        "bonus": 0,  # 20 points (bonus question)
        "total": 0,
        "notes": []
    }

    response_lower = response_text.lower()

    # Check for correct answer (40 points)
    # Look for the key assignments in the response
    correct_assignments = 0
    total_assignments = 5

    checks = [
        ("9:00" in response_text and "anderson" in response_lower, "9:00 AM: Anderson"),
        ("10:30" in response_text and "chen" in response_lower, "10:30 AM: Chen"),
        ("1:00" in response_text and "evans" in response_lower, "1:00 PM: Evans"),
        ("2:30" in response_text and "dubois" in response_lower, "2:30 PM: Dubois"),
        ("4:00" in response_text and "brown" in response_lower, "4:00 PM: Brown")
    ]

    for check, desc in checks:
        if check:
            correct_assignments += 1
        else:
            score["notes"].append(f"Missing or incorrect: {desc}")

    score["correctness"] = int((correct_assignments / total_assignments) * 40)

    # Check reasoning quality (20 points)
    reasoning_indicators = [
        "constraint" in response_lower,
        "therefore" in response_lower or "thus" in response_lower or "so" in response_lower,
        any(word in response_lower for word in ["must", "cannot", "only", "exactly"]),
        len(response_text) > 500  # Detailed explanation
    ]
    score["reasoning_quality"] = sum(reasoning_indicators) * 5

    # Check constraint tracking (20 points)
    # Look for mentions of constraint numbers or systematic checking
    constraint_mentions = sum(1 for i in range(1, 9) if f"constraint {i}" in response_lower or f"{i}." in response_text or str(i) in response_text)
    score["constraint_tracking"] = min(20, constraint_mentions * 3)

    # Check verification (20 points)
    verification_indicators = [
        "verif" in response_lower,
        "check" in response_lower,
        correct_assignments >= 4  # Mostly correct suggests verification happened
    ]
    score["verification"] = sum(verification_indicators) * 7
    score["verification"] = min(20, score["verification"])

    # Check bonus question (20 points)
    if "brown" in response_lower and any(phrase in response_lower for phrase in ["could take", "replace", "2:30", "dubois"]):
        score["bonus"] = 20
        score["notes"].append("Bonus question answered correctly")

    score["total"] = (score["correctness"] + score["reasoning_quality"] +
                     score["constraint_tracking"] + score["verification"] + score["bonus"])

    return score

def main():
    """Main test execution function."""
    print("=" * 80)
    print("POLISH REASONING LANGUAGE TEST")
    print("Testing Claude Sonnet 4.5 across 4 languages")
    print("=" * 80)
    print()

    results = {
        "test_name": "Polish Reasoning Efficiency Test",
        "model": "Claude Sonnet 4.5",
        "timestamp": datetime.now().isoformat(),
        "languages": []
    }

    for language, config in LANGUAGES.items():
        print(f"\n{'='*80}")
        print(f"Testing: {language} ({config['description']})")
        print(f"{'='*80}\n")

        prompt = create_test_prompt(language)

        # Save the prompt for reference
        prompt_file = f"/home/user/claude-code-puzzle/test_prompts/{config['code']}_prompt.txt"
        os.makedirs(os.path.dirname(prompt_file), exist_ok=True)
        with open(prompt_file, 'w', encoding='utf-8') as f:
            f.write(prompt)

        print(f"Prompt saved to: {prompt_file}")
        print(f"Prompt length: {len(prompt)} characters")
        print()

        language_result = {
            "language": language,
            "language_code": config["code"],
            "prompt_length": len(prompt),
            "prompt_file": prompt_file
        }

        results["languages"].append(language_result)

    # Save initial results
    results_file = "/home/user/claude-code-puzzle/test_results.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*80}")
    print(f"Test preparation complete!")
    print(f"Results will be saved to: {results_file}")
    print(f"{'='*80}\n")

    print("\nNOTE: This script prepares the test infrastructure.")
    print("The actual test execution will be done using Claude Code subagents.")
    print("\nNext steps:")
    print("1. Run subagents with each language prompt")
    print("2. Collect responses")
    print("3. Score using the scoring function")
    print("4. Analyze comparative results")

if __name__ == "__main__":
    main()
