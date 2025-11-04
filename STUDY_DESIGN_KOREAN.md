# Enhanced Multilingual Reasoning Study with Korean Language

## Study Design Overview

This enhanced study builds upon the original Polish reasoning language experiment by:
1. **Increasing difficulty**: 7 researchers, 7 time slots, 10-12 constraints (vs. original 5/5/7)
2. **Adding Korean language**: Testing 5 languages total (English, Polish, Simplified Chinese, Traditional Chinese, Korean)
3. **Expanding test count**: 50 tests (10 puzzles × 5 languages) vs. original 20 tests
4. **Ensuring isolation**: Each test runs in a separate subagent to prevent context pollution

## Study Parameters

### Puzzle Complexity
- **People**: 7 researchers (up from 5)
- **Time slots**: 7 slots spanning morning and afternoon (up from 5)
- **Constraints**: 10-12 constraints per puzzle (up from 7)
- **Constraint types**: 10 different constraint patterns including:
  - Ordering constraints (before/after, not consecutive)
  - Exclusion constraints (cannot present at specific times)
  - Spacing constraints (exactly N slots between)
  - Pattern constraints (vowel-starting names, time period requirements)
  - Adjacency constraints (must/must not be adjacent)
  - Positional constraints (first/second half of schedule)

### Languages Tested

| Language | Code | Why Tested |
|----------|------|------------|
| English | en | Baseline/control (primary training language) |
| Polish | pl | Top performer in ONERULER study |
| Simplified Chinese | zh-CN | High efficiency, logographic system |
| Traditional Chinese | zh-TW | Character set comparison |
| **Korean** | **ko** | **NEW: Agglutinative language with unique writing system** |

### Why Korean?

Korean presents interesting linguistic features:
- **Agglutinative morphology**: Similar to Turkish, Finnish
- **Hangul writing system**: Alphabetic but arranged in syllabic blocks
- **Subject-Object-Verb (SOV) word order**: Different from English (SVO) and Polish (relatively free)
- **Honorific system**: Rich grammatical encoding of social relationships
- **Hybrid character density**: Between alphabetic and logographic systems

This allows us to test whether:
1. Agglutinative features provide reasoning advantages similar to Polish's inflectional richness
2. The unique Hangul system affects logical reasoning differently than pure alphabets or logographs
3. SOV word order impacts constraint processing

## Test Matrix

**Total tests**: 50 (10 puzzles × 5 languages)

### Puzzle Distribution

| Puzzle ID | Constraints | People | Slots | Languages |
|-----------|-------------|--------|-------|-----------|
| 1 | 10 | 7 | 7 | 5 |
| 2 | 10 | 7 | 7 | 5 |
| 3 | 12 | 7 | 7 | 5 |
| 4 | 10 | 7 | 7 | 5 |
| 5 | 10 | 7 | 7 | 5 |
| 6 | 10 | 7 | 7 | 5 |
| 7 | 11 | 7 | 7 | 5 |
| 8 | 10 | 7 | 7 | 5 |
| 9 | 11 | 7 | 7 | 5 |
| 10 | 12 | 7 | 7 | 5 |

**Average constraints per puzzle**: 10.6 (vs. 7 in original study)

## Methodology

### Test Execution Strategy

**Isolation Protocol**:
- Each of the 50 tests runs in a completely separate subagent
- No shared context between tests
- Prevents language contamination effects
- Ensures independent reasoning for each language

**Test Workflow**:
1. Generate puzzle with verified unique solution
2. Translate to all 5 languages
3. Launch 5 independent subagents (one per language)
4. Collect responses
5. Analyze correctness, reasoning quality, and efficiency

### Translation Quality

All translations are semantically equivalent:
- Native-level language proficiency
- Culturally appropriate terminology (e.g., "Dr." titles in all languages)
- Maintained constraint clarity across languages
- Korean translations use appropriate formal register (합쇼체/hapsyoche)

## Expected Outcomes

### Hypotheses

**H1: Polish maintains top performance**
- Based on ONERULER findings and original study (84% accuracy)
- Morphological richness aids constraint tracking

**H2: Korean shows strong performance**
- Agglutinative features may provide similar benefits to Polish inflections
- Rich case-marking system could aid entity tracking
- Syllabic block structure might enhance visual parsing

**H3: Chinese languages remain efficient**
- High token efficiency (3-4x better than alphabetic languages)
- Compact representation of logical constraints

**H4: Performance decreases with increased difficulty**
- More constraints create more opportunities for errors
- Baseline accuracy expected to be lower than original study across all languages

### Metrics

1. **Correctness**: Percentage of correctly assigned time slots (0-100%)
2. **Constraint satisfaction**: Which constraints were violated in incorrect solutions
3. **Word/character count**: Response length and efficiency
4. **Reasoning quality**: Systematic approach, verification present
5. **Error patterns**: Types of errors by language

## Comparative Analysis

### vs. Original Study

| Aspect | Original Study | Enhanced Study |
|--------|---------------|----------------|
| **Languages** | 4 (EN, PL, ZH-CN, ZH-TW) | **5 (+Korean)** |
| **Puzzles** | 5 | **10** |
| **Total tests** | 20 | **50** |
| **Puzzle size** | 5 people, 5 slots | **7 people, 7 slots** |
| **Constraints** | 7 per puzzle | **10-12 per puzzle** |
| **Difficulty** | Medium | **Hard** |
| **Context isolation** | Not specified | **Strict (separate subagents)** |

### vs. ONERULER Paper

| Aspect | ONERULER | This Study |
|--------|----------|------------|
| **Task type** | Long-context retrieval | Short-term logical reasoning |
| **Context length** | 8K-128K tokens | ~2K tokens |
| **Languages tested** | 26 | 5 (focused subset) |
| **Polish ranking** | #1 | Hypothesis: #1 |
| **Korean tested** | No | **Yes** |

## Infrastructure

### Files Created

**Puzzle Generation**:
- `puzzle_generator_hard.py`: Generates 7×7 puzzles with 10-12 constraints
- `puzzle_set_hard.json`: 10 generated puzzles with verified solutions

**Translation**:
- `multilingual_prompts_with_korean.py`: Supports 5 languages including Korean
- `hard_test_prompts/`: 50 translated prompt files

**Test Execution**:
- `prepare_hard_test_matrix.py`: Creates 50-test matrix
- `run_hard_tests_with_subagents.py`: Generates isolated test execution plans
- `hard_test_matrix.json`: Complete test configuration
- `hard_test_execution_metadata.json`: Metadata for all 50 tests

**Analysis**:
- (To be created) Analysis scripts for 5-language comparison
- (To be created) Statistical analysis including Korean

### Test Execution

Each test follows this prompt structure:
```
You are solving Test [ID]: Puzzle [N] in [Language].

[Puzzle prompt in target language]

INSTRUCTIONS:
1. Show complete reasoning process
2. Track each constraint carefully
3. Verify final answer against ALL constraints
4. Present final answer in clear format
```

Responses are saved to:
```
hard_test_responses/puzzle_[N]_[lang]_response.txt
```

## Research Questions

### Primary Questions

1. **Does Polish maintain its advantage with increased difficulty?**
   - Original study: 84% (medium difficulty)
   - This study: ? (hard difficulty)

2. **How does Korean compare to Polish?**
   - Both have rich morphological features
   - Different language families (Indo-European vs. Koreanic)
   - Different writing systems (alphabet vs. syllabic blocks)

3. **Do agglutinative features help reasoning?**
   - Korean agglutination vs. Polish inflection
   - Impact on constraint satisfaction problems

4. **How does difficulty scale across languages?**
   - Uniform impact or language-specific degradation?
   - Which constraints are hardest for which languages?

### Secondary Questions

5. **Does Hangul's unique structure affect reasoning?**
   - Alphabetic components arranged in syllabic blocks
   - Visual density between Roman alphabet and Chinese characters

6. **How does SOV word order impact constraint processing?**
   - Korean and some Polish constructions use SOV
   - English uses SVO
   - Does this affect temporal/sequential reasoning?

7. **What is the optimal language for different constraint types?**
   - Ordering constraints
   - Spacing constraints
   - Exclusion constraints
   - Pattern matching constraints

## Implementation Status

### Completed ✓

- [x] Hard puzzle generator (7×7, 10-12 constraints)
- [x] Korean language support in translation system
- [x] 10 hard puzzles generated with verified solutions
- [x] 50 prompts generated (10 puzzles × 5 languages)
- [x] Test matrix and execution infrastructure
- [x] First batch of 10 tests executed (Puzzles 1-2, all languages)

### In Progress

- [ ] Complete remaining 40 tests
- [ ] Analysis scripts for 5 languages
- [ ] Statistical analysis including Korean data

### Planned

- [ ] Comparative analysis with original study
- [ ] Language-specific error analysis
- [ ] Constraint difficulty ranking by language
- [ ] Final research report with Korean findings

## Expected Impact

### Scientific Contribution

1. **First systematic study of Korean for LLM reasoning tasks**
   - No prior work on Korean reasoning performance
   - Fills gap in linguistic diversity research

2. **Increased difficulty testing**
   - Shows how language advantages scale with problem complexity
   - More realistic task difficulty

3. **Methodological rigor**
   - Strict context isolation prevents contamination
   - Larger sample size (n=10 per language vs. n=5)

### Practical Implications

1. **Language selection guidance**
   - Which language for which task type and difficulty?
   - Trade-offs between accuracy and efficiency

2. **Multilingual prompt engineering**
   - Best practices for complex reasoning tasks
   - Language-specific prompt optimization

3. **Model training insights**
   - Which linguistic features correlate with reasoning performance?
   - How to balance training data across languages?

## Timeline

**Phase 1: Design & Implementation** ✓ (Completed)
- Puzzle generator
- Korean translation support
- Infrastructure setup

**Phase 2: Test Execution** (In Progress)
- Batch 1 (Tests 1-10): ✓ Completed
- Batch 2 (Tests 11-20): Pending
- Batch 3 (Tests 21-30): Pending
- Batch 4 (Tests 31-40): Pending
- Batch 5 (Tests 41-50): Pending

**Phase 3: Analysis** (Pending)
- Response parsing
- Correctness scoring
- Statistical analysis
- Report generation

**Phase 4: Publication** (Pending)
- Comprehensive analysis report
- Comparison with original study
- Korean language findings

## Conclusion

This enhanced study represents a significant expansion of the original Polish reasoning language experiment:
- **2.5x more tests** (50 vs. 20)
- **50% harder puzzles** (10-12 constraints vs. 7)
- **New language** (Korean) with unique linguistic properties
- **Rigorous methodology** (strict context isolation)

The addition of Korean is particularly valuable as it represents an understudied language family (Koreanic) with unique features (agglutinative morphology, Hangul script, SOV order) that may shed light on which linguistic properties enable better logical reasoning in large language models.

Results will extend our understanding of:
- Language-reasoning relationships in LLMs
- Scalability of language advantages with difficulty
- Optimal language selection for different task types
- The role of morphological richness, writing systems, and word order in logical reasoning

---

**Study Status**: Infrastructure Complete, Testing Phase 1 of 5 Complete
**Next Steps**: Complete test execution, implement 5-language analysis, generate comprehensive report with Korean findings
