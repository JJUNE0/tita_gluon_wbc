#!/usr/bin/env bash
# TRAINING_SIM: queue the heading-drift run after the sphere-wheel training chain (exp5) finishes.
#   DDT-Velocity-Flat-Tita-My-PosKneeMA2-Sphere-Fast-Heading-v0 = exp3 (sphere, MA2, +-1.5/+-3, no ramp)
#   + zero_command_heading_drift reward + critic heading_drift_error. FlashSAC, seed 42, 100k steps, 4096 envs.
# Own systemd user unit (MemoryMax) so VS Code memory pressure cannot kill it. No robot command.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$REPO/docs/exp/2026-10-19/heading_drift_experiment"
PY=/home/cocel/isaac/env_isaaclab/bin/python
UNIT=heading-ma2-fast-s42
mkdir -p "$OUT"
systemctl --user reset-failed "$UNIT" 2>/dev/null || true
systemd-run --user --unit="$UNIT" -p MemoryMax=16G -p MemoryHigh=14G \
  --setenv=WANDB_USERNAME="${WANDB_USERNAME:-}" --setenv=HOME="$HOME" --working-directory="$REPO/lab/ddt_lab" \
  -p StandardOutput=append:"$OUT/${UNIT}_console.log" -p StandardError=append:"$OUT/${UNIT}_console.log" \
  bash -c "while systemctl --user is-active --quiet sphere-chain; do sleep 60; done; \
           echo \"[TRAINING_SIM] sphere-chain finished; starting $UNIT at \$(date -Is)\"; \
           exec $PY -u scripts/flash_sac/train.py --task DDT-Velocity-Flat-Tita-My-PosKneeMA2-Sphere-Fast-Heading-v0 \
             --num_envs 4096 --steps 100000 --seed 42 --device cuda:0 --headless --logger wandb \
             --wandb_project tita_flat_flash_sac --run_name heading_ma2_fast_s42"
echo "[TRAINING_SIM] queued $UNIT (starts after sphere-chain) -> $OUT/${UNIT}_console.log"
