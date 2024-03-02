# Scratch for testing/introspecting launch files in python


from ament_index_python.packages import get_package_share_directory
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch import LaunchDescription

pkgs = ['turtlebot4_ignition_bringup', 'tb4_ignition']

for pkg in pkgs:
    print(pkg + ": " + get_package_share_directory(pkg))

ARGUMENTS = [
    DeclareLaunchArgument('namespace', default_value='',
                          description='Robot namespace'),
    DeclareLaunchArgument('rviz', default_value='false',
                          choices=['true', 'false'], description='Start rviz.')
]


testarg = LaunchConfiguration('testarg')
testarg_launcharg = DeclareLaunchArgument('testarg',default_value='hi')
print(testarg)
    
