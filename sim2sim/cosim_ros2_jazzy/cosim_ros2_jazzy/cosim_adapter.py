"""Thin adapter boundary for ideas borrowed from the existing cosim repository.

The first ROS2-native TITA implementation does not import cosim directly because
cosim's main tester path is tied to a PyQt worker/UI lifecycle. The reused design
ideas are:

- strict policy wrapper around ONNX Runtime
- environment wrapper with reset/step/render responsibilities
- command injection through a reproducible external interface
- debug/report separation from the simulation loop
"""

from __future__ import annotations

from pathlib import Path


def cosim_root(project_root: str = "/home/cocel/Desktop/Research/tita_gluon_wbc/sim2sim") -> Path:
    return Path(project_root) / "cosim"
