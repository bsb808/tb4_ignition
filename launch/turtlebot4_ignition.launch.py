# Flattened version of turtlebot4_ignition.launch.py and ignition.launch.py from turtlebot4_simulator/turtlebot4_ignition_bringup
import os
from pathlib import Path

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.actions import GroupAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch.conditions import IfCondition, UnlessCondition
from launch.conditions import LaunchConfigurationEquals, LaunchConfigurationNotEquals


ARGUMENTS = [
    DeclareLaunchArgument('namespace', default_value='',
                          description='Robot namespace'),
    DeclareLaunchArgument('rviz', default_value='false',
                          choices=['true', 'false'], description='Start rviz.'),
    DeclareLaunchArgument('world', default_value='warehouse',
                          description="""Ignition World.  See files in 
                          IGN_GAZEBO_RESOURCE_PATH (defined in this source) 
                          for possible worlds"""),
    DeclareLaunchArgument('model', default_value='standard',
                          choices=['standard', 'lite'],
                          description='Turtlebot4 Model'),
    DeclareLaunchArgument('use_sim_time', default_value='true',
                          choices=['true', 'false'],
                          description='use_sim_time'),
    DeclareLaunchArgument('list_ign_resources', default_value='false',
                          choices=['true', 'false'],
                          description="""If 'true', then list ignition 
                          resource information, e.g., 
                          paths, world files, etc."""),
]

for pose_element in ['x', 'y', 'z', 'yaw']:
    ARGUMENTS.append(DeclareLaunchArgument(pose_element, default_value='0.0',
                     description=f'{pose_element} component of the robot pose.'))


def generate_launch_description():
    # Directories
    pkg_turtlebot4_ignition_bringup = get_package_share_directory(
        'turtlebot4_ignition_bringup')
    pkg_turtlebot4_ignition_gui_plugins = get_package_share_directory(
        'turtlebot4_ignition_gui_plugins')
    pkg_turtlebot4_description = get_package_share_directory(
        'turtlebot4_description')
    pkg_irobot_create_description = get_package_share_directory(
        'irobot_create_description')
    pkg_irobot_create_ignition_bringup = get_package_share_directory(
        'irobot_create_ignition_bringup')
    pkg_irobot_create_ignition_plugins = get_package_share_directory(
        'irobot_create_ignition_plugins')
    pkg_ros_ign_gazebo = get_package_share_directory(
        'ros_ign_gazebo')
    pkg_tb4_ignition = get_package_share_directory(
        'tb4_ignition')

    # Paths
    #ignition_launch = PathJoinSubstitution(
    #    [pkg_turtlebot4_ignition_bringup, 'launch', 'ignition.launch.py'])
    robot_spawn_launch = PathJoinSubstitution(
        [pkg_turtlebot4_ignition_bringup, 'launch',
         'turtlebot4_spawn.launch.py'])
    #ign_gazebo_launch = PathJoinSubstitution(
    #    [pkg_ros_ign_gazebo, 'launch', 'ign_gazebo.launch.py'])


   # ignition = IncludeLaunchDescription(
   #     PythonLaunchDescriptionSource([ignition_launch]),
   #     launch_arguments=[
   #         ('world', LaunchConfiguration('world'))
   #     ]
   # )

    # From turtlebot4_ignition_bringup/launch/ignition.launch.py
    # ---
    # Action: Set ignition resource path
    ign_resource_path = SetEnvironmentVariable(
        name='IGN_GAZEBO_RESOURCE_PATH',
        value=[
            os.path.join(pkg_tb4_ignition, 'worlds'), ':' +
            os.path.join(pkg_turtlebot4_ignition_bringup, 'worlds'), ':' +
            os.path.join(pkg_irobot_create_ignition_bringup, 'worlds'), ':' +
            str(Path(pkg_turtlebot4_description).parent.resolve()), ':' +
            str(Path(pkg_irobot_create_description).parent.resolve())])

    # Action: Set ignition gui plugin path
    ign_gui_plugin_path = SetEnvironmentVariable(
        name='IGN_GUI_PLUGIN_PATH',
        value=[
            os.path.join(pkg_turtlebot4_ignition_gui_plugins, 'lib'), ':' +
            os.path.join(pkg_irobot_create_ignition_plugins, 'lib')]
    )
    
    # Paths
    ign_gazebo_launch = PathJoinSubstitution(
        [pkg_ros_ign_gazebo, 'launch', 'ign_gazebo.launch.py'])

    # Action: Ignition gazebo
    ignition_gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([ign_gazebo_launch]),
        launch_arguments=[
            ('ign_args', [LaunchConfiguration('world'),
                          '.sdf',
                          ' -v 4',
                          ' --gui-config ',
                          PathJoinSubstitution(
                            [pkg_turtlebot4_ignition_bringup,
                             'gui',
                             LaunchConfiguration('model'),
                             'gui.config'])])
        ]
    )

    # Action: Clock bridge
    clock_bridge = Node(package='ros_gz_bridge', executable='parameter_bridge',
                        name='clock_bridge',
                        output='screen',
                        arguments=[
                            '/clock' + '@rosgraph_msgs/msg/Clock' +
                            '[ignition.msgs.Clock'
                        ])
    # ---

    # Action: Spawn turtlebot
    robot_spawn = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([robot_spawn_launch]),
        launch_arguments=[
            ('namespace', LaunchConfiguration('namespace')),
            ('rviz', LaunchConfiguration('rviz')),
            ('x', LaunchConfiguration('x')),
            ('y', LaunchConfiguration('y')),
            ('z', LaunchConfiguration('z')),
            ('yaw', LaunchConfiguration('yaw'))]
        )

    # Action: List Ignition resources
    list_ign_resources_action = ExecuteProcess(
        cmd = [[
            'echo ${IGN_GAZEBO_RESOURCE_PATH} && echo ${IGN_GUI_PLUGIN_PATH}'
            ]],
        shell = True,
        output = 'screen'
    )
    
    # Create launch description and add actions
    ld = LaunchDescription(ARGUMENTS)
    #ld.add_action(ignition) - replaced by the 4 actions below
    ld.add_action(ign_resource_path)
    ld.add_action(ign_gui_plugin_path)

    # Define two groups, depending on the 'list_ign_resources' argument
    ga_false = GroupAction([ignition_gazebo,
                            clock_bridge,
                            robot_spawn],
                           condition = LaunchConfigurationEquals(
                               'list_ign_resources', 'false')
                           )
    ga_true = GroupAction([list_ign_resources_action],
                          condition = LaunchConfigurationEquals(
                              'list_ign_resources', 'true')
                          )
    ld.add_action(ga_false)
    ld.add_action(ga_true)
    return ld
