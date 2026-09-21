#!/usr/bin/env bash
set -o pipefail

# --- Configuration ---
CONFIG_FILE="$UPLOADED_FILES/mypy.ini"
TARGET_PATH="assignment.py"     # Target file or directory
MAX_POINTS=10                   # Total points possible
PENALTY_PER_ERROR=2             # Deduction per mypy error
MIN_SCORE=0                     # Floor score

award() {  # print score line + structured output, always exit 0 so feedback shows
    echo "{\"tag\": \"points\", \"points\": \"$1/${MAX_POINTS}\"}" >&3
    exit 0
}

echo "=========================================="
echo " Running Static Type Analysis (mypy)"
echo "=========================================="

# Guard 1: the expected file must exist
if [ ! -e "$TARGET_PATH" ]; then
    echo "ERROR: $TARGET_PATH not found in your submission."
    echo "Make sure your file is named exactly: $TARGET_PATH"
    award 0
fi

# Run mypy and capture output + exit code
MYPY_OUTPUT=$(python3 -m mypy --config-file "$CONFIG_FILE" --strict --allow-untyped-decorators "$TARGET_PATH" 2>&1)
EXIT_CODE=$?

echo "$MYPY_OUTPUT"
echo "=========================================="

ERROR_COUNT=$(echo "$MYPY_OUTPUT" | grep -c ": error:")

# Guard 2: mypy failed without producing type errors (crash, bad config,
# unreadable file). Without this, a broken run scores full points.
if [ "$EXIT_CODE" -ne 0 ] && [ "$ERROR_COUNT" -eq 0 ]; then
    echo "mypy could not analyze the submission (exit code $EXIT_CODE)."
    echo "No type check was performed, so no points were awarded."
    echo "If you believe this is a mistake, contact your teacher."
    award 0
fi

# --- Scoring ---
DEDUCTION=$(( ERROR_COUNT * PENALTY_PER_ERROR ))
RAW_SCORE=$(( MAX_POINTS - DEDUCTION ))
FINAL_SCORE=$(( RAW_SCORE < MIN_SCORE ? MIN_SCORE : RAW_SCORE ))
PERCENTAGE=$(( FINAL_SCORE * 100 / MAX_POINTS ))

echo "SUMMARY:"
echo " - Total Errors Found : $ERROR_COUNT"
echo " - Penalty per Error  : -$PENALTY_PER_ERROR pts"
echo " - Final Score        : $FINAL_SCORE / $MAX_POINTS ($PERCENTAGE%)"
echo "=========================================="

award "$FINAL_SCORE"
