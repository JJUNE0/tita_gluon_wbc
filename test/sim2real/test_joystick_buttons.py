"""DESKTOP_DRY_RUN: compile and run pure C++ button/state regression scenarios."""
from pathlib import Path
import subprocess
import tempfile

REPO = Path(__file__).resolve().parents[2]
with tempfile.TemporaryDirectory(dir=REPO / 'test/sim2real', prefix='buttons_') as tmp:
    binary = Path(tmp) / 'buttons'
    subprocess.run([
        'g++', '-std=c++17', '-Wall', '-Wextra', '-Werror', '-pedantic',
        '-I', str(REPO / 'sim2real/tita_ws/src/tita_controller/include'),
        str(REPO / 'test/sim2real/joystick_buttons_runtime.cpp'), '-o', str(binary),
    ], check=True)
    subprocess.run([str(binary)], check=True)
