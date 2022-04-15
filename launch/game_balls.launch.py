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


def generate_launch_description():

    return LaunchDescription([
        # Assume empty robot_namespace for now
        Node(package='chris_world_models', executable='model_spawner', parameters=[{'models_string': 'ball1, ,red_ball.urdf.xacro, -1.2192, -1.0, 0.25'}], output='screen'),
        Node(package='chris_world_models', executable='model_spawner', parameters=[{'models_string': 'ball2, ,red_ball.urdf.xacro,  1.2192, -1.5, 0.25'}], output='screen'),
        Node(package='chris_world_models', executable='model_spawner', parameters=[{'models_string': 'ball3, ,green_ball.urdf.xacro,  0.69, -3.0, 0.25'}], output='screen'),
        Node(package='chris_world_models', executable='model_spawner', parameters=[{'models_string': 'ball4, ,green_ball.urdf.xacro, -1.25, -3.0, 0.25'}], output='screen'),
        Node(package='chris_world_models', executable='model_spawner', parameters=[{'models_string': 'ball5, ,blue_ball.urdf.xacro,  -1.75, -2.5, 0.25'}], output='screen'),
        Node(package='chris_world_models', executable='model_spawner', parameters=[{'models_string': 'ball6, ,blue_ball.urdf.xacro,   1.75, -3.6, 0.25'}], output='screen'),
        ])
