# Copyright (c) 2023 Direct Drive Technology Co., Ltd. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    declared_arguments = []
    declared_arguments.append(
        DeclareLaunchArgument(
            "debug",
            default_value="false",
            description="Debug mode",
        )
    )
    config = os.path.join(
        get_package_share_directory('teleop_command'),
        'config',
        'param.yaml'
    )

    return LaunchDescription(declared_arguments + [
        Node(
            package='teleop_command',
            executable='teleop_command_node',
            # name='teleop_command_node',
            namespace=os.environ.get('ROBOT_NS', ''),
            output='screen',
            parameters=[config, {"debug": LaunchConfiguration("debug")}]
        )
    ])
