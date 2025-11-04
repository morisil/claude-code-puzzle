#!/usr/bin/env python3
"""
Synthetic Constraint Satisfaction Puzzle Generator
Generates multiple variants of scheduling puzzles with verified solutions
"""

import random
import json
from itertools import permutations
from typing import List, Dict, Tuple, Optional

class SchedulingPuzzleGenerator:
    """Generates constraint satisfaction puzzles for scheduling problems."""

    def __init__(self, num_people=5, num_slots=5, seed=None):
        if seed:
            random.seed(seed)
        self.num_people = num_people
        self.num_slots = num_slots

        # Name pools for variety
        self.first_names = ['Alice', 'Bob', 'Carol', 'David', 'Emma', 'Frank', 'Grace', 'Henry']
        self.last_names = ['Anderson', 'Brown', 'Chen', 'Davis', 'Evans', 'Fischer',
                          'Green', 'Hughes', 'Ivanov', 'Jones']

        # Time slot pools
        self.morning_slots = ['8:00', '9:00', '9:30', '10:00', '10:30', '11:00']
        self.afternoon_slots = ['1:00', '1:30', '2:00', '2:30', '3:00', '3:30', '4:00', '4:30']

    def generate_names(self, count: int) -> List[str]:
        """Generate unique person names."""
        # Ensure we have vowel-starting and consonant-starting names
        vowel_starts = [n for n in self.last_names if n[0] in 'AEIOU']
        consonant_starts = [n for n in self.last_names if n[0] not in 'AEIOU']

        # Randomly select names, ensuring at least one vowel starter
        selected = random.sample(self.last_names, min(count, len(self.last_names)))

        # If no vowel starters in selection, force one
        if vowel_starts and not any(n[0] in 'AEIOU' for n in selected):
            selected[0] = random.choice(vowel_starts)

        names = [f"Dr. {name}" for name in selected[:count]]
        return names

    def generate_time_slots(self, count: int) -> List[str]:
        """Generate time slots with AM/PM mix."""
        # Ensure mix of morning and afternoon
        num_morning = count // 2
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
                            constraints: List) -> Optional[Dict[str, str]]:
        """Find if there's a unique solution for the given constraints."""
        solutions = []

        # Try all permutations
        for perm in permutations(people):
            assignment = {slot: person for slot, person in zip(slots, perm)}
            if self.verify_solution(assignment, constraints):
                solutions.append(assignment)
                if len(solutions) > 1:
                    return None  # Not unique

        return solutions[0] if len(solutions) == 1 else None

    def generate_puzzle(self, puzzle_id: int) -> Dict:
        """Generate a complete puzzle with verified unique solution."""
        max_attempts = 100

        for attempt in range(max_attempts):
            people = self.generate_names(self.num_people)
            slots = self.generate_time_slots(self.num_slots)

            # Generate constraints
            constraints = self.generate_constraints(people, slots)

            # Find solution
            solution = self.find_unique_solution(people, slots, constraints)

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

    def generate_constraints(self, people: List[str], slots: List[str]) -> List[Dict]:
        """Generate a set of constraints for the puzzle."""
        constraints = []
        slot_indices = {slot: i for i, slot in enumerate(slots)}
        used_people = set()

        # Constraint 1: Person A before Person B (not consecutive)
        p1, p2 = random.sample(people, 2)
        used_people.update([p1, p2])
        constraints.append({
            'text': f"{p1} must present before {p2}, but not in consecutive time slots.",
            'checker': lambda assign, p1=p1, p2=p2: self._before_not_consecutive(assign, p1, p2, slot_indices)
        })

        # Constraint 2: Person cannot be at specific slots
        available = [p for p in people if p not in used_people]
        p3 = available[0] if available else people[0]
        used_people.add(p3)
        excluded_slots = random.sample(slots, min(2, len(slots)))
        constraints.append({
            'text': f"{p3} cannot present at {excluded_slots[0]} or {excluded_slots[1]}.",
            'checker': lambda assign, p3=p3, ex=excluded_slots: all(
                assign[slot] != p3 for slot in ex if slot in assign
            )
        })

        # Constraint 3: Person X exactly N slots after Person Y
        available = [p for p in people if p not in used_people]
        if len(available) >= 2:
            p4, p5 = random.sample(available, 2)
        elif len(available) == 1:
            p4 = available[0]
            p5 = random.choice([p for p in people if p != p4])
        else:
            p4, p5 = random.sample(people, 2)

        used_people.update([p4, p5])
        offset = random.choice([2, 3])
        constraints.append({
            'text': f"{p4} presents exactly {offset} time slots after {p5}.",
            'checker': lambda assign, p4=p4, p5=p5, off=offset: self._exactly_n_after(assign, p4, p5, off, slot_indices)
        })

        # Constraint 4: Person immediately after another
        available = [p for p in people if p not in used_people]
        if available:
            p6 = available[0]
            p7 = random.choice([p for p in people if p != p6])
            constraints.append({
                'text': f"{p6}'s presentation immediately follows {p7}'s presentation (consecutive slots).",
                'checker': lambda assign, p6=p6, p7=p7: self._immediately_follows(assign, p6, p7, slot_indices)
            })

        # Constraint 5: Specific slot has person with vowel-starting name
        vowel_slot = random.choice([s for s in slots if ':' in s])
        constraints.append({
            'text': f"The {vowel_slot} slot is occupied by someone whose name starts with a vowel.",
            'checker': lambda assign, vs=vowel_slot: self._vowel_starter(assign, vs)
        })

        # Constraint 6: Person in afternoon/morning
        p_time = random.choice(people)
        is_afternoon = random.choice([True, False])
        afternoon_slots = [s for s in slots if self._is_afternoon(s)]
        morning_slots = [s for s in slots if not self._is_afternoon(s)]

        time_text = "afternoon (1:00 PM or later)" if is_afternoon else "morning (before 1:00 PM)"
        valid_slots = afternoon_slots if is_afternoon else morning_slots

        constraints.append({
            'text': f"{p_time} presents in the {time_text}.",
            'checker': lambda assign, pt=p_time, vs=valid_slots: any(
                assign[slot] == pt for slot in vs if slot in assign
            )
        })

        # Constraint 7: Exactly N presentations between two people
        pairs = [(p1, p2) for p1, p2 in zip(people[:-1], people[1:]) if p1 != p2]
        if pairs:
            pa, pb = random.choice(pairs)
            between_count = random.choice([1, 2])
            constraints.append({
                'text': f"There are exactly {between_count} presentation(s) between {pa} and {pb}.",
                'checker': lambda assign, pa=pa, pb=pb, bc=between_count: self._n_between(assign, pa, pb, bc, slot_indices)
            })

        # Constraint 8: Another time-based constraint
        p_morning = random.choice(people)
        morning_slots_list = [s for s in slots if not self._is_afternoon(s)]
        constraints.append({
            'text': f"{p_morning}'s presentation is in the morning (before 1:00 PM).",
            'checker': lambda assign, pm=p_morning, ms=morning_slots_list: any(
                assign[slot] == pm for slot in ms if slot in assign
            )
        })

        return constraints

    # Helper constraint checkers
    def _before_not_consecutive(self, assign: Dict, p1: str, p2: str, slot_idx: Dict) -> bool:
        """Check if p1 is before p2 but not consecutive."""
        slots_list = sorted(slot_idx.keys(), key=lambda x: slot_idx[x])
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

def generate_puzzle_set(num_puzzles: int, output_file: str):
    """Generate a set of puzzles and save to JSON."""
    generator = SchedulingPuzzleGenerator()
    puzzles = []

    print(f"Generating {num_puzzles} puzzles...")
    for i in range(num_puzzles):
        try:
            puzzle = generator.generate_puzzle(i + 1)
            puzzles.append(puzzle)
            print(f"✓ Puzzle {i+1} generated (attempt {puzzle['attempt']})")
        except Exception as e:
            print(f"✗ Failed to generate puzzle {i+1}: {e}")

    # Save to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(puzzles, f, indent=2, ensure_ascii=False)

    print(f"\n{len(puzzles)} puzzles saved to {output_file}")
    return puzzles

if __name__ == "__main__":
    puzzles = generate_puzzle_set(5, "/home/user/claude-code-puzzle/puzzle_set.json")

    # Print summary
    print("\n" + "="*80)
    print("PUZZLE SET SUMMARY")
    print("="*80)
    for p in puzzles:
        print(f"\nPuzzle {p['id']}:")
        print(f"  People: {', '.join(p['people'])}")
        print(f"  Time slots: {', '.join(p['slots'])}")
        print(f"  Constraints: {p['num_constraints']}")
        print(f"  Solution found in attempt: {p['attempt']}")
