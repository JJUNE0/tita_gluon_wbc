"""DESKTOP_DRY_RUN / ROBOT_COMMAND_FREE_RUNTIME: compare pure C++ replay output.

Uses only the standard library; never imports ROS, a robot SDK or CAN APIs.
"""
import math
from pathlib import Path
import sys


def main():
    actual = [[float(v) for v in line.split()] for line in Path(sys.argv[1]).read_text().splitlines()]
    expected = [[float(v) for v in line.split()] for line in Path(sys.argv[2]).read_text().splitlines()]
    assert len(actual) == len(expected) == 5501, (len(actual), len(expected))
    maximum = [0.] * 25
    for i, (row, reference) in enumerate(zip(actual, expected)):
        assert len(row) == len(reference) == 25, i
        for j, (value, target) in enumerate(zip(row, reference)):
            assert math.isfinite(value) and math.isfinite(target), (i, j)
            error = abs(value - target)
            maximum[j] = max(maximum[j], error)
            absolute, relative = (3e-6, 1e-6) if j < 9 else (1e-4, 1e-5)
            assert error <= absolute + relative * abs(target), (i, j, value, target)
        assert abs(row[6]) <= 2. + 1e-12, i
        assert max(abs(row[j]) for j in (12, 16)) <= 12. + 1e-12, i
        for j in (0, 1, 2, 4, 5, 6):
            assert row[9 + j] == row[17 + j], (i, j)
    print('PASS: 5501 samples; ARM C++ / Python reference; bias +/-2 m/s; final wheel torque +/-12 Nm; unchanged leg torques')
    print('Maximum errors in diagnostic/torque columns:', maximum)
    print('Pure offline calculation; no robot API, CAN access or physical torque output')


if __name__ == '__main__':
    main()
