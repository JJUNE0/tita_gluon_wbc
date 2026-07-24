#!/usr/bin/env bash

set -uo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || {
    echo "ERROR: Not inside a Git repository."
    exit 1
}

cd "$ROOT"

result=0

echo
echo "=================================================="
echo "Branch"
echo "=================================================="
git branch --show-current

echo
echo "=================================================="
echo "Git status"
echo "=================================================="
git status --short

echo
echo "=================================================="
echo "Changed files"
echo "=================================================="
git diff HEAD --name-status

echo
echo "=================================================="
echo "Diff statistics"
echo "=================================================="
git diff HEAD --stat

echo
echo "=================================================="
echo "Diff integrity check"
echo "=================================================="
if ! git diff HEAD --check; then
    echo "ERROR: git diff --check failed."
    result=1
else
    echo "PASS: No whitespace or conflict-marker errors."
fi

echo
echo "=================================================="
echo "Fast tests"
echo "=================================================="
if [[ -x "./scripts/test-fast.sh" ]]; then
    if ! ./scripts/test-fast.sh; then
        echo "ERROR: Fast tests failed."
        result=1
    fi
else
    echo "SKIP: scripts/test-fast.sh does not exist or is not executable."
fi

echo
echo "=================================================="
echo "Experiment Log Directory Check"
echo "=================================================="
if [[ -d "docs/exp" ]]; then
    invalid_exp_dirs=$(find docs/exp -mindepth 1 -maxdepth 1 -type d ! -name "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]" 2>/dev/null || true)
    if [[ -n "$invalid_exp_dirs" ]]; then
        echo "ERROR: Invalid experiment directory format found in docs/exp/:"
        echo "$invalid_exp_dirs"
        echo "Directory names in docs/exp/ must follow YYYY-MM-DD format (no hours/minutes)."
        result=1
    else
        echo "PASS: docs/exp/ directory naming convention OK."
    fi
fi


echo
echo "=================================================="
echo "Final result"
echo "=================================================="

if [[ "$result" -eq 0 ]]; then
    echo "PASS"
else
    echo "FAIL"
fi

exit "$result"
