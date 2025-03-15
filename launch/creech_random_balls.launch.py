#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

from chris_world_models.random_models import generate_random_spawn_string


def generate_launch_description():

    models = ['chris_world_models/urdf/blue_ball.sdf',
              'chris_world_models/urdf/red_ball.sdf',
              'chris_world_models/urdf/green_ball.sdf' ]
    counts = [8, 2, 4]

    map_path = os.path.join(get_package_share_directory('chris_world_models'), "maps", "creech_map_050")
    print("map path: ", map_path)
    spawn_string = generate_random_spawn_string(map_path, models, counts)
    print(spawn_string)

    return LaunchDescription([
        Node(package='chris_world_models',
             executable='model_spawner',
             parameters=[{'models_string': spawn_string}],
             output='screen'),
        ])
