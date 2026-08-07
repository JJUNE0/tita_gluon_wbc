#!/usr/bin/env python3
"""Sample the GLUON URDF joint limits and summarize the link6 workspace."""

import argparse
import math
from pathlib import Path
import xml.etree.ElementTree as ET

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_URDF = (
    REPO_ROOT
    / "sim2sim"
    / "gluon_2L6_4L3_urdf"
    / "urdf"
    / "gluon_2L6_4L3_sim.urdf"
)
JOINT_NAMES = tuple(f"axis_joint_{index}" for index in range(1, 7))


def wrap_to_pi(angle: np.ndarray | float) -> np.ndarray:
    """Wrap angles to the half-open interval [-pi, pi)."""
    return (np.asarray(angle) + math.pi) % (2.0 * math.pi) - math.pi


def rpy_matrix(rpy: np.ndarray) -> np.ndarray:
    """Return the URDF fixed-axis roll-pitch-yaw rotation matrix."""
    roll, pitch, yaw = rpy
    sr, cr = math.sin(roll), math.cos(roll)
    sp, cp = math.sin(pitch), math.cos(pitch)
    sy, cy = math.sin(yaw), math.cos(yaw)
    return np.array(
        [
            [cy * cp, cy * sp * sr - sy * cr, cy * sp * cr + sy * sr],
            [sy * cp, sy * sp * sr + cy * cr, sy * sp * cr - cy * sr],
            [-sp, cp * sr, cp * cr],
        ],
        dtype=np.float64,
    )


def axis_angle_matrices(axis: np.ndarray, angles: np.ndarray) -> np.ndarray:
    """Return vectorized Rodrigues rotation matrices for one normalized axis."""
    axis = axis / np.linalg.norm(axis)
    x, y, z = axis
    skew = np.array([[0.0, -z, y], [z, 0.0, -x], [-y, x, 0.0]])
    outer = np.outer(axis, axis)
    identity = np.eye(3)
    cosine = np.cos(angles)[:, None, None]
    sine = np.sin(angles)[:, None, None]
    return cosine * identity + sine * skew + (1.0 - cosine) * outer


def load_chain(urdf_path: Path) -> list[dict[str, np.ndarray | float | str]]:
    root = ET.parse(urdf_path).getroot()
    joints_by_name = {joint.attrib["name"]: joint for joint in root.findall("joint")}
    chain = []
    for name in JOINT_NAMES:
        joint = joints_by_name[name]
        origin = joint.find("origin")
        axis = joint.find("axis")
        limit = joint.find("limit")
        chain.append(
            {
                "name": name,
                "xyz": np.fromstring(origin.attrib.get("xyz", "0 0 0"), sep=" "),
                "rotation": rpy_matrix(
                    np.fromstring(origin.attrib.get("rpy", "0 0 0"), sep=" ")
                ),
                "axis": np.fromstring(axis.attrib["xyz"], sep=" "),
                "lower": float(limit.attrib["lower"]),
                "upper": float(limit.attrib["upper"]),
            }
        )
    return chain


def forward_link6_with_jacobian(
    chain: list[dict], joint_positions: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Return link6 positions and geometric linear Jacobians in base_link."""
    sample_count = joint_positions.shape[0]
    rotation = np.broadcast_to(np.eye(3), (sample_count, 3, 3)).copy()
    position = np.zeros((sample_count, 3), dtype=np.float64)
    joint_origins = []
    joint_axes_b = []
    for joint_index, joint in enumerate(chain):
        position += np.einsum("nij,j->ni", rotation, joint["xyz"])
        rotation = rotation @ joint["rotation"]
        joint_origins.append(position.copy())
        joint_axes_b.append(
            np.einsum(
                "nij,j->ni",
                rotation,
                joint["axis"] / np.linalg.norm(joint["axis"]),
            )
        )
        rotation = rotation @ axis_angle_matrices(
            joint["axis"], joint_positions[:, joint_index]
        )
    jacobian_columns = [
        np.cross(axis_b, position - origin)
        for origin, axis_b in zip(joint_origins, joint_axes_b)
    ]
    return position, np.stack(jacobian_columns, axis=2)


def forward_link6(chain: list[dict], joint_positions: np.ndarray) -> np.ndarray:
    return forward_link6_with_jacobian(chain, joint_positions)[0]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--urdf", type=Path, default=DEFAULT_URDF)
    parser.add_argument("--samples", type=int, default=250_000)
    parser.add_argument("--seed", type=int, default=20260806)
    parser.add_argument(
        "--candidate-w1",
        type=float,
        nargs=6,
        metavar=("X_MIN", "X_MAX", "Y_MIN", "Y_MAX", "Z_MIN", "Z_MAX"),
        default=(0.36, 0.48, -0.08, 0.09, -0.20, -0.11),
        help="Candidate base-frame W1 box evaluated against conditioned samples.",
    )
    parser.add_argument("--candidate-grid", type=int, default=5)
    parser.add_argument(
        "--candidate-w2-cylindrical",
        type=float,
        nargs=6,
        metavar=(
            "X_MIN",
            "X_MAX",
            "R_MIN",
            "R_MAX",
            "THETA_CENTER_DEG",
            "THETA_HALF_RANGE_DEG",
        ),
        default=(0.36, 0.48, 0.13, 0.21, -70.0, 105.0),
        help="Candidate W2 cylindrical sector about the base +X axis.",
    )
    parser.add_argument("--sigma-min", type=float, default=0.01)
    args = parser.parse_args()
    if args.samples <= 0:
        parser.error("--samples must be positive")
    if args.candidate_grid < 2:
        parser.error("--candidate-grid must be at least 2")
    if args.sigma_min <= 0.0:
        parser.error("--sigma-min must be positive")

    chain = load_chain(args.urdf.resolve())
    lower = np.array([joint["lower"] for joint in chain])
    upper = np.array([joint["upper"] for joint in chain])
    rng = np.random.default_rng(args.seed)
    soft_lower = 0.95 * lower
    soft_upper = 0.95 * upper
    q_samples = rng.uniform(soft_lower, soft_upper, size=(args.samples, len(chain)))
    reference_q = np.array(
        [
            np.zeros(6),
            np.array([0.0, 0.8, 1.6, 0.8, 0.0, 0.0]),
            lower,
            upper,
        ]
    )
    q_all = np.vstack((q_samples, reference_q))
    positions, jacobians = forward_link6_with_jacobian(chain, q_all)
    sampled_positions = positions[: args.samples]
    sampled_sigma_min = np.linalg.svd(
        jacobians[: args.samples, :, :5], compute_uv=False
    )[:, -1]
    shoulder_center_b = chain[0]["xyz"]
    radial = np.linalg.norm(sampled_positions - shoulder_center_b, axis=1)
    max_index = int(np.argmax(radial))
    theoretical_upper = sum(
        float(np.linalg.norm(joint["xyz"])) for joint in chain[1:]
    )

    print("GLUON_WORKSPACE_ANALYSIS,domain=VALIDATION_SIM", flush=True)
    print(f"urdf={args.urdf.resolve()}", flush=True)
    print(f"samples={args.samples},seed={args.seed}", flush=True)
    print(f"shoulder_center_b_m={shoulder_center_b.tolist()}", flush=True)
    print(f"q0_link6_b_m={positions[args.samples].tolist()}", flush=True)
    print(f"work_link6_b_m={positions[args.samples + 1].tolist()}", flush=True)
    print(
        f"sample_xyz_min_b_m={sampled_positions.min(axis=0).tolist()},"
        f"sample_xyz_max_b_m={sampled_positions.max(axis=0).tolist()}",
        flush=True,
    )
    print(
        "shoulder_radius_m,"
        f"min={radial.min():.9g},p01={np.percentile(radial, 1):.9g},"
        f"p50={np.percentile(radial, 50):.9g},"
        f"p95={np.percentile(radial, 95):.9g},"
        f"p99={np.percentile(radial, 99):.9g},max={radial[max_index]:.9g},"
        f"triangle_upper_bound={theoretical_upper:.9g}",
        flush=True,
    )
    print(f"sample_max_radius_q_rad={q_samples[max_index].tolist()}", flush=True)
    print(
        "sample_sigma_min,"
        f"p01={np.percentile(sampled_sigma_min, 1):.9g},"
        f"p50={np.percentile(sampled_sigma_min, 50):.9g},"
        f"p95={np.percentile(sampled_sigma_min, 95):.9g},"
        f"threshold={args.sigma_min:.9g},"
        f"accepted_fraction={np.mean(sampled_sigma_min >= args.sigma_min):.9g}",
        flush=True,
    )

    candidate_bounds = np.asarray(args.candidate_w1, dtype=np.float64).reshape(3, 2)
    if np.any(candidate_bounds[:, 0] >= candidate_bounds[:, 1]):
        parser.error("candidate W1 lower bounds must be below upper bounds")
    candidate_axes = [
        np.linspace(bounds[0], bounds[1], args.candidate_grid)
        for bounds in candidate_bounds
    ]
    candidate_points = np.stack(
        np.meshgrid(*candidate_axes, indexing="ij"), axis=-1
    ).reshape(-1, 3)
    conditioned_mask = sampled_sigma_min >= args.sigma_min
    conditioned_positions = sampled_positions[conditioned_mask]
    nearest_distances = []
    for target in candidate_points:
        nearest_distances.append(
            float(np.min(np.linalg.norm(conditioned_positions - target, axis=1)))
        )
    nearest_distances = np.asarray(nearest_distances)
    print(
        f"candidate_w1_b_m={candidate_bounds.tolist()},grid={args.candidate_grid},"
        f"grid_points={len(candidate_points)},"
        f"conditioned_nearest_distance_m_max={nearest_distances.max():.9g},"
        f"p95={np.percentile(nearest_distances, 95):.9g},"
        f"median={np.median(nearest_distances):.9g}",
        flush=True,
    )
    worst_indices = np.argsort(nearest_distances)[-10:][::-1]
    for rank, index in enumerate(worst_indices, start=1):
        print(
            f"candidate_worst,rank={rank},target_b_m={candidate_points[index].tolist()},"
            f"nearest_conditioned_m={nearest_distances[index]:.9g}",
            flush=True,
        )

    (
        w2_x_min,
        w2_x_max,
        w2_radius_min,
        w2_radius_max,
        w2_theta_center_deg,
        w2_theta_half_range_deg,
    ) = args.candidate_w2_cylindrical
    if w2_x_min >= w2_x_max:
        parser.error("candidate W2 x lower bound must be below upper bound")
    if w2_radius_min <= 0.0 or w2_radius_min >= w2_radius_max:
        parser.error("candidate W2 radii must satisfy 0 < r_min < r_max")
    if not 0.0 < w2_theta_half_range_deg < 180.0:
        parser.error("candidate W2 theta half range must be in (0, 180) deg")
    theta_center = math.radians(w2_theta_center_deg)
    theta_half_range = math.radians(w2_theta_half_range_deg)
    w2_axes = (
        np.linspace(w2_x_min, w2_x_max, args.candidate_grid),
        np.linspace(w2_radius_min, w2_radius_max, args.candidate_grid),
        theta_center
        + np.linspace(-theta_half_range, theta_half_range, args.candidate_grid),
    )
    w2_cylindrical_points = np.stack(
        np.meshgrid(*w2_axes, indexing="ij"), axis=-1
    ).reshape(-1, 3)
    w2_points = np.column_stack(
        (
            w2_cylindrical_points[:, 0],
            w2_cylindrical_points[:, 1] * np.cos(w2_cylindrical_points[:, 2]),
            w2_cylindrical_points[:, 1] * np.sin(w2_cylindrical_points[:, 2]),
        )
    )
    w2_nearest_distances = []
    for target in w2_points:
        w2_nearest_distances.append(
            float(np.min(np.linalg.norm(conditioned_positions - target, axis=1)))
        )
    w2_nearest_distances = np.asarray(w2_nearest_distances)
    w1_volume = float(np.prod(candidate_bounds[:, 1] - candidate_bounds[:, 0]))
    w2_volume = (
        (w2_x_max - w2_x_min)
        * theta_half_range
        * (w2_radius_max**2 - w2_radius_min**2)
    )
    print(
        "candidate_w2_cylindrical,"
        f"x_m=[{w2_x_min},{w2_x_max}],"
        f"radius_m=[{w2_radius_min},{w2_radius_max}],"
        f"theta_center_deg={w2_theta_center_deg},"
        f"theta_half_range_deg={w2_theta_half_range_deg},"
        f"grid={args.candidate_grid},grid_points={len(w2_points)},"
        f"volume_m3={w2_volume:.9g},volume_ratio_to_w1={w2_volume / w1_volume:.9g},"
        "conditioned_nearest_distance_m_max="
        f"{w2_nearest_distances.max():.9g},"
        f"p95={np.percentile(w2_nearest_distances, 95):.9g},"
        f"median={np.median(w2_nearest_distances):.9g}",
        flush=True,
    )
    w2_worst_indices = np.argsort(w2_nearest_distances)[-10:][::-1]
    for rank, index in enumerate(w2_worst_indices, start=1):
        print(
            f"candidate_w2_worst,rank={rank},"
            f"target_cyl=[{w2_cylindrical_points[index, 0]},"
            f"{w2_cylindrical_points[index, 1]},"
            f"{math.degrees(wrap_to_pi(w2_cylindrical_points[index, 2]))}],"
            f"target_b_m={w2_points[index].tolist()},"
            f"nearest_conditioned_m={w2_nearest_distances[index]:.9g}",
            flush=True,
        )

    expected_q0 = np.array([0.576196, -1.9e-5, -0.136004])
    q0_error = float(np.linalg.norm(positions[args.samples] - expected_q0))
    print(f"q0_contract_error_m={q0_error:.9g}", flush=True)
    if q0_error > 1.0e-3:
        print("GLUON_WORKSPACE_ANALYSIS: FAIL", flush=True)
        return 1
    print("GLUON_WORKSPACE_ANALYSIS: PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
