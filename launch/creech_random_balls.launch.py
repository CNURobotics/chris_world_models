#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

from chris_world_models.random_models import generate_random_spawn_string
def generate_launch_description():

    models = ['blue_ball.urdf.xacro', 'red_ball.urdf.xacro', 'green_ball.urdf.xacro' ]
    counts = [8, 2, 4]

    map_path = os.path.join(get_package_share_directory('chris_world_models'), "maps", "creech_map_050")
    print("map path: ", map_path)
    spawn_string = generate_random_spawn_string(map_path, models, counts)
    print(spawn_string)

    return LaunchDescription([
        Node(package='chris_world_models', executable='model_spawner',
             parameters=[{'models_string': spawn_string}],
             output='screen'),
        ])
