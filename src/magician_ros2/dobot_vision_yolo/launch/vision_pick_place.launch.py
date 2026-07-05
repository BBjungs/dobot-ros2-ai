from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    package_share = Path(get_package_share_directory("dobot_vision_yolo"))
    config_dir = package_share / "config"

    dry_run = LaunchConfiguration("dry_run")
    start_calibration_tool = LaunchConfiguration("start_calibration_tool")
    common_params = {
        "dry_run": ParameterValue(dry_run, value_type=bool),
    }
    yolo_config = str(config_dir / "yolo.yaml")
    camera_config = str(config_dir / "camera_to_robot.yaml")
    workspace_config = str(config_dir / "workspace.yaml")
    place_config = str(config_dir / "place_positions.yaml")
    camera_params = {
        "dry_run": ParameterValue(dry_run, value_type=bool),
        "calibration_config_path": camera_config,
    }
    target_selector_params = {
        "dry_run": ParameterValue(dry_run, value_type=bool),
        "calibration_config_path": camera_config,
        "place_positions_path": place_config,
    }
    safety_params = {
        "dry_run": ParameterValue(dry_run, value_type=bool),
        "workspace_config_path": workspace_config,
    }

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "dry_run",
                default_value="true",
                description="Keep all vision pick-and-place nodes in dry-run mode.",
            ),
            DeclareLaunchArgument(
                "start_calibration_tool",
                default_value="false",
                description="Start the calibration skeleton together with the pipeline.",
            ),
            Node(
                package="dobot_vision_yolo",
                executable="yolo_detector_node",
                name="yolo_detector_node",
                output="screen",
                emulate_tty=True,
                parameters=[yolo_config, common_params],
            ),
        Node(
            package="dobot_vision_yolo",
            executable="target_selector_node",
            name="target_selector_node",
            output="screen",
            emulate_tty=True,
            parameters=[yolo_config, target_selector_params],
        ),
            Node(
                package="dobot_vision_yolo",
                executable="pixel_to_robot_node",
                name="pixel_to_robot_node",
                output="screen",
                emulate_tty=True,
                parameters=[camera_params],
            ),
        Node(
            package="dobot_vision_yolo",
            executable="vision_pick_place_node",
            name="vision_pick_place_node",
            output="screen",
            emulate_tty=True,
            parameters=[workspace_config, place_config, common_params],
        ),
        Node(
            package="dobot_vision_yolo",
            executable="safety_guard_node",
            name="safety_guard_node",
            output="screen",
            emulate_tty=True,
            parameters=[workspace_config, safety_params],
        ),
        Node(
            package="dobot_vision_yolo",
            executable="camera_calibration_tool",
                name="camera_calibration_tool",
                output="screen",
                emulate_tty=True,
                condition=IfCondition(start_calibration_tool),
                parameters=[camera_params],
            ),
        ]
    )
