import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

import rclpy
import yaml
from ament_index_python.packages import PackageNotFoundError
from ament_index_python.packages import get_package_share_directory
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node


PACKAGE_NAME = "dobot_vision_yolo"


@dataclass(frozen=True)
class SafetyDecision:
    allowed: bool
    reason: str


@dataclass(frozen=True)
class WorkspaceLimits:
    x_min_mm: float
    x_max_mm: float
    y_min_mm: float
    y_max_mm: float
    z_min_mm: float
    z_max_mm: float

    def contains(self, pose_mm: Sequence[float]) -> bool:
        if len(pose_mm) < 3:
            return False
        x, y, z = pose_mm[:3]
        return (
            self.x_min_mm <= float(x) <= self.x_max_mm
            and self.y_min_mm <= float(y) <= self.y_max_mm
            and self.z_min_mm <= float(z) <= self.z_max_mm
        )

    def violation_reason(self, pose_mm: Sequence[float], label: str) -> str:
        if len(pose_mm) < 3:
            return f"{label} must contain at least x, y, z"
        x, y, z = [float(value) for value in pose_mm[:3]]
        problems = []
        if not self.x_min_mm <= x <= self.x_max_mm:
            problems.append(
                f"x={x:g} outside [{self.x_min_mm:g}, {self.x_max_mm:g}]"
            )
        if not self.y_min_mm <= y <= self.y_max_mm:
            problems.append(
                f"y={y:g} outside [{self.y_min_mm:g}, {self.y_max_mm:g}]"
            )
        if not self.z_min_mm <= z <= self.z_max_mm:
            problems.append(
                f"z={z:g} outside [{self.z_min_mm:g}, {self.z_max_mm:g}]"
            )
        if not problems:
            return f"{label} is inside workspace"
        return f"{label} outside workspace: " + ", ".join(problems)

    def as_dict(self) -> Dict[str, float]:
        return {
            "x_min": self.x_min_mm,
            "x_max": self.x_max_mm,
            "y_min": self.y_min_mm,
            "y_max": self.y_max_mm,
            "z_min": self.z_min_mm,
            "z_max": self.z_max_mm,
        }


@dataclass(frozen=True)
class SafetyConfig:
    workspace: WorkspaceLimits
    min_confidence: float = 0.70
    require_homing: bool = True
    homing_policy: str = "reject"
    dry_run_default: bool = True
    allow_real_motion: bool = False
    camera_timeout_sec: float = 5.0

    def as_dict(self) -> Dict[str, Any]:
        return {
            "workspace": self.workspace.as_dict(),
            "min_confidence": self.min_confidence,
            "require_homing": self.require_homing,
            "homing_policy": self.homing_policy,
            "dry_run_default": self.dry_run_default,
            "allow_real_motion": self.allow_real_motion,
            "camera_timeout_sec": self.camera_timeout_sec,
        }


def default_safety_config() -> SafetyConfig:
    return SafetyConfig(
        workspace=WorkspaceLimits(
            x_min_mm=150.0,
            x_max_mm=320.0,
            y_min_mm=-180.0,
            y_max_mm=180.0,
            z_min_mm=-45.0,
            z_max_mm=120.0,
        )
    )


def resolve_workspace_config_path(config_path: str = "") -> Path:
    if config_path:
        return Path(config_path).expanduser()

    env_path = os.environ.get("DOBOT_VISION_WORKSPACE_PATH", "")
    if env_path:
        return Path(env_path).expanduser()

    candidates = [
        Path.cwd()
        / "src"
        / "magician_ros2"
        / PACKAGE_NAME
        / "config"
        / "workspace.yaml",
        Path(__file__).resolve().parents[1] / "config" / "workspace.yaml",
    ]
    try:
        candidates.append(
            Path(get_package_share_directory(PACKAGE_NAME))
            / "config"
            / "workspace.yaml"
        )
    except PackageNotFoundError:
        pass

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def _load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as stream:
        loaded = yaml.safe_load(stream) or {}
    if not isinstance(loaded, dict):
        raise ValueError(f"{path} root must be an object")
    return loaded


def _as_bool(value: Any, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in ("1", "true", "yes", "on")
    return bool(value)


def _as_float(value: Any, name: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be numeric") from exc


def _pose(value: Any, name: str) -> Optional[List[float]]:
    if value is None:
        return None
    if not isinstance(value, (list, tuple)) or len(value) != 4:
        raise ValueError(f"{name} must be [x, y, z, r]")
    try:
        return [float(item) for item in value]
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must contain numeric values") from exc


def load_safety_config(config_path: str = "") -> SafetyConfig:
    path = resolve_workspace_config_path(config_path)
    data = _load_yaml(path)
    defaults = default_safety_config()

    workspace_data = data.get("workspace", {})
    if not isinstance(workspace_data, dict):
        raise ValueError("workspace must be an object")

    workspace = WorkspaceLimits(
        x_min_mm=_as_float(
            workspace_data.get("x_min", defaults.workspace.x_min_mm),
            "workspace.x_min",
        ),
        x_max_mm=_as_float(
            workspace_data.get("x_max", defaults.workspace.x_max_mm),
            "workspace.x_max",
        ),
        y_min_mm=_as_float(
            workspace_data.get("y_min", defaults.workspace.y_min_mm),
            "workspace.y_min",
        ),
        y_max_mm=_as_float(
            workspace_data.get("y_max", defaults.workspace.y_max_mm),
            "workspace.y_max",
        ),
        z_min_mm=_as_float(
            workspace_data.get("z_min", defaults.workspace.z_min_mm),
            "workspace.z_min",
        ),
        z_max_mm=_as_float(
            workspace_data.get("z_max", defaults.workspace.z_max_mm),
            "workspace.z_max",
        ),
    )
    if workspace.x_min_mm >= workspace.x_max_mm:
        raise ValueError("workspace.x_min must be less than workspace.x_max")
    if workspace.y_min_mm >= workspace.y_max_mm:
        raise ValueError("workspace.y_min must be less than workspace.y_max")
    if workspace.z_min_mm >= workspace.z_max_mm:
        raise ValueError("workspace.z_min must be less than workspace.z_max")

    homing_policy = str(data.get("homing_policy", defaults.homing_policy))
    if homing_policy not in ("warn", "reject"):
        raise ValueError("homing_policy must be warn or reject")

    return SafetyConfig(
        workspace=workspace,
        min_confidence=_as_float(
            data.get("min_confidence", defaults.min_confidence),
            "min_confidence",
        ),
        require_homing=_as_bool(
            data.get("require_homing"),
            defaults.require_homing,
        ),
        homing_policy=homing_policy,
        dry_run_default=_as_bool(
            data.get("dry_run_default"),
            defaults.dry_run_default,
        ),
        allow_real_motion=_as_bool(
            data.get("allow_real_motion"),
            defaults.allow_real_motion,
        ),
        camera_timeout_sec=_as_float(
            data.get("camera_timeout_sec", defaults.camera_timeout_sec),
            "camera_timeout_sec",
        ),
    )


class SafetyGuard:
    """Shared validation for dry-run vision pick decisions."""

    def __init__(
        self,
        workspace: Optional[WorkspaceLimits] = None,
        dry_run: bool = True,
        config: Optional[SafetyConfig] = None,
    ):
        self.config = config or SafetyConfig(
            workspace=workspace or default_safety_config().workspace,
            dry_run_default=dry_run,
        )
        self.workspace = self.config.workspace
        self.dry_run = dry_run

    def validate_target_pose(self, pose_mm: Sequence[float]) -> SafetyDecision:
        if len(pose_mm) != 4:
            return SafetyDecision(False, "target pose must contain x, y, z, r")
        if not self.workspace.contains(pose_mm):
            return SafetyDecision(
                False,
                self.workspace.violation_reason(pose_mm, "target pose"),
            )
        if not self.dry_run and not self.config.allow_real_motion:
            return SafetyDecision(
                False,
                "real motion is disabled by safety config",
            )
        return SafetyDecision(True, "dry-run target pose accepted")

    def validate_pick(
        self,
        selected_target: Optional[Dict[str, Any]],
        camera_status: Optional[Dict[str, Any]] = None,
        yolo_status: Optional[Dict[str, Any]] = None,
        calibration_status: Optional[Dict[str, Any]] = None,
        places: Optional[Dict[str, Any]] = None,
        dry_run: Optional[bool] = None,
        robot_homed: Optional[bool] = None,
    ) -> Dict[str, Any]:
        checks = []
        warnings = []
        errors = []

        def add_check(name: str, label: str, ok: bool, reason: str, severity="error"):
            item = {
                "name": name,
                "label": label,
                "ok": bool(ok),
                "reason": reason,
                "severity": severity,
            }
            checks.append(item)
            if not ok and severity == "warning":
                warnings.append(reason)
            elif not ok:
                errors.append(reason)

        camera_status = camera_status or {}
        frame_age = camera_status.get("frame_age_sec")
        has_frame = bool(camera_status.get("has_frame", False))
        camera_fresh = frame_age is None or float(frame_age) <= self.config.camera_timeout_sec
        add_check(
            "camera",
            "Camera OK",
            has_frame and camera_fresh,
            (
                "Camera frame is available"
                if has_frame and camera_fresh
                else "Camera is offline or frame is stale"
            ),
        )

        yolo_status = yolo_status or {}
        yolo_ok = bool(yolo_status.get("ok", False)) and bool(
            yolo_status.get("model_loaded", False)
        )
        add_check(
            "yolo",
            "YOLO OK",
            yolo_ok,
            "YOLO detector is ready" if yolo_ok else yolo_status.get(
                "error",
                "YOLO detector is not ready",
            ),
        )

        calibration_status = calibration_status or {}
        validation_errors = calibration_status.get("validation_errors", [])
        validation = calibration_status.get("validation", {}) or {}
        calibration_warning = validation.get("warning", "")
        calibration_ok = (
            bool(calibration_status.get("is_complete", False))
            and not validation_errors
            and not calibration_warning
        )
        add_check(
            "calibration",
            "Calibration OK",
            calibration_ok,
            (
                "Calibration is valid"
                if calibration_ok
                else "; ".join(validation_errors)
                or calibration_warning
                or "Calibration is incomplete"
            ),
        )

        selected_ok = bool(selected_target and selected_target.get("selected", False))
        add_check(
            "target",
            "Target OK",
            selected_ok,
            "Selected target is available"
            if selected_ok
            else "No selected target is available",
        )

        confidence_ok = False
        if selected_ok:
            try:
                confidence = float(selected_target.get("confidence", 0.0))
            except (TypeError, ValueError):
                confidence = 0.0
            confidence_ok = confidence >= self.config.min_confidence
        add_check(
            "confidence",
            "Confidence OK",
            confidence_ok,
            (
                f"confidence is at least {self.config.min_confidence:g}"
                if confidence_ok
                else f"confidence is below {self.config.min_confidence:g}"
            ),
        )

        places = places or {}
        place_id = selected_target.get("place_id") if selected_ok else None
        place_ok = bool(place_id and place_id in places)
        add_check(
            "place",
            "Place OK",
            place_ok,
            f"place_id '{place_id}' exists"
            if place_ok
            else f"place_id '{place_id}' is not configured",
        )

        workspace_ok = False
        workspace_reason = "No target pose to validate"
        if selected_ok:
            try:
                pick_pose = _pose(selected_target.get("pick_pose"), "pick_pose")
                configured_place = places.get(place_id, {}) if place_ok else {}
                place_pose = configured_place.get("pose") or selected_target.get("place_pose")
                place_pose = _pose(place_pose, "place_pose")
                pick_ok = pick_pose is not None and self.workspace.contains(pick_pose)
                place_pose_ok = place_pose is not None and self.workspace.contains(place_pose)
                workspace_ok = pick_ok and place_pose_ok
                if workspace_ok:
                    workspace_reason = "pick_pose and place_pose are inside workspace"
                else:
                    reasons = []
                    if pick_pose is None or not pick_ok:
                        reasons.append(
                            self.workspace.violation_reason(pick_pose or [], "pick_pose")
                        )
                    if place_pose is None or not place_pose_ok:
                        reasons.append(
                            self.workspace.violation_reason(place_pose or [], "place_pose")
                        )
                    workspace_reason = "; ".join(reasons)
            except ValueError as exc:
                workspace_reason = str(exc)
        add_check(
            "workspace",
            "Workspace OK",
            workspace_ok,
            workspace_reason,
        )

        effective_dry_run = self.config.dry_run_default if dry_run is None else bool(dry_run)
        dry_run_ok = effective_dry_run or self.config.allow_real_motion
        add_check(
            "dry_run",
            "Dry Run",
            dry_run_ok,
            "Dry run is enabled"
            if effective_dry_run
            else "Real motion is disabled by safety config",
        )

        if self.config.require_homing:
            homing_ok = bool(robot_homed)
            severity = "warning" if self.config.homing_policy == "warn" else "error"
            add_check(
                "homing",
                "Homing",
                homing_ok,
                "Robot homing is confirmed"
                if homing_ok
                else "Robot homing is not confirmed",
                severity=severity,
            )
        else:
            add_check(
                "homing",
                "Homing",
                True,
                "Homing confirmation is not required by config",
            )

        return {
            "allowed": len(errors) == 0,
            "dry_run": effective_dry_run,
            "checks": checks,
            "errors": errors,
            "warnings": warnings,
            "reason": "Safety validation passed"
            if len(errors) == 0
            else "; ".join(errors),
            "config": self.config.as_dict(),
        }


def workspace_from_node(node) -> WorkspaceLimits:
    return WorkspaceLimits(
        x_min_mm=float(node.get_parameter("workspace_x_min_mm").value),
        x_max_mm=float(node.get_parameter("workspace_x_max_mm").value),
        y_min_mm=float(node.get_parameter("workspace_y_min_mm").value),
        y_max_mm=float(node.get_parameter("workspace_y_max_mm").value),
        z_min_mm=float(node.get_parameter("workspace_z_min_mm").value),
        z_max_mm=float(node.get_parameter("workspace_z_max_mm").value),
    )


class SafetyGuardNode(Node):
    def __init__(self):
        super().__init__("safety_guard_node")
        self.declare_parameter("dry_run", True)
        self.declare_parameter("workspace_config_path", "")
        self.declare_parameter("workspace_x_min_mm", 150.0)
        self.declare_parameter("workspace_x_max_mm", 320.0)
        self.declare_parameter("workspace_y_min_mm", -180.0)
        self.declare_parameter("workspace_y_max_mm", 180.0)
        self.declare_parameter("workspace_z_min_mm", -45.0)
        self.declare_parameter("workspace_z_max_mm", 120.0)
        self.declare_parameter("min_confidence", 0.70)
        self.declare_parameter("require_homing", True)
        self.declare_parameter("status_period_sec", 5.0)

        config_path = str(self.get_parameter("workspace_config_path").value)
        try:
            config = load_safety_config(config_path)
        except Exception as exc:
            self.get_logger().warn(
                "Workspace YAML unavailable, using node parameters: %s" % exc
            )
            config = SafetyConfig(
                workspace=workspace_from_node(self),
                min_confidence=float(self.get_parameter("min_confidence").value),
                require_homing=bool(self.get_parameter("require_homing").value),
            )

        self.guard = SafetyGuard(
            workspace=config.workspace,
            dry_run=bool(self.get_parameter("dry_run").value),
            config=config,
        )
        period = float(self.get_parameter("status_period_sec").value)
        self.create_timer(max(period, 1.0), self._log_status)
        self.get_logger().info(
            "Safety guard ready. dry_run=%s config=%s"
            % (self.guard.dry_run, config.as_dict())
        )

    def _log_status(self):
        self.get_logger().info(
            "Safety guard idle. Workspace=%s min_confidence=%.2f"
            % (
                self.guard.workspace.as_dict(),
                self.guard.config.min_confidence,
            )
        )


def main(args=None):
    rclpy.init(args=args)
    node = SafetyGuardNode()
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
