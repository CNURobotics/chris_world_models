#!/usr/bin/env python3
#
# Copyright 2022 CHRISLab
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless requigazebo_jackal_race_worldred by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""Launch a Gazebo with given world file."""
import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

def gazebo_launch_description(world_file_name):
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    world = os.path.join(get_package_share_directory('chris_world_models'),
                         'worlds', world_file_name)
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')

    print(f"   Load {world} file using {pkg_gazebo_ros} ...")
    return LaunchDescription([
        DeclareLaunchArgument('gui', default_value='true',
                              description='Set to "false" to run headless.'),

        DeclareLaunchArgument('server', default_value='true',
                              description='Set to "false" not to run gzserver.'),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([pkg_gazebo_ros, '/launch',  '/gzserver.launch.py']),
            condition=IfCondition(LaunchConfiguration('server')),
            launch_arguments={'world': world, 'verbose':'true'}.items(),
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([pkg_gazebo_ros, '/launch', '/gzclient.launch.py']),
            condition=IfCondition(LaunchConfiguration('gui')),
            launch_arguments={'verbose':'true'}.items(),
        ),
    ])
