# gluon_urdf

Self-contained ROS 2 description package for viewing the Gluon robot arm in RViz.

## Build

Place this directory in a ROS 2 workspace `src` directory, then run:

```bash
cd ~/ros2_ws
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install --packages-select gluon_urdf
source install/setup.bash
```

## View

```bash
ros2 launch gluon_urdf display.launch.py
```

To hide the joint slider window:

```bash
ros2 launch gluon_urdf display.launch.py use_gui:=false
```

The package only publishes the URDF, joint states, and transforms for visualization. It does not connect to or command hardware.
