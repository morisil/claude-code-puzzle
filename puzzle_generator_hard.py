#!/usr/bin/env python3
"""
Hard Constraint Satisfaction Puzzle Generator
Generates more complex scheduling puzzles with 7 people, 7 slots, and 10-12 constraints
"""

import random
import json
from itertools import permutations
from typing import List, Dict, Tuple, Optional

class HardSchedulingPuzzleGenerator:
    """Generates harder constraint satisfaction puzzles for scheduling problems."""

    def __init__(self, num_people=7, num_slots=7, seed=None):
        if seed:
            random.seed(seed)
        self.num_people = num_people
        self.num_slots = num_slots

        # Expanded name pools for variety
        self.last_names = ['Anderson', 'Brown', 'Chen', 'Davis', 'Evans', 'Fischer',
                          'Green', 'Hughes', 'Ivanov', 'Jones', 'Kumar', 'Lee',
                          'Martinez', 'Nelson', 'O\'Brien', 'Patel', 'Quinn']

        # Expanded time slot pools
        self.morning_slots = ['8:00', '8:30', '9:00', '9:30', '10:00', '10:30', '11:00', '11:30']
        self.afternoon_slots = ['1:00', '1:30', '2:00', '2:30', '3:00', '3:30', '4:00', '4:30', '5:00', '5:30']

    def generate_names(self, count: int) -> List[str]:
        """Generate unique person names."""
        # Ensure we have vowel-starting and consonant-starting names
        vowel_starts = [n for n in self.last_names if n[0] in 'AEIOU']
        consonant_starts = [n for n in self.last_names if n[0] not in 'AEIOU']

        # Randomly select names, ensuring at least two vowel starters
        selected = random.sample(self.last_names, min(count, len(self.last_names)))

        # If less than 2 vowel starters in selection, force them
        vowel_count = sum(1 for n in selected if n[0] in 'AEIOU')
        if vowel_count < 2 and len(vowel_starts) >= 2:
            for i in range(min(2 - vowel_count, len(selected))):
                if selected[i][0] not in 'AEIOU':
                    selected[i] = random.choice([v for v in vowel_starts if v not in selected])

        names = [f"Dr. {name}" for name in selected[:count]]
        return names

    def generate_time_slots(self, count: int) -> List[str]:
        """Generate time slots with AM/PM mix."""
        # Ensure mix of morning and afternoon
        num_morning = random.randint(count // 3, 2 * count // 3)
        num_afternoon = count - num_morning

        morning = random.sample(self.morning_slots, num_morning)
        afternoon = random.sample(self.afternoon_slots, num_afternoon)

        slots = sorted(morning) + sorted(afternoon)
        return slots

    def verify_solution(self, assignment: Dict[str, str], constraints: List) -> bool:
        """Verify if an assignment satisfies all constraints."""
        for constraint in constraints:
            if not constraint['checker'](assignment):
                return False
        return True

    def find_unique_solution(self, people: List[str], slots: List[str],
                            constraints: List, max_check=5000) -> Optional[Dict[str, str]]:
        """Find if there's a unique solution for the given constraints."""
        solutions = []
        checked = 0

        # Try permutations (with limit for performance)
        for perm in permutations(people):
            assignment = {slot: person for slot, person in zip(slots, perm)}
            if self.verify_solution(assignment, constraints):
                solutions.append(assignment)
                if len(solutions) > 1:
                    return None  # Not unique

            checked += 1
            if checked >= max_check:
                break

        return solutions[0] if len(solutions) == 1 else None

    def generate_puzzle(self, puzzle_id: int) -> Dict:
        """Generate a complete puzzle with verified unique solution."""
        max_attempts = 200

        for attempt in range(max_attempts):
            people = self.generate_names(self.num_people)
            slots = self.generate_time_slots(self.num_slots)

            # Generate constraints (10-12 constraints for harder difficulty)
            num_constraints = random.randint(10, 12)
            constraints = self.generate_constraints(people, slots, num_constraints)

            # Find solution (with limited search for performance)
            solution = self.find_unique_solution(people, slots, constraints, max_check=5000)

            if solution:
                # Found valid puzzle
                return {
                    'id': puzzle_id,
                    'people': people,
                    'slots': slots,
                    'constraints_text': [c['text'] for c in constraints],
                    'solution': solution,
                    'num_constraints': len(constraints),
                    'attempt': attempt + 1
                }

        raise Exception(f"Could not generate valid puzzle after {max_attempts} attempts")

    def generate_constraints(self, people: List[str], slots: List[str], num_constraints: int) -> List[Dict]:
        """Generate a set of constraints for the puzzle."""
        constraints = []
        slot_indices = {slot: i for i, slot in enumerate(slots)}
        used_pairs = set()

        constraint_generators = [
            self._gen_before_not_consecutive,
            self._gen_cannot_present_at,
            self._gen_exactly_n_after,
            self._gen_immediately_follows,
            self._gen_vowel_starter,
            self._gen_time_period,
            self._gen_n_between,
            self._gen_not_adjacent_to,
            self._gen_in_first_or_last_half,
            self._gen_at_least_n_apart,
        ]

        # Generate constraints ensuring variety
        attempts = 0
        max_attempts_per_constraint = 20

        while len(constraints) < num_constraints and attempts < num_constraints * max_attempts_per_constraint:
            attempts += 1
            generator = random.choice(constraint_generators)

            try:
                constraint = generator(people, slots, slot_indices, used_pairs)
                if constraint:
                    constraints.append(constraint)
            except:
                continue

        return constraints[:num_constraints]

    # Constraint generators
    def _gen_before_not_consecutive(self, people, slots, slot_indices, used_pairs):
        """Person A before Person B (not consecutive)."""
        available = [p for i, p in enumerate(people) for q in people[i+1:] if (p, q) not in used_pairs and (q, p) not in used_pairs]
        if len(people) < 2:
            return None

        p1, p2 = random.sample(people, 2)
        used_pairs.add((p1, p2))

        return {
            'text': f"{p1} must present before {p2}, but not in consecutive time slots.",
            'checker': lambda assign, p1=p1, p2=p2: self._before_not_consecutive(assign, p1, p2, slot_indices)
        }

    def _gen_cannot_present_at(self, people, slots, slot_indices, used_pairs):
        """Person cannot be at specific slots."""
        p = random.choice(people)
        excluded_slots = random.sample(slots, min(2, len(slots)))

        return {
            'text': f"{p} cannot present at {excluded_slots[0]} or {excluded_slots[1]}.",
            'checker': lambda assign, p=p, ex=excluded_slots: all(
                assign[slot] != p for slot in ex if slot in assign
            )
        }

    def _gen_exactly_n_after(self, people, slots, slot_indices, used_pairs):
        """Person X exactly N slots after Person Y."""
        if len(people) < 2:
            return None

        p1, p2 = random.sample(people, 2)
        offset = random.choice([2, 3, 4])
        used_pairs.add((p1, p2))

        return {
            'text': f"{p1} presents exactly {offset} time slots after {p2}.",
            'checker': lambda assign, p1=p1, p2=p2, off=offset: self._exactly_n_after(assign, p1, p2, off, slot_indices)
        }

    def _gen_immediately_follows(self, people, slots, slot_indices, used_pairs):
        """Person X immediately follows Person Y."""
        if len(people) < 2:
            return None

        p1, p2 = random.sample(people, 2)
        used_pairs.add((p1, p2))

        return {
            'text': f"{p1}'s presentation immediately follows {p2}'s presentation (consecutive slots).",
            'checker': lambda assign, p1=p1, p2=p2: self._immediately_follows(assign, p1, p2, slot_indices)
        }

    def _gen_vowel_starter(self, people, slots, slot_indices, used_pairs):
        """Specific slot has person with vowel-starting name."""
        vowel_slot = random.choice(slots)

        return {
            'text': f"The {vowel_slot} slot is occupied by someone whose name starts with a vowel.",
            'checker': lambda assign, vs=vowel_slot: self._vowel_starter(assign, vs)
        }

    def _gen_time_period(self, people, slots, slot_indices, used_pairs):
        """Person in afternoon/morning."""
        p = random.choice(people)
        is_afternoon = random.choice([True, False])
        afternoon_slots = [s for s in slots if self._is_afternoon(s)]
        morning_slots = [s for s in slots if not self._is_afternoon(s)]

        if is_afternoon and not afternoon_slots:
            return None
        if not is_afternoon and not morning_slots:
            return None

        time_text = "afternoon (1:00 PM or later)" if is_afternoon else "morning (before 1:00 PM)"
        valid_slots = afternoon_slots if is_afternoon else morning_slots

        return {
            'text': f"{p} presents in the {time_text}.",
            'checker': lambda assign, pt=p, vs=valid_slots: any(
                assign[slot] == pt for slot in vs if slot in assign
            )
        }

    def _gen_n_between(self, people, slots, slot_indices, used_pairs):
        """Exactly N presentations between two people."""
        if len(people) < 2:
            return None

        p1, p2 = random.sample(people, 2)
        between_count = random.choice([1, 2, 3])
        used_pairs.add((p1, p2))

        return {
            'text': f"There are exactly {between_count} presentation(s) between {p1} and {p2}.",
            'checker': lambda assign, p1=p1, p2=p2, bc=between_count: self._n_between(assign, p1, p2, bc, slot_indices)
        }

    def _gen_not_adjacent_to(self, people, slots, slot_indices, used_pairs):
        """Person A cannot be adjacent to Person B."""
        if len(people) < 2:
            return None

        p1, p2 = random.sample(people, 2)
        used_pairs.add((p1, p2))

        return {
            'text': f"{p1} and {p2} cannot present in adjacent time slots.",
            'checker': lambda assign, p1=p1, p2=p2: self._not_adjacent(assign, p1, p2, slot_indices)
        }

    def _gen_in_first_or_last_half(self, people, slots, slot_indices, used_pairs):
        """Person presents in first or last half of schedule."""
        p = random.choice(people)
        is_first_half = random.choice([True, False])
        mid_point = len(slots) // 2

        if is_first_half:
            valid_slots = slots[:mid_point]
            text = f"{p} presents in the first half of the schedule."
        else:
            valid_slots = slots[mid_point:]
            text = f"{p} presents in the second half of the schedule."

        return {
            'text': text,
            'checker': lambda assign, pt=p, vs=valid_slots: any(
                assign[slot] == pt for slot in vs if slot in assign
            )
        }

    def _gen_at_least_n_apart(self, people, slots, slot_indices, used_pairs):
        """Person A and B must be at least N slots apart."""
        if len(people) < 2:
            return None

        p1, p2 = random.sample(people, 2)
        min_distance = random.choice([3, 4])
        used_pairs.add((p1, p2))

        return {
            'text': f"{p1} and {p2} must be at least {min_distance} time slots apart.",
            'checker': lambda assign, p1=p1, p2=p2, md=min_distance: self._at_least_n_apart(assign, p1, p2, md, slot_indices)
        }

    # Helper constraint checkers
    def _before_not_consecutive(self, assign: Dict, p1: str, p2: str, slot_idx: Dict) -> bool:
        """Check if p1 is before p2 but not consecutive."""
        p1_slot = None
        p2_slot = None

        for slot, person in assign.items():
            if person == p1:
                p1_slot = slot_idx[slot]
            if person == p2:
                p2_slot = slot_idx[slot]

        if p1_slot is None or p2_slot is None:
            return False

        return p1_slot < p2_slot and abs(p1_slot - p2_slot) > 1

    def _exactly_n_after(self, assign: Dict, p1: str, p2: str, n: int, slot_idx: Dict) -> bool:
        """Check if p1 is exactly n slots after p2."""
        p1_slot = None
        p2_slot = None

        for slot, person in assign.items():
            if person == p1:
                p1_slot = slot_idx[slot]
            if person == p2:
                p2_slot = slot_idx[slot]

        if p1_slot is None or p2_slot is None:
            return False

        return p1_slot == p2_slot + n

    def _immediately_follows(self, assign: Dict, p1: str, p2: str, slot_idx: Dict) -> bool:
        """Check if p1 immediately follows p2."""
        return self._exactly_n_after(assign, p1, p2, 1, slot_idx)

    def _vowel_starter(self, assign: Dict, slot: str) -> bool:
        """Check if person at slot has vowel-starting name."""
        if slot not in assign:
            return False
        person = assign[slot]
        # Extract last name
        name = person.split()[-1]
        return name[0].upper() in 'AEIOU'

    def _is_afternoon(self, slot: str) -> bool:
        """Check if time slot is in afternoon."""
        # Parse hour from slot like "1:00" or "9:00"
        hour = int(slot.split(':')[0])
        return hour >= 1 and hour <= 6  # 1:00 PM to 6:00 PM

    def _n_between(self, assign: Dict, p1: str, p2: str, n: int, slot_idx: Dict) -> bool:
        """Check if exactly n presentations between p1 and p2."""
        p1_slot = None
        p2_slot = None

        for slot, person in assign.items():
            if person == p1:
                p1_slot = slot_idx[slot]
            if person == p2:
                p2_slot = slot_idx[slot]

        if p1_slot is None or p2_slot is None:
            return False

        distance = abs(p1_slot - p2_slot)
        return distance == n + 1

    def _not_adjacent(self, assign: Dict, p1: str, p2: str, slot_idx: Dict) -> bool:
        """Check if p1 and p2 are not adjacent."""
        p1_slot = None
        p2_slot = None

        for slot, person in assign.items():
            if person == p1:
                p1_slot = slot_idx[slot]
            if person == p2:
                p2_slot = slot_idx[slot]

        if p1_slot is None or p2_slot is None:
            return False

        return abs(p1_slot - p2_slot) != 1

    def _at_least_n_apart(self, assign: Dict, p1: str, p2: str, n: int, slot_idx: Dict) -> bool:
        """Check if p1 and p2 are at least n slots apart."""
        p1_slot = None
        p2_slot = None

        for slot, person in assign.items():
            if person == p1:
                p1_slot = slot_idx[slot]
            if person == p2:
                p2_slot = slot_idx[slot]

        if p1_slot is None or p2_slot is None:
            return False

        return abs(p1_slot - p2_slot) >= n

def generate_hard_puzzle_set(num_puzzles: int, output_file: str):
    """Generate a set of hard puzzles and save to JSON."""
    generator = HardSchedulingPuzzleGenerator()
    puzzles = []

    print(f"Generating {num_puzzles} HARD puzzles (7 people, 7 slots, 10-12 constraints)...")
    for i in range(num_puzzles):
        try:
            puzzle = generator.generate_puzzle(i + 1)
            puzzles.append(puzzle)
            print(f"✓ Puzzle {i+1} generated ({puzzle['num_constraints']} constraints, attempt {puzzle['attempt']})")
        except Exception as e:
            print(f"✗ Failed to generate puzzle {i+1}: {e}")

    # Save to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(puzzles, f, indent=2, ensure_ascii=False)

    print(f"\n{len(puzzles)} hard puzzles saved to {output_file}")
    return puzzles

if __name__ == "__main__":
    puzzles = generate_hard_puzzle_set(10, "/home/user/claude-code-puzzle/puzzle_set_hard.json")

    # Print summary
    print("\n" + "="*80)
    print("HARD PUZZLE SET SUMMARY")
    print("="*80)
    for p in puzzles:
        print(f"\nPuzzle {p['id']}:")
        print(f"  People: {', '.join(p['people'])}")
        print(f"  Time slots: {', '.join(p['slots'])}")
        print(f"  Constraints: {p['num_constraints']}")
        print(f"  Solution found in attempt: {p['attempt']}")
