# Copyright 2022 CHRISLab, Christopher Newport University
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
#
# Author: David Conner

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import ThisLaunchFileDir


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='true') # Assume simulation for now
    yaml_file_base_name = 'creech_map_050'

    chris_world_models_prefix = get_package_share_directory('chris_world_models')
    yaml_file_path = os.path.join(chris_world_models_prefix, "maps", yaml_file_base_name+".yaml")

    return LaunchDescription([

        Node(
            package='nav2_map_server',
            executable='map_server',
            name="map_server",
            output='screen',
            emulate_tty=True,  # https://github.com/ros2/launch/issues/188
            parameters=[{'use_sim_time': use_sim_time,
                         'yaml_filename': yaml_file_path}],
            ),
    ])
