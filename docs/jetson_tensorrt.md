# Jetson TensorRT YOLO Guide

This guide configures YOLO inference on Jetson using GPU/TensorRT when a local `.engine` file is available.

The project never downloads model files automatically.

## Model Directory

Place model artifacts here:

```text
models/
```

Supported files:

```text
best.engine  # TensorRT engine, preferred
best.pt      # PyTorch fallback
```

Do not commit model binaries. The local `models/` directory is recreated by the export script when needed.

The following are ignored:

```text
*.pt
*.engine
*.onnx
models/*.pt
models/*.engine
models/*.onnx
datasets/
runs/
```

## Install Runtime

Install Ultralytics explicitly:

```bash
python3 -m pip install --user --no-deps ultralytics
```

On Jetson, use a PyTorch/Ultralytics version that matches the installed JetPack, CUDA, and TensorRT stack.

## Optional Max Performance Mode

```bash
./scripts/jetson_max_perf.sh
```

The script prints each step before running:

```bash
sudo nvpmodel -m 0
sudo jetson_clocks
```

Optional monitoring:

```bash
sudo -H pip3 install -U jetson-stats
jtop
```

## Export best.pt to best.engine

Place `best.pt` first:

```text
models/best.pt
```

Export:

```bash
cd /home/jetson/dobot-magician
./scripts/export_yolo26_tensorrt.sh
```

Optional settings:

```bash
IMGSZ=640 PRECISION=fp16 DEVICE=cuda \
./scripts/export_yolo26_tensorrt.sh models/best.pt models
```

Expected output:

```text
models/best.engine
```

The script exits with an error if:

- `best.pt` does not exist.
- `ultralytics` is not installed.
- export fails.

It does not download any model.

## Detector Config

`src/magician_ros2/dobot_vision_yolo/config/yolo.yaml`:

```yaml
yolo_detector_node:
  ros__parameters:
    model_path: models/best.engine
    fallback_model_path: models/best.pt
    prefer_tensorrt: true
    precision: fp16
    device: cuda
    imgsz: 640
```

Behavior:

- If `best.engine` exists, it is used.
- If `best.engine` is missing and `best.pt` exists, `.pt` is used.
- If both are missing, detector publishes a model error and continues without inference.

## Run Detector

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

## Check FPS and Active Model

```bash
ros2 topic echo /dobot_vision/status
```

Fields to check:

```text
fps
model_loaded
model_path
configured_model_path
fallback_model_path
prefer_tensorrt
precision
device
imgsz
model_error
```

HTTP:

```bash
curl http://localhost:8080/api/vision/status
```

## Fallback to .pt

To test fallback, remove or rename the engine:

```bash
mv models/best.engine models/best.engine.disabled
```

Keep:

```text
models/best.pt
```

Restart the detector. The status should show `model_path` ending in `best.pt`.

## Troubleshooting

Ultralytics import fails:

```bash
python3 -c "import ultralytics; print(ultralytics.__version__)"
python3 -m pip install --user --no-deps ultralytics
```

Model not found:

- Check file names are exactly `best.engine` or `best.pt`.
- Check path under `models/`.
- Check `/dobot_vision/status` field `model_error`.

TensorRT engine fails to load:

- Re-export on the same Jetson where it will run.
- Match JetPack/TensorRT/CUDA versions.
- Try deleting the engine and falling back to `.pt`.

Low FPS:

- Run `./scripts/jetson_max_perf.sh`.
- Confirm `device: cuda`.
- Confirm `model_path` points to `.engine`.
- Lower `imgsz` only if accuracy remains acceptable.

CUDA device error:

- Confirm Jetson GPU stack is installed.
- Try fallback with `device=cpu` only for debugging:

```bash
ros2 run dobot_vision_yolo yolo_detector_node --ros-args \
  -p dry_run:=true \
  -p prefer_tensorrt:=false \
  -p model_path:=models/best.pt \
  -p device:=cpu
```
