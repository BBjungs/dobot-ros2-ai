import ast
import json
import time
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.request import Request
from urllib.request import urlopen
from typing import Any, Dict, List, Optional, Sequence

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import String

from dobot_vision_yolo.safety_guard import SafetyConfig
from dobot_vision_yolo.safety_guard import SafetyGuard
from dobot_vision_yolo.safety_guard import workspace_from_node


def _as_pose(value: Any, name: str) -> List[float]:
    if not isinstance(value, (list, tuple)) or len(value) != 4:
        raise ValueError(f"{name} must be [x, y, z, r]")
    try:
        return [float(item) for item in value]
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must contain numeric values") from exc


def _as_xy(value: Any, name: str) -> List[float]:
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise ValueError(f"{name} must be [x, y]")
    try:
        return [float(value[0]), float(value[1])]
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must contain numeric values") from exc


def _safe_z(selected_target: Dict[str, Any]) -> float:
    if selected_target.get("safe_z") is not None:
        return float(selected_target["safe_z"])
    pick_pose = selected_target.get("pick_pose") or selected_target.get("pose_mm")
    if isinstance(pick_pose, (list, tuple)) and len(pick_pose) >= 3:
        return max(float(pick_pose[2]) + 30.0, 60.0)
    return 60.0


def _step_safety(
    pose: Optional[Sequence[float]],
    safety_guard: Optional[SafetyGuard],
    tool_step: bool = False,
) -> Dict[str, Any]:
    if tool_step:
        return {
            "allowed": True,
            "reason": "simulated tool command only; no hardware I/O",
        }
    if safety_guard is None:
        return {
            "allowed": True,
            "reason": "validated by preview safety gate",
        }
    if pose is None:
        return {
            "allowed": True,
            "reason": "no robot pose for simulated command",
        }
    decision = safety_guard.validate_target_pose(pose)
    return {
        "allowed": bool(decision.allowed),
        "reason": decision.reason,
    }


def _sequence_step(
    step: int,
    command: str,
    pose: Optional[Sequence[float]],
    safety_guard: Optional[SafetyGuard],
    tool_step: bool = False,
) -> Dict[str, Any]:
    return {
        "step": step,
        "command": command,
        "pose": [round(float(item), 3) for item in pose] if pose is not None else None,
        "simulated": True,
        "safety_result": _step_safety(pose, safety_guard, tool_step=tool_step),
    }


def build_motion_sequence(
    selected_target: Dict[str, Any],
    safety_guard: Optional[SafetyGuard] = None,
) -> List[Dict[str, Any]]:
    if not isinstance(selected_target, dict):
        raise ValueError("selected_target must be an object")
    if not selected_target.get("selected", False):
        raise ValueError("selected_target must be selected before preview")
    if not bool(selected_target.get("dry_run", True)):
        raise ValueError("motion preview is dry_run only")

    robot_xy = selected_target.get("robot_xy")
    if robot_xy is None and selected_target.get("pick_pose"):
        robot_xy = selected_target["pick_pose"][:2]
    robot_xy = _as_xy(robot_xy, "robot_xy")

    pick_pose = selected_target.get("pick_pose") or selected_target.get("pose_mm")
    if pick_pose is None:
        pick_z = float(selected_target.get("pick_z", -35.0))
        pick_pose = [robot_xy[0], robot_xy[1], pick_z, 0.0]
    pick_pose = _as_pose(pick_pose, "pick_pose")

    place_pose = _as_pose(selected_target.get("place_pose"), "place_pose")
    safe_z = _safe_z(selected_target)
    above_target = [pick_pose[0], pick_pose[1], safe_z, pick_pose[3]]
    above_place = [place_pose[0], place_pose[1], safe_z, place_pose[3]]

    sequence = [
        _sequence_step(1, "move_above_target", above_target, safety_guard),
        _sequence_step(2, "move_down_to_pick", pick_pose, safety_guard),
        _sequence_step(3, "tool_on_simulated", pick_pose, safety_guard, tool_step=True),
        _sequence_step(4, "move_up_from_pick", above_target, safety_guard),
        _sequence_step(5, "move_above_place", above_place, safety_guard),
        _sequence_step(6, "move_down_to_place", place_pose, safety_guard),
        _sequence_step(7, "tool_off_simulated", place_pose, safety_guard, tool_step=True),
        _sequence_step(8, "move_up_from_place", above_place, safety_guard),
    ]

    blocked = [
        step
        for step in sequence
        if not step.get("safety_result", {}).get("allowed", False)
    ]
    if blocked:
        reasons = "; ".join(
            step.get("safety_result", {}).get("reason", "blocked")
            for step in blocked
        )
        raise ValueError(f"motion sequence failed safety validation: {reasons}")
    return sequence


def build_real_motion_sequence(
    selected_target: Dict[str, Any],
    safety_guard: Optional[SafetyGuard] = None,
    tool_type: str = "suction",
    wait_after_tool_sec: float = 0.5,
) -> List[Dict[str, Any]]:
    if not isinstance(selected_target, dict):
        raise ValueError("selected_target must be an object")
    if not selected_target.get("selected", False):
        raise ValueError("selected_target must be selected before execution")
    if bool(selected_target.get("dry_run", True)):
        raise ValueError("real execution target must have dry_run=false")

    tool_type = str(tool_type or "suction").lower()
    if tool_type not in ("suction", "gripper"):
        raise ValueError("tool_type must be suction or gripper")

    robot_xy = selected_target.get("robot_xy")
    if robot_xy is None and selected_target.get("pick_pose"):
        robot_xy = selected_target["pick_pose"][:2]
    robot_xy = _as_xy(robot_xy, "robot_xy")

    pick_pose = selected_target.get("pick_pose") or selected_target.get("pose_mm")
    if pick_pose is None:
        pick_z = float(selected_target.get("pick_z", -35.0))
        pick_pose = [robot_xy[0], robot_xy[1], pick_z, 0.0]
    pick_pose = _as_pose(pick_pose, "pick_pose")
    place_pose = _as_pose(selected_target.get("place_pose"), "place_pose")
    safe_z = _safe_z(selected_target)
    above_target = [pick_pose[0], pick_pose[1], safe_z, pick_pose[3]]
    above_place = [place_pose[0], place_pose[1], safe_z, place_pose[3]]
    tool_on = "suction_on" if tool_type == "suction" else "gripper_close"
    tool_off = "suction_off" if tool_type == "suction" else "gripper_open"

    sequence = [
        _sequence_step(1, "move_above_target", above_target, safety_guard),
        _sequence_step(2, "move_down_to_pick", pick_pose, safety_guard),
        _sequence_step(3, tool_on, pick_pose, safety_guard, tool_step=True),
        {
            "step": 4,
            "command": "wait_after_tool_on",
            "pose": None,
            "duration_sec": round(float(wait_after_tool_sec), 3),
            "simulated": False,
            "safety_result": {
                "allowed": True,
                "reason": "timed wait only; no hardware command",
            },
        },
        _sequence_step(5, "move_up_from_pick", above_target, safety_guard),
        _sequence_step(6, "move_above_place", above_place, safety_guard),
        _sequence_step(7, "move_down_to_place", place_pose, safety_guard),
        _sequence_step(8, tool_off, place_pose, safety_guard, tool_step=True),
        _sequence_step(9, "move_up_from_place", above_place, safety_guard),
    ]
    for step in sequence:
        step["simulated"] = False

    blocked = [
        step
        for step in sequence
        if not step.get("safety_result", {}).get("allowed", False)
    ]
    if blocked:
        reasons = "; ".join(
            step.get("safety_result", {}).get("reason", "blocked")
            for step in blocked
        )
        raise ValueError(f"real motion sequence failed safety validation: {reasons}")
    return sequence


class HTTPMotionExecutor:
    def __init__(
        self,
        api_base_url: str,
        velocity_ratio: float = 0.3,
        acceleration_ratio: float = 0.2,
        tool_type: str = "suction",
        move_timeout_sec: float = 45.0,
    ):
        self.api_base_url = api_base_url.rstrip("/")
        self.velocity_ratio = float(velocity_ratio)
        self.acceleration_ratio = float(acceleration_ratio)
        self.tool_type = str(tool_type or "suction").lower()
        self.move_timeout_sec = float(move_timeout_sec)
        if self.tool_type not in ("suction", "gripper"):
            raise ValueError("tool_type must be suction or gripper")
        if not 0.0 < self.velocity_ratio <= 0.5:
            raise ValueError("velocity_ratio must be within (0.0, 0.5] for vision pick")
        if not 0.0 < self.acceleration_ratio <= 0.5:
            raise ValueError(
                "acceleration_ratio must be within (0.0, 0.5] for vision pick"
            )

    def execute(self, sequence: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        tool_active = False
        try:
            for step in sequence:
                result = self._execute_step(step)
                if step["command"] in ("suction_on", "gripper_close"):
                    tool_active = True
                elif step["command"] in ("suction_off", "gripper_open"):
                    tool_active = False
                results.append(result)
        except Exception as exc:
            if tool_active:
                try:
                    results.append(
                        {
                            "step": "cleanup",
                            "command": "tool_off_cleanup",
                            "response": self._tool(False),
                        }
                    )
                except Exception as cleanup_exc:
                    results.append(
                        {
                            "step": "cleanup",
                            "command": "tool_off_cleanup",
                            "error": str(cleanup_exc),
                        }
                    )
            raise RuntimeError(f"vision pick execution failed: {exc}") from exc
        return results

    def _execute_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        command = step.get("command", "")
        if command.startswith("move_"):
            response = self._move(step["pose"])
            if response.get("accepted") is False:
                raise RuntimeError(response.get("message", "motion goal rejected"))
            self._wait_until_motion_idle()
        elif command == "suction_on" or command == "gripper_close":
            response = self._tool(True)
        elif command == "suction_off" or command == "gripper_open":
            response = self._tool(False)
        elif command == "wait_after_tool_on":
            time.sleep(float(step.get("duration_sec", 0.5)))
            response = {"waited_sec": float(step.get("duration_sec", 0.5))}
        else:
            raise ValueError(f"Unsupported motion command '{command}'")
        return {
            "step": step.get("step"),
            "command": command,
            "response": response,
        }

    def _move(self, pose: Sequence[float]) -> Dict[str, Any]:
        return self._post(
            "/api/move",
            {
                "motion_type": 2,
                "target_pose": [float(item) for item in pose],
                "velocity_ratio": self.velocity_ratio,
                "acceleration_ratio": self.acceleration_ratio,
            },
        )

    def _tool(self, enable: bool) -> Dict[str, Any]:
        if self.tool_type == "suction":
            return self._post("/api/suction", {"enable_suction": bool(enable)})
        return self._post(
            "/api/gripper",
            {
                "state": "close" if enable else "open",
                "keep_compressor_running": bool(enable),
            },
        )

    def _wait_until_motion_idle(self):
        deadline = time.monotonic() + self.move_timeout_sec
        while time.monotonic() < deadline:
            status = self._get("/api/status")
            if not status.get("motion", {}).get("active_goal", False):
                return
            time.sleep(0.2)
        raise TimeoutError("Timed out waiting for motion goal to finish")

    def _get(self, path: str) -> Dict[str, Any]:
        with urlopen(self.api_base_url + path, timeout=5.0) as response:
            return json.loads(response.read().decode("utf-8"))

    def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        data = json.dumps(payload).encode("utf-8")
        request = Request(
            self.api_base_url + path,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=10.0) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"HTTP {exc.code} from {path}: {detail}") from exc
        except URLError as exc:
            raise RuntimeError(f"HTTP request to {path} failed: {exc}") from exc


class VisionPickPlaceNode(Node):
    def __init__(self):
        super().__init__("vision_pick_place_node")
        self.declare_parameter("dry_run", True)
        self.declare_parameter("robot_target_topic", "/dobot_vision_yolo/robot_target")
        self.declare_parameter("status_topic", "/dobot_vision_yolo/pick_place_status")
        self.declare_parameter("workspace_x_min_mm", 150.0)
        self.declare_parameter("workspace_x_max_mm", 320.0)
        self.declare_parameter("workspace_y_min_mm", -180.0)
        self.declare_parameter("workspace_y_max_mm", 180.0)
        self.declare_parameter("workspace_z_min_mm", -45.0)
        self.declare_parameter("workspace_z_max_mm", 120.0)
        self.declare_parameter("allow_real_motion", False)
        self.declare_parameter("web_api_base_url", "http://127.0.0.1:8080")
        self.declare_parameter("velocity_ratio", 0.3)
        self.declare_parameter("acceleration_ratio", 0.2)
        self.declare_parameter("tool_type", "suction")
        self.declare_parameter("status_period_sec", 5.0)

        self.dry_run = bool(self.get_parameter("dry_run").value)
        self.allow_real_motion = bool(self.get_parameter("allow_real_motion").value)
        self.robot_target_topic = str(self.get_parameter("robot_target_topic").value)
        self.status_topic = str(self.get_parameter("status_topic").value)
        self.web_api_base_url = str(self.get_parameter("web_api_base_url").value)
        self.velocity_ratio = float(self.get_parameter("velocity_ratio").value)
        self.acceleration_ratio = float(self.get_parameter("acceleration_ratio").value)
        self.tool_type = str(self.get_parameter("tool_type").value)
        workspace = workspace_from_node(self)
        self.safety_guard = SafetyGuard(
            workspace,
            self.dry_run,
            config=SafetyConfig(
                workspace=workspace,
                dry_run_default=self.dry_run,
                allow_real_motion=self.allow_real_motion,
            ),
        )
        self.last_preview = None

        self.status_publisher = self.create_publisher(String, self.status_topic, 10)
        self.subscription = self.create_subscription(
            String,
            self.robot_target_topic,
            self._robot_target_callback,
            10,
        )
        period = float(self.get_parameter("status_period_sec").value)
        self.create_timer(max(period, 1.0), self._log_status)

        self.get_logger().info(
            "Vision pick-and-place preview started. dry_run=%s. "
            "No /PTP_action or end-effector service clients are created."
            % self.dry_run
        )

    def _robot_target_callback(self, msg):
        try:
            target = self._extract_target(msg.data)
            if target.get("execute_real", False):
                preview = self._execute_real_target(target)
                self.last_preview = preview
                self._publish_status(preview)
                self.get_logger().info("Published real execution status.")
                return

            target["dry_run"] = True
            sequence = build_motion_sequence(target, self.safety_guard)
            preview = {
                "source": "vision_pick_place_node",
                "dry_run": True,
                "preview_only": True,
                "selected_target": target,
                "motion_sequence": sequence,
                "message": "Dry-run motion preview generated. No robot command was sent.",
            }
        except Exception as exc:
            preview = {
                "source": "vision_pick_place_node",
                "dry_run": True,
                "preview_only": True,
                "error": str(exc),
                "motion_sequence": [],
            }

        self.last_preview = preview
        self._publish_status(preview)
        self.get_logger().info("Published dry-run motion preview status.")

    def _execute_real_target(self, target: Dict[str, Any]) -> Dict[str, Any]:
        if not self.allow_real_motion:
            return {
                "source": "vision_pick_place_node",
                "accepted": False,
                "executed": False,
                "reason": "allow_real_motion=false; real robot motion is disabled",
            }
        if self.dry_run or bool(target.get("dry_run", True)):
            return {
                "source": "vision_pick_place_node",
                "accepted": False,
                "executed": False,
                "reason": "dry_run=true; real robot motion is disabled",
            }
        if not bool(target.get("confirm_real_motion", False)):
            return {
                "source": "vision_pick_place_node",
                "accepted": False,
                "executed": False,
                "reason": "confirm_real_motion=true is required",
            }

        sequence = build_real_motion_sequence(
            target,
            self.safety_guard,
            tool_type=target.get("tool_type", self.tool_type),
        )
        executor = HTTPMotionExecutor(
            self.web_api_base_url,
            velocity_ratio=float(target.get("velocity_ratio", self.velocity_ratio)),
            acceleration_ratio=float(
                target.get("acceleration_ratio", self.acceleration_ratio)
            ),
            tool_type=str(target.get("tool_type", self.tool_type)),
        )
        execution_log = executor.execute(sequence)
        return {
            "source": "vision_pick_place_node",
            "accepted": True,
            "executed": True,
            "transport": "http_api",
            "motion_sequence": sequence,
            "execution_log": execution_log,
        }

    def _extract_target(self, payload: str) -> Dict[str, Any]:
        try:
            data = json.loads(payload)
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError:
            pass

        pose = self._extract_pose(payload)
        if not pose:
            raise ValueError("robot target payload must be JSON or contain [x, y, z, r]")
        return {
            "selected": True,
            "dry_run": True,
            "robot_xy": pose[:2],
            "pick_pose": pose,
            "place_pose": [pose[0], pose[1], pose[2], pose[3]],
        }

    def _extract_pose(self, payload: str):
        start = payload.find("[")
        end = payload.find("]", start)
        if start == -1 or end == -1:
            return []
        try:
            value = ast.literal_eval(payload[start : end + 1])
        except (SyntaxError, ValueError):
            return []
        if not isinstance(value, list):
            return []
        return [float(item) for item in value]

    def _publish_status(self, payload):
        msg = String()
        msg.data = json.dumps(payload, separators=(",", ":"))
        self.status_publisher.publish(msg)

    def _log_status(self):
        self.get_logger().info(
            "Vision pick-and-place preview idle in dry-run mode. "
            "Hardware command path disabled."
        )


def main(args=None):
    rclpy.init(args=args)
    node = VisionPickPlaceNode()
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
