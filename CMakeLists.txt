cmake_minimum_required(VERSION 2.8.3)
project(chris_world_models)

find_package(gazebo REQUIRED)


find_package(catkin REQUIRED COMPONENTS gazebo_ros
                                        gazebo_plugins
                                        geometry_msgs
                                        nav_msgs
                                        roscpp
                                        sensor_msgs
                                        std_msgs
                                        tf2_ros)

catkin_package(CATKIN_DEPENDS gazebo_ros
                              gazebo_plugins
                              geometry_msgs
                              nav_msgs
                              roscpp
                              sensor_msgs
                              std_msgs
                              tf2_ros)

install(DIRECTORY worlds
        DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
        PATTERN "*~" EXCLUDE
)

install(DIRECTORY maps
        DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
        PATTERN "*~" EXCLUDE
)

install(DIRECTORY launch
        DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
        PATTERN "*~" EXCLUDE
)
