from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    host_arg = DeclareLaunchArgument(
        'host',
        default_value='0.0.0.0',
        description='HTTP bind host.',
    )
    port_arg = DeclareLaunchArgument(
        'port',
        default_value='8080',
        description='HTTP bind port.',
    )
    raw_topic_arg = DeclareLaunchArgument(
        'camera_raw_topic',
        default_value='/camera/color/image_raw',
        description='Raw sensor_msgs/Image camera topic.',
    )
    compressed_topic_arg = DeclareLaunchArgument(
        'camera_compressed_topic',
        default_value='/camera/color/image_raw/compressed',
        description='Compressed sensor_msgs/CompressedImage camera topic.',
    )
    camera_device_arg = DeclareLaunchArgument(
        'camera_device',
        default_value='/dev/video0',
        description='Direct V4L2/OpenCV camera device. Use an empty value to disable.',
    )
    camera_width_arg = DeclareLaunchArgument(
        'camera_width',
        default_value='1280',
        description='Direct camera capture width.',
    )
    camera_height_arg = DeclareLaunchArgument(
        'camera_height',
        default_value='720',
        description='Direct camera capture height.',
    )
    camera_fps_arg = DeclareLaunchArgument(
        'camera_fps',
        default_value='15.0',
        description='Direct camera capture frame rate.',
    )
    fps_arg = DeclareLaunchArgument(
        'stream_fps',
        default_value='12.0',
        description='MJPEG stream frame rate.',
    )

    web_node = Node(
        package='dobot_web_interface',
        executable='web_interface',
        output='screen',
        parameters=[{
            'host': LaunchConfiguration('host'),
            'port': LaunchConfiguration('port'),
            'camera_raw_topic': LaunchConfiguration('camera_raw_topic'),
            'camera_compressed_topic': LaunchConfiguration('camera_compressed_topic'),
            'camera_device': LaunchConfiguration('camera_device'),
            'camera_width': LaunchConfiguration('camera_width'),
            'camera_height': LaunchConfiguration('camera_height'),
            'camera_fps': LaunchConfiguration('camera_fps'),
            'stream_fps': LaunchConfiguration('stream_fps'),
        }],
    )

    return LaunchDescription([
        host_arg,
        port_arg,
        raw_topic_arg,
        compressed_topic_arg,
        camera_device_arg,
        camera_width_arg,
        camera_height_arg,
        camera_fps_arg,
        fps_arg,
        web_node,
    ])
