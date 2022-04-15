CHRISLab World Models
================================

## Introduction

CHRISLab specific Gazebo-simulation launch files and maps for navigation demonstrations.

This repository is used with the new open-source CHRISLab [Flexible Navigation] system.

This package includes launch files and map files, as well as some simple python scripts used to create some worlds.

This package bundles other example files including Willow Garage and Jackal race examples, as well
as CHRISLab specific setups.

## Operation
---------

 `ros2 launch chris_world_models <launch file>.launch.py`
 * This is a simple world with obstacles; no robots are included.
 * The robots and additional obstacles are spawned in separate hardware specific launch files

 There are additional launch files for add balls and cubes of different colors to the environment,
 including at random positions based on the map extents.

 
[ROS]: http://www.ros.org
[Flexible Navigation]: https://github.com/FlexBE/flexible_navigation
