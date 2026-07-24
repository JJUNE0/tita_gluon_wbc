# tita_gluon_urdf

Self-contained ROS 2 package containing separate TITA and Gluon URDF viewers.
This first step intentionally does not join the robots or add a mounting jig.

## Build

```bash
cd ~/ros2_ws
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install --packages-select tita_gluon_urdf
source install/setup.bash
```

## View TITA

```bash
ros2 launch tita_gluon_urdf tita.launch.py
```

## View Gluon

```bash
ros2 launch tita_gluon_urdf gluon.launch.py
```

Both launch files are visualization-only. They publish `robot_description`, synthetic joint
states, and TF; they do not load ros2_control or access hardware.

## View the combined draft

```bash
ros2 launch tita_gluon_urdf combined.launch.py
```

The draft aligns the TITA and Gluon base X/Y origins, uses the same axis orientation, and places
the Gluon base at `z=0.1564 m` in the TITA `base_link` frame. The initial jig is a
`0.12 x 0.12 x 0.03 m` box. Adjust the height interactively when launching:

```bash
ros2 launch tita_gluon_urdf combined.launch.py gluon_z:=0.18
```

The other adjustable arguments are `jig_x`, `jig_y`, and `jig_height`, all in metres. The default
is only a visual first draft: physical measurements are required before manufacturing a jig.

## Static combined URDF

`urdf/tita_gluon.urdf` stores the default combined draft for conversion tools such as the Isaac
Lab URDF importer. Regenerate it after changing the mounting dimensions with:

```bash
python3 scripts/generate_combined_urdf.py \
  --gluon-z 0.1564 \
  --jig-x 0.12 \
  --jig-y 0.12 \
  --jig-height 0.03
```

## GLUON 2L6-4L3

View the measured-motor-mass 2L6-4L3 model by itself:

```bash
ros2 launch tita_gluon_urdf gluon_2l6_4l3.launch.py
```

View it mounted on TITA with the same initial jig placement:

```bash
ros2 launch tita_gluon_urdf tita_gluon_2l6_4l3.launch.py
```

The 2L6-4L3 combined model assigns the `0.12 x 0.12 x 0.03 m` mounting jig a mass of `1.0 kg`,
with its COM at the box center and uniform-box inertia.

The corresponding static conversion asset is `urdf/tita_gluon_2L6_4L3.urdf`. Regenerate it with:

```bash
python3 scripts/generate_tita_gluon_2l6_4l3_urdf.py
```
