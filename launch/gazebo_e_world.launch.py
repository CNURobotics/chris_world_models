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
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""Launch a Gazebo server with a simple E world and initialize ROS with command line arguments."""

from chris_world_models.gazebo_launch_description import gazebo_launch_description

def generate_launch_description():
    print("Launching Gazebo with E-world environment ...")
    return gazebo_launch_description(world_file_name='e_map.world')
