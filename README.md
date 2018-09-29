# Dynamixel Gripper
# Purpose


.. Copyright 2018 pohyk123

============================
Cartographer ROS Integration
============================

Purpose
=======

An end effector is the device at the end of a robotic arm, designed to interact with the environment. To provide for a low cost gripper solution for the underlying project, 2 `dynamixel motors`_ with claws affixed are attached alongside each other. This library (built & tested with kinetic) provides a easy-to-use ROS package to control the grip.

.. _dynamixel motors: http://www.robotis.us/dynamixel-ax-18a/

Getting started
===============

* Ensure dynamixel motors have the proper power supply & both servos have a different ID (you can change them by using a `GUI tool`_
* Download & place this package in your_catkin_workspace/src
* Run the following commands in your terminal/command line:
```
catkin_make
roslaunch dynamixel_gripper gripper_manager.roslaunch
```

.. _GUI tool: http://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_workbench/#gui

ROS API
===============

Published Topics
* /gripper/load (dynamixel_gripper/load_state)
** Returns the current load in both servos
* /gripper/state (dynamixel_gripper/grip_state)
** Returns 0 if gripper is open, and 1 if gripper is closed; contains other motor info as well

Subscribed Topics
* /gripper/command (dynamixel_gripper, std_msgs/Int32)
** 0 - open, 1 - close
