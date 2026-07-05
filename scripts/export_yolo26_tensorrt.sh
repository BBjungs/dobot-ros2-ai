#!/usr/bin/env bash
set -euo pipefail

MODEL_PATH="${1:-src/magician_ros2/dobot_vision_yolo/models/best.pt}"
OUTPUT_DIR="${2:-src/magician_ros2/dobot_vision_yolo/models}"
IMGSZ="${IMGSZ:-640}"
PRECISION="${PRECISION:-fp16}"
DEVICE="${DEVICE:-cuda}"

echo "[export] YOLO TensorRT export for Jetson"
echo "[export] This script does not download models."
echo "[export] Input model: ${MODEL_PATH}"
echo "[export] Output dir: ${OUTPUT_DIR}"
echo "[export] imgsz=${IMGSZ} precision=${PRECISION} device=${DEVICE}"

if [ ! -f "${MODEL_PATH}" ]; then
  echo "[export] ERROR: ${MODEL_PATH} not found."
  echo "[export] Place best.pt in src/magician_ros2/dobot_vision_yolo/models/ first."
  exit 1
fi

echo "[export] Checking ultralytics import..."
python3 - <<'PY'
import importlib.util
import sys

if importlib.util.find_spec("ultralytics") is None:
    print("[export] ERROR: ultralytics is not installed.")
    print("[export] Install it explicitly: python3 -m pip install --user ultralytics")
    sys.exit(1)
print("[export] ultralytics is available.")
PY

mkdir -p "${OUTPUT_DIR}"

echo "[export] Starting TensorRT export. This can take several minutes on Jetson."
python3 - <<PY
from pathlib import Path
from ultralytics import YOLO

model_path = Path("${MODEL_PATH}").expanduser().resolve()
output_dir = Path("${OUTPUT_DIR}").expanduser().resolve()
imgsz = int("${IMGSZ}")
precision = "${PRECISION}".lower()
device = "${DEVICE}"

print(f"[export] Loading {model_path}")
model = YOLO(str(model_path))
half = precision == "fp16"
print(f"[export] Exporting format=engine half={half} imgsz={imgsz} device={device}")
exported = model.export(format="engine", half=half, imgsz=imgsz, device=device)
exported_path = Path(exported).resolve()
target_path = output_dir / "best.engine"
print(f"[export] Exported engine: {exported_path}")
if exported_path != target_path:
    print(f"[export] Copying engine to {target_path}")
    target_path.write_bytes(exported_path.read_bytes())
print(f"[export] Done: {target_path}")
PY

echo "[export] TensorRT engine ready: ${OUTPUT_DIR}/best.engine"
