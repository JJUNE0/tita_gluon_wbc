#!/usr/bin/env bash
# TRAINING_SIM: sequential queue for the 2026-10-18 sphere-wheel experiments 3 -> 4 -> 5.
# Waits until exp1/exp2 units are no longer active, then runs each training in its own systemd user
# unit (MemoryMax 16G) with `systemd-run --wait`, one at a time. A failed run does not block the next.
# Started by `test/launch_sphere_wheel_experiments.sh chain` inside the `sphere-chain` unit. No robot command.
set -uo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
LAB="$REPO/lab/ddt_lab"
OUT="$REPO/docs/exp/2026-10-18/sphere_wheel_experiments"
PY=/home/cocel/isaac/env_isaaclab/bin/python
JOBS=(
  "sphere-ma2-fast-s42 DDT-Velocity-Flat-Tita-My-PosKneeMA2-Sphere-Fast-v0"
  "sphere-noma2-fast-s42 DDT-Velocity-Flat-Tita-My-PosKnee-Sphere-Fast-v0"
  "cyl-noma2-s42 DDT-Velocity-Flat-Tita-My-PosKnee-v0"
)

while systemctl --user is-active --quiet sphere-ma2-s42 sphere-noma2-s42; do sleep 60; done
echo "[TRAINING_SIM] exp1/exp2 finished at $(date -Is)"

for job in "${JOBS[@]}"; do
  read -r unit task <<< "$job"
  log="$OUT/${unit}_console.log"
  systemctl --user reset-failed "$unit" 2>/dev/null || true
  echo "[TRAINING_SIM] start $unit ($task) at $(date -Is) -> $log"
  systemd-run --user --wait --unit="$unit" -p MemoryMax=16G -p MemoryHigh=14G \
    --setenv=WANDB_USERNAME="${WANDB_USERNAME:-}" --setenv=HOME="$HOME" --working-directory="$LAB" \
    -p StandardOutput=append:"$log" -p StandardError=append:"$log" \
    "$PY" -u scripts/flash_sac/train.py --task "$task" --num_envs 4096 --steps 100000 --seed 42 \
    --device cuda:0 --headless --logger wandb --wandb_project tita_flat_flash_sac --run_name "${unit//-/_}"
  echo "[TRAINING_SIM] end $unit at $(date -Is) exit=$?"
done
echo "[TRAINING_SIM] chain finished at $(date -Is)"
