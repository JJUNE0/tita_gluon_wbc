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
