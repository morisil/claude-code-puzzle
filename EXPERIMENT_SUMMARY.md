# Language-Based Reasoning Accuracy Experiment

## Motivation

Inspired by recent research suggesting that prompting in Polish may improve inference accuracy, this experiment tests whether language choice affects logical reasoning performance in AI models.

## Experimental Design

### Puzzle Generation
- Created a synthetic Einstein-style logic puzzle generator
- Generated a complex puzzle with 5 positions and 5 categories (Person, Color, Drink, Pet, Profession)
- 16 clues requiring multi-step deductive reasoning
- Question: "Who drinks Water?"
- Correct answer: **Alice**

### Methodology
1. Generated identical puzzle in three languages: English, Polish, and Chinese
2. Launched three independent subagents (fresh token windows)
3. Each agent solved the puzzle in their assigned language
4. Compared grid accuracy (all 25 attribute assignments) and final answers

### Languages Tested
- **English**: Control language (standard training data language)
- **Polish**: Test language (based on recent research suggesting improved accuracy)
- **Chinese**: Additional comparison (high-resource language, different script)

## Results

| Language | Grid Accuracy | Final Answer | Ranking |
|----------|--------------|--------------|---------|
| English  | 100.0%       | ✓ CORRECT    | 1st     |
| Chinese  | 92.0%        | ✗ INCORRECT  | 2nd     |
| Polish   | 40.0%        | ✓ CORRECT    | 3rd     |

### Detailed Analysis

#### English Performance
- **Perfect solution**: 25/25 attributes correctly assigned
- **Reasoning quality**: Systematic, step-by-step deduction
- **Final answer**: Correct (Alice)

#### Chinese Performance
- **Near-perfect grid**: 23/25 attributes correct (92%)
- **Critical errors**: Swapped Juice and Water between positions 1 and 5
  - Assigned Water to David (position 1) instead of Alice (position 5)
  - Assigned Juice to Alice (position 5) instead of David (position 1)
- **Final answer**: Incorrect (said David instead of Alice)
- **Note**: The reasoning was otherwise excellent, but a single swap led to wrong answer

#### Polish Performance
- **Significant grid errors**: 10/25 attributes correct (40%)
- **Major mistakes**: Swapped positions 2 and 4 entirely (Bob ↔ Emma)
- **Color errors**: Multiple color misassignments
- **Profession errors**: Several profession misassignments
- **Final answer**: Correct (Alicja = Alice)
- **Interesting finding**: Despite many grid errors, correctly identified the person who drinks water

### Error Breakdown

**Polish errors (15 total)**:
- Person assignments: 2 errors (swapped Bob and Emma)
- Colors: 4 errors
- Drinks: 2 errors
- Pets: 2 errors
- Professions: 5 errors

**Chinese errors (2 total)**:
- Drinks: 2 errors (swapped Juice and Water)

## Key Findings

1. **English performed best**: 100% accuracy suggests that standard English prompting works excellently for logical reasoning tasks

2. **Chinese performed well but failed on answer**: High grid accuracy (92%) but made a critical error that led to wrong final answer

3. **Polish had low grid accuracy but correct answer**: This is unexpected and interesting - the agent made many mistakes in the complete solution but still identified the correct person

4. **Hypothesis not confirmed**: The research suggesting Polish improves accuracy was not replicated in this single-puzzle experiment

## Limitations

1. **Sample size**: Only one puzzle tested - results may vary with different puzzles
2. **Translation quality**: Puzzle translations were done by the same AI, which may introduce biases
3. **Model variability**: AI responses have inherent randomness - multiple runs needed for statistical significance
4. **Complexity**: The puzzle may not be complex enough to reveal language-based differences
5. **Cultural context**: Name/category translations might affect reasoning (e.g., "Alicja" vs "Alice")

## Conclusions

Based on this single experiment:
- **English provides the most reliable reasoning** for this type of logic puzzle
- **Language choice does appear to affect reasoning patterns** - different error types emerged
- **Grid accuracy ≠ answer accuracy** - Polish got the answer right despite low grid accuracy
- **More research needed** - One puzzle is insufficient to draw firm conclusions

## Future Research Directions

1. Test with 50-100 different puzzles for statistical significance
2. Try other languages (German, French, Japanese, Arabic, etc.)
3. Test with different puzzle types (math, spatial, verbal reasoning)
4. Analyze reasoning quality, not just accuracy
5. Control for translation effects by using native speakers
6. Test with different model architectures and sizes

## Files Generated

- `puzzle_generator.py` - Synthetic puzzle generator
- `puzzle_description.txt` - English puzzle
- `puzzle_polish.txt` - Polish translation
- `puzzle_chinese.txt` - Chinese translation
- `evaluate_results.py` - Evaluation script
- `experiment_results.json` - Machine-readable results
- `EXPERIMENT_SUMMARY.md` - This document

## Reproducibility

All code and puzzles are included in this repository. The experiment can be reproduced by:
1. Running `python3 puzzle_generator.py` to generate a new puzzle
2. Manually solving with different language prompts
3. Running `python3 evaluate_results.py` to compare results

---

**Experiment Date**: 2025-11-02
**Model Used**: Claude (Sonnet 4.5)
**Puzzle Seed**: 42 (for reproducibility)
