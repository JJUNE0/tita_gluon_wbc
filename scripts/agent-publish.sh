#!/usr/bin/env bash

set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 \"commit and PR title\""
    exit 2
fi

TITLE="$1"
BRANCH="$(git branch --show-current)"

case "$BRANCH" in
    ""|main|master)
        echo "ERROR: Refusing to publish from branch '$BRANCH'."
        echo "Create an agent task branch first."
        exit 1
        ;;
esac

if [[ "$BRANCH" != agent/* ]]; then
    echo "ERROR: Branch must follow: agent/<tool>/<task>"
    echo "Current branch: $BRANCH"
    exit 1
fi

if [[ -z "$(git status --porcelain)" ]]; then
    echo "ERROR: No changes to publish."
    exit 1
fi

./scripts/agent-check.sh

echo
echo "Changes to be committed:"
git status --short

git add -A
git commit -m "$TITLE"
git push --set-upstream origin "$BRANCH"

gh pr create \
    --draft \
    --fill \
    --title "$TITLE"

echo
echo "Published draft pull request."
git rev-parse --short HEAD
