import threading
import time
from pathlib import Path

import cv2
import numpy as np
import rclpy
from cv_bridge import CvBridge
from dobot_msgs.action import PointToPoint
from dobot_msgs.srv import ExecuteHomingProcedure, GripperControl, SuctionCupControl
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, Response, StreamingResponse
from fastapi.staticfiles import StaticFiles
from rclpy.action import ActionClient
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage, Image
import uvicorn
from sensor_msgs.msg import JointState


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

        self.get_logger().info(
            f'Web interface will listen on http://{self.host}:{self.port}'
        )
        self.get_logger().info(
            f'Camera topics: {self.camera_raw_topic}, {self.camera_compressed_topic}'
        )
        if self.camera_device:
            self._capture_thread = threading.Thread(
                target=self._capture_device_loop,
                name='dobot_web_camera_capture',
                daemon=True,
            )
            self._capture_thread.start()
            self.get_logger().info(f'Direct camera device: {self.camera_device}')

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
            },
        }

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

    @app.post('/api/gripper')
    async def api_gripper(request: Request):
        return _call_api(node.call_gripper, await request.json())

    @app.post('/api/suction')
    async def api_suction(request: Request):
        return _call_api(node.call_suction, await request.json())

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
