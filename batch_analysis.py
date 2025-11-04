#!/usr/bin/env python3
"""
Comprehensive Statistical Analysis of Polish Reasoning Language Experiment
Analyzes all 20 test runs (5 puzzles × 4 languages)
"""

import json
import os
import re
from typing import Dict, List
from collections import defaultdict
import statistics

def load_puzzle_solutions():
    """Load the verified solutions for each puzzle."""
    with open('/home/user/claude-code-puzzle/puzzle_set.json', 'r') as f:
        puzzles = json.load(f)

    solutions = {}
    for puzzle in puzzles:
        # Convert solution format to time->person mapping
        solutions[puzzle['id']] = puzzle['solution']

    return solutions

def extract_schedule_from_response(response_text: str, puzzle_id: int) -> Dict[str, str]:
    """Extract the proposed schedule from a response."""
    schedule = {}

    # Try to find schedule patterns
    # Look for patterns like "9:00 AM - Dr. Anderson" or "9:00: Dr. Anderson"
    patterns = [
        r'(\d{1,2}:\d{2})\s*(?:AM|PM|am|pm)?\s*[-:→—]\s*(?:Dr\.\s+)?(\w+)',
        r'(\d{1,2}:\d{2})\s*(?:上午|下午)?\s*[-:→—]\s*(?:Dr\.\s+)?(\w+)',
    ]

    for pattern in patterns:
        matches = re.findall(pattern, response_text)
        for time, person in matches:
            # Normalize the person name
            person = person.strip()
            if not person.startswith('Dr'):
                person = f'Dr. {person}'
            schedule[time] = person

    return schedule

def score_response(response_file: str, puzzle_id: int, language: str, expected_solution: Dict) -> Dict:
    """Score a single response."""
    try:
        with open(response_file, 'r', encoding='utf-8') as f:
            response_text = f.read()
    except FileNotFoundError:
        return {
            'error': 'File not found',
            'correctness': 0,
            'word_count': 0,
            'has_verification': False,
            'has_step_by_step': False
        }

    # Extract the schedule from response
    proposed_schedule = extract_schedule_from_response(response_text, puzzle_id)

    # Calculate correctness
    correct_assignments = 0
    total_assignments = len(expected_solution)

    for time_slot, expected_person in expected_solution.items():
        # Try to find this time in the proposed schedule
        for proposed_time, proposed_person in proposed_schedule.items():
            # Match if times are the same (ignoring formatting)
            if proposed_time.replace(':', '') in time_slot.replace(':', ''):
                if proposed_person in expected_person or expected_person in proposed_person:
                    correct_assignments += 1
                    break

    correctness_score = (correct_assignments / total_assignments * 100) if total_assignments > 0 else 0

    # Analyze response quality
    word_count = len(response_text.split())
    has_verification = any(term in response_text.lower() for term in ['verif', '验证', '驗證', 'sprawdz'])
    has_step_by_step = any(term in response_text.lower() for term in ['step', 'krok', '步骤', '步驟'])
    has_constraints = response_text.lower().count('constraint') + response_text.count('约束') + response_text.count('約束') + response_text.lower().count('ograniczeni')

    return {
        'correctness': correctness_score,
        'correct_assignments': correct_assignments,
        'total_assignments': total_assignments,
        'word_count': word_count,
        'has_verification': has_verification,
        'has_step_by_step': has_step_by_step,
        'constraint_mentions': has_constraints,
        'response_length': len(response_text)
    }

def analyze_all_results():
    """Analyze all 20 test results."""
    solutions = load_puzzle_solutions()

    languages = {
        'en': 'English',
        'pl': 'Polish',
        'zh-CN': 'Simplified Chinese',
        'zh-TW': 'Traditional Chinese'
    }

    results = []

    for puzzle_id in range(1, 6):
        for lang_code, lang_name in languages.items():
            response_file = f'/home/user/claude-code-puzzle/batch_test_responses/puzzle_{puzzle_id}_{lang_code}_response.txt'

            score = score_response(response_file, puzzle_id, lang_name, solutions[puzzle_id])

            result = {
                'puzzle_id': puzzle_id,
                'language_code': lang_code,
                'language_name': lang_name,
                'response_file': response_file,
                **score
            }

            results.append(result)

            print(f"Puzzle {puzzle_id} - {lang_name}: {score['correctness']:.1f}% correct ({score.get('correct_assignments', 0)}/{score.get('total_assignments', 0)})")

    return results

def aggregate_by_language(results: List[Dict]) -> Dict:
    """Aggregate results by language."""
    by_language = defaultdict(list)

    for result in results:
        lang = result['language_name']
        by_language[lang].append(result)

    aggregated = {}

    for lang, lang_results in by_language.items():
        correctness_scores = [r['correctness'] for r in lang_results]
        word_counts = [r['word_count'] for r in lang_results]

        aggregated[lang] = {
            'n': len(lang_results),
            'mean_correctness': statistics.mean(correctness_scores),
            'stdev_correctness': statistics.stdev(correctness_scores) if len(correctness_scores) > 1 else 0,
            'median_correctness': statistics.median(correctness_scores),
            'min_correctness': min(correctness_scores),
            'max_correctness': max(correctness_scores),
            'mean_word_count': statistics.mean(word_counts),
            'total_verifications': sum(1 for r in lang_results if r['has_verification']),
            'total_step_by_step': sum(1 for r in lang_results if r['has_step_by_step']),
            'correctness_scores': correctness_scores
        }

    return aggregated

def calculate_effect_size(group1, group2):
    """Calculate Cohen's d effect size."""
    mean1 = statistics.mean(group1)
    mean2 = statistics.mean(group2)

    if len(group1) < 2 or len(group2) < 2:
        return 0

    var1 = statistics.variance(group1)
    var2 = statistics.variance(group2)

    n1 = len(group1)
    n2 = len(group2)

    pooled_std = ((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2)
    pooled_std = pooled_std ** 0.5

    if pooled_std == 0:
        return 0

    return (mean1 - mean2) / pooled_std

def main():
    """Main analysis function."""
    print("=" * 80)
    print("COMPREHENSIVE STATISTICAL ANALYSIS")
    print("Polish Reasoning Language Experiment - Batch Testing")
    print("=" * 80)
    print()

    # Analyze all results
    results = analyze_all_results()

    print("\n" + "=" * 80)
    print("AGGREGATED RESULTS BY LANGUAGE")
    print("=" * 80)

    # Aggregate by language
    aggregated = aggregate_by_language(results)

    # Sort by mean correctness
    sorted_langs = sorted(aggregated.items(), key=lambda x: x[1]['mean_correctness'], reverse=True)

    for i, (lang, stats) in enumerate(sorted_langs, 1):
        print(f"\n{i}. {lang}")
        print(f"   Mean Correctness: {stats['mean_correctness']:.2f}% (±{stats['stdev_correctness']:.2f})")
        print(f"   Median: {stats['median_correctness']:.2f}%")
        print(f"   Range: {stats['min_correctness']:.2f}% - {stats['max_correctness']:.2f}%")
        print(f"   Mean Word Count: {stats['mean_word_count']:.0f}")
        print(f"   Verifications: {stats['total_verifications']}/{stats['n']}")
        print(f"   Step-by-step: {stats['total_step_by_step']}/{stats['n']}")

    # Calculate effect sizes
    print("\n" + "=" * 80)
    print("EFFECT SIZES (Cohen's d)")
    print("=" * 80)

    lang_names = list(aggregated.keys())
    for i, lang1 in enumerate(lang_names):
        for lang2 in lang_names[i+1:]:
            effect = calculate_effect_size(
                aggregated[lang1]['correctness_scores'],
                aggregated[lang2]['correctness_scores']
            )
            print(f"{lang1} vs {lang2}: d = {effect:.3f}")

    # Save detailed results
    output = {
        'individual_results': results,
        'aggregated_by_language': {
            lang: {k: v for k, v in stats.items() if k != 'correctness_scores'}
            for lang, stats in aggregated.items()
        },
        'ranking': [lang for lang, _ in sorted_langs]
    }

    with open('/home/user/claude-code-puzzle/batch_analysis_results.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 80)
    print("Analysis complete! Results saved to batch_analysis_results.json")
    print("=" * 80)

if __name__ == "__main__":
    main()
