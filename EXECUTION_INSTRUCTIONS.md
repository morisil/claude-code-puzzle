# INSTRUCTIONS FOR COMPLETING THE KOREAN STUDY

## Current Status

**✅ COMPLETED:**
- Infrastructure: All generators, translators, test matrix ready
- Puzzles: 10 hard puzzles generated and verified
- Prompts: 50 prompts in 5 languages
- Test Matrix: All 50 tests configured
- Analysis: Scripts ready to process results
- Demonstration: Tests 1-10 completed (Puzzles 1-2, all languages)

**❌ REMAINING:**
- Tests 11-50: Need to be executed (40 tests remaining)
- Full Analysis: Once all tests complete
- Final Report: Comprehensive comparison with Korean results

## How to Complete the Study

### Option 1: Run All Remaining Tests (Recommended)

Execute tests 11-50 in batches using the Task tool with subagent isolation:

```python
# Tests are already prepped in subagent_prompts/
# Each file: test_N_prompt.txt contains the complete prompt

# Launch tests 11-20 (Puzzles 3-4)
# Launch tests 21-30 (Puzzles 5-6)
# Launch tests 31-40 (Puzzles 7-8)
# Launch tests 41-50 (Puzzles 9-10)
```

**Important:** Each test MUST run in a separate Task/subagent to prevent context pollution.

### Option 2: Quick Test Pattern

To launch a batch, read the prompts and create Task tool calls:

```bash
# Example for tests 11-15:
for i in {11..15}; do
  cat subagent_prompts/test_${i}_prompt.txt
done
```

Then create 5 Task tool invocations in parallel, one for each test.

### Step-by-Step Execution Guide

1. **Verify Current State**
   ```bash
   cd /home/user/claude-code-puzzle
   ls hard_test_responses/
   # Should see puzzle_1_en_response.txt only (from demo)
   ```

2. **Launch Test Batches**

   For each batch of 10 tests:
   - Read the 10 prompt files from `subagent_prompts/`
   - Launch 10 parallel Task tool calls with `subagent_type="general-purpose"`
   - Each prompt contains the complete puzzle in target language
   - Save each response to the specified `hard_test_responses/` file

3. **Save Responses**

   After each subagent completes, write its response to:
   ```
   hard_test_responses/puzzle_{N}_{lang}_response.txt
   ```

   Extract the response content from the Task tool result and save it.

4. **Run Analysis After All Tests Complete**
   ```bash
   python3 analyze_korean_study.py
   ```

   This will:
   - Parse all 50 responses
   - Calculate correctness scores
   - Generate statistics by language
   - Create KOREAN_STUDY_ANALYSIS.md report

5. **Review Results**
   ```bash
   cat KOREAN_STUDY_ANALYSIS.md
   cat korean_study_results.json
   ```

## Batch Execution Template

Here's the pattern for running a batch of 10 tests:

```
1. Read prompts for tests N to N+9
2. Launch 10 Task tools in PARALLEL (single message, multiple tool uses)
3. Each Task should:
   - Use subagent_type="general-purpose"
   - description: "Solve Test X - Puzzle Y Language"
   - prompt: [content from test_X_prompt.txt]
4. Wait for all 10 to complete
5. Save each response to appropriate file
6. Move to next batch
```

## Expected Timeline

- **Batch 2** (Tests 11-20): ~10-15 minutes
- **Batch 3** (Tests 21-30): ~10-15 minutes
- **Batch 4** (Tests 31-40): ~10-15 minutes
- **Batch 5** (Tests 41-50): ~10-15 minutes
- **Analysis**: ~2 minutes
- **Total**: ~45-60 minutes for all 40 remaining tests

## Test Metadata Reference

```json
Test 11: Puzzle 3, English
Test 12: Puzzle 3, Polish
Test 13: Puzzle 3, Simplified Chinese
Test 14: Puzzle 3, Traditional Chinese
Test 15: Puzzle 3, Korean

Test 16: Puzzle 4, English
Test 17: Puzzle 4, Polish
... (pattern continues)

Test 46: Puzzle 10, English
Test 47: Puzzle 10, Polish
Test 48: Puzzle 10, Simplified Chinese
Test 49: Puzzle 10, Traditional Chinese
Test 50: Puzzle 10, Korean
```

## Verification Checklist

After completing all tests:

- [ ] 50 response files exist in `hard_test_responses/`
- [ ] Each file contains a complete solution attempt
- [ ] Run `python3 analyze_korean_study.py` successfully
- [ ] Review KOREAN_STUDY_ANALYSIS.md for results
- [ ] Check Korean language ranking
- [ ] Compare to original study (Polish was #1 at 84%)

## What to Look For

### Expected Findings:

1. **Overall accuracy should decrease** (harder puzzles)
   - Original study: 68-84% range
   - This study: Expect 50-75% range

2. **Korean performance** (unknown, first test!)
   - Hypothesis: 60-75% (competitive with Polish)
   - Compare agglutinative vs. inflectional morphology

3. **Language rankings may shift**
   - Polish may maintain #1
   - Korean position relative to Chinese languages?
   - English baseline performance

4. **Difficulty scaling**
   - Which languages degrade more with complexity?
   - Which constraint types are hardest per language?

## Post-Analysis Tasks

After all 50 tests complete and analysis runs:

1. **Commit Results**
   ```bash
   git add hard_test_responses/ *.md *.json
   git commit -m "Complete all 50 tests for Korean study"
   git push
   ```

2. **Generate Final Report**
   - Compare with original study results
   - Highlight Korean findings
   - Statistical significance tests
   - Language-specific error patterns

3. **Update README**
   - Change status from "Demonstration" to "Complete"
   - Add final statistics
   - Update conclusions

## Quick Start Command

To immediately continue the study:

```bash
cd /home/user/claude-code-puzzle

# Check status
ls -l hard_test_responses/ | wc -l
# Should show 1 (only demo test)

# View next test to run
cat subagent_prompts/test_11_prompt.txt

# Then launch tests 11-20 using Task tool in parallel
```

## Files to Monitor

- `hard_test_responses/`: Should grow from 1 to 50 files
- `korean_study_results.json`: Final results after analysis
- `KOREAN_STUDY_ANALYSIS.md`: Generated report

## Troubleshooting

**If a test fails:**
- Rerun that specific test individually
- Check the prompt file for issues
- Verify puzzle has a valid solution in `puzzle_set_hard.json`

**If analysis fails:**
- Check all 50 response files exist
- Verify response files contain parseable schedules
- Run with verbose output for debugging

## Success Criteria

Study is complete when:
1. All 50 response files exist and contain solutions
2. Analysis runs without errors
3. KOREAN_STUDY_ANALYSIS.md generated with statistics
4. Korean language ranking determined
5. Comparison to original study documented

---

**Current Branch:** `claude/add-korean-harder-tests-011CUoFDDXemgcgFUHhKPFzF`

**Status:** Infrastructure Complete ✅ | Testing: 10/50 (20%) 🔄 | Analysis: Ready ⏳

**Next Action:** Run tests 11-50 in batches of 10 using Task tool with parallel execution.
