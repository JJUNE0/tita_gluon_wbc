#!/usr/bin/env python3
"""Build a Cartesian-uniform, collision-checked WORK hub graph for GLUON.

Execution domain: VALIDATION_SIM.

The input reachability map proves collision-free *poses* only.  This builder
selects spatially distributed target poses and admits a target only when the
complete WORK-to-target joint interpolation passes joint-margin, Jacobian
conditioning, and Pinocchio/hpp-fcl collision checks.  Isaac/PhysX self
collisions remain disabled; this tool does not start Isaac Sim or robot SDKs.

The first graph intentionally uses a WORK hub.  Every stored edge is therefore
independently validated and runtime routing is trivial.  A later graph may add
validated target-to-target edges without changing the runtime artifact schema.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import sys
import time

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REACHABILITY_MAP = (
    REPO_ROOT / "test" / "eval_logs" / "tita_gluon_reachability_q6_zero.npz"
)
DEFAULT_GLUON_URDF = (
    REPO_ROOT
    / "sim2sim"
    / "robot" / "gluon"
    / "urdf"
    / "gluon_2L6_4L3_sim.urdf"
)
DEFAULT_COMBINED_URDF = (
    REPO_ROOT
    / "sim2sim"
    / "robot" / "tita_gluon"
    / "urdf"
    / "tita_gluon_2L6_4L3.urdf"
)
DEFAULT_OUTPUT = (
    REPO_ROOT
    / "lab"
    / "ddt_lab"
    / "ddt_lab"
    / "tasks"
    / "moo_based"
    / "locomanipulation"
    / "velocity"
    / "tita_gluon"
    / "data"
    / "tita_gluon_cartesian_work_hub_graph.npz"
)
WORK_Q_RAD = np.asarray((0.0, 0.8, 1.6, 0.8, 0.0, 0.0), dtype=np.float64)

# The parent environment resets TITA between default and 10% folded posture,
# plus independent +/-0.06 rad noise.  These three postures cover the nominal
# pose and the reset envelope corners.  They are not a proof for every dynamic
# locomotion pose; that limitation is recorded in the graph metadata.
TITA_COLLISION_CHECK_POSES_RAD = np.asarray(
    (
        (0.0, 0.8, -1.5, 0.0, 0.0, 0.8, -1.5, 0.0),
        (-0.06, 0.74, -1.44, -0.06, 0.06, 0.74, -1.44, -0.06),
        (0.135, 0.90, -1.68, 0.06, -0.135, 0.90, -1.68, 0.06),
    ),
    dtype=np.float64,
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def spatial_representatives(
    positions: np.ndarray,
    quality: np.ndarray,
    voxel_size_m: float,
) -> np.ndarray:
    """Return the highest-quality input index in each coarse Cartesian voxel."""
    coarse = np.floor(positions / voxel_size_m).astype(np.int32)
    order = np.lexsort((-quality, coarse[:, 2], coarse[:, 1], coarse[:, 0]))
    sorted_voxels = coarse[order]
    first = np.ones(len(order), dtype=bool)
    first[1:] = np.any(sorted_voxels[1:] != sorted_voxels[:-1], axis=1)
    return order[first]


def shell_interleaved_order(
    distances: np.ndarray,
    shell_count: int,
    seed: int,
) -> np.ndarray:
    """Deterministically interleave near and far Cartesian target shells."""
    if not len(distances):
        return np.empty(0, dtype=np.int64)
    maximum = max(float(np.max(distances)), np.finfo(np.float64).eps)
    shell_ids = np.minimum((distances / maximum * shell_count).astype(int), shell_count - 1)
    rng = np.random.default_rng(seed)
    shells: list[list[int]] = []
    for shell_id in range(shell_count):
        members = np.flatnonzero(shell_ids == shell_id)
        rng.shuffle(members)
        shells.append(members.tolist())
    interleaved: list[int] = []
    while any(shells):
        for members in shells:
            if members:
                interleaved.append(members.pop())
    return np.asarray(interleaved, dtype=np.int64)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reachability-map", type=Path, default=DEFAULT_REACHABILITY_MAP)
    parser.add_argument("--gluon-urdf", type=Path, default=DEFAULT_GLUON_URDF)
    parser.add_argument("--combined-urdf", type=Path, default=DEFAULT_COMBINED_URDF)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--max-targets", type=int, default=1024)
    parser.add_argument("--candidate-voxel-size-m", type=float, default=0.04)
    parser.add_argument("--min-target-distance-m", type=float, default=0.04)
    parser.add_argument("--max-target-distance-m", type=float, default=0.42)
    parser.add_argument("--min-ee-z-tita-base-m", type=float, default=0.30)
    parser.add_argument("--max-ee-z-tita-base-m", type=float, default=0.72)
    parser.add_argument("--sigma-min", type=float, default=0.015)
    parser.add_argument("--joint-limit-margin-deg", type=float, default=10.0)
    parser.add_argument("--collision-clearance-m", type=float, default=0.02)
    parser.add_argument("--max-path-joint-step-deg", type=float, default=2.0)
    parser.add_argument("--min-path-samples", type=int, default=33)
    parser.add_argument("--shell-count", type=int, default=8)
    parser.add_argument("--seed", type=int, default=20260810)
    parser.add_argument("--progress-every", type=int, default=100)
    args = parser.parse_args()

    if args.max_targets <= 0:
        parser.error("--max-targets must be positive")
    for name in (
        "candidate_voxel_size_m",
        "max_target_distance_m",
        "sigma_min",
        "collision_clearance_m",
        "max_path_joint_step_deg",
    ):
        if getattr(args, name) <= 0.0:
            parser.error(f"--{name.replace('_', '-')} must be positive")
    if args.min_target_distance_m < 0.0:
        parser.error("--min-target-distance-m cannot be negative")
    if args.min_target_distance_m >= args.max_target_distance_m:
        parser.error("target distance bounds must be ordered")
    if args.min_ee_z_tita_base_m >= args.max_ee_z_tita_base_m:
        parser.error("EE z bounds must be ordered")
    if args.joint_limit_margin_deg < 0.0:
        parser.error("--joint-limit-margin-deg cannot be negative")
    if args.min_path_samples < 2 or args.shell_count <= 0:
        parser.error("--min-path-samples >= 2 and --shell-count > 0 are required")

    started = time.perf_counter()
    reachability_path = args.reachability_map.resolve()
    gluon_urdf = args.gluon_urdf.resolve()
    combined_urdf = args.combined_urdf.resolve()
    output = args.output.resolve()
    for path in (reachability_path, gluon_urdf, combined_urdf):
        if not path.is_file():
            parser.error(f"input file not found: {path}")

    # Test utilities are the canonical offline FK and hpp-fcl implementation.
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from analyze_gluon_workspace import forward_link6_with_jacobian, load_chain
    from analyze_tita_gluon_reachability import (
        CollisionChecker,
        load_tita_to_gluon_transform,
        transform_points,
    )

    source = np.load(reachability_path)
    source_metadata = json.loads(source["metadata_json"].item())
    current_gluon_hash = sha256_file(gluon_urdf)
    current_combined_hash = sha256_file(combined_urdf)
    if source_metadata.get("gluon_urdf_sha256") != current_gluon_hash:
        raise RuntimeError("reachability map GLUON URDF hash does not match current file")
    if source_metadata.get("combined_urdf_sha256") != current_combined_hash:
        raise RuntimeError("reachability map combined URDF hash does not match current file")

    source_positions = np.asarray(source["voxel_centers_tita_b_m"], dtype=np.float64)
    source_q = np.asarray(source["voxel_representative_q_rad"], dtype=np.float64)
    source_sigma = np.asarray(source["voxel_max_sigma_min"], dtype=np.float64)
    source_margin = np.asarray(source["voxel_max_joint_margin_rad"], dtype=np.float64)
    if source_positions.shape[0] != source_q.shape[0] or source_q.shape[1] != 6:
        raise RuntimeError("reachability map node arrays have incompatible shapes")

    chain = load_chain(gluon_urdf)
    lower = np.asarray([joint["lower"] for joint in chain], dtype=np.float64)
    upper = np.asarray([joint["upper"] for joint in chain], dtype=np.float64)
    margin_rad = math.radians(args.joint_limit_margin_deg)
    if np.any(WORK_Q_RAD < lower + margin_rad) or np.any(WORK_Q_RAD > upper - margin_rad):
        raise RuntimeError("WORK posture violates the configured joint-limit margin")

    t_tita_gluon = load_tita_to_gluon_transform(combined_urdf)
    work_gluon, _ = forward_link6_with_jacobian(chain, WORK_Q_RAD.reshape(1, -1))
    work_position = transform_points(t_tita_gluon, work_gluon)[0]
    source_distance = np.linalg.norm(source_positions - work_position, axis=1)
    finite = np.all(np.isfinite(source_positions), axis=1) & np.all(np.isfinite(source_q), axis=1)
    candidate_mask = (
        finite
        & (source_sigma >= args.sigma_min)
        & (source_margin >= margin_rad)
        & (source_distance >= args.min_target_distance_m)
        & (source_distance <= args.max_target_distance_m)
        & (source_positions[:, 2] >= args.min_ee_z_tita_base_m)
        & (source_positions[:, 2] <= args.max_ee_z_tita_base_m)
        & np.isclose(source_q[:, 5], 0.0, atol=1.0e-7)
    )
    candidate_source_ids = np.flatnonzero(candidate_mask)
    if not len(candidate_source_ids):
        raise RuntimeError("no reachability nodes survive the Cartesian admission bounds")

    candidate_positions = source_positions[candidate_source_ids]
    candidate_quality = source_sigma[candidate_source_ids] + 0.05 * source_margin[candidate_source_ids]
    representative_local_ids = spatial_representatives(
        candidate_positions, candidate_quality, args.candidate_voxel_size_m
    )
    candidate_source_ids = candidate_source_ids[representative_local_ids]
    candidate_distances = source_distance[candidate_source_ids]
    candidate_source_ids = candidate_source_ids[
        shell_interleaved_order(candidate_distances, args.shell_count, args.seed)
    ]

    collision_checkers = [
        CollisionChecker(combined_urdf, pose, args.collision_clearance_m)
        for pose in TITA_COLLISION_CHECK_POSES_RAD
    ]
    max_joint_step_rad = math.radians(args.max_path_joint_step_deg)
    rejection_counts: Counter[str] = Counter()
    accepted_q: list[np.ndarray] = []
    accepted_positions: list[np.ndarray] = []
    accepted_min_sigma: list[float] = []
    accepted_min_margin: list[float] = []
    accepted_sample_counts: list[int] = []

    print(
        "TITA_GLUON_CARTESIAN_GRAPH_BUILD,domain=VALIDATION_SIM,"
        f"source_nodes={len(source_q)},candidate_nodes={len(candidate_source_ids)},"
        f"max_targets={args.max_targets},collision_poses={len(collision_checkers)},"
        f"clearance_m={args.collision_clearance_m}",
        flush=True,
    )

    for checked_count, source_id in enumerate(candidate_source_ids, start=1):
        target_q = source_q[source_id]
        maximum_delta = float(np.max(np.abs(target_q - WORK_Q_RAD)))
        sample_count = max(
            args.min_path_samples,
            int(math.ceil(maximum_delta / max_joint_step_rad)) + 1,
        )
        fractions = np.linspace(0.0, 1.0, sample_count)
        path_q = WORK_Q_RAD[None, :] + fractions[:, None] * (target_q - WORK_Q_RAD)[None, :]
        path_positions_gluon, path_jacobians = forward_link6_with_jacobian(chain, path_q)
        path_sigma = np.linalg.svd(path_jacobians[:, :, :5], compute_uv=False)[:, -1]
        minimum_sigma = float(np.min(path_sigma))
        if minimum_sigma < args.sigma_min:
            rejection_counts["sigma_min"] += 1
            continue
        minimum_margin = float(np.min(np.minimum(path_q - lower, upper - path_q)))
        if minimum_margin < margin_rad:
            rejection_counts["joint_margin"] += 1
            continue

        collision_name = None
        for checker_index, checker in enumerate(collision_checkers):
            for joint_position in path_q:
                collision_name = checker.collision_name(joint_position)
                if collision_name is not None:
                    rejection_counts[f"collision_pose_{checker_index}:{collision_name}"] += 1
                    break
            if collision_name is not None:
                break
        if collision_name is not None:
            continue

        accepted_q.append(target_q.copy())
        accepted_positions.append(transform_points(t_tita_gluon, path_positions_gluon[[-1]])[0])
        accepted_min_sigma.append(minimum_sigma)
        accepted_min_margin.append(minimum_margin)
        accepted_sample_counts.append(sample_count)
        if len(accepted_q) >= args.max_targets:
            break
        if args.progress_every > 0 and checked_count % args.progress_every == 0:
            print(
                "graph_progress,"
                f"checked={checked_count},accepted={len(accepted_q)},"
                f"elapsed_s={time.perf_counter() - started:.3f}",
                flush=True,
            )

    if not accepted_q:
        rejection_summary = dict(rejection_counts.most_common())
        print(
            "TITA_GLUON_CARTESIAN_GRAPH_FAIL,domain=VALIDATION_SIM,"
            f"status=FAIL,checked={len(candidate_source_ids)},"
            f"rejections={json.dumps(rejection_summary, sort_keys=True)}",
            flush=True,
        )
        raise RuntimeError("no candidate WORK-to-target path passed every gate")

    target_q = np.asarray(accepted_q, dtype=np.float32)
    target_positions = np.asarray(accepted_positions, dtype=np.float32)
    target_distances = np.linalg.norm(target_positions - work_position, axis=1)
    maximum_distance = float(np.max(target_distances))
    node_q = np.vstack((WORK_Q_RAD.astype(np.float32), target_q))
    node_positions = np.vstack((work_position.astype(np.float32), target_positions))
    node_distance = np.concatenate(([0.0], target_distances)).astype(np.float32)
    node_curriculum_progress = (node_distance / maximum_distance).astype(np.float32)
    edge_index = np.column_stack(
        (np.zeros(len(target_q), dtype=np.int32), np.arange(1, len(target_q) + 1, dtype=np.int32))
    )

    evidence_status = "SUSPICIOUS"
    metadata = {
        "schema_version": 1,
        "execution_domain": "VALIDATION_SIM",
        "evidence_status": evidence_status,
        "semantics": "collision_checked_work_hub_cartesian_targets",
        "source_reachability_map": str(reachability_path),
        "source_reachability_map_sha256": sha256_file(reachability_path),
        "source_reachability_evidence_status": source_metadata.get("evidence_status"),
        "gluon_urdf": str(gluon_urdf),
        "gluon_urdf_sha256": current_gluon_hash,
        "combined_urdf": str(combined_urdf),
        "combined_urdf_sha256": current_combined_hash,
        "work_q_rad": WORK_Q_RAD.tolist(),
        "work_ee_tita_base_m": work_position.tolist(),
        "q6_rad": 0.0,
        "target_count": int(len(target_q)),
        "node_count": int(len(node_q)),
        "edge_count": int(len(edge_index)),
        "candidate_count_after_spatial_thinning": int(len(candidate_source_ids)),
        "candidate_voxel_size_m": float(args.candidate_voxel_size_m),
        "target_distance_m": {
            "min": float(np.min(target_distances)),
            "p50": float(np.percentile(target_distances, 50)),
            "p95": float(np.percentile(target_distances, 95)),
            "max": maximum_distance,
        },
        "target_xyz_min_tita_base_m": target_positions.min(axis=0).tolist(),
        "target_xyz_max_tita_base_m": target_positions.max(axis=0).tolist(),
        "sigma_min_threshold": float(args.sigma_min),
        "path_sigma_min": {
            "min": float(np.min(accepted_min_sigma)),
            "p50": float(np.percentile(accepted_min_sigma, 50)),
        },
        "joint_limit_margin_deg": float(args.joint_limit_margin_deg),
        "path_joint_margin_deg": {
            "min": float(math.degrees(np.min(accepted_min_margin))),
            "p50": float(math.degrees(np.percentile(accepted_min_margin, 50))),
        },
        "collision_clearance_m": float(args.collision_clearance_m),
        "collision_pair_count": int(collision_checkers[0].pair_count),
        "tita_collision_check_poses_rad": TITA_COLLISION_CHECK_POSES_RAD.tolist(),
        "max_path_joint_step_deg": float(args.max_path_joint_step_deg),
        "path_sample_count": {
            "min": int(np.min(accepted_sample_counts)),
            "max": int(np.max(accepted_sample_counts)),
        },
        "rejection_counts": dict(rejection_counts.most_common()),
        "seed": int(args.seed),
        "elapsed_s": float(time.perf_counter() - started),
        "limitations": [
            "Isaac/PhysX self collision remains disabled; safety comes from offline admission only.",
            "The combined URDF has simplified or absent TITA collision geometry.",
            "The mount-jig geometry and transform remain provisional until measured.",
            "The graph is checked against reset-envelope TITA poses, not every dynamic locomotion posture.",
            "Ground-plane clearance is not yet included in the offline hpp-fcl pair set.",
            "The graph controls the link6 origin with q6 fixed at zero; no gripper/tool geometry is included.",
            "Every stored edge is WORK-to-target; arbitrary target-to-target motion is not admitted.",
        ],
    }

    output.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        output,
        metadata_json=np.asarray(json.dumps(metadata, sort_keys=True)),
        node_q_rad=node_q,
        node_ee_pos_tita_b_m=node_positions,
        node_distance_from_work_m=node_distance,
        node_curriculum_progress=node_curriculum_progress,
        edge_index=edge_index,
        edge_min_sigma=np.asarray(accepted_min_sigma, dtype=np.float32),
        edge_min_joint_margin_rad=np.asarray(accepted_min_margin, dtype=np.float32),
        edge_path_sample_count=np.asarray(accepted_sample_counts, dtype=np.int32),
    )
    json_output = output.with_suffix(".json")
    json_output.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        "TITA_GLUON_CARTESIAN_GRAPH,domain=VALIDATION_SIM,"
        f"status={evidence_status},targets={len(target_q)},edges={len(edge_index)},"
        f"max_distance_m={maximum_distance:.6g},output={output}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
