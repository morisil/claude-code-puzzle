#!/usr/bin/env python3
"""
Analyze and score the test results from the Polish reasoning language experiment.
"""

import json
import os
from datetime import datetime

def analyze_response(file_path, language):
    """Analyze and score a response file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    content_lower = content.lower()

    # Initialize scoring
    score = {
        "language": language,
        "file": file_path,
        "word_count": len(content.split()),
        "char_count": len(content),
        "correctness": 0,  # 40 points max
        "reasoning_quality": 0,  # 20 points max
        "constraint_tracking": 0,  # 20 points max
        "verification": 0,  # 20 points max
        "bonus": 0,  # 20 points max (bonus question)
        "total": 0,
        "notes": [],
        "details": {}
    }

    # 1. CORRECTNESS (40 points)
    # Check for correct schedule assignments
    correct_assignments = []

    # Check each assignment
    checks = {
        "anderson_9": ("9:00" in content or "9am" in content_lower) and "anderson" in content_lower,
        "chen_1030": ("10:30" in content or "10.30" in content) and "chen" in content_lower,
        "evans_1": ("1:00" in content or "13:00" in content or "1pm" in content_lower) and "evans" in content_lower,
        "dubois_230": ("2:30" in content or "14:30" in content or "2.30" in content) and "dubois" in content_lower,
        "brown_4": ("4:00" in content or "16:00" in content or "4pm" in content_lower) and "brown" in content_lower
    }

    for key, check in checks.items():
        if check:
            correct_assignments.append(key)
        else:
            score["notes"].append(f"Missing or unclear: {key}")

    score["correctness"] = int((len(correct_assignments) / 5) * 40)
    score["details"]["correct_assignments"] = len(correct_assignments)

    # 2. REASONING QUALITY (20 points)
    reasoning_indicators = {
        "uses_constraints": any(word in content_lower for word in ["constraint", "ograniczeni", "约束", "約束"]),
        "shows_deduction": any(word in content_lower for word in ["therefore", "thus", "so", "wniosek", "因此", "結論"]),
        "uses_logical_operators": any(word in content_lower for word in ["must", "cannot", "only", "exactly", "musi", "nie może", "必须", "不能", "必須"]),
        "detailed_explanation": len(content) > 800,
        "step_by_step": any(word in content_lower for word in ["step", "krok", "步骤", "步驟"]),
        "case_analysis": any(word in content_lower for word in ["case", "przypadek", "情况", "情況"])
    }

    reasoning_score = sum(reasoning_indicators.values())
    score["reasoning_quality"] = min(20, reasoning_score * 4)
    score["details"]["reasoning_indicators"] = {k: v for k, v in reasoning_indicators.items() if v}

    # 3. CONSTRAINT TRACKING (20 points)
    # Count mentions of constraints (1-8)
    constraint_mentions = 0
    for i in range(1, 9):
        if (f"constraint {i}" in content_lower or
            f"ograniczeni{i}" in content_lower or  # Polish: ograniczenie/ograniczenia
            f"约束{i}" in content or f"約束{i}" in content or  # Chinese
            f"{i}." in content or f"({i})" in content):
            constraint_mentions += 1

    score["constraint_tracking"] = min(20, constraint_mentions * 3)
    score["details"]["constraints_mentioned"] = constraint_mentions

    # 4. VERIFICATION (20 points)
    verification_indicators = {
        "explicit_verification": any(word in content_lower for word in ["verif", "sprawdzen", "驗證", "验证", "检查", "檢查"]),
        "constraint_checking": "✓" in content or "✗" in content or "checkmark" in content_lower,
        "re_validates_solution": content_lower.count("constraint") >= 8 or constraint_mentions >= 6,
        "shows_correctness": all(checks.values())  # Got all assignments right
    }

    verification_score = sum(verification_indicators.values())
    score["verification"] = min(20, verification_score * 5)
    score["details"]["verification_indicators"] = {k: v for k, v in verification_indicators.items() if v}

    # 5. BONUS QUESTION (20 points)
    # Check if bonus question was answered correctly (Brown can replace Dubois)
    bonus_indicators = {
        "mentions_brown": "brown" in content_lower,
        "mentions_replacement": any(word in content_lower for word in ["replace", "take", "zająć", "zastęp", "接替", "代替"]),
        "mentions_230_or_dubois": ("2:30" in content or "14:30" in content or "dubois" in content_lower),
        "correct_reasoning": any(phrase in content_lower for phrase in ["brown", "afternoon", "po południu", "下午"])
    }

    if sum(bonus_indicators.values()) >= 3:
        score["bonus"] = 20
        score["notes"].append("Bonus question answered correctly")
    elif sum(bonus_indicators.values()) >= 2:
        score["bonus"] = 10
        score["notes"].append("Bonus question partially answered")
    else:
        score["notes"].append("Bonus question not adequately answered")

    score["details"]["bonus_indicators"] = {k: v for k, v in bonus_indicators.items() if v}

    # Calculate total
    score["total"] = (score["correctness"] + score["reasoning_quality"] +
                     score["constraint_tracking"] + score["verification"] + score["bonus"])

    return score

def main():
    """Main analysis function."""
    print("=" * 80)
    print("ANALYZING POLISH REASONING TEST RESULTS")
    print("=" * 80)
    print()

    responses = {
        "English": "/home/user/claude-code-puzzle/test_responses/english_response.txt",
        "Polish": "/home/user/claude-code-puzzle/test_responses/polish_response.txt",
        "Chinese (Simplified)": "/home/user/claude-code-puzzle/test_responses/chinese_response.txt",
        "Traditional Chinese": "/home/user/claude-code-puzzle/test_responses/traditional_chinese_response.txt"
    }

    results = []

    for language, filepath in responses.items():
        print(f"\nAnalyzing {language}...")
        score = analyze_response(filepath, language)
        results.append(score)

        print(f"  Correctness: {score['correctness']}/40")
        print(f"  Reasoning Quality: {score['reasoning_quality']}/20")
        print(f"  Constraint Tracking: {score['constraint_tracking']}/20")
        print(f"  Verification: {score['verification']}/20")
        print(f"  Bonus: {score['bonus']}/20")
        print(f"  TOTAL: {score['total']}/120")
        print(f"  Word Count: {score['word_count']}")

    # Sort by total score
    results_sorted = sorted(results, key=lambda x: x['total'], reverse=True)

    print("\n" + "=" * 80)
    print("RANKING BY TOTAL SCORE")
    print("=" * 80)

    for i, result in enumerate(results_sorted, 1):
        print(f"{i}. {result['language']}: {result['total']}/120 ({result['total']/120*100:.1f}%)")

    # Calculate detailed statistics
    analysis = {
        "timestamp": datetime.now().isoformat(),
        "test_name": "Polish Reasoning Efficiency Test",
        "model": "Claude Sonnet 4.5",
        "scores": results,
        "ranking": [r['language'] for r in results_sorted],
        "statistics": {
            "highest_score": results_sorted[0]['total'],
            "lowest_score": results_sorted[-1]['total'],
            "average_score": sum(r['total'] for r in results) / len(results),
            "score_range": results_sorted[0]['total'] - results_sorted[-1]['total']
        }
    }

    # Save detailed results
    output_file = "/home/user/claude-code-puzzle/analysis_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)

    print(f"\n\nDetailed analysis saved to: {output_file}")

    # Print statistics
    print("\n" + "=" * 80)
    print("STATISTICS")
    print("=" * 80)
    print(f"Highest Score: {analysis['statistics']['highest_score']}/120")
    print(f"Lowest Score: {analysis['statistics']['lowest_score']}/120")
    print(f"Average Score: {analysis['statistics']['average_score']:.2f}/120")
    print(f"Score Range: {analysis['statistics']['score_range']} points")

    # Analyze by category
    print("\n" + "=" * 80)
    print("AVERAGE SCORES BY CATEGORY")
    print("=" * 80)

    categories = ["correctness", "reasoning_quality", "constraint_tracking", "verification", "bonus"]
    for cat in categories:
        avg = sum(r[cat] for r in results) / len(results)
        max_possible = 40 if cat == "correctness" else 20
        print(f"{cat.replace('_', ' ').title()}: {avg:.2f}/{max_possible} ({avg/max_possible*100:.1f}%)")

    return analysis

if __name__ == "__main__":
    main()
