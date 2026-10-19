#!/usr/bin/env bash
# TRAINING_SIM: queue the heading runs (FlashSAC, seed 42, 100k steps, 4096 envs, own systemd user unit, MemoryMax).
#   ma2   (default): DDT-Velocity-Flat-Tita-My-PosKneeMA2-Sphere-Fast-HeadingObs-v0, unit heading-obs-ma2-fast-s42,
#                    exp3 (sphere, MA2, +-1.5/+-3, no ramp) + heading drift reward + critic/actor heading error;
#                    waits for sphere-chain. (The critic-only unit heading-ma2-fast-s42 was cancelled before start.)
#   noma2:           DDT-Velocity-Flat-Tita-My-PosKnee-Sphere-HeadingObs-v0, unit heading-obs-noma2-s42,
#                    exp2 (sphere, no MA2, default commands/ramp) + the same heading terms; waits for the ma2 run.
#                    (Stopped at step 8300: the 1 s heading warmup produced a clockwise turn after every stop.)
#   noma2w0:         DDT-Velocity-Flat-Tita-My-PosKnee-Sphere-HeadingObsW0-v0, unit heading-obs-noma2-w0-s42,
#                    noma2 with no heading warmup; starts as soon as the noma2 unit is not active.
# No robot command. Usage: test/launch_heading_experiment.sh [ma2|noma2|noma2w0]
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$REPO/docs/exp/2026-10-19/heading_obs_experiment"
PY=/home/cocel/isaac/env_isaaclab/bin/python
case "${1:-ma2}" in
  ma2)   TASK=DDT-Velocity-Flat-Tita-My-PosKneeMA2-Sphere-Fast-HeadingObs-v0; UNIT=heading-obs-ma2-fast-s42; WAIT=sphere-chain ;;
  noma2) TASK=DDT-Velocity-Flat-Tita-My-PosKnee-Sphere-HeadingObs-v0; UNIT=heading-obs-noma2-s42; WAIT=heading-obs-ma2-fast-s42 ;;
  noma2w0) TASK=DDT-Velocity-Flat-Tita-My-PosKnee-Sphere-HeadingObsW0-v0; UNIT=heading-obs-noma2-w0-s42; WAIT=heading-obs-noma2-s42 ;;
  *) echo "unknown mode: $1" >&2; exit 2 ;;
esac
mkdir -p "$OUT"
systemctl --user reset-failed "$UNIT" 2>/dev/null || true
systemd-run --user --unit="$UNIT" -p MemoryMax=16G -p MemoryHigh=14G \
  --setenv=WANDB_USERNAME="${WANDB_USERNAME:-}" --setenv=HOME="$HOME" --working-directory="$REPO/lab/ddt_lab" \
  -p StandardOutput=append:"$OUT/${UNIT}_console.log" -p StandardError=append:"$OUT/${UNIT}_console.log" \
  bash -c "while systemctl --user is-active --quiet $WAIT; do sleep 60; done; \
           echo \"[TRAINING_SIM] $WAIT finished; starting $UNIT at \$(date -Is)\"; \
           exec $PY -u scripts/flash_sac/train.py --task $TASK \
             --num_envs 4096 --steps 100000 --seed 42 --device cuda:0 --headless --logger wandb \
             --wandb_project tita_flat_flash_sac --run_name ${UNIT//-/_}"
echo "[TRAINING_SIM] queued $UNIT (starts after $WAIT) -> $OUT/${UNIT}_console.log"
