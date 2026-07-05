import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Sequence
from urllib.request import urlopen

import cv2
import numpy as np
import rclpy
import yaml
from ament_index_python.packages import PackageNotFoundError
from ament_index_python.packages import get_package_share_directory
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node


PACKAGE_NAME = "dobot_vision_yolo"
MEAN_ERROR_THRESHOLD_MM = 5.0
MAX_ERROR_THRESHOLD_MM = 10.0
CLI_COMMANDS = {"status", "add-point", "compute", "test-point", "click-snapshot"}


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
        "calibration_valid": False,
        "mean_error_mm": None,
        "max_error_mm": None,
        "calibrated_at": None,
        "validation": {
            "mean_error_mm": None,
            "max_error_mm": None,
            "point_errors_mm": [],
            "calibration_valid": False,
            "calibrated_at": None,
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


def _as_optional_float(value: Any, name: str):
    if value is None:
        return None
    return _as_float(value, name)


def _as_bool(value: Any, name: str) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in ("1", "true", "yes", "on"):
            return True
        if lowered in ("0", "false", "no", "off"):
            return False
    if isinstance(value, (int, float)):
        return bool(value)
    raise CalibrationError(f"{name} must be boolean")


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00",
        "Z",
    )


def _error_within_thresholds(mean_error, max_error) -> bool:
    if mean_error is None or max_error is None:
        return False
    return (
        float(mean_error) <= MEAN_ERROR_THRESHOLD_MM
        and float(max_error) <= MAX_ERROR_THRESHOLD_MM
    )


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
        data["calibration_valid"] = (
            bool(data.get("calibration_valid", False))
            and not errors
            and len(data["homography"]) == 9
            and not data.get("validation", {}).get("warning")
        )
        data["is_complete"] = data["calibration_valid"]
        data["validation_errors"] = errors
        return data

    def add_point(self, image_point: Sequence[float], robot_point: Sequence[float]):
        data = self.load()
        data["image_points"].append(_as_point(image_point, "image_point"))
        data["robot_points"].append(_as_point(robot_point, "robot_point"))
        data["homography"] = []
        data["calibration_valid"] = False
        data["mean_error_mm"] = None
        data["max_error_mm"] = None
        data["calibrated_at"] = None
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
        data["calibration_valid"] = bool(data["validation"]["calibration_valid"])
        data["mean_error_mm"] = data["validation"]["mean_error_mm"]
        data["max_error_mm"] = data["validation"]["max_error_mm"]
        data["calibrated_at"] = _utc_now_iso()
        data["validation"]["calibrated_at"] = data["calibrated_at"]
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
            "calibration_valid": bool(data.get("calibration_valid", False)),
            "mean_error_mm": data.get("mean_error_mm"),
            "max_error_mm": data.get("max_error_mm"),
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
        raw_validation = data.get("validation") if isinstance(data, dict) else {}
        if not isinstance(raw_validation, dict):
            raw_validation = {}
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
        validation = default_calibration()["validation"]
        validation.update(normalized.get("validation", {}))

        mean_error = normalized.get("mean_error_mm", raw_validation.get("mean_error_mm"))
        max_error = normalized.get("max_error_mm", raw_validation.get("max_error_mm"))
        normalized["mean_error_mm"] = _as_optional_float(mean_error, "mean_error_mm")
        normalized["max_error_mm"] = _as_optional_float(max_error, "max_error_mm")

        calibrated_at = normalized.get(
            "calibrated_at",
            raw_validation.get("calibrated_at"),
        )
        if calibrated_at is not None and not isinstance(calibrated_at, str):
            raise CalibrationError("calibrated_at must be a string or null")
        normalized["calibrated_at"] = calibrated_at

        has_valid_field = "calibration_valid" in data or "calibration_valid" in raw_validation
        calibration_valid = normalized.get(
            "calibration_valid",
            raw_validation.get("calibration_valid", False),
        )
        normalized["calibration_valid"] = _as_bool(
            calibration_valid,
            "calibration_valid",
        )
        if not has_valid_field and normalized["homography"]:
            normalized["calibration_valid"] = _error_within_thresholds(
                normalized["mean_error_mm"],
                normalized["max_error_mm"],
            ) and not validation.get("warning")

        validation["mean_error_mm"] = normalized["mean_error_mm"]
        validation["max_error_mm"] = normalized["max_error_mm"]
        validation["calibration_valid"] = normalized["calibration_valid"]
        validation["calibrated_at"] = normalized["calibrated_at"]
        if not isinstance(validation.get("point_errors_mm"), list):
            validation["point_errors_mm"] = []
        if not isinstance(validation.get("warning", ""), str):
            raise CalibrationError("validation.warning must be a string")
        normalized["validation"] = validation
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
        if mean_error is not None and mean_error > MEAN_ERROR_THRESHOLD_MM:
            warning = (
                f"Average calibration error {mean_error} mm exceeds "
                f"{MEAN_ERROR_THRESHOLD_MM:g} mm"
            )
        elif max_error is not None and max_error > MAX_ERROR_THRESHOLD_MM:
            warning = (
                f"Maximum calibration error {max_error} mm exceeds "
                f"{MAX_ERROR_THRESHOLD_MM:g} mm"
            )
        return {
            "mean_error_mm": mean_error,
            "max_error_mm": max_error,
            "point_errors_mm": point_errors,
            "calibration_valid": _error_within_thresholds(mean_error, max_error),
            "calibrated_at": None,
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


def _print_json(payload: Dict[str, Any]) -> int:
    print(json.dumps(payload, indent=2, sort_keys=False))
    return 0


def _store_from_args(args) -> CalibrationStore:
    return CalibrationStore(str(getattr(args, "config", "") or ""))


def _cli_status(args) -> int:
    return _print_json(_store_from_args(args).status())


def _cli_add_point(args) -> int:
    image_point = args.image_point if args.image_point is not None else args.pixel
    if image_point is None:
        raise CalibrationError("--image-point or --pixel is required")
    return _print_json(_store_from_args(args).add_point(image_point, args.robot_point))


def _cli_compute(args) -> int:
    return _print_json(_store_from_args(args).compute())


def _cli_test_point(args) -> int:
    image_point = args.image_point if args.image_point is not None else args.pixel
    if image_point is None:
        raise CalibrationError("--image-point or --pixel is required")
    return _print_json(_store_from_args(args).test_point(image_point))


def _load_snapshot_bytes(args) -> bytes:
    if args.file:
        return Path(args.file).expanduser().read_bytes()
    with urlopen(args.url, timeout=float(args.timeout_sec)) as response:
        return response.read()


def _cli_click_snapshot(args) -> int:
    data = np.frombuffer(_load_snapshot_bytes(args), dtype=np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if image is None:
        raise CalibrationError("Snapshot could not be decoded as an image")

    points: List[List[int]] = []
    window_name = "Dobot calibration snapshot"

    def on_mouse(event, x, y, _flags, _userdata):
        if event != cv2.EVENT_LBUTTONDOWN:
            return
        points.append([int(x), int(y)])
        cv2.circle(image, (int(x), int(y)), 5, (0, 255, 255), -1)
        cv2.putText(
            image,
            str(len(points)),
            (int(x) + 8, int(y) - 8),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 255),
            2,
            cv2.LINE_AA,
        )

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(window_name, on_mouse)
    print("Click calibration markers. Press Enter when done, Esc to cancel.")
    while True:
        cv2.imshow(window_name, image)
        key = cv2.waitKey(20) & 0xFF
        if key in (13, 10):
            break
        if key == 27:
            points = []
            break
        if args.count and len(points) >= int(args.count):
            break
    cv2.destroyWindow(window_name)

    result = {"image_points": points, "point_count": len(points)}
    if args.output:
        output_path = Path(args.output).expanduser()
        with output_path.open("w", encoding="utf-8") as stream:
            yaml.safe_dump(result, stream, sort_keys=False)
        result["output"] = str(output_path)
    return _print_json(result)


def _build_cli_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage Dobot camera-to-robot homography calibration.",
    )
    parser.add_argument(
        "--config",
        default="",
        help="Calibration YAML path. Defaults to DOBOT_VISION_CALIBRATION_PATH or package config.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    status = subparsers.add_parser("status", help="Print calibration status as JSON.")
    status.set_defaults(func=_cli_status)

    add_point = subparsers.add_parser(
        "add-point",
        help="Append one matching image/robot calibration point.",
    )
    add_point.add_argument("--image-point", nargs=2, type=float, metavar=("U", "V"))
    add_point.add_argument("--pixel", nargs=2, type=float, metavar=("U", "V"))
    add_point.add_argument(
        "--robot-point",
        nargs=2,
        type=float,
        required=True,
        metavar=("X", "Y"),
    )
    add_point.set_defaults(func=_cli_add_point)

    compute = subparsers.add_parser(
        "compute",
        help="Compute homography and validation error from saved points.",
    )
    compute.set_defaults(func=_cli_compute)

    test_point = subparsers.add_parser(
        "test-point",
        help="Transform one pixel into Dobot X/Y using the saved homography.",
    )
    test_point.add_argument("--image-point", nargs=2, type=float, metavar=("U", "V"))
    test_point.add_argument("--pixel", nargs=2, type=float, metavar=("U", "V"))
    test_point.set_defaults(func=_cli_test_point)

    click_snapshot = subparsers.add_parser(
        "click-snapshot",
        help="Click pixels from a snapshot image without moving the robot.",
    )
    click_snapshot.add_argument(
        "--url",
        default="http://127.0.0.1:8080/api/snapshot",
        help="Snapshot URL to load when --file is not provided.",
    )
    click_snapshot.add_argument("--file", default="", help="Local snapshot image path.")
    click_snapshot.add_argument("--count", type=int, default=4)
    click_snapshot.add_argument("--output", default="", help="Optional YAML output path.")
    click_snapshot.add_argument("--timeout-sec", type=float, default=3.0)
    click_snapshot.set_defaults(func=_cli_click_snapshot)

    return parser


def _run_cli(argv: Sequence[str]) -> int:
    parser = _build_cli_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except CalibrationError as exc:
        parser.exit(2, f"error: {exc}\n")


def main(args=None):
    argv = list(sys.argv[1:] if args is None else args)
    if argv and (
        any(item in CLI_COMMANDS for item in argv)
        or any(item in ("-h", "--help") for item in argv)
    ):
        raise SystemExit(_run_cli(argv))

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
