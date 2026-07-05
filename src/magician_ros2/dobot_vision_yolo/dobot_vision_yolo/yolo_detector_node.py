import json
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

import rclpy
from ament_index_python.packages import PackageNotFoundError
from ament_index_python.packages import get_package_share_directory
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import String

try:
    import cv2
except ImportError:  # pragma: no cover - depends on target image
    cv2 = None

try:
    import numpy as np
except ImportError:  # pragma: no cover - depends on target image
    np = None

try:
    import yaml
except ImportError:  # pragma: no cover - config falls back to built-in defaults
    yaml = None


PACKAGE_NAME = "dobot_vision_yolo"
DEFAULT_ANNOTATED_IMAGE_PATH = "/tmp/dobot_vision_annotated.jpg"
ULTRALYTICS_INSTALL_HINT = (
    "Install ultralytics with: python3 -m pip install --user ultralytics"
)


BUILTIN_DEFAULTS = {
    "model_path": "models/best.engine",
    "fallback_model_path": "models/best.pt",
    "prefer_tensorrt": True,
    "precision": "fp16",
    "device": "cuda",
    "imgsz": 640,
    "camera_device": "/dev/video0",
    "http_snapshot_url": "http://127.0.0.1:8080/api/snapshot",
    "source_type": "camera",
    "detections_topic": "/dobot_vision/detections",
    "status_topic": "/dobot_vision/status",
    "detect_once_command_topic": "/dobot_vision/detect_once",
    "confidence_threshold": 0.70,
    "detect_fps": 10.0,
    "image_width": 640,
    "image_height": 480,
    "dry_run": True,
    "detect_only": True,
    "annotated_image_path": DEFAULT_ANNOTATED_IMAGE_PATH,
}


def _package_share_path():
    try:
        return Path(get_package_share_directory(PACKAGE_NAME))
    except PackageNotFoundError:
        return None


def _source_package_path():
    return Path(__file__).resolve().parents[1]


def _read_config_defaults():
    defaults = dict(BUILTIN_DEFAULTS)
    if yaml is None:
        return defaults

    candidates = []
    share_path = _package_share_path()
    if share_path is not None:
        candidates.append(share_path / "config" / "yolo.yaml")
    candidates.append(_source_package_path() / "config" / "yolo.yaml")

    for path in candidates:
        if not path.exists():
            continue
        with path.open("r", encoding="utf-8") as stream:
            config = yaml.safe_load(stream) or {}
        node_config = config.get("yolo_detector_node", {})
        ros_parameters = node_config.get("ros__parameters", {})
        defaults.update(ros_parameters)
        defaults["config_path"] = str(path)
        return defaults

    return defaults


class YoloDetectorNode(Node):
    def __init__(self):
        super().__init__("yolo_detector_node")
        self.config_defaults = _read_config_defaults()
        self._declare_parameters()

        self.dry_run = self._get_bool("dry_run")
        self.detect_only = self._get_bool("detect_only")
        self.source_type = self._get_string("source_type").lower()
        self.camera_device = self._get_string("camera_device")
        self.http_snapshot_url = self._get_string("http_snapshot_url")
        self.model_path = self._get_string("model_path")
        self.fallback_model_path = self._get_string("fallback_model_path")
        self.prefer_tensorrt = self._get_bool("prefer_tensorrt")
        self.precision = self._get_string("precision").lower()
        self.device = self._get_string("device")
        self.imgsz = self._get_int("imgsz")
        self.confidence_threshold = self._get_float("confidence_threshold")
        self.detect_fps = max(self._get_float("detect_fps"), 0.1)
        self.image_width = self._get_int("image_width")
        self.image_height = self._get_int("image_height")
        self.annotated_image_path = self._get_string("annotated_image_path")
        self.detect_once_command_topic = self._get_string("detect_once_command_topic")

        detections_topic = self._get_string("detections_topic")
        status_topic = self._get_string("status_topic")
        self.detections_publisher = self.create_publisher(String, detections_topic, 10)
        self.status_publisher = self.create_publisher(String, status_topic, 10)
        self.command_subscription = self.create_subscription(
            String,
            self.detect_once_command_topic,
            self._detect_once_command_callback,
            10,
        )

        self.model = None
        self.model_loaded = False
        self.model_error = ""
        self.active_model_path = ""
        self.frame_count = 0
        self.inference_count = 0
        self.last_detection_count = 0
        self.last_fps = 0.0
        self.last_error = ""
        self.last_source_ok = False
        self.capture = None
        self.last_inference_time = time.monotonic()
        self.last_status_log_time = 0.0
        self.last_source_warning_time = 0.0
        self.next_source_retry_time = 0.0
        self.detect_once_requested = False
        self.detect_once_request_count = 0
        self.last_detect_once_command = None

        self._load_model()
        self._write_placeholder_image("Starting Dobot vision detector")

        period = 1.0 / self.detect_fps
        self.timer = self.create_timer(period, self._detect_once)
        self.get_logger().info(
            "YOLO detector node started in detect-only mode. dry_run=%s, "
            "source_type=%s, detections_topic=%s, status_topic=%s, command_topic=%s"
            % (
                self.dry_run,
                self.source_type,
                detections_topic,
                status_topic,
                self.detect_once_command_topic,
            )
        )
        self.get_logger().info(
            "Config loaded from: %s"
            % self.config_defaults.get("config_path", "built-in defaults")
        )

    def _detect_once_command_callback(self, msg):
        try:
            command = json.loads(msg.data)
        except json.JSONDecodeError:
            command = {"raw": msg.data}

        if not bool(command.get("dry_run", True)):
            self.get_logger().warn("Rejected detect_once command because dry_run=false")
            return

        self.detect_once_requested = True
        self.detect_once_request_count += 1
        self.last_detect_once_command = command
        self.get_logger().info(
            "Received dry-run detect_once request #%d"
            % self.detect_once_request_count
        )

    def _declare_parameters(self):
        for name, default in self.config_defaults.items():
            if name == "config_path":
                continue
            self.declare_parameter(name, default)

    def _get_bool(self, name):
        return bool(self.get_parameter(name).value)

    def _get_float(self, name):
        return float(self.get_parameter(name).value)

    def _get_int(self, name):
        return int(self.get_parameter(name).value)

    def _get_string(self, name):
        return str(self.get_parameter(name).value)

    def _load_model(self):
        if cv2 is None or np is None:
            self.model_error = (
                "OpenCV and numpy are required for camera/snapshot detection. "
                "Install ROS/OpenCV packages such as python3-opencv and python3-numpy."
            )
            self.get_logger().error(self.model_error)
            return

        resolved_path, message = self._resolve_model_path()
        if resolved_path is None:
            self.model_error = message
            self.get_logger().error(self.model_error)
            return

        if resolved_path.suffix.lower() not in [".pt", ".engine"]:
            self.model_error = (
                "Unsupported model extension '%s'. Use .pt or .engine."
                % resolved_path.suffix
            )
            self.get_logger().error(self.model_error)
            return

        try:
            from ultralytics import YOLO
        except ImportError:
            self.model_error = "ultralytics is not installed. %s" % ULTRALYTICS_INSTALL_HINT
            self.get_logger().error(self.model_error)
            return

        try:
            self.model = YOLO(str(resolved_path))
            self.model_loaded = True
            self.active_model_path = str(resolved_path)
            self.model_error = ""
            self.get_logger().info(
                "Loaded YOLO model: %s (prefer_tensorrt=%s, device=%s, imgsz=%d, precision=%s)"
                % (
                    self.active_model_path,
                    self.prefer_tensorrt,
                    self.device,
                    self.imgsz,
                    self.precision,
                )
            )
        except Exception as exc:  # pragma: no cover - depends on model/runtime
            self.model_error = "Failed to load YOLO model '%s': %s" % (
                resolved_path,
                exc,
            )
            self.get_logger().error(self.model_error)

    def _resolve_model_path(self):
        checked = []
        configured_paths = [self.model_path, self.fallback_model_path]
        if not self.prefer_tensorrt:
            configured_paths = [self.fallback_model_path, self.model_path]

        for configured_path in configured_paths:
            if not configured_path:
                continue
            for candidate in self._model_path_candidates(configured_path):
                checked.append(str(candidate))
                if candidate.exists() and candidate.is_file():
                    if candidate.suffix.lower() == ".pt" and self.prefer_tensorrt:
                        self.get_logger().warn(
                            "TensorRT engine not found; falling back to PyTorch .pt model: %s"
                            % candidate
                        )
                    return candidate, ""

        return (
            None,
            "YOLO model not found. Checked: %s. Place best.engine or best.pt "
            "under src/magician_ros2/dobot_vision_yolo/models/ and rebuild, "
            "or pass an absolute model_path parameter." % ", ".join(checked),
        )

    def _model_path_candidates(self, configured_path):
        path = Path(configured_path).expanduser()
        if path.is_absolute():
            return [path]

        candidates = []
        share_path = _package_share_path()
        if share_path is not None:
            candidates.append(share_path / path)
        source_path = _source_package_path()
        candidates.append(source_path / path)
        candidates.append(Path.cwd() / path)
        return candidates

    def _detect_once(self):
        loop_started = time.monotonic()
        had_detect_once_request = self.detect_once_requested
        frame = self._read_frame()
        if frame is None:
            self._publish_empty_detections()
            self._publish_status()
            if had_detect_once_request:
                self.detect_once_requested = False
            return

        detections = []
        annotated = frame.copy()
        if self.model_loaded:
            detections, annotated = self._run_inference(frame)
        else:
            self.last_error = self.model_error
            self._draw_text(annotated, "NO MODEL: see /dobot_vision/status")
            self.last_fps = 1.0 / max(time.monotonic() - loop_started, 1e-6)

        self._save_annotated_image(annotated)
        self._publish_detections(detections)
        self._publish_status()
        if had_detect_once_request:
            self.detect_once_requested = False

    def _read_frame(self):
        if cv2 is None or np is None:
            self.last_error = "OpenCV or numpy is unavailable"
            self.last_source_ok = False
            return None

        if self.source_type == "camera":
            return self._read_camera_frame()
        if self.source_type in ["http_snapshot", "snapshot", "http"]:
            return self._read_http_snapshot()

        self.last_error = (
            "Unsupported source_type '%s'. Use 'camera' or 'http_snapshot'."
            % self.source_type
        )
        self.last_source_ok = False
        self._write_placeholder_image(self.last_error)
        self.get_logger().error(self.last_error)
        return None

    def _read_camera_frame(self):
        now = time.monotonic()
        capture_closed = self.capture is None or not self.capture.isOpened()
        if capture_closed and now < self.next_source_retry_time:
            return None

        if capture_closed:
            self.capture = cv2.VideoCapture(self.camera_device, cv2.CAP_V4L2)
            if not self.capture.isOpened():
                self.capture.release()
                self.capture = None
                self.last_error = "Unable to open camera_device '%s'" % self.camera_device
                self.last_source_ok = False
                self.next_source_retry_time = time.monotonic() + 2.0
                self._write_placeholder_image(self.last_error)
                self._warn_source(self.last_error)
                return None
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.image_width)
            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.image_height)
            self.get_logger().info("Opened camera_device: %s" % self.camera_device)

        ok, frame = self.capture.read()
        if not ok or frame is None:
            self.last_error = "Failed to read camera frame from '%s'" % self.camera_device
            self.last_source_ok = False
            self._warn_source(self.last_error)
            return None

        self.last_error = ""
        self.last_source_ok = True
        self.frame_count += 1
        return self._resize_frame(frame)

    def _read_http_snapshot(self):
        now = time.monotonic()
        if now < self.next_source_retry_time:
            return None

        try:
            with urlopen(self.http_snapshot_url, timeout=1.5) as response:
                data = response.read()
        except (OSError, URLError) as exc:
            self.last_error = "Failed to read http_snapshot_url '%s': %s" % (
                self.http_snapshot_url,
                exc,
            )
            self.last_source_ok = False
            self.next_source_retry_time = time.monotonic() + 2.0
            self._write_placeholder_image(self.last_error)
            self._warn_source(self.last_error)
            return None

        buffer = np.frombuffer(data, dtype=np.uint8)
        frame = cv2.imdecode(buffer, cv2.IMREAD_COLOR)
        if frame is None:
            self.last_error = "Snapshot response is not a decodable image"
            self.last_source_ok = False
            self.next_source_retry_time = time.monotonic() + 2.0
            self._warn_source(self.last_error)
            return None

        self.last_error = ""
        self.last_source_ok = True
        self.frame_count += 1
        return self._resize_frame(frame)

    def _resize_frame(self, frame):
        if self.image_width > 0 and self.image_height > 0:
            return cv2.resize(frame, (self.image_width, self.image_height))
        return frame

    def _run_inference(self, frame):
        started = time.monotonic()
        try:
            predict_kwargs = {
                "conf": self.confidence_threshold,
                "verbose": False,
                "imgsz": self.imgsz,
            }
            if self.device:
                predict_kwargs["device"] = self.device
            if (
                self.precision == "fp16"
                and self.active_model_path
                and not self.active_model_path.endswith(".engine")
            ):
                predict_kwargs["half"] = True
            results = self.model(frame, **predict_kwargs)
        except Exception as exc:  # pragma: no cover - depends on model/runtime
            self.last_error = "YOLO inference failed: %s" % exc
            self.get_logger().error(self.last_error)
            self._draw_text(frame, self.last_error)
            return [], frame

        elapsed = max(time.monotonic() - started, 1e-6)
        self.last_fps = 1.0 / elapsed
        self.inference_count += 1

        result = results[0]
        detections = self._detections_from_result(result)
        annotated = result.plot()
        self.last_error = ""
        self.get_logger().info(
            "Detection frame=%d fps=%.2f objects=%d"
            % (self.frame_count, self.last_fps, len(detections))
        )
        for detection in detections:
            self.get_logger().info(
                "Detected %s confidence=%.2f bbox=%s center_pixel=%s"
                % (
                    detection["class_name"],
                    detection["confidence"],
                    detection["bbox"],
                    detection["center_pixel"],
                )
            )
        return detections, annotated

    def _detections_from_result(self, result):
        detections = []
        boxes = getattr(result, "boxes", None)
        if boxes is None:
            return detections

        names = getattr(result, "names", None) or getattr(self.model, "names", {})
        for index, box in enumerate(boxes, start=1):
            xyxy = box.xyxy[0].tolist()
            x1, y1, x2, y2 = [int(round(value)) for value in xyxy]
            confidence = float(box.conf[0])
            class_id = int(box.cls[0])
            class_name = str(names.get(class_id, class_id))
            detections.append(
                {
                    "id": index,
                    "class_name": class_name,
                    "confidence": round(confidence, 4),
                    "bbox": [x1, y1, x2, y2],
                    "center_pixel": [
                        int(round((x1 + x2) / 2.0)),
                        int(round((y1 + y2) / 2.0)),
                    ],
                }
            )
        return detections

    def _publish_empty_detections(self):
        self._publish_detections([])

    def _publish_detections(self, detections):
        self.last_detection_count = len(detections)
        payload = {
            "stamp": self.get_clock().now().nanoseconds / 1e9,
            "detections": detections,
        }
        msg = String()
        msg.data = json.dumps(payload, separators=(",", ":"))
        self.detections_publisher.publish(msg)

    def _publish_status(self):
        payload = {
            "stamp": self.get_clock().now().nanoseconds / 1e9,
            "node": "yolo_detector_node",
            "dry_run": self.dry_run,
            "detect_only": self.detect_only,
            "source_type": self.source_type,
            "source_ok": self.last_source_ok,
            "model_loaded": self.model_loaded,
            "model_path": self.active_model_path,
            "configured_model_path": self.model_path,
            "fallback_model_path": self.fallback_model_path,
            "prefer_tensorrt": self.prefer_tensorrt,
            "precision": self.precision,
            "device": self.device,
            "imgsz": self.imgsz,
            "model_error": self.model_error,
            "last_error": self.last_error,
            "confidence_threshold": self.confidence_threshold,
            "fps": round(self.last_fps, 2),
            "frame_count": self.frame_count,
            "inference_count": self.inference_count,
            "detection_count": self.last_detection_count,
            "detect_once_request_count": self.detect_once_request_count,
            "last_detect_once_command": self.last_detect_once_command,
            "detect_once_pending": self.detect_once_requested,
            "annotated_image_path": self.annotated_image_path,
        }
        msg = String()
        msg.data = json.dumps(payload, separators=(",", ":"))
        self.status_publisher.publish(msg)
        self._log_status(payload)

    def _log_status(self, payload):
        now = time.monotonic()
        if now - self.last_status_log_time < 2.0:
            return
        self.last_status_log_time = now
        self.get_logger().info(
            "Status fps=%.2f source_ok=%s model_loaded=%s detections=%d error=%s"
            % (
                payload["fps"],
                payload["source_ok"],
                payload["model_loaded"],
                payload["detection_count"],
                payload["last_error"] or payload["model_error"] or "none",
            )
        )

    def _warn_source(self, message):
        now = time.monotonic()
        if now - self.last_source_warning_time < 2.0:
            return
        self.last_source_warning_time = now
        self.get_logger().warn(message)

    def _save_annotated_image(self, image):
        if cv2 is None:
            return
        ok = cv2.imwrite(self.annotated_image_path, image)
        if not ok:
            self.get_logger().warn(
                "Failed to write annotated image: %s" % self.annotated_image_path
            )

    def _write_placeholder_image(self, text):
        if cv2 is None or np is None:
            return
        image = np.full(
            (max(self.image_height, 240), max(self.image_width, 320), 3),
            32,
            dtype=np.uint8,
        )
        self._draw_text(image, text)
        self._save_annotated_image(image)

    def _draw_text(self, image, text):
        if cv2 is None:
            return
        safe_text = text[:80]
        cv2.putText(
            image,
            safe_text,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2,
            cv2.LINE_AA,
        )

    def destroy_node(self):
        if self.capture is not None:
            self.capture.release()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = YoloDetectorNode()
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
