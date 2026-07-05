#!/usr/bin/env bash
set -euo pipefail

MODEL_PATH="${1:-models/best.pt}"
OUTPUT_DIR="${2:-models}"
IMGSZ="${IMGSZ:-640}"
PRECISION="${PRECISION:-fp16}"
DEVICE="${DEVICE:-cuda}"

echo "[export] YOLO TensorRT export for Jetson"
echo "[export] This script uses only local model files and does not download models."
echo "[export] Input model: ${MODEL_PATH}"
echo "[export] Output dir: ${OUTPUT_DIR}"
echo "[export] imgsz=${IMGSZ} precision=${PRECISION} device=${DEVICE}"

mkdir -p "${OUTPUT_DIR}"

if [ ! -f "${MODEL_PATH}" ]; then
  echo "[export] ERROR: ${MODEL_PATH} not found."
  echo "[export] Place your trained YOLO model at models/best.pt first."
  exit 1
fi

echo "[export] Checking Python dependencies and CUDA availability..."
python3 - <<'PY'
import importlib.util
import sys

if importlib.util.find_spec("ultralytics") is None:
    print("[export] ERROR: ultralytics is not installed.")
    print("[export] Jetson-safe install suggestion:")
    print("[export]   python3 -m pip install --user --no-deps ultralytics")
    print("[export] Then install only missing non-torch dependencies explicitly.")
    sys.exit(1)

try:
    import torch
except Exception as exc:
    print(f"[export] ERROR: torch import failed: {exc}")
    sys.exit(1)

print(f"[export] torch={torch.__version__}")
print(f"[export] torch.cuda.is_available={torch.cuda.is_available()}")
if not torch.cuda.is_available():
    print("[export] ERROR: CUDA is not available to PyTorch. Refusing TensorRT export.")
    sys.exit(1)

print("[export] ultralytics and CUDA are available.")
PY

echo "[export] Starting TensorRT export. This can take several minutes on Jetson."
python3 - <<PY
from pathlib import Path
from ultralytics import YOLO

model_path = Path("${MODEL_PATH}").expanduser().resolve()
output_dir = Path("${OUTPUT_DIR}").expanduser().resolve()
imgsz = int("${IMGSZ}")
precision = "${PRECISION}".lower()
device = "${DEVICE}".lower()
half = precision in ("fp16", "half", "true", "1", "yes")
export_device = 0 if device in ("cuda", "gpu") else device

print(f"[export] Loading {model_path}")
model = YOLO(str(model_path))
print(
    "[export] Exporting format=engine "
    f"imgsz={imgsz} half={half} device={device}"
)
exported = model.export(
    format="engine",
    imgsz=imgsz,
    half=half,
    device=export_device,
)

exported_path = Path(exported).expanduser().resolve()
target_path = output_dir / "best.engine"
if exported_path != target_path:
    target_path.write_bytes(exported_path.read_bytes())
    print(f"[export] Copied {exported_path} -> {target_path}")
else:
    print(f"[export] Engine written to {target_path}")
PY

echo "[export] TensorRT engine ready: ${OUTPUT_DIR}/best.engine"
