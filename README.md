CHRISLab World Models
================================

## Introduction

CHRISLab specific Gazebo-simulation launch files and maps for navigation demonstrations.

This repository is used for demonstrations of [FlexBE] -- the Flexible Behavior Engine --
with the open-source Flexible Navigation and Flexible Behavior Trees packages.

This package includes launch files and map files, as well as some simple python scripts used to create some worlds.

This package bundles other example files including Willow Garage and Jackal race examples,
as well as CHRISLab specific setups.

For complete Turtlebot2-based demonstrations, see [Turtlebot2 Flexible Navigation] and [Turtlebot2 Flexible Behavior Trees]

## Operation
---------

 `ros2 launch chris_world_models <launch file>.launch.py`
 * This is a simple world with obstacles; no robots are included.
 * The robots and additional obstacles are spawned in separate hardware specific launch files

 There are additional launch files for add balls and cubes of different colors to the environment,
 including at random positions based on the map extents.

-----

[ROS]: http://www.ros.org
[FlexBE]: https://github.com/FlexBE
[Turtlebot2 Flexible Navigation]: https://github.com/CNURobotics/flex_nav_turtlebot2_demo
[Turtlebot2 Flexible Behavior Trees]: https://github.com/CNURobotics/flex_bt_turtlebot2_demo
