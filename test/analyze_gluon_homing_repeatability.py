#!/usr/bin/env python3
"""Summarize repeated manual GLUON hard-stop visits from a CVP sweep CSV."""

import argparse
import csv
import statistics
from collections import defaultdict


def percentile(values, fraction):
    ordered = sorted(values)
    position = fraction * (len(ordered) - 1)
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    weight = position - lower
    return ordered[lower] * (1.0 - weight) + ordered[upper] * weight


def endpoint_visits(samples, side, endpoint, tolerance_turns):
    visits = []
    current = []
    for timestamp, position in samples:
        near_endpoint = (
            position <= endpoint + tolerance_turns
            if side == "lower"
            else position >= endpoint - tolerance_turns
        )
        if near_endpoint:
            current.append((timestamp, position))
        else:
            if len(current) >= 3:
                visits.append(
                    percentile(
                        [value for _, value in current],
                        0.05 if side == "lower" else 0.95,
                    )
                )
            current = []
    if len(current) >= 3:
        visits.append(
            percentile(
                [value for _, value in current],
                0.05 if side == "lower" else 0.95,
            )
        )
    return visits


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path")
    parser.add_argument("--details", action="store_true")
    args = parser.parse_args()

    samples_by_id = defaultdict(list)
    with open(args.csv_path, newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            samples_by_id[int(row["id"])].append(
                (int(row["time_unix_ms"]), float(row["position_turns"]))
            )

    print(
        "id,side,visit_count,median_turns,visit_peak_to_peak_turns,"
        "visit_peak_to_peak_joint_deg"
    )
    for actuator_id in sorted(samples_by_id):
        positions = [position for _, position in samples_by_id[actuator_id]]
        # Ignore actuators that stayed effectively stationary during a
        # per-joint calibration run.
        if max(positions) - min(positions) < 1.0:
            continue
        endpoints = {
            "lower": percentile(positions, 0.005),
            "upper": percentile(positions, 0.995),
        }
        tolerance_turns = min(1.0, (endpoints["upper"] - endpoints["lower"]) * 0.03)
        for side, endpoint in endpoints.items():
            visits = endpoint_visits(
                samples_by_id[actuator_id], side, endpoint, tolerance_turns
            )
            if visits:
                median_turns = statistics.median(visits)
                peak_to_peak_turns = max(visits) - min(visits)
            else:
                median_turns = float("nan")
                peak_to_peak_turns = float("nan")
            print(
                f"{actuator_id},{side},{len(visits)},{median_turns:.6f},"
                f"{peak_to_peak_turns:.6f},{peak_to_peak_turns * 10.0:.4f}"
            )
            if args.details:
                print(
                    "# visits=" + ",".join(f"{value:.6f}" for value in visits)
                )


if __name__ == "__main__":
    main()
