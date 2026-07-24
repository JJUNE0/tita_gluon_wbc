#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--urdf", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument(
        "--generated-dir",
        default="/home/cocel/Desktop/Research/tita_gluon_wbc/sim2sim/cosim_ros2_jazzy/models/generated",
    )
    args = parser.parse_args()

    import mujoco

    urdf = Path(args.urdf).resolve()
    out = Path(args.out).resolve()
    generated = Path(args.generated_dir).resolve()
    generated.mkdir(parents=True, exist_ok=True)
    out.parent.mkdir(parents=True, exist_ok=True)

    # Keep the original URDF untouched. Copy it into generated/ so mesh path fixes can be made there.
    generated_urdf = generated / urdf.name
    text = urdf.read_text(encoding="utf-8")
    # Common package URI fix for this repository.
    text = text.replace(
        "package://tita_description/",
        "/home/cocel/Desktop/Research/tita_gluon_wbc/tita_gluon_ws/src/ddt_ros2_control/urdfs/tita_description/",
    )
    generated_urdf.write_text(text, encoding="utf-8")

    mesh_src = urdf.parents[1] / "meshes"
    mesh_dst = generated / "meshes"
    if mesh_src.exists() and not mesh_dst.exists():
        shutil.copytree(mesh_src, mesh_dst)

    model = mujoco.MjModel.from_xml_path(str(generated_urdf))
    mujoco.mj_saveLastXML(str(out), model)
    print(f"Wrote MJCF: {out}")


if __name__ == "__main__":
    main()
