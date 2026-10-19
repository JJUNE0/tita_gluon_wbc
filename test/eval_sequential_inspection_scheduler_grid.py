#!/usr/bin/env python3
"""Tune the classical concurrent timing baseline in a bounded dry-run model.

Execution domain: DESKTOP_DRY_RUN.

This is an interface/timing Go/No-Go, not physics or collision evidence.  It
uses the same persistent executor FSM as the planned Isaac environment and
sets base travel time and graph transition time to the same 2--4 second
range.  The selected grid parameters must later be re-tuned in VALIDATION_SIM.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
import importlib.util
import math
from pathlib import Path
import random
import statistics
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = (
    REPO_ROOT
    / "lab"
    / "ddt_lab"
    / "ddt_lab"
    / "tasks"
    / "moo_based"
    / "locomanipulation"
    / "velocity"
    / "tita_gluon"
    / "sequential_inspection.py"
)
SPEC = importlib.util.spec_from_file_location("tita_gluon_sequential_inspection", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
inspection = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = inspection
SPEC.loader.exec_module(inspection)


@dataclass(frozen=True)
class EpisodeResult:
    success: bool
    cycle_time_s: float
    concurrent_ratio: float
    option_rejections: int


def _parse_grid(text: str) -> tuple[float, ...]:
    values = tuple(float(value) for value in text.split(",") if value.strip())
    if not values:
        raise argparse.ArgumentTypeError("grid must contain at least one value")
    return values


def simulate_episode(controller, seed: int, timeout_s: float = 40.0, dt_s: float = 0.05) -> EpisodeResult:
    rng = random.Random(seed)
    targets = inspection.sample_target_layout(seed)
    executor = inspection.SequentialInspectionExecutor(target_count=len(targets), dwell_time_s=0.3)
    # Bootstrap is excluded from cycle time: the episode begins at the first
    # target's selected graph hub, as specified by the locked task contract.
    executor.begin_bootstrap()
    executor.step(dt_s, inspection.ExecutorStepInput(graph_finished=True))

    base_s_m = 0.0
    elapsed_s = 0.0
    moving_elapsed_s = 0.0
    overlap_elapsed_s = 0.0
    option_rejections = 0
    graph_remaining_s = 0.0
    local_servo_remaining_s = 0.0
    previous_vx_cmd_m_s = 0.0
    previous_state = executor.state

    while elapsed_s < timeout_s and not executor.task_complete:
        target = targets[executor.current_target_index]
        target_error_m = target.route_s_m - base_s_m
        local_valid = abs(target_error_m) <= 0.20
        obs = inspection.CoordinatorObservation(
            target_index=executor.current_target_index,
            target_count=len(targets),
            longitudinal_distance_m=target_error_m,
            yaw_error_rad=0.0,
            local_region_valid=local_valid,
            prepared_for_current=executor.prepared_target_index
            == executor.current_target_index,
            at_stow=executor.at_stow,
            executor_state=executor.state,
            task_complete=executor.task_complete,
            base_speed_m_s=abs(previous_vx_cmd_m_s),
            target_minus_hub_x_m=target_error_m,
            target_minus_hub_y_m=0.0,
        )
        command = controller.command(obs)
        previous_vx_cmd_m_s = command.vx_cmd_m_s
        event = executor.request(
            command.arm_option,
            local_region_valid=local_valid,
            validated_stow_path=True,
        )
        if event == inspection.ExecutorEvent.OPTION_REJECTED:
            option_rejections += 1

        if previous_state != executor.state:
            if executor.state == inspection.ExecutorState.GRAPH_EXECUTION:
                graph_remaining_s = rng.uniform(2.0, 4.0)
            elif executor.state == inspection.ExecutorState.LOCAL_TARGET_SERVO:
                local_servo_remaining_s = rng.uniform(0.35, 0.65)
        previous_state = executor.state

        arm_moving = executor.state in (
            inspection.ExecutorState.GRAPH_EXECUTION,
            inspection.ExecutorState.LOCAL_TARGET_SERVO,
        )
        base_moving = abs(command.vx_cmd_m_s) > 1.0e-4
        moving_elapsed_s += dt_s if base_moving or arm_moving else 0.0
        overlap_elapsed_s += dt_s if base_moving and arm_moving else 0.0
        base_s_m += command.vx_cmd_m_s * dt_s

        step_input = inspection.ExecutorStepInput(local_region_valid=local_valid)
        if executor.state == inspection.ExecutorState.GRAPH_EXECUTION:
            graph_remaining_s -= dt_s
            step_input = inspection.ExecutorStepInput(
                graph_finished=graph_remaining_s <= 0.0,
                local_region_valid=local_valid,
            )
        elif executor.state == inspection.ExecutorState.LOCAL_TARGET_SERVO:
            local_servo_remaining_s -= dt_s
            step_input = inspection.ExecutorStepInput(
                local_region_valid=local_valid,
                pose_within_tolerance=local_servo_remaining_s <= 0.0,
            )
        elif executor.state == inspection.ExecutorState.DWELL:
            step_input = inspection.ExecutorStepInput(
                local_region_valid=local_valid,
                pose_within_tolerance=True,
            )
        executor.step(dt_s, step_input)
        elapsed_s += dt_s

        if executor.state == inspection.ExecutorState.EMERGENCY_HOLD:
            break

    concurrent_ratio = overlap_elapsed_s / max(moving_elapsed_s, dt_s)
    return EpisodeResult(
        success=executor.task_complete,
        cycle_time_s=elapsed_s,
        concurrent_ratio=concurrent_ratio,
        option_rejections=option_rejections,
    )


def summarize(name: str, parameters: str, results: list[EpisodeResult]) -> dict[str, object]:
    successes = [result for result in results if result.success]
    return {
        "controller": name,
        "parameters": parameters,
        "episodes": len(results),
        "success_rate": len(successes) / len(results),
        "successful_cycle_time_s": statistics.mean(
            result.cycle_time_s for result in successes
        )
        if successes
        else math.inf,
        "concurrent_ratio": statistics.mean(result.concurrent_ratio for result in results),
        "mean_option_rejections": statistics.mean(
            result.option_rejections for result in results
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--episodes", type=int, default=64)
    parser.add_argument("--seed", type=int, default=20260810)
    parser.add_argument("--start-distance-grid", type=_parse_grid, default=_parse_grid("0.5,0.8,1.1,1.4,1.7"))
    parser.add_argument("--speed-scale-grid", type=_parse_grid, default=_parse_grid("0.0,0.2,0.4,0.6"))
    parser.add_argument(
        "--output",
        type=Path,
        default=REPO_ROOT / "docs" / "exp" / "2026-08-10" / "sequential_inspection_scheduler_grid.csv",
    )
    args = parser.parse_args()
    if args.episodes <= 0:
        parser.error("--episodes must be positive")
    if any(distance <= 0.10 for distance in args.start_distance_grid):
        parser.error("all start distances must exceed the 0.10 m execute distance")
    if any(scale < 0.0 or scale > 1.0 for scale in args.speed_scale_grid):
        parser.error("speed scales must be within [0, 1]")

    seeds = [args.seed + index for index in range(args.episodes)]
    rows = []
    stop_go = inspection.StopAndGoController()
    rows.append(
        summarize(
            "stop_and_go",
            "max_vx=0.5,stop_distance=0.1",
            [simulate_episode(stop_go, seed) for seed in seeds],
        )
    )
    for start_distance in args.start_distance_grid:
        for speed_scale in args.speed_scale_grid:
            scheduler = inspection.TunedConcurrentScheduler(
                start_distance_m=start_distance,
                arm_motion_speed_scale=speed_scale,
            )
            rows.append(
                summarize(
                    "concurrent_scheduler",
                    f"start_distance_m={start_distance:.3f},arm_speed_scale={speed_scale:.3f}",
                    [simulate_episode(scheduler, seed) for seed in seeds],
                )
            )

    rows.sort(key=lambda row: (-float(row["success_rate"]), float(row["successful_cycle_time_s"])))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    best = rows[0]
    print(
        "SEQUENTIAL_INSPECTION_SCHEDULER_GRID,domain=DESKTOP_DRY_RUN,status=PASS,"
        f"episodes_per_candidate={args.episodes},candidates={len(rows)},"
        f"best_controller={best['controller']},best_parameters={best['parameters']},"
        f"success_rate={best['success_rate']:.6f},"
        f"successful_cycle_time_s={best['successful_cycle_time_s']:.6f},"
        f"concurrent_ratio={best['concurrent_ratio']:.6f},output={args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
