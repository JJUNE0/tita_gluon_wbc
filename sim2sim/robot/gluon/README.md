# gluon_2L6_4L3_urdf

Upright ROS 2 visualization and conversion package derived from `gluon/urdf/left_gravity.urdf`.

## Physical assumptions

- The source link inertials are treated as structure-only values that exclude actuator mass.
- Measured actuator masses are used: joints 1-2 are `0.540 kg`; joints 3-6 are `0.245 kg`.
- PR60 dimensions are approximated as a solid cylinder, diameter `80 mm`, length `69.3 mm`.
- NE30 dimensions are approximated as a solid cylinder, diameter `52 mm`, length `68.8 mm`.
- Each actuator COM is assumed to coincide with its child-link origin, with cylinder axis along Z.
- The source dual-arm model is made upright with a `-90 deg` world-Y root rotation.
- Joint 2 is re-zeroed so new `q2=0` is the source model's `q2=+pi/2`; its limits are shifted
  by `-pi/2` to preserve the same physical range.
- Joint 6 is active. Motor turns `0` is the provisional `q6=0` reference and
  the generated URDF enforces a software range of
  `[-150, +150] deg`. This is not a measured mechanical-stop range; the current
  `direction=+1` mapping must be verified before relying on signed nonzero poses.
- Joint 1 uses a measured motor-side zero of `8.880584 turns` and
  `direction=-1`. Its mechanical stops are approximately `+/-2.706657 rad`;
  the generated URDF uses `+/-2.584484 rad`, seven degrees inside those stops.
- Joints 2-5 use the recorded visual-zero turns and `direction=+1`, based on
  the operator-confirmed match between decreasing raw turns and negative URDF
  joint poses. Their generated limits likewise stay seven degrees inside the
  observed hard stops; see `config/gluon_calibration.yaml` for exact values.

The structure-only inertial and motor-cylinder inertial are combined using the parallel-axis theorem.
The resulting model mass is `4.2676113806 kg`.

## Build and view

```bash
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install --packages-select gluon_2l6_4l3_urdf
source install/setup.bash
ros2 launch gluon_2l6_4l3_urdf display.launch.py
```

Regenerate after changing the assumptions in `scripts/generate_urdf.py`:

```bash
python3 scripts/generate_urdf.py
```

Audit the generated masses, COM values, inertia matrices, total mass, and mesh references:

```bash
python3 scripts/audit_inertials.py
```

Model files now live in `sim2sim/robot/gluon/`. The ROS package name remains
`gluon_2l6_4l3_urdf`. `urdf/gluon_2L6_4L3_assembly.urdf` preserves the original
combined-model variant; `urdf/gluon.urdf` and `meshes/legacy/` preserve the older arm.
