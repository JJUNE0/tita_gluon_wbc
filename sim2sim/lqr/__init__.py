"""VALIDATION_SIM: isolated FlashSAC and adaptive wheel LQR ablations."""

from pathlib import Path
import sys

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / 'sim2sim/sim2sim_ros2_jazzy'))
