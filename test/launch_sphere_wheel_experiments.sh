#!/usr/bin/env bash
# TRAINING_SIM: 2026-10-18 sphere-wheel experiments (FlashSAC, seed 42, 100k steps, 4096 envs).
#   exp1 sphere + MA2                   DDT-Velocity-Flat-Tita-My-PosKneeMA2-Sphere-v0       (concurrent with exp2)
#   exp2 sphere, no MA2                 DDT-Velocity-Flat-Tita-My-PosKnee-Sphere-v0
#   exp3 sphere + MA2, fast, no ramp    DDT-Velocity-Flat-Tita-My-PosKneeMA2-Sphere-Fast-v0  (after exp1/2, alone)
#   exp4 sphere, no MA2, fast, no ramp  DDT-Velocity-Flat-Tita-My-PosKnee-Sphere-Fast-v0     (after exp3, alone)
#   exp5 cylinder, no MA2               DDT-Velocity-Flat-Tita-My-PosKnee-v0                 (after exp4, alone)
# Each run is a systemd user unit (own cgroup, MemoryMax) so VS Code memory pressure cannot kill it.
# The GPU is saturated (99 %), so sequential runs give the same total throughput and earlier results.
# Simultaneous starts race in the URDF->USD conversion (/tmp/IsaacLab/usd_<time>_*), so starts are staggered.
# No robot command. Usage: test/launch_sphere_wheel_experiments.sh [all|chain|<unit to relaunch>]
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
LAB="$REPO/lab/ddt_lab"
OUT="$REPO/docs/exp/2026-10-18/sphere_wheel_experiments"
PY=/home/cocel/isaac/env_isaaclab/bin/python
mkdir -p "$OUT"

train_cmd() {  # task run_name
  echo "$PY -u scripts/flash_sac/train.py --task $1 --num_envs 4096 --steps 100000 --seed 42 --device cuda:0" \
       "--headless --logger wandb --wandb_project tita_flat_flash_sac --run_name $2"
}

launch() {  # unit task run_name memory_max
  local log="$OUT/$1_console.log"
  systemctl --user reset-failed "$1" 2>/dev/null || true
  systemd-run --user --unit="$1" -p MemoryMax="$4" -p MemoryHigh="$(( ${4%G} - 2 ))G" \
    --setenv=WANDB_USERNAME="${WANDB_USERNAME:-}" --setenv=HOME="$HOME" --working-directory="$LAB" \
    -p StandardOutput=append:"$log" -p StandardError=append:"$log" \
    bash -c "$(train_cmd "$2" "$3")"
  echo "[TRAINING_SIM] started $1 -> $log"
}

declare -A TASK=(
  [sphere-ma2-s42]=DDT-Velocity-Flat-Tita-My-PosKneeMA2-Sphere-v0
  [sphere-noma2-s42]=DDT-Velocity-Flat-Tita-My-PosKnee-Sphere-v0
)
mode="${1:-all}"
if [[ "$mode" == all ]]; then
  for unit in sphere-ma2-s42 sphere-noma2-s42; do
    launch "$unit" "${TASK[$unit]}" "${unit//-/_}" 16G
    sleep 90
  done
elif [[ -n "${TASK[$mode]:-}" ]]; then
  launch "$mode" "${TASK[$mode]}" "${mode//-/_}" 16G
  exit 0
elif [[ "$mode" != chain ]]; then
  echo "unknown mode: $mode" >&2; exit 2
fi

# exp3 -> exp4 -> exp5 one at a time after exp1/exp2 (test/run_sphere_wheel_chain.sh).
systemctl --user reset-failed sphere-chain 2>/dev/null || true
systemd-run --user --unit=sphere-chain -p MemoryMax=1G --setenv=WANDB_USERNAME="${WANDB_USERNAME:-}" \
  --setenv=HOME="$HOME" -p StandardOutput=append:"$OUT/sphere-chain.log" -p StandardError=append:"$OUT/sphere-chain.log" \
  bash "$REPO/test/run_sphere_wheel_chain.sh"
echo "[TRAINING_SIM] queued sphere-chain (exp3 -> exp4 -> exp5 after exp1/exp2) -> $OUT/sphere-chain.log"
