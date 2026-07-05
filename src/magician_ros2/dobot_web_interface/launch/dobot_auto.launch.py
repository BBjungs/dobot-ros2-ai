from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    OpaqueFunction,
    SetEnvironmentVariable,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node


def _truthy(value):
    return str(value).strip().lower() in ('1', 'true', 'yes', 'on')


def _maybe_start_bringup(context, *args, **kwargs):
    if not _truthy(LaunchConfiguration('start_bringup').perform(context)):
        return []

    bringup_launch = PathJoinSubstitution([
        get_package_share_directory('dobot_bringup'),
        'dobot_magician_control_system.launch.py',
    ])
    return [
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(bringup_launch),
        ),
    ]


def generate_launch_description():
    tool_arg = DeclareLaunchArgument(
        'tool',
        default_value='extended_gripper',
        choices=['none', 'pen', 'suction_cup', 'gripper', 'extended_gripper'],
        description='Dobot end effector configuration.',
    )
    host_arg = DeclareLaunchArgument('host', default_value='0.0.0.0')
    port_arg = DeclareLaunchArgument('port', default_value='8080')
    camera_device_arg = DeclareLaunchArgument('camera_device', default_value='/dev/video0')
    camera_width_arg = DeclareLaunchArgument('camera_width', default_value='1280')
    camera_height_arg = DeclareLaunchArgument('camera_height', default_value='720')
    camera_fps_arg = DeclareLaunchArgument('camera_fps', default_value='15.0')
    stream_fps_arg = DeclareLaunchArgument('stream_fps', default_value='12.0')
    start_bringup_arg = DeclareLaunchArgument(
        'start_bringup',
        default_value='false',
        description='Start Dobot hardware bringup. Keep false for dry-run web tests.',
    )

    web_node = Node(
        package='dobot_web_interface',
        executable='web_interface',
        output='screen',
        parameters=[{
            'host': LaunchConfiguration('host'),
            'port': LaunchConfiguration('port'),
            'camera_device': LaunchConfiguration('camera_device'),
            'camera_width': LaunchConfiguration('camera_width'),
            'camera_height': LaunchConfiguration('camera_height'),
            'camera_fps': LaunchConfiguration('camera_fps'),
            'stream_fps': LaunchConfiguration('stream_fps'),
        }],
    )

    return LaunchDescription([
        tool_arg,
        host_arg,
        port_arg,
        camera_device_arg,
        camera_width_arg,
        camera_height_arg,
        camera_fps_arg,
        stream_fps_arg,
        start_bringup_arg,
        SetEnvironmentVariable('MAGICIAN_TOOL', LaunchConfiguration('tool')),
        OpaqueFunction(function=_maybe_start_bringup),
        web_node,
    ])
