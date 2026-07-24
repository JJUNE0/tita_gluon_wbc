from glob import glob
from setuptools import find_packages, setup

package_name = "cosim_ros2_jazzy"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        ("share/" + package_name + "/launch", glob("launch/*.launch.py")),
        ("share/" + package_name + "/config", glob("config/*.yaml")),
        ("share/" + package_name + "/models", glob("models/*")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="cocel",
    maintainer_email="cocel@example.com",
    description="Native ROS2 Jazzy + MuJoCo sim-to-sim framework for DDT TITA policy validation.",
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "mujoco_policy_node = cosim_ros2_jazzy.mujoco_policy_node:main",
            "tita_mujoco_real2sim_node = cosim_ros2_jazzy.tita_mujoco_real2sim_node:main",
            "tita_state_relay_sender = cosim_ros2_jazzy.tita_state_relay_sender:main",
            "tita_state_relay_receiver = cosim_ros2_jazzy.tita_state_relay_receiver:main",
            "tita_real_policy_ghost_node = cosim_ros2_jazzy.tita_real_policy_ghost_node:main",
            "keyboard_command_node = cosim_ros2_jazzy.keyboard_command_node:main",
            "tita_joy_bridge_node = cosim_ros2_jazzy.tita_joy_bridge_node:main",
            "tita_dds_snapshot = cosim_ros2_jazzy.tita_dds_snapshot:main",
            "tita_readonly_bag_record = cosim_ros2_jazzy.tita_readonly_bag_record:main",
        ],
    },
)
