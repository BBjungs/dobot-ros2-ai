# YOLO Model Directory

Place local model artifacts here when running on the Jetson:

- `best.engine` - TensorRT engine, preferred when present.
- `best.pt` - PyTorch fallback when no engine is present.

Model binaries are intentionally ignored by git. Do not commit `.pt`, `.engine`, or `.onnx` files.

Export `best.engine` from an existing `best.pt`:

```bash
./scripts/export_yolo26_tensorrt.sh src/magician_ros2/dobot_vision_yolo/models/best.pt
```
