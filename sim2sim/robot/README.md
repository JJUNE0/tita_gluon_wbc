# Robot assets

```text
robot/
  tita/
    urdf/tita.urdf
    meshes/
  gluon/
    urdf/gluon_2L6_4L3.urdf             # canonical standalone model
    urdf/gluon_2L6_4L3_sim.urdf         # validated simulation variant
    urdf/gluon_2L6_4L3_assembly.urdf    # original combined-model variant
    urdf/gluon.urdf                    # legacy arm model
    urdf/left_gravity_source.urdf       # generator input
    meshes/                           # shared canonical meshes
    meshes/legacy/
    usd/
    config/model_contract.json
  tita_gluon/
    urdf/tita_gluon.urdf
    urdf/tita_gluon_2L6_4L3.urdf
    usd/
```

Combined URDFs use the sibling TITA/GLUON meshes. Generators, ROS viewers and
lab assets resolve these locations directly. The assembly variant is retained
because it differs from the standalone GLUON model. Identical mesh copies are
shared; physical model values are preserved.

ROS package names: `tita_urdf`, `gluon_2l6_4l3_urdf`, `tita_gluon_urdf`.
Build from repository root (`DESKTOP_DRY_RUN`):

```bash
source /opt/ros/jazzy/setup.bash
colcon --log-base docs/exp/$(date +%F)/robot_build_logs build \
  --symlink-install --base-paths sim2sim/robot \
  --packages-select tita_urdf gluon_2l6_4l3_urdf tita_gluon_urdf \
  --build-base sim2sim/.ros2/build --install-base sim2sim/.ros2/install
```
