CHRISLab World Models
================================

## Introduction

CHRISLab specific Gazebo-simulation launch files and maps for navigation demonstrations.

This repository is used with the new open-source CHRISLab [Flexible Navigation] system.

This package includes launch files and map files, as well as some simple python scripts used to create some worlds.

| Gazebo-Simulation Launch Files | Description |
|-------------|-------------|
|gazebo_empty_world.launch | Launch gazebo with empty world without any robots (launch robots separately)|
|gazebo_willow_world.launch| Launch gazebo using Willow Garage office model (without any robots) |
|gazebo_corridors_world.launch| Launch gazebo using the simple corridors model (without any robots)|
|gazebo_simple_creech_world.launch| Launch gazebo using the creech world model (without any robots)|


## Operation
---------

The following directions are for a simple demonstration on a single ROS network.

`roscore`
 * Required for ROS network
 * Start a separate ROS core to simplify startup and re-running nodes as needed


### Start the simulated robot


 `roslaunch chris_world_models gazebo_simple_creech_world.launch`
 * This is a simple world with obstacles; no robots are included.
 * The robots are spawned in separate hardware specific launch files
 * Other launch files include the Willow Garage office model and simple corridors

[ROS]: http://www.ros.org
[Flexible Navigation]: https://github.com/CNURobotics/flexible_navigation
