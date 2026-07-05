import os
from pathlib import Path
from typing import Any, Dict, List, Sequence

import cv2
import numpy as np
import rclpy
import yaml
from ament_index_python.packages import PackageNotFoundError
from ament_index_python.packages import get_package_share_directory
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node


PACKAGE_NAME = "dobot_vision_yolo"
ERROR_WARNING_THRESHOLD_MM = 5.0


class CalibrationError(ValueError):
    pass


def resolve_calibration_config_path(config_path: str = "") -> Path:
    if config_path:
        return Path(config_path).expanduser()

    env_path = os.environ.get("DOBOT_VISION_CALIBRATION_PATH", "")
    if env_path:
        return Path(env_path).expanduser()

    candidates = []
    candidates.append(
        Path.cwd()
        / "src"
        / "magician_ros2"
        / PACKAGE_NAME
        / "config"
        / "camera_to_robot.yaml"
    )
    candidates.append(
        Path(__file__).resolve().parents[1] / "config" / "camera_to_robot.yaml"
    )

    try:
        candidates.append(
            Path(get_package_share_directory(PACKAGE_NAME))
            / "config"
            / "camera_to_robot.yaml"
        )
    except PackageNotFoundError:
        pass

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def default_calibration() -> Dict[str, Any]:
    return {
        "image_points": [],
        "robot_points": [],
        "safe_z": 60.0,
        "pick_z": -35.0,
        "homography": [],
        "validation": {
            "mean_error_mm": None,
            "max_error_mm": None,
            "point_errors_mm": [],
            "warning": "",
        },
    }


def _as_point(value: Any, name: str) -> List[float]:
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise CalibrationError(f"{name} must be [x, y]")
    try:
        return [float(value[0]), float(value[1])]
    except (TypeError, ValueError) as exc:
        raise CalibrationError(f"{name} must contain numeric values") from exc


def _as_points(value: Any, name: str) -> List[List[float]]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise CalibrationError(f"{name} must be a list of [x, y] points")
    return [_as_point(point, f"{name}[{index}]") for index, point in enumerate(value)]


def _as_float(value: Any, name: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise CalibrationError(f"{name} must be numeric") from exc


def _as_homography_values(value: Any) -> List[float]:
    if value in (None, []):
        return []
    if not isinstance(value, list):
        raise CalibrationError("homography must be a list of 9 numeric values")
    if len(value) != 9:
        raise CalibrationError("homography must contain 9 numeric values")
    try:
        return [float(item) for item in value]
    except (TypeError, ValueError) as exc:
        raise CalibrationError("homography must contain numeric values") from exc


def _homography_matrix(value: Any) -> np.ndarray:
    if not isinstance(value, list) or len(value) != 9:
        raise CalibrationError("Homography is not computed yet")
    try:
        matrix = np.array(value, dtype=np.float64).reshape(3, 3)
    except (TypeError, ValueError) as exc:
        raise CalibrationError("Homography contains invalid numeric values") from exc
    if abs(float(matrix[2, 2])) < 1e-9:
        raise CalibrationError("Homography is invalid: bottom-right value is zero")
    return matrix


def transform_pixel(homography: Sequence[float], image_point: Sequence[float]):
    matrix = _homography_matrix(list(homography))
    point = _as_point(image_point, "image_point")
    src = np.array([[[point[0], point[1]]]], dtype=np.float64)
    dst = cv2.perspectiveTransform(src, matrix)[0][0]
    return [round(float(dst[0]), 3), round(float(dst[1]), 3)]


class CalibrationStore:
    def __init__(self, config_path: str = ""):
        self.path = resolve_calibration_config_path(config_path)

    def load(self) -> Dict[str, Any]:
        data = default_calibration()
        if self.path.exists():
            with self.path.open("r", encoding="utf-8") as stream:
                loaded = yaml.safe_load(stream) or {}
            if not isinstance(loaded, dict):
                raise CalibrationError("Calibration YAML root must be an object")
            data.update(loaded)
        return self._normalize(data)

    def save(self, data: Dict[str, Any]) -> Dict[str, Any]:
        normalized = self._normalize(data)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as stream:
            yaml.safe_dump(normalized, stream, sort_keys=False)
        return normalized

    def status(self) -> Dict[str, Any]:
        data = self.load()
        errors = self.validation_errors(data)
        data["config_path"] = str(self.path)
        data["point_count"] = len(data["image_points"])
        data["is_complete"] = not errors and len(data["homography"]) == 9
        data["validation_errors"] = errors
        return data

    def add_point(self, image_point: Sequence[float], robot_point: Sequence[float]):
        data = self.load()
        data["image_points"].append(_as_point(image_point, "image_point"))
        data["robot_points"].append(_as_point(robot_point, "robot_point"))
        data["homography"] = []
        data["validation"] = default_calibration()["validation"]
        self.save(data)
        return self.status()

    def compute(self):
        data = self.load()
        errors = self.validation_errors(data, require_homography=False)
        if errors:
            raise CalibrationError("; ".join(errors))

        image_points = np.array(data["image_points"], dtype=np.float64)
        robot_points = np.array(data["robot_points"], dtype=np.float64)
        homography, _mask = cv2.findHomography(image_points, robot_points, 0)
        if homography is None:
            raise CalibrationError("OpenCV could not compute homography")

        data["homography"] = [round(float(value), 10) for value in homography.reshape(-1)]
        data["validation"] = self._validation_result(data)
        self.save(data)
        return self.status()

    def test_point(self, image_point: Sequence[float]):
        data = self.load()
        errors = self.validation_errors(data)
        if errors:
            raise CalibrationError("; ".join(errors))

        robot_xy = transform_pixel(data["homography"], image_point)
        return {
            "ok": True,
            "image_point": _as_point(image_point, "image_point"),
            "robot_xy": robot_xy,
            "safe_z": float(data["safe_z"]),
            "pick_z": float(data["pick_z"]),
            "validation": data.get("validation", {}),
        }

    def validation_errors(self, data: Dict[str, Any], require_homography: bool = True):
        errors = []
        try:
            image_points = _as_points(data.get("image_points", []), "image_points")
        except CalibrationError as exc:
            errors.append(str(exc))
            image_points = []
        try:
            robot_points = _as_points(data.get("robot_points", []), "robot_points")
        except CalibrationError as exc:
            errors.append(str(exc))
            robot_points = []

        if len(image_points) != len(robot_points):
            errors.append("image_points and robot_points must have the same length")
        if len(image_points) < 4:
            errors.append("At least 4 calibration points are required")

        for index, point in enumerate(image_points):
            try:
                _as_point(point, f"image_points[{index}]")
            except CalibrationError as exc:
                errors.append(str(exc))
        for index, point in enumerate(robot_points):
            try:
                _as_point(point, f"robot_points[{index}]")
            except CalibrationError as exc:
                errors.append(str(exc))

        for key, default in (("safe_z", 60.0), ("pick_z", -35.0)):
            try:
                _as_float(data.get(key, default), key)
            except CalibrationError as exc:
                errors.append(str(exc))

        if require_homography:
            try:
                _homography_matrix(_as_homography_values(data.get("homography", [])))
            except CalibrationError as exc:
                errors.append(str(exc))

        return errors

    def _normalize(self, data: Dict[str, Any]) -> Dict[str, Any]:
        normalized = default_calibration()
        normalized.update(data)
        normalized["image_points"] = _as_points(
            normalized.get("image_points", []),
            "image_points",
        )
        normalized["robot_points"] = _as_points(
            normalized.get("robot_points", []),
            "robot_points",
        )
        normalized["safe_z"] = _as_float(normalized.get("safe_z", 60.0), "safe_z")
        normalized["pick_z"] = _as_float(normalized.get("pick_z", -35.0), "pick_z")
        normalized["homography"] = _as_homography_values(
            normalized.get("homography", [])
        )
        if not isinstance(normalized.get("validation"), dict):
            normalized["validation"] = default_calibration()["validation"]
        return normalized

    def _validation_result(self, data: Dict[str, Any]):
        errors = []
        for image_point, robot_point in zip(data["image_points"], data["robot_points"]):
            projected = transform_pixel(data["homography"], image_point)
            target = _as_point(robot_point, "robot_point")
            errors.append(float(np.linalg.norm(np.array(projected) - np.array(target))))

        point_errors = [round(value, 3) for value in errors]
        mean_error = round(float(np.mean(errors)), 3) if errors else None
        max_error = round(float(np.max(errors)), 3) if errors else None
        warning = ""
        if mean_error is not None and mean_error > ERROR_WARNING_THRESHOLD_MM:
            warning = (
                f"Average calibration error {mean_error} mm exceeds "
                f"{ERROR_WARNING_THRESHOLD_MM:g} mm"
            )
        elif max_error is not None and max_error > ERROR_WARNING_THRESHOLD_MM:
            warning = (
                f"Maximum calibration error {max_error} mm exceeds "
                f"{ERROR_WARNING_THRESHOLD_MM:g} mm"
            )
        return {
            "mean_error_mm": mean_error,
            "max_error_mm": max_error,
            "point_errors_mm": point_errors,
            "warning": warning,
        }


class CameraCalibrationTool(Node):
    def __init__(self):
        super().__init__("camera_calibration_tool")
        self.declare_parameter("dry_run", True)
        self.declare_parameter("image_topic", "/camera/color/image_raw")
        self.declare_parameter("calibration_config_path", "")
        self.declare_parameter("status_period_sec", 5.0)

        self.dry_run = bool(self.get_parameter("dry_run").value)
        self.image_topic = str(self.get_parameter("image_topic").value)
        self.store = CalibrationStore(
            str(self.get_parameter("calibration_config_path").value)
        )

        period = float(self.get_parameter("status_period_sec").value)
        self.create_timer(max(period, 1.0), self._log_status)
        self.get_logger().info(
            "Camera calibration tool ready. dry_run=%s, image_topic=%s, config=%s"
            % (self.dry_run, self.image_topic, self.store.path)
        )

    def _log_status(self):
        status = self.store.status()
        self.get_logger().info(
            "Calibration points=%d complete=%s mean_error_mm=%s"
            % (
                status["point_count"],
                status["is_complete"],
                status.get("validation", {}).get("mean_error_mm"),
            )
        )


def main(args=None):
    rclpy.init(args=args)
    node = CameraCalibrationTool()
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
