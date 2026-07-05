import json

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import String

from dobot_vision_yolo.camera_calibration_tool import CalibrationError
from dobot_vision_yolo.camera_calibration_tool import CalibrationStore


class PixelToRobotNode(Node):
    def __init__(self):
        super().__init__("pixel_to_robot_node")
        self.declare_parameter("dry_run", True)
        self.declare_parameter("detections_topic", "/dobot_vision/detections")
        self.declare_parameter("robot_detections_topic", "/dobot_vision/detections_robot")
        self.declare_parameter("selected_target_topic", "/dobot_vision_yolo/selected_target")
        self.declare_parameter("robot_target_topic", "/dobot_vision_yolo/robot_target")
        self.declare_parameter("status_topic", "/dobot_vision/pixel_to_robot/status")
        self.declare_parameter("calibration_config_path", "")
        self.declare_parameter("status_period_sec", 5.0)

        self.dry_run = bool(self.get_parameter("dry_run").value)
        self.detections_topic = str(self.get_parameter("detections_topic").value)
        self.robot_detections_topic = str(
            self.get_parameter("robot_detections_topic").value
        )
        self.selected_target_topic = str(
            self.get_parameter("selected_target_topic").value
        )
        self.robot_target_topic = str(self.get_parameter("robot_target_topic").value)
        self.status_topic = str(self.get_parameter("status_topic").value)
        self.store = CalibrationStore(
            str(self.get_parameter("calibration_config_path").value)
        )

        self.robot_detections_publisher = self.create_publisher(
            String,
            self.robot_detections_topic,
            10,
        )
        self.robot_target_publisher = self.create_publisher(
            String,
            self.robot_target_topic,
            10,
        )
        self.status_publisher = self.create_publisher(String, self.status_topic, 10)
        self.detections_subscription = self.create_subscription(
            String,
            self.detections_topic,
            self._detections_callback,
            10,
        )
        self.selected_target_subscription = self.create_subscription(
            String,
            self.selected_target_topic,
            self._selected_target_callback,
            10,
        )
        period = float(self.get_parameter("status_period_sec").value)
        self.create_timer(max(period, 1.0), self._publish_status)

        self.get_logger().info(
            "Pixel-to-robot node ready. dry_run=%s, detections_topic=%s, config=%s"
            % (self.dry_run, self.detections_topic, self.store.path)
        )

    def _detections_callback(self, msg):
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError as exc:
            self._publish_error(f"Invalid detections JSON: {exc}")
            return

        status = self.store.status()
        detections = payload.get("detections", [])
        if not isinstance(detections, list):
            self._publish_error("detections must be a list")
            return

        enriched = []
        for detection in detections:
            item = dict(detection)
            center_pixel = item.get("center_pixel")
            if not status["is_complete"]:
                item["robot_xy_error"] = "Calibration is incomplete; robot_xy not computed"
            elif center_pixel is None:
                item["robot_xy_error"] = "center_pixel is missing"
            else:
                try:
                    result = self.store.test_point(center_pixel)
                    item["robot_xy"] = result["robot_xy"]
                    item["pick_pose_mm"] = [
                        result["robot_xy"][0],
                        result["robot_xy"][1],
                        result["pick_z"],
                        0.0,
                    ]
                except CalibrationError as exc:
                    item["robot_xy_error"] = str(exc)
            enriched.append(item)

        output = {
            "stamp": payload.get("stamp"),
            "dry_run": self.dry_run,
            "calibration_complete": status["is_complete"],
            "validation": status.get("validation", {}),
            "detections": enriched,
        }
        self._publish_json(self.robot_detections_publisher, output)

    def _selected_target_callback(self, msg):
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError as exc:
            self._publish_error(f"Invalid selected target JSON: {exc}")
            return

        if not payload.get("selected", False):
            self.get_logger().info("No selected target to transform.")
            return

        status = self.store.status()
        if not status["is_complete"]:
            self._publish_error(
                "Calibration is incomplete; pick pose will not be published"
            )
            return

        center_pixel = payload.get("center_pixel")
        if center_pixel is None:
            self._publish_error("Selected target has no center_pixel")
            return

        try:
            result = self.store.test_point(center_pixel)
        except CalibrationError as exc:
            self._publish_error(str(exc))
            return

        pick_pose = [
            result["robot_xy"][0],
            result["robot_xy"][1],
            result["pick_z"],
            0.0,
        ]
        target = {
            "source": "pixel_to_robot_node",
            "dry_run": self.dry_run,
            "selected": True,
            "id": payload.get("id"),
            "class_name": payload.get("class_name"),
            "confidence": payload.get("confidence"),
            "center_pixel": center_pixel,
            "robot_xy": result["robot_xy"],
            "safe_z": result["safe_z"],
            "pick_z": result["pick_z"],
            "pick_pose": pick_pose,
            "pose_mm": pick_pose,
            "place_id": payload.get("place_id"),
            "place_pose": payload.get("place_pose"),
            "selection_mode": payload.get("selection_mode"),
            "detection": payload.get("detection"),
            "request": payload.get("request"),
            "validation": result["validation"],
        }
        self._publish_json(self.robot_target_publisher, target)
        self.get_logger().info("Published dry-run robot target pose from calibration.")

    def _publish_status(self):
        status = self.store.status()
        self._publish_json(
            self.status_publisher,
            {
                "dry_run": self.dry_run,
                "calibration_complete": status["is_complete"],
                "point_count": status["point_count"],
                "validation": status.get("validation", {}),
                "validation_errors": status.get("validation_errors", []),
                "config_path": status["config_path"],
            },
        )

    def _publish_error(self, message):
        self.get_logger().warn(message)
        self._publish_json(
            self.status_publisher,
            {
                "dry_run": self.dry_run,
                "calibration_complete": False,
                "error": message,
            },
        )

    @staticmethod
    def _publish_json(publisher, payload):
        msg = String()
        msg.data = json.dumps(payload, separators=(",", ":"))
        publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = PixelToRobotNode()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
