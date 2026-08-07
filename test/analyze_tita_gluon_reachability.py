#!/usr/bin/env python3
"""Build a collision-aware GLUON link6 reachability map in the TITA base frame.

This is an offline VALIDATION_SIM tool.  It never opens the robot SDK and never
commands hardware.  The output is a sampled lower-bound on reachability, not a
proof that unsampled space is unreachable and not a guarantee that two occupied
voxels are connected by a collision-free joint trajectory.
"""

from __future__ import annotations

import argparse
from collections import Counter, deque
import hashlib
import json
import math
from pathlib import Path
import sys
import time
import warnings
import xml.etree.ElementTree as ET

import numpy as np
from scipy.stats import qmc


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GLUON_URDF = (
    REPO_ROOT
    / "sim2sim"
    / "gluon_2L6_4L3_urdf"
    / "urdf"
    / "gluon_2L6_4L3_sim.urdf"
)
DEFAULT_COMBINED_URDF = (
    REPO_ROOT
    / "sim2sim"
    / "tita_gluon_urdf"
    / "urdf"
    / "tita_gluon_2L6_4L3.urdf"
)
DEFAULT_OUTPUT = (
    REPO_ROOT / "test" / "eval_logs" / "tita_gluon_reachability_q6_zero.npz"
)
DEFAULT_WORK_Q_RAD = np.array([0.0, 0.8, 1.6, 0.8, 0.0, 0.0])
DEFAULT_TITA_STAND_Q_RAD = np.array([0.1, 0.8, -1.5, 0.0, 0.1, 0.8, -1.5, 0.0])
GLUON_JOINT_NAMES = tuple(
    f"gluon_2L6_4L3_axis_joint_{index}" for index in range(1, 7)
)
TITA_JOINT_NAMES = (
    "joint_left_leg_1",
    "joint_left_leg_2",
    "joint_left_leg_3",
    "joint_left_leg_4",
    "joint_right_leg_1",
    "joint_right_leg_2",
    "joint_right_leg_3",
    "joint_right_leg_4",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _xyz_rpy_transform(origin: ET.Element | None) -> np.ndarray:
    if origin is None:
        xyz = np.zeros(3)
        rpy = np.zeros(3)
    else:
        xyz = np.fromstring(origin.attrib.get("xyz", "0 0 0"), sep=" ")
        rpy = np.fromstring(origin.attrib.get("rpy", "0 0 0"), sep=" ")
    roll, pitch, yaw = rpy
    sr, cr = math.sin(roll), math.cos(roll)
    sp, cp = math.sin(pitch), math.cos(pitch)
    sy, cy = math.sin(yaw), math.cos(yaw)
    rotation = np.array(
        [
            [cy * cp, cy * sp * sr - sy * cr, cy * sp * cr + sy * sr],
            [sy * cp, sy * sp * sr + cy * cr, sy * sp * cr - cy * sr],
            [-sp, cp * sr, cp * cr],
        ],
        dtype=np.float64,
    )
    transform = np.eye(4)
    transform[:3, :3] = rotation
    transform[:3, 3] = xyz
    return transform


def load_tita_to_gluon_transform(combined_urdf: Path) -> np.ndarray:
    """Return T_tita_base_gluon_base from the two fixed mount joints."""
    root = ET.parse(combined_urdf).getroot()
    joints = {joint.attrib["name"]: joint for joint in root.findall("joint")}
    joint_names = (
        "tita_to_mount_jig_2L6_4L3",
        "mount_jig_to_gluon_2L6_4L3",
    )
    missing = [name for name in joint_names if name not in joints]
    if missing:
        raise ValueError(f"combined URDF is missing mount joints: {missing}")
    transform = np.eye(4)
    for name in joint_names:
        transform = transform @ _xyz_rpy_transform(joints[name].find("origin"))
    return transform


def transform_points(transform: np.ndarray, points: np.ndarray) -> np.ndarray:
    return points @ transform[:3, :3].T + transform[:3, 3]


def connected_voxels_from_seed(
    voxel_indices: np.ndarray, seed_index: np.ndarray
) -> np.ndarray:
    """Return a 26-neighbor component mask rooted at ``seed_index``."""
    occupied = {tuple(int(value) for value in row) for row in voxel_indices}
    seed = tuple(int(value) for value in seed_index)
    if seed not in occupied:
        raise ValueError(f"WORK seed voxel {seed} is not occupied")
    neighbors = tuple(
        (dx, dy, dz)
        for dx in (-1, 0, 1)
        for dy in (-1, 0, 1)
        for dz in (-1, 0, 1)
        if (dx, dy, dz) != (0, 0, 0)
    )
    visited = {seed}
    queue = deque([seed])
    while queue:
        current = queue.popleft()
        for delta in neighbors:
            candidate = (
                current[0] + delta[0],
                current[1] + delta[1],
                current[2] + delta[2],
            )
            if candidate in occupied and candidate not in visited:
                visited.add(candidate)
                queue.append(candidate)
    return np.fromiter(
        (tuple(int(value) for value in row) in visited for row in voxel_indices),
        dtype=bool,
        count=len(voxel_indices),
    )


_FACE_CORNERS = (
    ((-1, 0, 0), ((0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 1, 0))),
    ((1, 0, 0), ((1, 0, 0), (1, 1, 0), (1, 1, 1), (1, 0, 1))),
    ((0, -1, 0), ((0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1))),
    ((0, 1, 0), ((0, 1, 0), (0, 1, 1), (1, 1, 1), (1, 1, 0))),
    ((0, 0, -1), ((0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 0, 0))),
    ((0, 0, 1), ((0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1))),
)


def voxel_surface_mesh(
    voxel_indices: np.ndarray, voxel_size_m: float
) -> tuple[np.ndarray, np.ndarray]:
    """Create an unsmoothed boundary mesh without filling unsampled voxels."""
    occupied = {tuple(int(value) for value in row) for row in voxel_indices}
    vertex_ids: dict[tuple[int, int, int], int] = {}
    lattice_vertices: list[tuple[int, int, int]] = []
    faces: list[tuple[int, int, int]] = []

    def vertex_id(vertex: tuple[int, int, int]) -> int:
        index = vertex_ids.get(vertex)
        if index is None:
            index = len(lattice_vertices)
            vertex_ids[vertex] = index
            lattice_vertices.append(vertex)
        return index

    for voxel in sorted(occupied):
        for neighbor_delta, corners in _FACE_CORNERS:
            neighbor = tuple(voxel[axis] + neighbor_delta[axis] for axis in range(3))
            if neighbor in occupied:
                continue
            quad = [
                vertex_id(
                    tuple(voxel[axis] + corner[axis] for axis in range(3))
                )
                for corner in corners
            ]
            faces.append((quad[0], quad[1], quad[2]))
            faces.append((quad[0], quad[2], quad[3]))
    vertices = np.asarray(lattice_vertices, dtype=np.float64) * voxel_size_m
    return vertices, np.asarray(faces, dtype=np.int32)


def write_ascii_ply(path: Path, vertices: np.ndarray, faces: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="ascii") as stream:
        stream.write("ply\nformat ascii 1.0\n")
        stream.write("comment frame tita_base_link\n")
        stream.write(f"element vertex {len(vertices)}\n")
        stream.write("property float x\nproperty float y\nproperty float z\n")
        stream.write(f"element face {len(faces)}\n")
        stream.write("property list uchar int vertex_indices\nend_header\n")
        for vertex in vertices:
            stream.write(f"{vertex[0]:.9g} {vertex[1]:.9g} {vertex[2]:.9g}\n")
        for face in faces:
            stream.write(f"3 {face[0]} {face[1]} {face[2]}\n")


class CollisionChecker:
    """Exact URDF collision-mesh checker backed by Pinocchio and hpp-fcl."""

    def __init__(
        self,
        combined_urdf: Path,
        tita_joint_positions: np.ndarray,
        clearance_m: float,
    ) -> None:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=UserWarning)
            import pinocchio as pin

            self.pin = pin
            self.model = pin.buildModelFromUrdf(str(combined_urdf))
            self.geometry_model = pin.buildGeomFromUrdf(
                self.model,
                str(combined_urdf),
                pin.GeometryType.COLLISION,
                [str(combined_urdf.parent)],
            )
        geometry_ids = {
            geometry.name: index
            for index, geometry in enumerate(self.geometry_model.geometryObjects)
        }
        tita_geometry_names = (
            "base_link_0",
            "left_leg_3_0",
            "left_leg_4_0",
            "right_leg_3_0",
            "right_leg_4_0",
            "mount_jig_2L6_4L3_0",
        )
        gluon_base_name = "gluon_2L6_4L3_base_link_0"
        arm_geometry_names = tuple(
            f"gluon_2L6_4L3_link{index}_0" for index in range(1, 7)
        )
        required = tita_geometry_names + (gluon_base_name,) + arm_geometry_names
        missing = [name for name in required if name not in geometry_ids]
        if missing:
            raise ValueError(f"combined collision model is missing geometries: {missing}")

        pair_ids: list[tuple[int, int]] = []
        for arm_name in arm_geometry_names:
            for body_name in tita_geometry_names:
                pair_ids.append((geometry_ids[arm_name], geometry_ids[body_name]))
        for arm_index in range(1, len(arm_geometry_names)):
            pair_ids.append(
                (
                    geometry_ids[arm_geometry_names[arm_index]],
                    geometry_ids[gluon_base_name],
                )
            )
        for first_index, first_name in enumerate(arm_geometry_names):
            for second_index in range(first_index + 2, len(arm_geometry_names)):
                pair_ids.append(
                    (geometry_ids[first_name], geometry_ids[arm_geometry_names[second_index]])
                )
        for first, second in pair_ids:
            self.geometry_model.addCollisionPair(pin.CollisionPair(first, second))

        self.model_data = self.model.createData()
        self.geometry_data = pin.GeometryData(self.geometry_model)
        for request in self.geometry_data.collisionRequests:
            request.security_margin = clearance_m
            request.enable_distance_lower_bound = True
        self.q = np.zeros(self.model.nq)
        for name, value in zip(TITA_JOINT_NAMES, tita_joint_positions):
            joint_id = self.model.getJointId(name)
            self.q[self.model.joints[joint_id].idx_q] = value
        self.gluon_q_indices = np.asarray(
            [
                self.model.joints[self.model.getJointId(name)].idx_q
                for name in GLUON_JOINT_NAMES
            ],
            dtype=np.int32,
        )

    @property
    def pair_count(self) -> int:
        return len(self.geometry_model.collisionPairs)

    def collision_name(self, gluon_q: np.ndarray) -> str | None:
        self.q[self.gluon_q_indices] = gluon_q
        colliding = self.pin.computeCollisions(
            self.model,
            self.model_data,
            self.geometry_model,
            self.geometry_data,
            self.q,
            True,
        )
        if not colliding:
            return None
        for pair_index, pair in enumerate(self.geometry_model.collisionPairs):
            if self.geometry_data.collisionResults[pair_index].isCollision():
                first = self.geometry_model.geometryObjects[pair.first].name
                second = self.geometry_model.geometryObjects[pair.second].name
                return f"{first}|{second}"
        return "unknown"


def _aggregate_voxels(
    voxel_indices: np.ndarray,
    sigma_min: np.ndarray,
    joint_margin_rad: np.ndarray,
    sample_indices: np.ndarray,
) -> dict[str, np.ndarray]:
    unique, inverse, hit_count = np.unique(
        voxel_indices, axis=0, return_inverse=True, return_counts=True
    )
    max_sigma = np.full(len(unique), -np.inf)
    max_joint_margin = np.full(len(unique), -np.inf)
    np.maximum.at(max_sigma, inverse, sigma_min)
    np.maximum.at(max_joint_margin, inverse, joint_margin_rad)
    representative_sample = np.full(len(unique), -1, dtype=np.int64)
    for local_index in np.argsort(sigma_min):
        representative_sample[inverse[local_index]] = sample_indices[local_index]
    return {
        "indices": unique.astype(np.int32),
        "hit_count": hit_count.astype(np.int32),
        "max_sigma_min": max_sigma,
        "max_joint_margin_rad": max_joint_margin,
        "representative_sample": representative_sample,
    }


def _percentiles(values: np.ndarray) -> dict[str, float]:
    return {
        "min": float(np.min(values)),
        "p01": float(np.percentile(values, 1)),
        "p50": float(np.percentile(values, 50)),
        "p99": float(np.percentile(values, 99)),
        "max": float(np.max(values)),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gluon-urdf", type=Path, default=DEFAULT_GLUON_URDF)
    parser.add_argument("--combined-urdf", type=Path, default=DEFAULT_COMBINED_URDF)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--samples", type=int, default=262_144)
    parser.add_argument("--seed", type=int, default=20260807)
    parser.add_argument("--joint-limit-margin-deg", type=float, default=5.0)
    parser.add_argument("--sigma-min", type=float, default=0.01)
    parser.add_argument("--collision-clearance-m", type=float, default=0.01)
    parser.add_argument("--voxel-size-m", type=float, default=0.01)
    parser.add_argument("--q6-rad", type=float, default=0.0)
    parser.add_argument(
        "--tita-joint-rad",
        type=float,
        nargs=8,
        default=DEFAULT_TITA_STAND_Q_RAD.tolist(),
        metavar=("L1", "L2", "L3", "LW", "R1", "R2", "R3", "RW"),
    )
    parser.add_argument("--progress-every", type=int, default=25_000)
    args = parser.parse_args()
    if args.samples <= 0:
        parser.error("--samples must be positive")
    if args.joint_limit_margin_deg < 0.0:
        parser.error("--joint-limit-margin-deg cannot be negative")
    if args.sigma_min <= 0.0:
        parser.error("--sigma-min must be positive")
    if args.collision_clearance_m < 0.0:
        parser.error("--collision-clearance-m cannot be negative")
    if args.voxel_size_m <= 0.0:
        parser.error("--voxel-size-m must be positive")

    started = time.perf_counter()
    gluon_urdf = args.gluon_urdf.resolve()
    combined_urdf = args.combined_urdf.resolve()
    output = args.output.resolve()
    for path in (gluon_urdf, combined_urdf):
        if not path.is_file():
            parser.error(f"URDF not found: {path}")

    # Reuse the already validated vectorized FK/Jacobian implementation.
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from analyze_gluon_workspace import forward_link6_with_jacobian, load_chain

    chain = load_chain(gluon_urdf)
    lower = np.asarray([joint["lower"] for joint in chain], dtype=np.float64)
    upper = np.asarray([joint["upper"] for joint in chain], dtype=np.float64)
    margin_rad = math.radians(args.joint_limit_margin_deg)
    sample_lower = lower + margin_rad
    sample_upper = upper - margin_rad
    if np.any(sample_lower >= sample_upper):
        parser.error("joint limit margin consumes an entire joint interval")
    if not sample_lower[5] <= args.q6_rad <= sample_upper[5]:
        parser.error("--q6-rad is outside the margin-adjusted joint limit")

    sobol_count = 1 << math.ceil(math.log2(args.samples))
    sampler = qmc.Sobol(d=5, scramble=True, seed=args.seed)
    unit_samples = sampler.random_base2(int(math.log2(sobol_count)))[: args.samples]
    q_samples = np.empty((args.samples + 1, 6), dtype=np.float64)
    q_samples[: args.samples, :5] = qmc.scale(
        unit_samples, sample_lower[:5], sample_upper[:5]
    )
    q_samples[: args.samples, 5] = args.q6_rad
    q_samples[args.samples] = DEFAULT_WORK_Q_RAD
    if not np.all((q_samples[-1] >= sample_lower) & (q_samples[-1] <= sample_upper)):
        parser.error("WORK seed is outside the margin-adjusted joint limits")

    positions_gluon_b, jacobians_gluon_b = forward_link6_with_jacobian(
        chain, q_samples
    )
    sigma_min = np.linalg.svd(jacobians_gluon_b[:, :, :5], compute_uv=False)[:, -1]
    joint_margin_rad = np.min(
        np.minimum(q_samples[:, :5] - lower[:5], upper[:5] - q_samples[:, :5]),
        axis=1,
    )
    t_tita_gluon = load_tita_to_gluon_transform(combined_urdf)
    positions_tita_b = transform_points(t_tita_gluon, positions_gluon_b)

    checker = CollisionChecker(
        combined_urdf,
        np.asarray(args.tita_joint_rad, dtype=np.float64),
        args.collision_clearance_m,
    )
    conditioned_indices = np.flatnonzero(sigma_min >= args.sigma_min)
    collision_free = np.zeros(len(q_samples), dtype=bool)
    collision_counts: Counter[str] = Counter()
    print(
        "TITA_GLUON_REACHABILITY,domain=VALIDATION_SIM,"
        f"samples={args.samples},conditioned={len(conditioned_indices)},"
        f"collision_pairs={checker.pair_count}",
        flush=True,
    )
    collision_started = time.perf_counter()
    for checked_count, sample_index in enumerate(conditioned_indices, start=1):
        collision = checker.collision_name(q_samples[sample_index])
        if collision is None:
            collision_free[sample_index] = True
        else:
            collision_counts[collision] += 1
        if args.progress_every > 0 and checked_count % args.progress_every == 0:
            print(
                "collision_progress,"
                f"checked={checked_count},total={len(conditioned_indices)},"
                f"free={int(np.count_nonzero(collision_free))},"
                f"elapsed_s={time.perf_counter() - collision_started:.3f}",
                flush=True,
            )
    work_index = args.samples
    if sigma_min[work_index] < args.sigma_min:
        raise RuntimeError(
            f"WORK seed sigma_min={sigma_min[work_index]:.9g} is below threshold"
        )
    if not collision_free[work_index]:
        raise RuntimeError("WORK seed violates collision clearance")

    accepted_indices = np.flatnonzero(collision_free)
    accepted_positions_tita = positions_tita_b[accepted_indices]
    accepted_voxel_indices = np.floor(
        accepted_positions_tita / args.voxel_size_m
    ).astype(np.int32)
    voxels = _aggregate_voxels(
        accepted_voxel_indices,
        sigma_min[accepted_indices],
        joint_margin_rad[accepted_indices],
        accepted_indices,
    )
    work_voxel_index = np.floor(
        positions_tita_b[work_index] / args.voxel_size_m
    ).astype(np.int32)
    connected_mask = connected_voxels_from_seed(voxels["indices"], work_voxel_index)
    disconnected_voxel_count = int(np.count_nonzero(~connected_mask))
    for key in tuple(voxels):
        voxels[key] = voxels[key][connected_mask]
    voxel_centers_tita_b = (voxels["indices"].astype(np.float64) + 0.5) * args.voxel_size_m
    representative_q = q_samples[voxels["representative_sample"]]

    surface_vertices_tita_b, surface_faces = voxel_surface_mesh(
        voxels["indices"], args.voxel_size_m
    )
    t_gluon_tita = np.linalg.inv(t_tita_gluon)
    surface_vertices_gluon_b = transform_points(
        t_gluon_tita, surface_vertices_tita_b
    )
    connected_accepted_mask = connected_voxels_from_seed(
        accepted_voxel_indices, work_voxel_index
    )
    connected_sample_indices = accepted_indices[connected_accepted_mask]
    connected_positions_tita = positions_tita_b[connected_sample_indices]
    shoulder_gluon_b = np.asarray(chain[0]["xyz"], dtype=np.float64).reshape(1, 3)
    shoulder_tita_b = transform_points(t_tita_gluon, shoulder_gluon_b)[0]
    horizontal_radius = np.linalg.norm(
        connected_positions_tita[:, :2] - shoulder_tita_b[:2], axis=1
    )

    status = "SUSPICIOUS"
    metadata = {
        "schema_version": 1,
        "execution_domain": "VALIDATION_SIM",
        "evidence_status": status,
        "semantics": "sampled_collision_free_link6_origin_lower_bound",
        "coordinate_frame": "tita_base_link",
        "q6_rad": float(args.q6_rad),
        "samples_requested": int(args.samples),
        "samples_with_work_seed": int(len(q_samples)),
        "seed": int(args.seed),
        "joint_limit_margin_deg": float(args.joint_limit_margin_deg),
        "sigma_min_threshold": float(args.sigma_min),
        "collision_clearance_m": float(args.collision_clearance_m),
        "collision_pair_count": checker.pair_count,
        "tita_joint_rad": [float(value) for value in args.tita_joint_rad],
        "voxel_size_m": float(args.voxel_size_m),
        "conditioned_sample_count": int(len(conditioned_indices)),
        "collision_free_sample_count": int(len(accepted_indices)),
        "connected_collision_free_sample_count": int(len(connected_sample_indices)),
        "connected_voxel_count": int(len(voxels["indices"])),
        "disconnected_voxel_count": disconnected_voxel_count,
        "surface_vertex_count": int(len(surface_vertices_tita_b)),
        "surface_face_count": int(len(surface_faces)),
        "work_q_rad": DEFAULT_WORK_Q_RAD.tolist(),
        "work_link6_tita_b_m": positions_tita_b[work_index].tolist(),
        "work_sigma_min": float(sigma_min[work_index]),
        "shoulder_center_tita_b_m": shoulder_tita_b.tolist(),
        "sample_xyz_min_tita_b_m": connected_positions_tita.min(axis=0).tolist(),
        "sample_xyz_max_tita_b_m": connected_positions_tita.max(axis=0).tolist(),
        "horizontal_radius_about_shoulder_m": _percentiles(horizontal_radius),
        "sigma_min_connected": _percentiles(sigma_min[connected_sample_indices]),
        "joint_margin_rad_connected": _percentiles(
            joint_margin_rad[connected_sample_indices]
        ),
        "collision_first_hit_counts": dict(collision_counts.most_common()),
        "gluon_urdf": str(gluon_urdf),
        "gluon_urdf_sha256": sha256_file(gluon_urdf),
        "combined_urdf": str(combined_urdf),
        "combined_urdf_sha256": sha256_file(combined_urdf),
        "mount_tita_to_gluon": t_tita_gluon.tolist(),
        "limitations": [
            "The TITA-to-GLUON jig dimensions and transform are provisional, not measured.",
            "The combined URDF has simplified or absent TITA collision shapes.",
            "The result applies only to the recorded TITA standing pose.",
            "The end-effector is the link6 origin; no gripper/tool geometry is included.",
            "An occupied voxel contains a verified sample but does not prove every point in the voxel is reachable.",
            "Cartesian voxel connectivity does not prove a continuous collision-free joint-space path.",
            "An unoccupied voxel is unknown, not proven unreachable.",
        ],
    }
    metadata["elapsed_s"] = float(time.perf_counter() - started)

    output.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        output,
        metadata_json=np.asarray(json.dumps(metadata, sort_keys=True)),
        voxel_indices_tita_b=voxels["indices"],
        voxel_centers_tita_b_m=voxel_centers_tita_b.astype(np.float32),
        voxel_hit_count=voxels["hit_count"],
        voxel_max_sigma_min=voxels["max_sigma_min"].astype(np.float32),
        voxel_max_joint_margin_rad=voxels["max_joint_margin_rad"].astype(np.float32),
        voxel_representative_q_rad=representative_q.astype(np.float32),
        surface_vertices_tita_b_m=surface_vertices_tita_b.astype(np.float32),
        surface_vertices_gluon_b_m=surface_vertices_gluon_b.astype(np.float32),
        surface_faces=surface_faces,
        t_tita_base_gluon_base=t_tita_gluon,
    )
    ply_output = output.with_suffix(".ply")
    json_output = output.with_suffix(".json")
    write_ascii_ply(ply_output, surface_vertices_tita_b, surface_faces)
    json_output.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n")

    print(f"evidence_status={status}", flush=True)
    print(
        "acceptance,"
        f"sigma_conditioned={len(conditioned_indices)}/{len(q_samples)},"
        f"collision_free={len(accepted_indices)}/{len(conditioned_indices)},"
        f"connected_samples={len(connected_sample_indices)},"
        f"connected_voxels={len(voxels['indices'])},"
        f"disconnected_voxels={disconnected_voxel_count}",
        flush=True,
    )
    print(
        "bounds_tita_base_m,"
        f"min={metadata['sample_xyz_min_tita_b_m']},"
        f"max={metadata['sample_xyz_max_tita_b_m']}",
        flush=True,
    )
    print(
        "horizontal_radius_about_shoulder_m,"
        + ",".join(
            f"{key}={value:.9g}"
            for key, value in metadata["horizontal_radius_about_shoulder_m"].items()
        ),
        flush=True,
    )
    print(f"output_npz={output}", flush=True)
    print(f"output_ply={ply_output}", flush=True)
    print(f"output_json={json_output}", flush=True)
    print(f"elapsed_s={metadata['elapsed_s']:.3f}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
