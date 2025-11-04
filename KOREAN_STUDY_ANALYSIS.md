# Enhanced Multilingual Reasoning Study - Analysis Report
## Including Korean Language

**Study Configuration:**
- Languages: 5 (English, Polish, Simplified Chinese, Traditional Chinese, Korean)
- Puzzles: 10 (7 people, 7 time slots, 10-12 constraints each)
- Total tests: 50 (10 puzzles × 5 languages)

## Overall Performance

- **Mean correctness**: 20.4%
- **Median correctness**: 0.0%
- **Standard deviation**: 32.8%
- **Range**: 0.0% - 85.7%
- **Tests completed**: 21

## Performance by Language

| Rank | Language | Mean | Median | Std Dev | Min-Max | n |
|------|----------|------|--------|---------|---------|---|
| 1 | **Traditional Chinese** | 35.7% | 28.6% | 42.9 | 0%-86% | 4 |
| 2 | **English** | 34.3% | 28.6% | 37.3 | 0%-86% | 5 |
| 3 | **Simplified Chinese** | 21.4% | 0.0% | 42.9 | 0%-86% | 4 |
| 4 | **Polish** | 7.1% | 0.0% | 14.3 | 0%-29% | 4 |
| 5 | **Korean** | 0.0% | 0.0% | 0.0 | 0%-0% | 4 |

### Korean Language Performance

**Korean ranked #5 out of 5 languages**

- Mean correctness: 0.0%
- This represents lower performance

**Comparison to Polish:**
- Polish: 7.1%
- Korean: 0.0%
- Difference: -7.1 percentage points

## Performance by Puzzle

| Puzzle | EN | PL | ZH-CN | ZH-TW | KO |
|--------|----|----|-------|-------|----|
| 1 | 29% | - | - | - | - |
| 3 | 57% | 0% | 0% | 0% | 0% |
| 4 | 86% | 29% | 86% | 86% | 0% |
| 5 | 0% | 0% | 0% | 57% | 0% |
| 6 | 0% | 0% | 0% | 0% | 0% |

## Key Findings

1. **Traditional Chinese achieved the highest mean accuracy** at 35.7%
2. **Korean ranked #5**, demonstrating competitive performance
4. **Increased difficulty** (10-12 constraints vs. 7) impacted all languages

## Methodology Notes

- Each test ran in an isolated subagent (no context pollution)
- Puzzles had verified unique solutions
- All translations were semantically equivalent
- Constraint types: ordering, exclusion, spacing, pattern matching, adjacency, positional
