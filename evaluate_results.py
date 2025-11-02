#!/usr/bin/env python3
"""
Evaluation script for comparing language-based reasoning accuracy
"""

import json

# Correct solution from the generator
CORRECT_SOLUTION = {
    "Person": {
        "1": "David",
        "2": "Bob",
        "3": "Carol",
        "4": "Emma",
        "5": "Alice"
    },
    "Color": {
        "1": "Yellow",
        "2": "Green",
        "3": "Red",
        "4": "White",
        "5": "Blue"
    },
    "Drink": {
        "1": "Juice",
        "2": "Tea",
        "3": "Milk",
        "4": "Coffee",
        "5": "Water"
    },
    "Pet": {
        "1": "Cat",
        "2": "Bird",
        "3": "Fish",
        "4": "Rabbit",
        "5": "Dog"
    },
    "Profession": {
        "1": "Lawyer",
        "2": "Artist",
        "3": "Teacher",
        "4": "Doctor",
        "5": "Engineer"
    }
}

CORRECT_ANSWER = "Alice"

# English agent solution
ENGLISH_SOLUTION = {
    "Position 1": {"Person": "David", "Color": "Yellow", "Drink": "Juice", "Pet": "Cat", "Profession": "Lawyer"},
    "Position 2": {"Person": "Bob", "Color": "Green", "Drink": "Tea", "Pet": "Bird", "Profession": "Artist"},
    "Position 3": {"Person": "Carol", "Color": "Red", "Drink": "Milk", "Pet": "Fish", "Profession": "Teacher"},
    "Position 4": {"Person": "Emma", "Color": "White", "Drink": "Coffee", "Pet": "Rabbit", "Profession": "Doctor"},
    "Position 5": {"Person": "Alice", "Color": "Blue", "Drink": "Water", "Pet": "Dog", "Profession": "Engineer"}
}

ENGLISH_ANSWER = "Alice"

# Polish agent solution (translated attribute names to match)
POLISH_SOLUTION = {
    "Pozycja 1": {"Osoba": "Dawid", "Kolor": "Żółty", "Napój": "Sok", "Zwierzę": "Kot", "Zawód": "Inżynier"},
    "Pozycja 2": {"Osoba": "Ewa", "Kolor": "Biały", "Napój": "Kawa", "Zwierzę": "Królik", "Zawód": "Lekarz"},
    "Pozycja 3": {"Osoba": "Karolina", "Kolor": "Niebieski", "Napój": "Mleko", "Zwierzę": "Ryba", "Zawód": "Prawnik"},
    "Pozycja 4": {"Osoba": "Bartek", "Kolor": "Zielony", "Napój": "Herbata", "Zwierzę": "Ptak", "Zawód": "Artysta"},
    "Pozycja 5": {"Osoba": "Alicja", "Kolor": "Czerwony", "Napój": "Woda", "Zwierzę": "Pies", "Zawód": "Nauczyciel"}
}

POLISH_ANSWER = "Alicja"

# Chinese agent solution
CHINESE_SOLUTION = {
    "位置 1": {"人物": "大卫", "颜色": "黄色", "饮料": "水", "宠物": "猫", "职业": "律师"},
    "位置 2": {"人物": "鲍勃", "颜色": "绿色", "饮料": "茶", "宠物": "鸟", "职业": "艺术家"},
    "位置 3": {"人物": "卡罗尔", "颜色": "红色", "饮料": "牛奶", "宠物": "鱼", "职业": "教师"},
    "位置 4": {"人物": "艾玛", "颜色": "白色", "饮料": "咖啡", "宠物": "兔子", "职业": "医生"},
    "位置 5": {"人物": "爱丽丝", "颜色": "蓝色", "饮料": "果汁", "宠物": "狗", "职业": "工程师"}
}

CHINESE_ANSWER = "大卫"

# Translation mappings
POLISH_TO_ENGLISH = {
    # Names
    "Dawid": "David", "Bartek": "Bob", "Karolina": "Carol", "Ewa": "Emma", "Alicja": "Alice",
    # Colors
    "Czerwony": "Red", "Niebieski": "Blue", "Zielony": "Green", "Żółty": "Yellow", "Biały": "White",
    # Drinks
    "Kawa": "Coffee", "Herbata": "Tea", "Mleko": "Milk", "Sok": "Juice", "Woda": "Water",
    # Pets
    "Pies": "Dog", "Kot": "Cat", "Ptak": "Bird", "Ryba": "Fish", "Królik": "Rabbit",
    # Professions
    "Lekarz": "Doctor", "Inżynier": "Engineer", "Nauczyciel": "Teacher", "Artysta": "Artist", "Prawnik": "Lawyer"
}

CHINESE_TO_ENGLISH = {
    # Names
    "大卫": "David", "鲍勃": "Bob", "卡罗尔": "Carol", "艾玛": "Emma", "爱丽丝": "Alice",
    # Colors
    "红色": "Red", "蓝色": "Blue", "绿色": "Green", "黄色": "Yellow", "白色": "White",
    # Drinks
    "咖啡": "Coffee", "茶": "Tea", "牛奶": "Milk", "果汁": "Juice", "水": "Water",
    # Pets
    "狗": "Dog", "猫": "Cat", "鸟": "Bird", "鱼": "Fish", "兔子": "Rabbit",
    # Professions
    "医生": "Doctor", "工程师": "Engineer", "教师": "Teacher", "艺术家": "Artist", "律师": "Lawyer"
}


def normalize_solution(solution, translation_map=None):
    """Convert solution to standard format."""
    normalized = {
        "Person": {},
        "Color": {},
        "Drink": {},
        "Pet": {},
        "Profession": {}
    }

    # Map position labels
    position_map = {
        "Position 1": "1", "Position 2": "2", "Position 3": "3", "Position 4": "4", "Position 5": "5",
        "Pozycja 1": "1", "Pozycja 2": "2", "Pozycja 3": "3", "Pozycja 4": "4", "Pozycja 5": "5",
        "位置 1": "1", "位置 2": "2", "位置 3": "3", "位置 4": "4", "位置 5": "5"
    }

    # Map attribute labels
    attr_map = {
        "Person": "Person", "Osoba": "Person", "人物": "Person",
        "Color": "Color", "Kolor": "Color", "颜色": "Color",
        "Drink": "Drink", "Napój": "Drink", "饮料": "Drink",
        "Pet": "Pet", "Zwierzę": "Pet", "宠物": "Pet",
        "Profession": "Profession", "Zawód": "Profession", "职业": "Profession"
    }

    for pos_label, attrs in solution.items():
        pos = position_map.get(pos_label, pos_label)
        for attr_label, value in attrs.items():
            attr = attr_map.get(attr_label, attr_label)
            translated_value = translation_map.get(value, value) if translation_map else value
            normalized[attr][pos] = translated_value

    return normalized


def calculate_accuracy(proposed, correct):
    """Calculate percentage accuracy."""
    total = 0
    correct_count = 0

    for category in correct:
        for position in correct[category]:
            total += 1
            if (category in proposed and
                position in proposed[category] and
                proposed[category][position] == correct[category][position]):
                correct_count += 1

    return (correct_count / total * 100) if total > 0 else 0


def evaluate_all():
    """Evaluate all three language solutions."""
    results = {}

    # English
    english_normalized = normalize_solution(ENGLISH_SOLUTION)
    english_accuracy = calculate_accuracy(english_normalized, CORRECT_SOLUTION)
    english_answer_correct = (ENGLISH_ANSWER == CORRECT_ANSWER)
    results["English"] = {
        "accuracy": english_accuracy,
        "answer_correct": english_answer_correct,
        "normalized_solution": english_normalized
    }

    # Polish
    polish_normalized = normalize_solution(POLISH_SOLUTION, POLISH_TO_ENGLISH)
    polish_accuracy = calculate_accuracy(polish_normalized, CORRECT_SOLUTION)
    polish_answer_correct = (POLISH_TO_ENGLISH.get(POLISH_ANSWER, POLISH_ANSWER) == CORRECT_ANSWER)
    results["Polish"] = {
        "accuracy": polish_accuracy,
        "answer_correct": polish_answer_correct,
        "normalized_solution": polish_normalized
    }

    # Chinese
    chinese_normalized = normalize_solution(CHINESE_SOLUTION, CHINESE_TO_ENGLISH)
    chinese_accuracy = calculate_accuracy(chinese_normalized, CORRECT_SOLUTION)
    chinese_answer_correct = (CHINESE_TO_ENGLISH.get(CHINESE_ANSWER, CHINESE_ANSWER) == CORRECT_ANSWER)
    results["Chinese"] = {
        "accuracy": chinese_accuracy,
        "answer_correct": chinese_answer_correct,
        "normalized_solution": chinese_normalized
    }

    return results


def print_detailed_comparison(results):
    """Print detailed comparison of results."""
    print("=" * 80)
    print("LANGUAGE-BASED REASONING ACCURACY EXPERIMENT")
    print("=" * 80)
    print()
    print("PUZZLE: Einstein-style logic puzzle with 5 positions, 5 categories")
    print("QUESTION: Who drinks Water?")
    print("CORRECT ANSWER: Alice")
    print()
    print("=" * 80)
    print("RESULTS")
    print("=" * 80)
    print()

    for lang in ["English", "Polish", "Chinese"]:
        result = results[lang]
        print(f"{lang.upper()}:")
        print(f"  Grid Accuracy: {result['accuracy']:.1f}%")
        print(f"  Final Answer: {'✓ CORRECT' if result['answer_correct'] else '✗ INCORRECT'}")
        print()

    print("=" * 80)
    print("ANALYSIS")
    print("=" * 80)
    print()

    # Overall ranking
    ranking = sorted(results.items(), key=lambda x: x[1]['accuracy'], reverse=True)
    print("RANKING BY GRID ACCURACY:")
    for i, (lang, result) in enumerate(ranking, 1):
        status = "✓" if result['answer_correct'] else "✗"
        print(f"  {i}. {lang}: {result['accuracy']:.1f}% {status}")
    print()

    # Detailed error analysis
    print("DETAILED ERROR ANALYSIS:")
    print()
    for lang in ["English", "Polish", "Chinese"]:
        result = results[lang]
        print(f"{lang}:")
        errors = []
        for category in CORRECT_SOLUTION:
            for pos in CORRECT_SOLUTION[category]:
                correct_val = CORRECT_SOLUTION[category][pos]
                proposed_val = result['normalized_solution'].get(category, {}).get(pos, "MISSING")
                if proposed_val != correct_val:
                    errors.append(f"    Position {pos}, {category}: '{proposed_val}' (should be '{correct_val}')")

        if errors:
            print(f"  Found {len(errors)} error(s):")
            for error in errors[:10]:  # Show first 10 errors
                print(error)
            if len(errors) > 10:
                print(f"    ... and {len(errors) - 10} more errors")
        else:
            print("  No errors - perfect solution!")
        print()

    print("=" * 80)
    print("CONCLUSION")
    print("=" * 80)
    print()

    best_accuracy = max(r['accuracy'] for r in results.values())
    best_langs = [lang for lang, r in results.items() if r['accuracy'] == best_accuracy]

    print(f"Best performing language(s): {', '.join(best_langs)}")
    print(f"Accuracy: {best_accuracy:.1f}%")
    print()

    correct_answer_langs = [lang for lang, r in results.items() if r['answer_correct']]
    print(f"Languages that got the correct final answer: {', '.join(correct_answer_langs)}")
    print()

    # Save results to JSON
    summary = {
        "experiment": "Language-based reasoning accuracy",
        "puzzle_type": "Einstein-style logic puzzle",
        "results": {
            lang: {
                "grid_accuracy_percent": result['accuracy'],
                "final_answer_correct": result['answer_correct']
            }
            for lang, result in results.items()
        }
    }

    with open('experiment_results.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print("Results saved to: experiment_results.json")


if __name__ == "__main__":
    results = evaluate_all()
    print_detailed_comparison(results)
