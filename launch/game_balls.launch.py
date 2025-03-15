#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    return LaunchDescription([
        # Assume empty robot_namespace for now
        Node(package='chris_world_models', executable='model_spawner', parameters=[{'models_string': 'ball1, ,chris_world_models/urdf/red_ball.sdf, -1.2192, -1.0, 0.25'}], output='screen'),
        Node(package='chris_world_models', executable='model_spawner', parameters=[{'models_string': 'ball2, ,chris_world_models/urdf/red_ball.sdf,  1.2192, -1.5, 0.25'}], output='screen'),
        Node(package='chris_world_models', executable='model_spawner', parameters=[{'models_string': 'ball3, ,chris_world_models/urdf/green_ball.sdf,  0.69, -3.0, 0.25'}], output='screen'),
        Node(package='chris_world_models', executable='model_spawner', parameters=[{'models_string': 'ball4, ,chris_world_models/urdf/green_ball.sdf, -1.25, -3.0, 0.25'}], output='screen'),
        Node(package='chris_world_models', executable='model_spawner', parameters=[{'models_string': 'ball5, ,chris_world_models/urdf/blue_ball.sdf,  -1.75, -2.5, 0.25'}], output='screen'),
        Node(package='chris_world_models', executable='model_spawner', parameters=[{'models_string': 'ball6, ,chris_world_models/urdf/blue_ball.sdf,   1.75, -3.6, 0.25'}], output='screen'),
        ])
