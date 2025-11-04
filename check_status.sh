#!/bin/bash
# Quick command reference for completing the Korean study

echo "=================================="
echo "KOREAN STUDY - EXECUTION STATUS"
echo "=================================="
echo ""

# Count completed tests
completed=$(ls -1 hard_test_responses/*.txt 2>/dev/null | wc -l)
total=50

echo "Completed: $completed / $total tests"
echo "Remaining: $((total - completed)) tests"
echo ""

if [ $completed -eq 50 ]; then
    echo "✅ ALL TESTS COMPLETE!"
    echo ""
    echo "Next step: Run analysis"
    echo "  python3 analyze_korean_study.py"
    echo ""
elif [ $completed -eq 10 ]; then
    echo "📊 Demonstration batch complete (10 tests)"
    echo ""
    echo "Next: Run tests 11-20 (Puzzles 3-4)"
    echo "  View prompts in: subagent_prompts/test_11_prompt.txt through test_20_prompt.txt"
    echo "  Launch 10 Tasks in parallel"
    echo ""
elif [ $completed -eq 20 ]; then
    echo "📊 Batches 1-2 complete (20 tests)"
    echo ""
    echo "Next: Run tests 21-30 (Puzzles 5-6)"
    echo ""
elif [ $completed -eq 30 ]; then
    echo "📊 Batches 1-3 complete (30 tests)"
    echo ""
    echo "Next: Run tests 31-40 (Puzzles 7-8)"
    echo ""
elif [ $completed -eq 40 ]; then
    echo "📊 Batches 1-4 complete (40 tests)"
    echo ""
    echo "Next: Run tests 41-50 (Puzzles 9-10) - FINAL BATCH!"
    echo ""
else
    echo "⚠️  Incomplete - check status"
fi

echo "=================================="
echo "QUICK COMMANDS"
echo "=================================="
echo ""
echo "View test matrix:"
echo "  cat hard_test_execution_metadata.json | jq '.tests[] | select(.test_id > $completed)' | head"
echo ""
echo "Check next prompt:"
echo "  cat subagent_prompts/test_$((completed + 1))_prompt.txt | head -20"
echo ""
echo "Run analysis (after all tests):"
echo "  python3 analyze_korean_study.py"
echo ""
echo "Full instructions:"
echo "  cat EXECUTION_INSTRUCTIONS.md"
echo ""
