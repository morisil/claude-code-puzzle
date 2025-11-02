#!/usr/bin/env python3
"""
Synthetic Logical Puzzle Generator
Generates Einstein-style logic puzzles requiring complex deductive reasoning
"""

import random
import json
from typing import Dict, List, Tuple
from itertools import permutations


class LogicPuzzleGenerator:
    """Generates constraint-based logic puzzles with verifiable solutions."""

    def __init__(self, seed: int = 42):
        random.seed(seed)
        self.solution = {}
        self.clues = []

    def generate_puzzle(self, num_positions: int = 5) -> Dict:
        """
        Generate a logic puzzle with multiple categories and constraints.

        Args:
            num_positions: Number of positions/houses (complexity scales with this)

        Returns:
            Dictionary containing puzzle data, clues, and solution
        """
        # Define categories and their values
        categories = {
            'Person': ['Alice', 'Bob', 'Carol', 'David', 'Emma'],
            'Color': ['Red', 'Blue', 'Green', 'Yellow', 'White'],
            'Drink': ['Coffee', 'Tea', 'Milk', 'Juice', 'Water'],
            'Pet': ['Dog', 'Cat', 'Bird', 'Fish', 'Rabbit'],
            'Profession': ['Doctor', 'Engineer', 'Teacher', 'Artist', 'Lawyer']
        }

        # Generate a valid solution
        self.solution = self._generate_solution(categories, num_positions)

        # Generate clues that lead to the solution
        self.clues = self._generate_clues(self.solution, categories, num_positions)

        # Create puzzle structure
        puzzle = {
            'num_positions': num_positions,
            'categories': categories,
            'clues': self.clues,
            'solution': self.solution,
            'question': 'Who drinks Water?'
        }

        return puzzle

    def _generate_solution(self, categories: Dict, num_positions: int) -> Dict:
        """Generate a random valid solution."""
        solution = {}

        for category, values in categories.items():
            # Shuffle and assign values to positions
            shuffled = values[:num_positions].copy()
            random.shuffle(shuffled)
            solution[category] = {i+1: shuffled[i] for i in range(num_positions)}

        return solution

    def _generate_clues(self, solution: Dict, categories: Dict, num_positions: int) -> List[str]:
        """Generate clues that uniquely determine the solution."""
        clues = []
        cat_names = list(categories.keys())

        # Type 1: Direct position clues
        clues.append(f"The {solution['Person'][1]} lives in position 1.")
        clues.append(f"The person in position {num_positions} has a {solution['Pet'][num_positions]}.")

        # Type 2: Adjacent clues
        pos = random.randint(1, num_positions-1)
        clues.append(f"The {solution['Color'][pos]} house is immediately to the left of the {solution['Color'][pos+1]} house.")

        # Type 3: Same position clues (property co-occurrence)
        for i in range(2, num_positions):
            person = solution['Person'][i]
            drink = solution['Drink'][i]
            clues.append(f"{person} drinks {drink}.")

        # Type 4: Color and profession
        for i in range(1, num_positions+1):
            if i not in [1, num_positions]:  # Skip positions we already used
                color = solution['Color'][i]
                profession = solution['Profession'][i]
                clues.append(f"The {profession} lives in the {color} house.")

        # Type 5: Pet and drink relationships
        for i in range(1, num_positions+1):
            if solution['Pet'][i] != solution['Pet'][num_positions]:  # Vary the clues
                pet = solution['Pet'][i]
                person = solution['Person'][i]
                clues.append(f"{person} has a {pet}.")

        # Type 6: Positional relationships
        pos1 = random.randint(1, num_positions-2)
        pos2 = pos1 + 2
        clues.append(f"The {solution['Profession'][pos1]} lives exactly two positions to the left of the {solution['Profession'][pos2]}.")

        # Type 7: Middle position clue
        mid = (num_positions + 1) // 2
        clues.append(f"The person who drinks {solution['Drink'][mid]} lives in the middle position (position {mid}).")

        # Type 8: Negative clues (what's NOT true)
        wrong_pos = random.randint(2, num_positions-1)
        wrong_drink = [d for d in categories['Drink'] if d != solution['Drink'][wrong_pos]][0]
        clues.append(f"The person in position {wrong_pos} does NOT drink {wrong_drink}.")

        # Shuffle clues to make it harder
        random.shuffle(clues)

        return clues

    def verify_solution(self, proposed_solution: Dict, correct_solution: Dict) -> Tuple[bool, float]:
        """
        Verify if a proposed solution matches the correct solution.

        Returns:
            Tuple of (is_correct, accuracy_percentage)
        """
        total_assignments = 0
        correct_assignments = 0

        for category in correct_solution:
            for position in correct_solution[category]:
                total_assignments += 1
                if (category in proposed_solution and
                    position in proposed_solution[category] and
                    proposed_solution[category][position] == correct_solution[category][position]):
                    correct_assignments += 1

        accuracy = (correct_assignments / total_assignments * 100) if total_assignments > 0 else 0
        is_correct = (accuracy == 100.0)

        return is_correct, accuracy

    def format_puzzle_description(self, puzzle: Dict) -> str:
        """Format puzzle as a human-readable description."""
        description = "LOGIC PUZZLE\n" + "="*50 + "\n\n"
        description += f"There are {puzzle['num_positions']} positions (numbered 1 to {puzzle['num_positions']}).\n"
        description += "Each position has a unique combination of:\n"

        for category, values in puzzle['categories'].items():
            description += f"  - {category}: {', '.join(values[:puzzle['num_positions']])}\n"

        description += "\nCLUES:\n"
        for i, clue in enumerate(puzzle['clues'], 1):
            description += f"{i}. {clue}\n"

        description += f"\nQUESTION: {puzzle['question']}\n"

        return description


def main():
    """Generate and save a puzzle."""
    generator = LogicPuzzleGenerator(seed=42)
    puzzle = generator.generate_puzzle(num_positions=5)

    # Save puzzle
    with open('puzzle.json', 'w') as f:
        json.dump(puzzle, f, indent=2)

    # Print puzzle description
    description = generator.format_puzzle_description(puzzle)
    print(description)
    print("\n" + "="*50)
    print("SOLUTION (for verification):")
    print(json.dumps(puzzle['solution'], indent=2))

    # Save formatted descriptions
    with open('puzzle_description.txt', 'w') as f:
        f.write(description)

    print("\n✓ Puzzle saved to puzzle.json")
    print("✓ Description saved to puzzle_description.txt")


if __name__ == "__main__":
    main()
