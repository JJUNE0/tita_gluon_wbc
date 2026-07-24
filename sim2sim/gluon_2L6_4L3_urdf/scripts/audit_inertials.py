#!/usr/bin/env python3
"""Audit mass, COM, inertia validity, and mesh references in the generated URDF."""

from pathlib import Path
import xml.etree.ElementTree as ET

import numpy as np


PACKAGE_DIR = Path(__file__).resolve().parents[1]
URDF_PATH = PACKAGE_DIR / "urdf" / "gluon_2L6_4L3.urdf"
EXPECTED_TOTAL_MASS = 4.267611380601286


def main() -> None:
    root = ET.parse(URDF_PATH).getroot()
    total_mass = 0.0
    failures: list[str] = []

    print("link,mass_kg,com_xyz_m,min_inertia_eigenvalue,triangle_ok")
    for link in root.findall("link"):
        inertial = link.find("inertial")
        if inertial is None:
            if link.get("name") != "world":
                failures.append(f"{link.get('name')}: missing inertial")
            continue

        mass = float(inertial.find("mass").get("value"))
        origin = inertial.find("origin").get("xyz")
        values = inertial.find("inertia").attrib
        matrix = np.asarray(
            [
                [float(values["ixx"]), float(values["ixy"]), float(values["ixz"])],
                [float(values["ixy"]), float(values["iyy"]), float(values["iyz"])],
                [float(values["ixz"]), float(values["iyz"]), float(values["izz"])],
            ]
        )
        eigenvalues = np.linalg.eigvalsh(matrix)
        triangle_ok = eigenvalues[0] + eigenvalues[1] >= eigenvalues[2] - 1.0e-12
        total_mass += mass
        if mass <= 0.0:
            failures.append(f"{link.get('name')}: non-positive mass")
        if np.any(eigenvalues <= 0.0):
            failures.append(f"{link.get('name')}: inertia is not positive definite")
        if not triangle_ok:
            failures.append(f"{link.get('name')}: inertia triangle inequality failed")
        print(
            f"{link.get('name')},{mass:.12g},{origin},"
            f"{eigenvalues[0]:.12g},{triangle_ok}"
        )

    for mesh in root.iter("mesh"):
        mesh_path = (URDF_PATH.parent / mesh.get("filename")).resolve()
        if not mesh_path.exists():
            failures.append(f"missing mesh: {mesh_path}")

    if not np.isclose(total_mass, EXPECTED_TOTAL_MASS, rtol=0.0, atol=1.0e-9):
        failures.append(
            f"total mass {total_mass:.12g} != expected {EXPECTED_TOTAL_MASS:.12g}"
        )

    print(f"total_mass_kg={total_mass:.12g}")
    if failures:
        print("AUDIT: FAIL")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)
    print("AUDIT: PASS")


if __name__ == "__main__":
    main()
