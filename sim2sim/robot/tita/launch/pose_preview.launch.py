"""DESKTOP_DRY_RUN: RViz joint/body pose sliders, isolated from robot control."""

from datetime import datetime
import os
from pathlib import Path
import xml.etree.ElementTree as ET

from launch import LaunchDescription, LaunchService
from launch.actions import SetEnvironmentVariable
from launch_ros.actions import Node

ASSET = Path(__file__).resolve().parents[1]
REPO = ASSET.parents[2]


def generate_launch_description():
    robot = ET.parse(ASSET / 'urdf/tita.urdf').getroot()
    for mesh in robot.findall('.//mesh'):
        mesh.set('filename', (ASSET / 'urdf' / mesh.attrib['filename']).resolve().as_uri())
    # Virtual joints are visualization controls, not robot actuators.
    ET.SubElement(robot, 'link', name='preview_world')
    parent = 'preview_world'
    controls = (
        ('x', 'prismatic', '1 0 0', -.5, .5),
        ('y', 'prismatic', '0 1 0', -.5, .5),
        ('z', 'prismatic', '0 0 1', .1, .8),
        ('yaw', 'revolute', '0 0 1', -3.141593, 3.141593),
        ('pitch', 'revolute', '0 1 0', -.8, .8),
        ('roll', 'revolute', '1 0 0', -.8, .8),
    )
    for index, (name, kind, axis, low, high) in enumerate(controls):
        child = 'base_link' if index == len(controls) - 1 else 'preview_' + name
        if child != 'base_link':
            ET.SubElement(robot, 'link', name=child)
        joint = ET.SubElement(robot, 'joint', name='preview_base_' + name, type=kind)
        ET.SubElement(joint, 'parent', link=parent)
        ET.SubElement(joint, 'child', link=child)
        ET.SubElement(joint, 'axis', xyz=axis)
        ET.SubElement(joint, 'limit', lower=str(low), upper=str(high), effort='1', velocity='1')
        parent = child
    zeros = {'preview_base_z': .4}
    for side in ('left', 'right'):
        for index, value in enumerate((0., .8, -1.5, 0.), start=1):
            zeros[f'joint_{side}_leg_{index}'] = value
    description = ET.tostring(robot, encoding='unicode')
    remaps = [('/tf', 'tf'), ('/tf_static', 'tf_static')]
    return LaunchDescription([
        SetEnvironmentVariable('ROS_DOMAIN_ID', '88'),
        SetEnvironmentVariable('ROS_LOCALHOST_ONLY', '1'),
        Node(package='robot_state_publisher', executable='robot_state_publisher',
             namespace='tita_pose_preview', parameters=[{'robot_description': description}],
             remappings=remaps, output='screen'),
        Node(package='joint_state_publisher_gui', executable='joint_state_publisher_gui',
             namespace='tita_pose_preview', parameters=[{'robot_description': description, 'zeros': zeros}],
             output='screen'),
        Node(package='rviz2', executable='rviz2', namespace='tita_pose_preview',
             arguments=['-d', str(ASSET / 'rviz/pose_preview.rviz')],
             remappings=remaps, output='screen'),
    ])


if __name__ == '__main__':
    logs = REPO / 'docs/exp' / datetime.now().strftime('%Y-%m-%d') / 'pose_preview_ros_logs'
    logs.mkdir(parents=True, exist_ok=True)
    os.environ.update(ROS_DOMAIN_ID='88', ROS_LOCALHOST_ONLY='1', ROS_LOG_DIR=str(logs))
    print('[DESKTOP_DRY_RUN] RViz pose preview: 8 joint sliders + 6 body sliders; '
          'ROS domain 88, namespace /tita_pose_preview. No controller is started.', flush=True)
    service = LaunchService()
    service.include_launch_description(generate_launch_description())
    raise SystemExit(service.run())
