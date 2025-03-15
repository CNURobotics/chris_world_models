#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    return LaunchDescription([
        Node(package='chris_world_models',
             executable='model_spawner',
             parameters=[{'models_file': 'balls.csv'}],
             output='screen'),
        ])
