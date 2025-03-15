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
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.actions import IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, RegisterEventHandler, TimerAction, SetLaunchConfiguration, IncludeLaunchDescription
from launch.event_handlers import OnProcessExit, OnProcessStart
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare

from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource


def gazebo_launch_description(world_model_name):
    chris_worlds_pkg = 'chris_world_models'
    world_model_file = os.path.join(get_package_share_directory(chris_worlds_pkg),
                                    "worlds", world_model_name+".sdf")

    print(f"   Loading world model file '{world_model_name}' ...\n    '{world_model_file}'")
    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                [PathJoinSubstitution([FindPackageShare('ros_gz_sim'), 'launch', 'gz_sim.launch.py'])]
            ),
            launch_arguments=[("gz_args", ["-r ", world_model_file])])
    ])
