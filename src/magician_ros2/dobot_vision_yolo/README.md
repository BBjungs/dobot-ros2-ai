# dobot_vision_yolo

ROS 2 Humble package for Dobot Magician vision detection, calibration, dry-run preview, and guarded pick-and-place flow.

The default mode is safe: `dry_run=true` and real motion remains disabled unless explicitly enabled in safety config.

## Nodes

- `yolo_detector_node`: reads camera/snapshot frames, runs Ultralytics YOLO, publishes detections JSON, and writes `/tmp/dobot_vision_annotated.jpg`.
- `target_selector_node`: selects a detection by class/place/mode.
- `pixel_to_robot_node`: adds calibrated `robot_xy`.
- `vision_pick_place_node`: creates dry-run previews and guarded real execution when explicitly enabled.
- `camera_calibration_tool`: manages pixel-to-robot homography YAML.
- `safety_guard_node`: validates workspace and safety state.

## Build

```bash
cd /home/jetson/dobot-magician
source /opt/ros/humble/setup.bash
colcon build --packages-select dobot_vision_yolo
source install/setup.bash
```

## Install YOLO Runtime

```bash
python3 -m pip install --user ultralytics
```

On Jetson, install a PyTorch/Ultralytics combination that matches the JetPack, CUDA, and TensorRT stack already on the device.

## Model Files

Default paths:

```text
src/magician_ros2/dobot_vision_yolo/models/best.engine
src/magician_ros2/dobot_vision_yolo/models/best.pt
```

`best.engine` is preferred when present. If it is missing, the detector falls back to `best.pt`. No model is downloaded automatically.

Model binaries are ignored by git. Keep only `models/README.md` and `models/.gitkeep` committed.

## Jetson TensorRT Optimization

Optional max performance mode:

```bash
./scripts/jetson_max_perf.sh
```

Export an existing `best.pt` to TensorRT:

```bash
./scripts/export_yolo26_tensorrt.sh \
  src/magician_ros2/dobot_vision_yolo/models/best.pt
```

Override export settings if needed:

```bash
IMGSZ=640 PRECISION=fp16 DEVICE=cuda \
  ./scripts/export_yolo26_tensorrt.sh src/magician_ros2/dobot_vision_yolo/models/best.pt
```

The export script prints every step and exits if `best.pt` or `ultralytics` is missing. It does not download models.

## Run Detector

```bash
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

Run the full vision pipeline:

```bash
source install/setup.bash
ros2 launch dobot_vision_yolo vision_pick_place.launch.py dry_run:=true
```

## Check FPS

```bash
ros2 topic echo /dobot_vision/status
```

Check these fields:

```text
fps
model_path
prefer_tensorrt
device
imgsz
model_error
```

Published detector topics:

```text
/dobot_vision/detections  std_msgs/msg/String
/dobot_vision/status      std_msgs/msg/String
```

## Fallback Behavior

- If `models/best.engine` exists, it is used first.
- If the engine is missing and `models/best.pt` exists, `.pt` is used with a warning.
- If both are missing, the node publishes status with a clear model error and continues without inference.
