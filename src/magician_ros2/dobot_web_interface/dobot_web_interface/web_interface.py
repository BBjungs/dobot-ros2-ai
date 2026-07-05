import threading
import time
import json
import subprocess
from pathlib import Path

import cv2
import numpy as np
import rclpy
from cv_bridge import CvBridge
from dobot_msgs.action import PointToPoint
from dobot_msgs.srv import ExecuteHomingProcedure, GripperControl, SuctionCupControl
from fastapi import FastAPI, HTTPException, Request
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import HTMLResponse, Response, StreamingResponse
from fastapi.staticfiles import StaticFiles
from rclpy.action import ActionClient
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage, Image
import uvicorn
from sensor_msgs.msg import JointState
from std_msgs.msg import String

try:
    from dobot_vision_yolo.camera_calibration_tool import CalibrationError
    from dobot_vision_yolo.camera_calibration_tool import CalibrationStore
except ImportError:
    CalibrationError = ValueError
    CalibrationStore = None

try:
    from dobot_vision_yolo.target_selector_node import PlaceStore
    from dobot_vision_yolo.target_selector_node import TargetSelectionError
    from dobot_vision_yolo.target_selector_node import classes_from_detections
    from dobot_vision_yolo.target_selector_node import load_configured_classes
    from dobot_vision_yolo.target_selector_node import select_target_from_detections
except ImportError:
    PlaceStore = None
    TargetSelectionError = ValueError
    classes_from_detections = None
    load_configured_classes = None
    select_target_from_detections = None

try:
    from dobot_vision_yolo.safety_guard import SafetyGuard
    from dobot_vision_yolo.safety_guard import load_safety_config
except ImportError:
    SafetyGuard = None
    load_safety_config = None

try:
    from dobot_vision_yolo.vision_pick_place_node import HTTPMotionExecutor
    from dobot_vision_yolo.vision_pick_place_node import build_motion_sequence
    from dobot_vision_yolo.vision_pick_place_node import build_real_motion_sequence
except ImportError:
    HTTPMotionExecutor = None
    build_motion_sequence = None
    build_real_motion_sequence = None


class DobotWebNode(Node):
    def __init__(self):
        super().__init__('dobot_web_interface')

        self.declare_parameter('host', '0.0.0.0')
        self.declare_parameter('port', 8080)
        self.declare_parameter('camera_raw_topic', '/camera/color/image_raw')
        self.declare_parameter('camera_compressed_topic', '/camera/color/image_raw/compressed')
        self.declare_parameter('camera_device', '/dev/video0')
        self.declare_parameter('camera_width', 1280)
        self.declare_parameter('camera_height', 720)
        self.declare_parameter('camera_fps', 15.0)
        self.declare_parameter('stream_fps', 12.0)
        self.declare_parameter('jpeg_quality', 80)
        self.declare_parameter('vision_status_topic', '/dobot_vision/status')
        self.declare_parameter('vision_detections_topic', '/dobot_vision/detections')
        self.declare_parameter('vision_detect_once_topic', '/dobot_vision/detect_once')
        self.declare_parameter('vision_annotated_path', '/tmp/dobot_vision_annotated.jpg')
        self.declare_parameter('vision_calibration_path', '')
        self.declare_parameter('vision_place_positions_path', '')
        self.declare_parameter('vision_workspace_path', '')
        self.declare_parameter('vision_yolo_config_path', '')
        self.declare_parameter(
            'vision_selected_target_topic',
            '/dobot_vision_yolo/selected_target',
        )

        self.host = str(self.get_parameter('host').value)
        self.port = int(self.get_parameter('port').value)
        self.camera_raw_topic = str(self.get_parameter('camera_raw_topic').value)
        self.camera_compressed_topic = str(
            self.get_parameter('camera_compressed_topic').value
        )
        self.camera_device = str(self.get_parameter('camera_device').value)
        self.camera_width = int(self.get_parameter('camera_width').value)
        self.camera_height = int(self.get_parameter('camera_height').value)
        self.camera_fps = float(self.get_parameter('camera_fps').value)
        self.stream_fps = float(self.get_parameter('stream_fps').value)
        self.jpeg_quality = int(self.get_parameter('jpeg_quality').value)
        self.vision_status_topic = str(self.get_parameter('vision_status_topic').value)
        self.vision_detections_topic = str(
            self.get_parameter('vision_detections_topic').value
        )
        self.vision_detect_once_topic = str(
            self.get_parameter('vision_detect_once_topic').value
        )
        self.vision_annotated_path = Path(
            str(self.get_parameter('vision_annotated_path').value)
        )
        self.vision_calibration_path = str(
            self.get_parameter('vision_calibration_path').value
        )
        self.vision_place_positions_path = str(
            self.get_parameter('vision_place_positions_path').value
        )
        self.vision_workspace_path = str(
            self.get_parameter('vision_workspace_path').value
        )
        self.vision_yolo_config_path = str(
            self.get_parameter('vision_yolo_config_path').value
        )
        self.vision_selected_target_topic = str(
            self.get_parameter('vision_selected_target_topic').value
        )

        self.bridge = CvBridge()
        self._frame_condition = threading.Condition()
        self._latest_jpeg = None
        self._latest_frame_time = None
        self._latest_frame_source = None
        self._placeholder_jpeg = self._make_placeholder()
        self._capture_stop = threading.Event()
        self._capture_thread = None
        self._direct_camera_connected = False

        self._goal_lock = threading.Lock()
        self._active_goal_handle = None
        self._last_feedback = None
        self._last_result = None
        self._last_goal_time = None
        self._latest_joints_deg = None
        self._homing_confirmed = False
        self._vision_lock = threading.Lock()
        self._vision_status = None
        self._vision_status_time = None
        self._vision_detections = None
        self._vision_detections_time = None
        self._vision_last_command = None
        self._vision_selected_target = None
        self._calibration_store = (
            CalibrationStore(self.vision_calibration_path)
            if CalibrationStore is not None
            else None
        )
        self._place_store = (
            PlaceStore(self.vision_place_positions_path)
            if PlaceStore is not None
            else None
        )
        self._safety_guard = self._make_safety_guard()

        self.ptp_action = ActionClient(self, PointToPoint, 'PTP_action')
        self.homing_client = self.create_client(
            ExecuteHomingProcedure, 'dobot_homing_service'
        )
        self.gripper_client = self.create_client(GripperControl, 'dobot_gripper_service')
        self.suction_client = self.create_client(
            SuctionCupControl, 'dobot_suction_cup_service'
        )

        self.create_subscription(
            Image,
            self.camera_raw_topic,
            self._raw_image_callback,
            10,
        )
        self.create_subscription(
            CompressedImage,
            self.camera_compressed_topic,
            self._compressed_image_callback,
            10,
        )
        self.create_subscription(
            JointState,
            'dobot_joint_states',
            self._joint_state_callback,
            10,
        )
        self.create_subscription(
            String,
            self.vision_status_topic,
            self._vision_status_callback,
            10,
        )
        self.create_subscription(
            String,
            self.vision_detections_topic,
            self._vision_detections_callback,
            10,
        )
        self.vision_detect_once_publisher = self.create_publisher(
            String,
            self.vision_detect_once_topic,
            10,
        )
        self.vision_selected_target_publisher = self.create_publisher(
            String,
            self.vision_selected_target_topic,
            10,
        )

        self.get_logger().info(
            f'Web interface will listen on http://{self.host}:{self.port}'
        )
        self.get_logger().info(
            f'Camera topics: {self.camera_raw_topic}, {self.camera_compressed_topic}'
        )
        self.get_logger().info(
            'Vision topics: '
            f'{self.vision_status_topic}, {self.vision_detections_topic}, '
            f'{self.vision_detect_once_topic}'
        )
        if self._calibration_store is not None:
            self.get_logger().info(
                f'Vision calibration config: {self._calibration_store.path}'
            )
        if self._place_store is not None:
            self.get_logger().info(f'Vision place config: {self._place_store.path}')
        if self._safety_guard is not None:
            self.get_logger().info(
                f'Vision safety config: {self._safety_guard.config.as_dict()}'
            )
        if self.camera_device:
            self._capture_thread = threading.Thread(
                target=self._capture_device_loop,
                name='dobot_web_camera_capture',
                daemon=True,
            )
            self._capture_thread.start()
            self.get_logger().info(f'Direct camera device: {self.camera_device}')

    def _make_safety_guard(self):
        if SafetyGuard is None or load_safety_config is None:
            return None
        try:
            config = load_safety_config(self.vision_workspace_path)
        except Exception as exc:
            self.get_logger().warn(f'Failed to load vision safety config: {exc}')
            config = load_safety_config('')
        return SafetyGuard(
            workspace=config.workspace,
            dry_run=config.dry_run_default,
            config=config,
        )

    def _make_placeholder(self):
        image = np.full((540, 960, 3), (28, 31, 36), dtype=np.uint8)
        cv2.putText(
            image,
            'Waiting for camera frame',
            (250, 270),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.1,
            (222, 226, 230),
            2,
            cv2.LINE_AA,
        )
        ok, data = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 82])
        if not ok:
            return b''
        return data.tobytes()

    def _raw_image_callback(self, msg):
        try:
            if msg.encoding == 'mono8':
                cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='mono8')
            else:
                cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            self._store_cv_image(cv_image, self.camera_raw_topic)
        except Exception as exc:
            self.get_logger().warn(f'Failed to convert raw camera frame: {exc}')

    def _compressed_image_callback(self, msg):
        try:
            if 'jpeg' in msg.format.lower() or 'jpg' in msg.format.lower():
                self._store_jpeg(bytes(msg.data), self.camera_compressed_topic)
                return

            buffer = np.frombuffer(msg.data, dtype=np.uint8)
            cv_image = cv2.imdecode(buffer, cv2.IMREAD_COLOR)
            if cv_image is None:
                raise ValueError('cv2.imdecode returned no image')
            self._store_cv_image(cv_image, self.camera_compressed_topic)
        except Exception as exc:
            self.get_logger().warn(f'Failed to convert compressed camera frame: {exc}')

    def _store_cv_image(self, cv_image, source):
        ok, data = cv2.imencode(
            '.jpg',
            cv_image,
            [cv2.IMWRITE_JPEG_QUALITY, self.jpeg_quality],
        )
        if ok:
            self._store_jpeg(data.tobytes(), source)

    def _store_jpeg(self, jpeg_bytes, source):
        with self._frame_condition:
            self._latest_jpeg = jpeg_bytes
            self._latest_frame_time = time.monotonic()
            self._latest_frame_source = source
            self._frame_condition.notify_all()

    def _joint_state_callback(self, msg):
        if len(msg.position) < 4:
            return

        with self._goal_lock:
            self._latest_joints_deg = [
                round(float(np.degrees(value)), 2)
                for value in msg.position[:4]
            ]

    def _vision_status_callback(self, msg):
        payload = self._parse_json_message(msg.data, 'vision status')
        with self._vision_lock:
            self._vision_status = payload
            self._vision_status_time = time.monotonic()

    def _vision_detections_callback(self, msg):
        payload = self._parse_json_message(msg.data, 'vision detections')
        with self._vision_lock:
            self._vision_detections = payload
            self._vision_detections_time = time.monotonic()

    def _parse_json_message(self, data, label):
        try:
            payload = json.loads(data)
            if isinstance(payload, dict):
                return payload
            raise ValueError('JSON payload must be an object')
        except Exception as exc:
            self.get_logger().warn(f'Invalid {label} JSON: {exc}')
            return {
                'error': f'Invalid {label} JSON: {exc}',
                'raw': data,
            }

    def _capture_device_loop(self):
        warn_after = 0.0
        frame_delay = 1.0 / max(self.camera_fps, 1.0)

        while not self._capture_stop.is_set():
            capture = cv2.VideoCapture(self.camera_device, cv2.CAP_V4L2)
            if not capture.isOpened():
                self._direct_camera_connected = False
                now = time.monotonic()
                if now >= warn_after:
                    self.get_logger().warn(
                        f'Unable to open camera device {self.camera_device}'
                    )
                    warn_after = now + 5.0
                self._capture_stop.wait(2.0)
                continue

            self._direct_camera_connected = True
            capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
            capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.camera_width)
            capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.camera_height)
            capture.set(cv2.CAP_PROP_FPS, self.camera_fps)
            self.get_logger().info(
                f'Camera device opened: {self.camera_device} '
                f'{self.camera_width}x{self.camera_height}@{self.camera_fps:g}'
            )

            try:
                while not self._capture_stop.is_set():
                    started = time.monotonic()
                    ok, frame = capture.read()
                    if not ok or frame is None:
                        self._direct_camera_connected = False
                        self.get_logger().warn('Camera frame capture failed')
                        break

                    self._store_cv_image(frame, self.camera_device)
                    elapsed = time.monotonic() - started
                    self._capture_stop.wait(max(frame_delay - elapsed, 0.0))
            finally:
                capture.release()

            self._capture_stop.wait(1.0)

    def get_frame(self, wait_timeout=1.0):
        with self._frame_condition:
            if self._latest_jpeg is None:
                self._frame_condition.wait(timeout=wait_timeout)
            return self._latest_jpeg or self._placeholder_jpeg

    def status(self):
        with self._frame_condition:
            frame_age = None
            if self._latest_frame_time is not None:
                frame_age = round(time.monotonic() - self._latest_frame_time, 2)
            frame_source = self._latest_frame_source

        with self._goal_lock:
            active_goal = self._active_goal_handle is not None
            last_feedback = self._last_feedback
            last_result = self._last_result
            joints_deg = self._latest_joints_deg
            homing_confirmed = self._homing_confirmed
            last_goal_age = None
            if self._last_goal_time is not None:
                last_goal_age = round(time.monotonic() - self._last_goal_time, 2)

        return {
            'camera': {
                'raw_topic': self.camera_raw_topic,
                'compressed_topic': self.camera_compressed_topic,
                'device': self.camera_device,
                'direct_camera_connected': self._direct_camera_connected,
                'frame_age_sec': frame_age,
                'frame_source': frame_source,
                'has_frame': frame_source is not None,
            },
            'ros': {
                'ptp_action_ready': self.ptp_action.server_is_ready(),
                'homing_ready': self.homing_client.service_is_ready(),
                'gripper_ready': self.gripper_client.service_is_ready(),
                'suction_ready': self.suction_client.service_is_ready(),
            },
            'motion': {
                'active_goal': active_goal,
                'last_goal_age_sec': last_goal_age,
                'last_feedback': last_feedback,
                'last_result': last_result,
                'joints_deg': joints_deg,
                'homing_confirmed': homing_confirmed,
            },
        }

    def vision_status(self):
        now = time.monotonic()
        with self._vision_lock:
            payload = dict(self._vision_status or {})
            received_at = self._vision_status_time
            last_command = self._vision_last_command

        if received_at is None:
            return {
                'ok': False,
                'detector_running': False,
                'error': 'Vision detector status has not been received.',
                'age_sec': None,
                'fps': 0.0,
                'model_path': '',
                'confidence_threshold': None,
                'dry_run': True,
                'detect_only': True,
                'source_type': '',
                'source_ok': False,
                'model_loaded': False,
                'last_command': last_command,
                'raw': {},
            }

        age_sec = round(now - received_at, 2)
        stale = age_sec > 5.0
        model_error = payload.get('model_error') or ''
        last_error = payload.get('last_error') or ''
        error = ''
        if stale:
            error = f'Vision detector status is stale ({age_sec}s old).'
        elif model_error:
            error = model_error
        elif last_error:
            error = last_error

        return {
            'ok': not stale and not error,
            'detector_running': not stale,
            'error': error,
            'age_sec': age_sec,
            'fps': float(payload.get('fps') or 0.0),
            'model_path': payload.get('model_path')
            or payload.get('configured_model_path')
            or '',
            'configured_model_path': payload.get('configured_model_path', ''),
            'fallback_model_path': payload.get('fallback_model_path', ''),
            'confidence_threshold': payload.get('confidence_threshold'),
            'dry_run': bool(payload.get('dry_run', True)),
            'detect_only': bool(payload.get('detect_only', True)),
            'source_type': payload.get('source_type', ''),
            'source_ok': bool(payload.get('source_ok', False)),
            'model_loaded': bool(payload.get('model_loaded', False)),
            'annotated_image_path': payload.get(
                'annotated_image_path',
                str(self.vision_annotated_path),
            ),
            'last_command': last_command,
            'raw': payload,
        }

    def vision_detections(self):
        now = time.monotonic()
        with self._vision_lock:
            payload = dict(self._vision_detections or {})
            received_at = self._vision_detections_time

        if received_at is None:
            return {
                'ok': False,
                'error': 'Vision detections have not been received.',
                'age_sec': None,
                'stamp': None,
                'detections': [],
            }

        age_sec = round(now - received_at, 2)
        stale = age_sec > 5.0
        detections = payload.get('detections', [])
        if not isinstance(detections, list):
            detections = []
        return {
            'ok': not stale and not payload.get('error'),
            'error': (
                f'Vision detections are stale ({age_sec}s old).'
                if stale
                else payload.get('error', '')
            ),
            'age_sec': age_sec,
            'stamp': payload.get('stamp'),
            'detections': detections,
            'raw': payload,
        }

    def vision_detect_once(self, payload):
        dry_run = bool(payload.get('dry_run', True))
        if not dry_run:
            raise ValueError('Vision detect_once is dry_run only in this phase')

        command = {
            'stamp': time.time(),
            'dry_run': True,
            'object_class': str(payload.get('object_class', 'all')),
            'place_id': str(payload.get('place_id', payload.get('place_position', ''))),
            'place_position': str(payload.get('place_position', 'staging')),
        }
        msg = String()
        msg.data = json.dumps(command, separators=(',', ':'))
        self.vision_detect_once_publisher.publish(msg)
        with self._vision_lock:
            self._vision_last_command = command

        return {
            'accepted': True,
            'dry_run': True,
            'message': 'Dry-run detect_once command published. No robot motion was sent.',
            'command': command,
            'status': self.vision_status(),
            'detections': self.vision_detections(),
        }

    def vision_classes(self):
        if classes_from_detections is None or load_configured_classes is None:
            raise ConnectionError('dobot_vision_yolo target selector tools are not available')

        detected = classes_from_detections(self.vision_detections().get('detections', []))
        configured = load_configured_classes(self.vision_yolo_config_path)
        return {
            'classes': sorted(set(configured + detected)),
            'configured_classes': configured,
            'detected_classes': detected,
        }

    def vision_places(self):
        return self._places().status()

    def vision_select_target(self, payload):
        result = self._select_target_preview_source(payload)
        with self._vision_lock:
            self._vision_selected_target = result

        if result.get('selected'):
            msg = String()
            msg.data = json.dumps(result, separators=(',', ':'))
            self.vision_selected_target_publisher.publish(msg)

        return result

    def _select_target_preview_source(self, payload):
        if select_target_from_detections is None:
            raise ConnectionError('dobot_vision_yolo target selector tools are not available')

        dry_run = bool(payload.get('dry_run', True))
        if not dry_run:
            raise ValueError('Vision target selection is dry_run only in this phase')

        detections = self.vision_detections()
        if not detections.get('ok'):
            raise ValueError(
                detections.get('error') or 'Vision detections are not available.'
            )

        image_size = (
            int(payload.get('image_width', 640)),
            int(payload.get('image_height', 480)),
        )
        result = select_target_from_detections(
            detections,
            payload,
            self._places(),
            self._calibration(),
            dry_run=True,
            image_size=image_size,
            min_confidence=float(payload.get('min_confidence', 0.0)),
            source='dobot_web_interface',
        )
        return result

    def vision_safety(self):
        return self._safety_report({})

    def vision_validate_pick(self, payload):
        if not isinstance(payload, dict):
            raise ValueError('validate_pick payload must be an object')
        return self._safety_report(payload)

    def vision_preview_pick(self, payload):
        if build_motion_sequence is None:
            raise ConnectionError('dobot_vision_yolo motion preview tools are not available')
        if not isinstance(payload, dict):
            raise ValueError('preview_pick payload must be an object')
        if not bool(payload.get('dry_run', True)):
            raise ValueError('Vision motion preview is dry_run only in this phase')

        selected_target = self._select_target_preview_source(payload)
        with self._vision_lock:
            self._vision_selected_target = selected_target

        if not selected_target.get('selected'):
            return {
                'accepted': False,
                'dry_run': True,
                'preview_only': True,
                'reason': selected_target.get('reason', 'No target selected'),
                'selected_target': selected_target,
                'motion_sequence': [],
            }

        safety = self._safety_report({
            'selected_target': selected_target,
            'dry_run': True,
        })
        if not safety.get('allowed'):
            return {
                'accepted': False,
                'dry_run': True,
                'preview_only': True,
                'reason': safety.get('reason', 'Safety validation failed'),
                'selected_target': selected_target,
                'safety': safety,
                'motion_sequence': [],
            }

        sequence = build_motion_sequence(selected_target, self._safety())
        return {
            'accepted': True,
            'dry_run': True,
            'preview_only': True,
            'message': 'Dry-run motion preview generated. No robot command was sent.',
            'selected_target': selected_target,
            'safety': safety,
            'motion_sequence': sequence,
        }

    def vision_pick_selected(self, payload):
        if HTTPMotionExecutor is None or build_real_motion_sequence is None:
            raise ConnectionError('dobot_vision_yolo real motion tools are not available')
        if not isinstance(payload, dict):
            raise ValueError('pick_selected payload must be an object')

        guard = self._safety()
        dry_run = self._payload_bool(payload.get('dry_run', True))
        confirm_real_motion = self._payload_bool(
            payload.get('confirm_real_motion', False)
        )

        if not guard.config.allow_real_motion:
            return {
                'accepted': False,
                'executed': False,
                'dry_run': dry_run,
                'reason': 'allow_real_motion=false; real robot motion is disabled',
            }
        if dry_run:
            return {
                'accepted': False,
                'executed': False,
                'dry_run': True,
                'reason': 'dry_run=true; real robot motion is disabled',
            }
        if not confirm_real_motion:
            return {
                'accepted': False,
                'executed': False,
                'dry_run': False,
                'reason': 'confirm_real_motion=true is required',
            }

        selection_payload = dict(payload)
        selection_payload['dry_run'] = True
        selected_target = self._select_target_preview_source(selection_payload)
        if not selected_target.get('selected'):
            return {
                'accepted': False,
                'executed': False,
                'dry_run': False,
                'reason': selected_target.get('reason', 'No target selected'),
                'selected_target': selected_target,
            }

        selected_target = dict(selected_target)
        selected_target['dry_run'] = False
        with self._vision_lock:
            self._vision_selected_target = selected_target

        safety = self._safety_report({
            'selected_target': selected_target,
            'dry_run': False,
        })
        if not safety.get('allowed'):
            return {
                'accepted': False,
                'executed': False,
                'dry_run': False,
                'reason': safety.get('reason', 'Safety validation failed'),
                'selected_target': selected_target,
                'safety': safety,
            }

        tool_type = str(payload.get('tool_type', 'suction')).lower()
        velocity_ratio = float(payload.get('velocity_ratio', 0.3))
        acceleration_ratio = float(payload.get('acceleration_ratio', 0.2))
        wait_after_tool_sec = float(payload.get('wait_after_tool_sec', 0.5))
        sequence = build_real_motion_sequence(
            selected_target,
            guard,
            tool_type=tool_type,
            wait_after_tool_sec=wait_after_tool_sec,
        )
        executor = HTTPMotionExecutor(
            self._local_api_base_url(),
            velocity_ratio=velocity_ratio,
            acceleration_ratio=acceleration_ratio,
            tool_type=tool_type,
        )
        execution_log = executor.execute(sequence)
        return {
            'accepted': True,
            'executed': True,
            'dry_run': False,
            'transport': 'http_api',
            'message': 'Real vision pick-and-place sequence executed via HTTP API.',
            'selected_target': selected_target,
            'safety': safety,
            'motion_sequence': sequence,
            'execution_log': execution_log,
            'velocity_ratio': velocity_ratio,
            'acceleration_ratio': acceleration_ratio,
            'tool_type': tool_type,
        }

    def vision_cancel(self):
        return self.cancel_move()

    def _local_api_base_url(self):
        host = self.host
        if host in ('0.0.0.0', '::', ''):
            host = '127.0.0.1'
        return f'http://{host}:{self.port}'

    @staticmethod
    def _payload_bool(value):
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.strip().lower() in ('1', 'true', 'yes', 'on')
        return bool(value)

    def _safety_report(self, payload):
        guard = self._safety()
        selected_target = payload.get('selected_target')
        if selected_target is None:
            with self._vision_lock:
                selected_target = self._vision_selected_target

        status = self.status()
        dry_run = payload.get('dry_run')
        if dry_run is None:
            if isinstance(selected_target, dict) and 'dry_run' in selected_target:
                dry_run = bool(selected_target.get('dry_run', True))
            else:
                dry_run = guard.config.dry_run_default

        place_status = self._places().status()
        return guard.validate_pick(
            selected_target=selected_target,
            camera_status=status.get('camera', {}),
            yolo_status=self.vision_status(),
            calibration_status=self.vision_calibration(),
            places=place_status.get('places', {}),
            dry_run=dry_run,
            robot_homed=status.get('motion', {}).get('homing_confirmed', False),
        )

    def get_vision_annotated(self):
        if self.vision_annotated_path.exists():
            return self.vision_annotated_path.read_bytes()
        return self._make_vision_placeholder()

    def vision_calibration(self):
        return self._calibration().status()

    def vision_calibration_add_point(self, payload):
        image_point = self._extract_image_point(payload)
        robot_point = self._extract_robot_point(payload)
        return self._calibration().add_point(image_point, robot_point)

    def vision_calibration_compute(self):
        return self._calibration().compute()

    def vision_calibration_test_point(self, payload):
        image_point = self._extract_image_point(payload)
        return self._calibration().test_point(image_point)

    def _calibration(self):
        if self._calibration_store is None:
            raise ConnectionError(
                'dobot_vision_yolo calibration tools are not available'
            )
        return self._calibration_store

    def _places(self):
        if self._place_store is None:
            raise ConnectionError(
                'dobot_vision_yolo target selector tools are not available'
            )
        return self._place_store

    def _safety(self):
        if self._safety_guard is None:
            raise ConnectionError(
                'dobot_vision_yolo safety guard tools are not available'
            )
        return self._safety_guard

    @staticmethod
    def _extract_image_point(payload):
        if 'pixel' in payload:
            return payload['pixel']
        if 'image_point' in payload:
            return payload['image_point']
        if 'u' in payload and 'v' in payload:
            return [payload['u'], payload['v']]
        raise ValueError('pixel, image_point, or u/v is required')

    @staticmethod
    def _extract_robot_point(payload):
        if 'robot_point' in payload:
            return payload['robot_point']
        if 'x' in payload and 'y' in payload:
            return [payload['x'], payload['y']]
        if 'robot_x' in payload and 'robot_y' in payload:
            return [payload['robot_x'], payload['robot_y']]
        raise ValueError('robot_point or robot_x/robot_y is required')

    def _make_vision_placeholder(self):
        image = np.full((480, 640, 3), (28, 31, 36), dtype=np.uint8)
        cv2.putText(
            image,
            'Vision detector offline',
            (130, 220),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255, 214, 120),
            2,
            cv2.LINE_AA,
        )
        cv2.putText(
            image,
            'Start yolo_detector_node in dry-run mode',
            (80, 265),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.58,
            (222, 226, 230),
            1,
            cv2.LINE_AA,
        )
        ok, data = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 82])
        if not ok:
            return b''
        return data.tobytes()

    def send_move(self, payload):
        target_pose = payload.get('target_pose')
        if not isinstance(target_pose, list) or len(target_pose) != 4:
            raise ValueError('target_pose must contain four numbers')

        goal = PointToPoint.Goal()
        goal.motion_type = int(payload.get('motion_type', 1))
        goal.target_pose = [float(value) for value in target_pose]
        goal.velocity_ratio = float(payload.get('velocity_ratio', 0.5))
        goal.acceleration_ratio = float(payload.get('acceleration_ratio', 0.3))

        if goal.motion_type not in [1, 2, 4, 5]:
            raise ValueError('motion_type must be one of 1, 2, 4, 5')
        if not 0.0 < goal.velocity_ratio <= 1.0:
            raise ValueError('velocity_ratio must be within (0.0, 1.0]')
        if not 0.0 < goal.acceleration_ratio <= 1.0:
            raise ValueError('acceleration_ratio must be within (0.0, 1.0]')

        with self._goal_lock:
            if self._active_goal_handle is not None:
                raise RuntimeError('A motion goal is already active')

        if not self.ptp_action.wait_for_server(timeout_sec=0.25):
            raise ConnectionError('PTP_action server is not available')

        future = self.ptp_action.send_goal_async(
            goal,
            feedback_callback=self._feedback_callback,
        )
        goal_handle = self._wait_for_future(future, 5.0)
        if not goal_handle.accepted:
            return {'accepted': False, 'message': 'Goal rejected'}

        with self._goal_lock:
            self._active_goal_handle = goal_handle
            self._last_goal_time = time.monotonic()
            self._last_result = None

        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self._result_callback)

        return {
            'accepted': True,
            'message': 'Goal accepted',
            'target_pose': list(goal.target_pose),
            'motion_type': goal.motion_type,
        }

    def cancel_move(self):
        with self._goal_lock:
            goal_handle = self._active_goal_handle

        if goal_handle is None:
            return {'requested': False, 'message': 'No active goal'}

        future = goal_handle.cancel_goal_async()
        response = self._wait_for_future(future, 5.0)
        return {
            'requested': True,
            'goals_canceling': len(response.goals_canceling),
        }

    def call_homing(self):
        if not self.homing_client.wait_for_service(timeout_sec=0.25):
            raise ConnectionError('dobot_homing_service is not available')
        response = self._wait_for_future(
            self.homing_client.call_async(ExecuteHomingProcedure.Request()),
            20.0,
        )
        with self._goal_lock:
            self._homing_confirmed = bool(response.success)
        return {
            'success': bool(response.success),
            'message': response.instruction,
        }

    def call_gripper(self, payload):
        if not self.gripper_client.wait_for_service(timeout_sec=0.25):
            raise ConnectionError('dobot_gripper_service is not available')
        state = str(payload.get('state', '')).lower()
        if state not in ['open', 'close']:
            raise ValueError('state must be open or close')

        request = GripperControl.Request()
        request.gripper_state = state
        request.keep_compressor_running = bool(
            payload.get('keep_compressor_running', False)
        )
        response = self._wait_for_future(self.gripper_client.call_async(request), 8.0)
        return {
            'success': bool(response.success),
            'message': response.message,
        }

    def call_suction(self, payload):
        if not self.suction_client.wait_for_service(timeout_sec=0.25):
            raise ConnectionError('dobot_suction_cup_service is not available')
        request = SuctionCupControl.Request()
        request.enable_suction = bool(payload.get('enable_suction', False))
        response = self._wait_for_future(self.suction_client.call_async(request), 8.0)
        return {
            'success': bool(response.success),
            'message': response.message,
        }

    def _feedback_callback(self, feedback_msg):
        feedback = [round(value, 3) for value in feedback_msg.feedback.current_pose]
        with self._goal_lock:
            self._last_feedback = feedback

    def _result_callback(self, future):
        try:
            result_msg = future.result()
            achieved_pose = [
                round(value, 3) for value in result_msg.result.achieved_pose
            ]
            result = {
                'status': int(result_msg.status),
                'achieved_pose': achieved_pose,
            }
        except Exception as exc:
            result = {
                'status': -1,
                'error': str(exc),
            }

        with self._goal_lock:
            self._last_result = result
            self._active_goal_handle = None

    def _wait_for_future(self, future, timeout_sec):
        done = threading.Event()
        future.add_done_callback(lambda _: done.set())
        if not done.wait(timeout=timeout_sec):
            raise TimeoutError('ROS call timed out')
        return future.result()

    def restart_connection(self):
        command = ['systemctl', '--user', 'restart', 'dobot-magician.service']

        def restart_later():
            time.sleep(0.4)
            try:
                subprocess.Popen(
                    command,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    close_fds=True,
                )
            except Exception as exc:
                self.get_logger().error(f'Failed to restart Dobot service: {exc}')

        threading.Thread(
            target=restart_later,
            name='dobot_service_restart',
            daemon=True,
        ).start()
        return {
            'accepted': True,
            'message': 'Dobot connection restart requested. Reconnect in a few seconds.',
            'command': ' '.join(command),
        }

    def shutdown(self):
        self._capture_stop.set()
        if self._capture_thread is not None:
            self._capture_thread.join(timeout=2.0)


def create_app(node):
    app = FastAPI(title='Dobot Web Interface')
    static_dir = Path(__file__).with_name('static')
    app.mount('/static', StaticFiles(directory=str(static_dir)), name='static')

    @app.get('/', response_class=HTMLResponse)
    def index():
        return (static_dir / 'index.html').read_text(encoding='utf-8')

    @app.get('/api/status')
    def api_status():
        return node.status()

    @app.get('/api/snapshot')
    def snapshot():
        return Response(content=node.get_frame(), media_type='image/jpeg')

    @app.get('/api/vision/status')
    def api_vision_status():
        return node.vision_status()

    @app.get('/api/vision/detections')
    def api_vision_detections():
        return node.vision_detections()

    @app.get('/api/vision/classes')
    def api_vision_classes():
        return _call_api(node.vision_classes)

    @app.get('/api/vision/places')
    def api_vision_places():
        return _call_api(node.vision_places)

    @app.get('/api/vision/safety')
    def api_vision_safety():
        return _call_api(node.vision_safety)

    @app.get('/api/vision/annotated')
    def api_vision_annotated():
        return Response(
            content=node.get_vision_annotated(),
            media_type='image/jpeg',
            headers={'Cache-Control': 'no-store'},
        )

    @app.get('/api/vision/calibration')
    def api_vision_calibration():
        return _call_api(node.vision_calibration)

    @app.get('/stream')
    def stream():
        def frames():
            delay = 1.0 / max(node.stream_fps, 1.0)
            while True:
                frame = node.get_frame()
                yield (
                    b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n'
                    + f'Content-Length: {len(frame)}\r\n\r\n'.encode('ascii')
                    + frame
                    + b'\r\n'
                )
                time.sleep(delay)

        return StreamingResponse(
            frames(),
            media_type='multipart/x-mixed-replace; boundary=frame',
        )

    @app.post('/api/move')
    async def api_move(request: Request):
        return _call_api(node.send_move, await request.json(), busy_status=409)

    @app.post('/api/cancel')
    def api_cancel():
        return _call_api(node.cancel_move)

    @app.post('/api/homing')
    def api_homing():
        return _call_api(node.call_homing)

    @app.post('/api/restart_connection')
    def api_restart_connection():
        return _call_api(node.restart_connection)

    @app.post('/api/gripper')
    async def api_gripper(request: Request):
        return _call_api(node.call_gripper, await request.json())

    @app.post('/api/suction')
    async def api_suction(request: Request):
        return _call_api(node.call_suction, await request.json())

    @app.post('/api/vision/detect_once')
    async def api_vision_detect_once(request: Request):
        return _call_api(node.vision_detect_once, await request.json())

    @app.post('/api/vision/select_target')
    async def api_vision_select_target(request: Request):
        return _call_api(node.vision_select_target, await request.json())

    @app.post('/api/vision/validate_pick')
    async def api_vision_validate_pick(request: Request):
        return _call_api(node.vision_validate_pick, await request.json())

    @app.post('/api/vision/preview_pick')
    async def api_vision_preview_pick(request: Request):
        return _call_api(node.vision_preview_pick, await request.json())

    @app.post('/api/vision/pick_selected')
    async def api_vision_pick_selected(request: Request):
        payload = await request.json()
        return await run_in_threadpool(
            lambda: _call_api(node.vision_pick_selected, payload, busy_status=409)
        )

    @app.post('/api/vision/cancel')
    def api_vision_cancel():
        return _call_api(node.vision_cancel)

    @app.post('/api/vision/calibration/add_point')
    async def api_vision_calibration_add_point(request: Request):
        return _call_api(node.vision_calibration_add_point, await request.json())

    @app.post('/api/vision/calibration/compute')
    def api_vision_calibration_compute():
        return _call_api(node.vision_calibration_compute)

    @app.post('/api/vision/calibration/test_point')
    async def api_vision_calibration_test_point(request: Request):
        return _call_api(node.vision_calibration_test_point, await request.json())

    return app


def _call_api(func, *args, busy_status=400):
    try:
        return func(*args)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=busy_status, detail=str(exc)) from exc
    except ConnectionError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except TimeoutError as exc:
        raise HTTPException(status_code=504, detail=str(exc)) from exc


def main(args=None):
    rclpy.init(args=args)
    node = DobotWebNode()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    ros_thread = threading.Thread(target=executor.spin, daemon=True)
    ros_thread.start()

    app = create_app(node)
    server = uvicorn.Server(
        uvicorn.Config(
            app,
            host=node.host,
            port=node.port,
            log_level='info',
            access_log=False,
        )
    )

    try:
        server.run()
    finally:
        executor.shutdown()
        ros_thread.join(timeout=2.0)
        node.shutdown()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
