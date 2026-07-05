# Vision Pick-and-Place End-to-End Test

This guide runs the Dobot vision flow from camera and YOLO detection through calibration, target selection, dry-run preview, and guarded real pick.

Default safety state:

- `dry_run=true`
- `allow_real_motion=false`
- Real motion is blocked unless explicitly enabled.
- Always use `Preview Pick` and `/api/vision/validate_pick` before real motion.

## 1. Install Dependencies

```bash
cd /home/jetson/dobot-magician
sudo apt update
sudo apt install -y \
  python3-colcon-common-extensions \
  python3-rosdep \
  python3-pip \
  python3-fastapi \
  python3-uvicorn \
  python3-opencv \
  ros-humble-cv-bridge \
  python3-yaml
python3 -m pip install --user --no-deps ultralytics
```

## 2. Build

```bash
cd /home/jetson/dobot-magician
source /opt/ros/humble/setup.bash
rosdep install --from-paths src/magician_ros2 --ignore-src -r -y
pip3 install -r src/magician_ros2/requirements.txt
colcon build
source install/setup.bash
```

## 3. Start Web and Robot Stack

Dry-run web only:

```bash
cd /home/jetson/dobot-magician
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch dobot_web_interface dobot_web_interface.launch.py \
  host:=0.0.0.0 \
  port:=8080 \
  camera_device:=/dev/video0
```

Full control stack plus web:

```bash
cd /home/jetson/dobot-magician
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch dobot_web_interface dobot_auto.launch.py \
  tool:=suction_cup \
  host:=0.0.0.0 \
  port:=8080 \
  camera_device:=/dev/video0
```

Open:

```text
http://<jetson-ip>:8080/
```

## 4. Start Detector

```bash
cd /home/jetson/dobot-magician
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 run dobot_vision_yolo yolo_detector_node --ros-args \
  -p dry_run:=true \
  -p prefer_tensorrt:=true \
  -p model_path:=models/best.engine \
  -p fallback_model_path:=models/best.pt \
  -p device:=cuda \
  -p imgsz:=640 \
  -p precision:=fp16
```

Detector status:

```bash
ros2 topic echo /dobot_vision/status
```

HTTP status:

```bash
curl http://localhost:8080/api/vision/status
curl http://localhost:8080/api/vision/detections
```

## 5. Test Detection

From the web page, press `Detect Once`.

Or call:

```bash
curl -X POST http://localhost:8080/api/vision/detect_once \
  -H 'Content-Type: application/json' \
  -d '{"dry_run":true,"object_class":"all","place_id":"tray_A"}'
```

Expected result:

- `/api/vision/status` has `ok:true`
- `/api/vision/detections` shows detections
- annotated image appears in the Vision Pick page

## 6. Calibration

Follow [calibration.md](calibration.md). The short version:

1. Collect at least four image pixel points.
2. Record matching Dobot X/Y points.
3. Add each point in the Vision Pick Calibration panel.
4. Press `Compute Homography`.
5. Test pixel conversion with `Test Pixel`.

Check calibration:

```bash
curl http://localhost:8080/api/vision/calibration
```

## 7. Select Target

```bash
curl -X POST http://localhost:8080/api/vision/select_target \
  -H 'Content-Type: application/json' \
  -d '{
    "object_class":"black_cap",
    "place_id":"tray_A",
    "selection_mode":"highest_confidence",
    "manual_id":null,
    "dry_run":true
  }'
```

Expected selected target fields:

- `id`
- `class_name`
- `confidence`
- `center_pixel`
- `robot_xy`
- `pick_pose`
- `place_pose`

If no selected class is found, the API returns `selected:false` and does not publish a pick pose.

## 8. Validate Safety

```bash
curl http://localhost:8080/api/vision/safety
curl -X POST http://localhost:8080/api/vision/validate_pick \
  -H 'Content-Type: application/json' \
  -d '{"dry_run":true}'
```

The Safety Checklist must show:

- Camera OK
- YOLO OK
- Calibration OK
- Target OK
- Workspace OK
- Dry Run ON

## 9. Preview Pick

```bash
curl -X POST http://localhost:8080/api/vision/preview_pick \
  -H 'Content-Type: application/json' \
  -d '{
    "object_class":"black_cap",
    "place_id":"tray_A",
    "selection_mode":"highest_confidence",
    "dry_run":true
  }'
```

The response contains a simulated motion sequence:

1. move above target
2. move down to pick
3. tool on simulated
4. move up to safe Z
5. move above place
6. move down to place
7. tool off simulated
8. move up to safe Z

No `/api/move`, `/PTP_action`, gripper, or suction command is sent by preview.

## 10. Dry-Run Checklist Before Real Pick

Complete this checklist before enabling real motion:

- Robot homing completed.
- Calibration is complete and mean/max error are acceptable.
- Workspace limits match the physical table.
- Dry-run `select_target` works.
- Dry-run `validate_pick` passes.
- Dry-run `preview_pick` sequence is correct.
- Object is inside the reachable workspace.
- No obstacles are in the robot path.
- Operator is ready to press `Cancel`.

## 11. Enable Real Motion

Real motion is disabled by default. To enable it, edit:

```text
src/magician_ros2/dobot_vision_yolo/config/workspace.yaml
```

Set:

```yaml
allow_real_motion: true
```

Keep low speed settings:

```yaml
velocity_ratio: 0.3
acceleration_ratio: 0.2
```

Restart the web/vision process after editing config.

## 12. Pick Real

Only run this after all safety checks pass:

```bash
curl -X POST http://localhost:8080/api/vision/pick_selected \
  -H 'Content-Type: application/json' \
  -d '{
    "object_class":"black_cap",
    "place_id":"tray_A",
    "selection_mode":"highest_confidence",
    "dry_run":false,
    "confirm_real_motion":true,
    "tool_type":"suction",
    "velocity_ratio":0.3,
    "acceleration_ratio":0.2
  }'
```

Cancel:

```bash
curl -X POST http://localhost:8080/api/vision/cancel
```

The web page also has `Pick Selected` and `Cancel` buttons. `Pick Selected` stays disabled while `allow_real_motion=false`.

## System Inspection Commands

```bash
ros2 topic list
ros2 service list
ros2 action list
curl http://localhost:8080/api/status
curl http://localhost:8080/api/vision/status
curl http://localhost:8080/api/vision/safety
```

## Troubleshooting

Camera does not show:

- Check `camera_device` and permissions.
- Run `ls -l /dev/video*`.
- Try `curl http://localhost:8080/api/snapshot --output /tmp/snapshot.jpg`.

YOLO import fails:

- Install Ultralytics explicitly without replacing Jetson PyTorch: `python3 -m pip install --user --no-deps ultralytics`.
- Check the active Python environment used by ROS.

Model not found:

- Place `best.engine` or `best.pt` in `models/`.
- Check `/api/vision/status` field `model_error`.

TensorRT engine fails:

- Fall back to `best.pt`.
- Re-export the engine on the same Jetson/JetPack/TensorRT version.
- See [jetson_tensorrt.md](jetson_tensorrt.md).

Calibration error is high:

- Use points spread across the workspace.
- Verify pixel order matches robot point order.
- Recompute homography and check mean/max error.

Coordinates are outside workspace:

- Check `config/workspace.yaml`.
- Confirm calibration did not flip axes.
- Confirm object and place poses are physically reachable.

API move fails:

- Check `curl http://localhost:8080/api/status`.
- Confirm `/PTP_action` appears in `ros2 action list`.
- Confirm homing was completed.
- Keep velocity/acceleration low.
