Sandbox for turtlebo4 simulation 

## Build and test

Build
```
cd ~/tb4_ws
colcon build --symlink-install
```

Generates stderr
```
Starting >>> tb4_ignition
--- stderr: tb4_ignition                   
/usr/lib/python3/dist-packages/setuptools/command/easy_install.py:158: EasyInstallDeprecationWarning: easy_install command is deprecated. Use build and pip and other standards-based tools.
  warnings.warn(
/usr/lib/python3/dist-packages/setuptools/command/install.py:34: SetuptoolsDeprecationWarning: setup.py install is deprecated. Use build and pip and other standards-based tools.
  warnings.warn(
---
Finished <<< tb4_ignition [0.81s]

Summary: 1 package finished [0.89s]
  1 package had stderr output: tb4_ignition
```

This seems to be a sytematic issue with ROS2 and setuptools: https://github.com/ros-planning/navigation2/issues/3363
Downgrading the version of setuptools to 58.x.x seems like too much of a pain without switching over to pip.
Also appears to be a non-blocking error.
Another example of how you need to be a sysadmin to make this stack work!

Test
```
source ~/.bashrc
ros2 run tb4_ignition my_node 
```


## Turtlebot Ignition

```
ros2 launch tb4_ignition turtlebot4_ignition.launch.py --show-args
```

```
ls .ignition/fuel/fuel.ignitionrobotics.org/openrobotics/models/
```

Run with the `warehouse.sdf` file from turtlebot4_ignition_bringup
```
ros2 launch ./turtlebot4_ignition.launch.py world:=warehouse
```

Run with 'tb4_warehouse.sdf` file from this repo, tb4_ignition
```
ros2 launch ./turtlebot4_ignition.launch.py world:=tb4_warehouse
```


ros2 launch ./turtlebot4_ignition.launch.py list_ign_resources:=true
