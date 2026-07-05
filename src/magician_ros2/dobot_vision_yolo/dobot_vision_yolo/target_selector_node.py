import json
import math
import os
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import rclpy
import yaml
from ament_index_python.packages import PackageNotFoundError
from ament_index_python.packages import get_package_share_directory
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import String

from dobot_vision_yolo.camera_calibration_tool import CalibrationError
from dobot_vision_yolo.camera_calibration_tool import CalibrationStore


PACKAGE_NAME = "dobot_vision_yolo"
SELECTION_MODES = ("highest_confidence", "nearest_center", "manual_id")


class TargetSelectionError(ValueError):
    pass


def _package_config_path(filename: str) -> Path:
    return Path.cwd() / "src" / "magician_ros2" / PACKAGE_NAME / "config" / filename


def _source_config_path(filename: str) -> Path:
    return Path(__file__).resolve().parents[1] / "config" / filename


def _share_config_path(filename: str) -> Optional[Path]:
    try:
        return Path(get_package_share_directory(PACKAGE_NAME)) / "config" / filename
    except PackageNotFoundError:
        return None


def _resolve_config_path(
    filename: str,
    config_path: str = "",
    env_var: str = "",
) -> Path:
    if config_path:
        return Path(config_path).expanduser()

    if env_var:
        env_path = os.environ.get(env_var, "")
        if env_path:
            return Path(env_path).expanduser()

    candidates = [_package_config_path(filename), _source_config_path(filename)]
    share_path = _share_config_path(filename)
    if share_path is not None:
        candidates.append(share_path)

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def resolve_place_positions_path(config_path: str = "") -> Path:
    return _resolve_config_path(
        "place_positions.yaml",
        config_path,
        "DOBOT_VISION_PLACE_POSITIONS_PATH",
    )


def resolve_yolo_config_path(config_path: str = "") -> Path:
    return _resolve_config_path("yolo.yaml", config_path, "DOBOT_VISION_YOLO_CONFIG")


def _as_pose(value: Any, name: str) -> List[float]:
    if not isinstance(value, (list, tuple)) or len(value) != 4:
        raise TargetSelectionError(f"{name} must be [x, y, z, r]")
    try:
        return [float(item) for item in value]
    except (TypeError, ValueError) as exc:
        raise TargetSelectionError(f"{name} must contain numeric values") from exc


def _as_point(value: Any, name: str) -> List[float]:
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise TargetSelectionError(f"{name} must be [u, v]")
    try:
        return [float(value[0]), float(value[1])]
    except (TypeError, ValueError) as exc:
        raise TargetSelectionError(f"{name} must contain numeric values") from exc


def _load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as stream:
        loaded = yaml.safe_load(stream) or {}
    if not isinstance(loaded, dict):
        raise TargetSelectionError(f"{path} root must be an object")
    return loaded


class PlaceStore:
    def __init__(self, config_path: str = ""):
        self.path = resolve_place_positions_path(config_path)

    def load(self) -> Dict[str, Dict[str, Any]]:
        data = _load_yaml(self.path)
        raw_places = data.get("places", {})
        if not isinstance(raw_places, dict):
            raise TargetSelectionError("places must be a mapping of place_id to pose")

        places = {}
        for place_id, raw_place in raw_places.items():
            if isinstance(raw_place, dict):
                pose = raw_place.get("pose")
            else:
                pose = raw_place
            places[str(place_id)] = {"pose": _as_pose(pose, f"places.{place_id}.pose")}
        return places

    def get_pose(self, place_id: str) -> List[float]:
        places = self.load()
        if place_id not in places:
            raise TargetSelectionError(
                f"place_id '{place_id}' is not defined in {self.path}"
            )
        return list(places[place_id]["pose"])

    def status(self) -> Dict[str, Any]:
        places = self.load()
        return {
            "config_path": str(self.path),
            "places": places,
            "place_ids": sorted(places.keys()),
        }


def load_configured_classes(config_path: str = "") -> List[str]:
    path = resolve_yolo_config_path(config_path)
    data = _load_yaml(path)
    node_config = data.get("target_selector_node", {})
    ros_parameters = node_config.get("ros__parameters", {})
    raw_classes = ros_parameters.get("object_classes", [])
    if raw_classes is None:
        return []
    if not isinstance(raw_classes, list):
        raise TargetSelectionError("object_classes must be a list of class names")
    classes = [str(item) for item in raw_classes if str(item)]
    return sorted(set(classes))


def classes_from_detections(detections: Any) -> List[str]:
    values = []
    for detection in _extract_detections(detections):
        class_name = detection.get("class_name")
        if class_name is not None and str(class_name):
            values.append(str(class_name))
    return sorted(set(values))


def _extract_detections(detections_or_payload: Any) -> List[Dict[str, Any]]:
    if isinstance(detections_or_payload, dict):
        detections = detections_or_payload.get("detections", [])
    else:
        detections = detections_or_payload
    if not isinstance(detections, list):
        raise TargetSelectionError("detections must be a list")

    normalized = []
    for index, detection in enumerate(detections):
        if not isinstance(detection, dict):
            raise TargetSelectionError(f"detections[{index}] must be an object")
        normalized.append(dict(detection))
    return normalized


def _confidence(detection: Dict[str, Any]) -> float:
    try:
        return float(detection.get("confidence", 0.0))
    except (TypeError, ValueError):
        return 0.0


def _detection_id(detection: Dict[str, Any]) -> Any:
    return detection.get("id", detection.get("detection_id"))


def _filter_by_class(
    detections: Iterable[Dict[str, Any]],
    object_class: str,
) -> List[Dict[str, Any]]:
    if object_class in ("", "all", "*"):
        return list(detections)
    return [
        detection
        for detection in detections
        if str(detection.get("class_name", "")) == object_class
    ]


def _select_detection(
    detections: List[Dict[str, Any]],
    selection_mode: str,
    manual_id: Any,
    image_center: Sequence[float],
) -> Optional[Dict[str, Any]]:
    if not detections:
        return None

    if selection_mode == "highest_confidence":
        return max(detections, key=_confidence)

    if selection_mode == "nearest_center":
        center = _as_point(image_center, "image_center")

        def distance(detection: Dict[str, Any]) -> float:
            point = _as_point(detection.get("center_pixel"), "center_pixel")
            return math.hypot(point[0] - center[0], point[1] - center[1])

        return min(detections, key=distance)

    if selection_mode == "manual_id":
        if manual_id is None or str(manual_id) == "":
            raise TargetSelectionError("manual_id is required when selection_mode=manual_id")
        for detection in detections:
            if str(_detection_id(detection)) == str(manual_id):
                return detection
        return None

    raise TargetSelectionError(
        "selection_mode must be one of: %s" % ", ".join(SELECTION_MODES)
    )


def select_target_from_detections(
    detections_or_payload: Any,
    request: Dict[str, Any],
    place_store: PlaceStore,
    calibration_store: CalibrationStore,
    dry_run: bool = True,
    image_size: Tuple[int, int] = (640, 480),
    min_confidence: float = 0.0,
    source: str = "target_selector_node",
) -> Dict[str, Any]:
    if not isinstance(request, dict):
        raise TargetSelectionError("select_target payload must be an object")

    object_class = str(request.get("object_class", "") or "").strip()
    place_id = str(request.get("place_id", "") or "").strip()
    selection_mode = str(
        request.get("selection_mode", "highest_confidence") or "highest_confidence"
    )
    manual_id = request.get("manual_id")

    if not dry_run:
        raise TargetSelectionError("target selection is dry_run only")
    if not object_class:
        raise TargetSelectionError("object_class is required")
    if not place_id:
        raise TargetSelectionError("place_id is required")
    if selection_mode not in SELECTION_MODES:
        raise TargetSelectionError(
            "selection_mode must be one of: %s" % ", ".join(SELECTION_MODES)
        )

    place_pose = place_store.get_pose(place_id)
    detections = _extract_detections(detections_or_payload)
    detections = [
        detection
        for detection in detections
        if _confidence(detection) >= float(min_confidence)
    ]
    class_matches = _filter_by_class(detections, object_class)

    if not class_matches:
        return {
            "selected": False,
            "dry_run": True,
            "source": source,
            "reason": (
                "No detections found"
                if object_class in ("all", "*")
                else f"No detections found for class '{object_class}'"
            ),
            "request": {
                "object_class": object_class,
                "place_id": place_id,
                "selection_mode": selection_mode,
                "manual_id": manual_id,
            },
        }

    image_center = [float(image_size[0]) / 2.0, float(image_size[1]) / 2.0]
    try:
        selected = _select_detection(
            class_matches,
            selection_mode,
            manual_id,
            image_center,
        )
    except TargetSelectionError:
        raise
    except Exception as exc:
        raise TargetSelectionError(str(exc)) from exc

    if selected is None:
        return {
            "selected": False,
            "dry_run": True,
            "source": source,
            "reason": f"No detection matched manual_id '{manual_id}'",
            "request": {
                "object_class": object_class,
                "place_id": place_id,
                "selection_mode": selection_mode,
                "manual_id": manual_id,
            },
        }

    center_pixel = _as_point(selected.get("center_pixel"), "center_pixel")
    try:
        calibration = calibration_store.test_point(center_pixel)
    except CalibrationError as exc:
        return {
            "selected": False,
            "dry_run": True,
            "source": source,
            "reason": f"Calibration is incomplete: {exc}",
            "request": {
                "object_class": object_class,
                "place_id": place_id,
                "selection_mode": selection_mode,
                "manual_id": manual_id,
            },
        }

    robot_xy = calibration["robot_xy"]
    pick_pose = [robot_xy[0], robot_xy[1], calibration["pick_z"], 0.0]
    detection_id = _detection_id(selected)
    selected_detection = {
        "id": detection_id,
        "class_name": str(selected.get("class_name", "")),
        "confidence": round(_confidence(selected), 4),
        "center_pixel": center_pixel,
        "bbox": selected.get("bbox", []),
    }

    return {
        "selected": True,
        "dry_run": True,
        "source": source,
        "id": detection_id,
        "class_name": selected_detection["class_name"],
        "confidence": selected_detection["confidence"],
        "center_pixel": center_pixel,
        "robot_xy": robot_xy,
        "pick_pose": pick_pose,
        "safe_z": calibration["safe_z"],
        "pick_z": calibration["pick_z"],
        "place_id": place_id,
        "place_pose": place_pose,
        "selection_mode": selection_mode,
        "detection": selected_detection,
        "request": {
            "object_class": object_class,
            "place_id": place_id,
            "selection_mode": selection_mode,
            "manual_id": manual_id,
        },
        "validation": calibration.get("validation", {}),
    }


class TargetSelectorNode(Node):
    def __init__(self):
        super().__init__("target_selector_node")
        self.declare_parameter("dry_run", True)
        self.declare_parameter("detections_topic", "/dobot_vision/detections")
        self.declare_parameter("select_target_topic", "/dobot_vision/select_target")
        self.declare_parameter("selected_target_topic", "/dobot_vision_yolo/selected_target")
        self.declare_parameter("status_topic", "/dobot_vision/target_selector/status")
        self.declare_parameter("target_class", "all")
        self.declare_parameter("min_confidence", 0.0)
        self.declare_parameter("image_width", 640)
        self.declare_parameter("image_height", 480)
        self.declare_parameter("place_positions_path", "")
        self.declare_parameter("calibration_config_path", "")
        self.declare_parameter("status_period_sec", 5.0)

        self.dry_run = bool(self.get_parameter("dry_run").value)
        self.detections_topic = str(self.get_parameter("detections_topic").value)
        self.select_target_topic = str(self.get_parameter("select_target_topic").value)
        self.selected_target_topic = str(
            self.get_parameter("selected_target_topic").value
        )
        self.status_topic = str(self.get_parameter("status_topic").value)
        self.min_confidence = float(self.get_parameter("min_confidence").value)
        self.image_size = (
            int(self.get_parameter("image_width").value),
            int(self.get_parameter("image_height").value),
        )
        self.place_store = PlaceStore(str(self.get_parameter("place_positions_path").value))
        self.calibration_store = CalibrationStore(
            str(self.get_parameter("calibration_config_path").value)
        )
        self.last_detections_payload = {"detections": []}
        self.last_selection = None
        self.last_error = ""

        self.selected_target_publisher = self.create_publisher(
            String,
            self.selected_target_topic,
            10,
        )
        self.status_publisher = self.create_publisher(String, self.status_topic, 10)
        self.detections_subscription = self.create_subscription(
            String,
            self.detections_topic,
            self._detections_callback,
            10,
        )
        self.command_subscription = self.create_subscription(
            String,
            self.select_target_topic,
            self._select_target_callback,
            10,
        )

        period = float(self.get_parameter("status_period_sec").value)
        self.create_timer(max(period, 1.0), self._publish_status)
        self.get_logger().info(
            "Target selector ready. dry_run=%s detections_topic=%s places=%s"
            % (self.dry_run, self.detections_topic, self.place_store.path)
        )

    def _detections_callback(self, msg):
        try:
            payload = json.loads(msg.data)
            _extract_detections(payload)
        except Exception as exc:
            self.last_error = f"Invalid detections JSON: {exc}"
            self.get_logger().warn(self.last_error)
            return
        self.last_detections_payload = payload
        self.last_error = ""

    def _select_target_callback(self, msg):
        try:
            request = json.loads(msg.data)
            result = select_target_from_detections(
                self.last_detections_payload,
                request,
                self.place_store,
                self.calibration_store,
                dry_run=self.dry_run,
                image_size=self.image_size,
                min_confidence=self.min_confidence,
            )
        except Exception as exc:
            self.last_error = str(exc)
            self.get_logger().warn(self.last_error)
            self._publish_status()
            return

        self.last_selection = result
        if not result.get("selected"):
            self.get_logger().info(result.get("reason", "No target selected"))
            self._publish_status()
            return

        self._publish_json(self.selected_target_publisher, result)
        self.get_logger().info(
            "Selected detection %s class=%s place_id=%s dry-run only"
            % (result["id"], result["class_name"], result["place_id"])
        )
        self._publish_status()

    def _publish_status(self):
        places = {}
        place_ids = []
        try:
            place_status = self.place_store.status()
            places = place_status["places"]
            place_ids = place_status["place_ids"]
        except Exception as exc:
            self.last_error = str(exc)

        detections = []
        try:
            detections = _extract_detections(self.last_detections_payload)
        except TargetSelectionError:
            detections = []

        payload = {
            "dry_run": self.dry_run,
            "detections_topic": self.detections_topic,
            "select_target_topic": self.select_target_topic,
            "selected_target_topic": self.selected_target_topic,
            "detection_count": len(detections),
            "classes": classes_from_detections(detections),
            "places": places,
            "place_ids": place_ids,
            "last_selection": self.last_selection,
            "error": self.last_error,
        }
        self._publish_json(self.status_publisher, payload)

    @staticmethod
    def _publish_json(publisher, payload):
        msg = String()
        msg.data = json.dumps(payload, separators=(",", ":"))
        publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = TargetSelectorNode()
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
