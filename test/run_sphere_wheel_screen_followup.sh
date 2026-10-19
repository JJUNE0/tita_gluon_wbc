#!/usr/bin/env bash
# VALIDATION_SIM: after the training chain (exp4 100k, exp5) finishes, export the new checkpoints and run
# the same screen into docs/exp/2026-10-19/sphere_wheel_screen (existing results are kept). No robot command.
set -uo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$REPO/docs/exp/2026-10-19/sphere_wheel_screen"
while systemctl --user is-active --quiet sphere-chain; do sleep 120; done
echo "[VALIDATION_SIM] training chain finished at $(date -Is)"
cd "$REPO"
/home/cocel/isaac/env_isaaclab/bin/python -u test/screen_sphere_wheel_runs.py --output "$OUT" --prepare
/home/cocel/venvs/cosim_ros2_jazzy/bin/python -u test/screen_sphere_wheel_runs.py --output "$OUT" --evaluate --workers 8
/home/cocel/venvs/cosim_ros2_jazzy/bin/python -u test/screen_sphere_wheel_runs.py --output "$OUT" --summarize
echo "[VALIDATION_SIM] follow-up screen finished at $(date -Is)"
