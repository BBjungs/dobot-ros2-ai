# Camera Calibration: Pixel to Dobot X/Y

This guide calibrates camera pixels to Dobot robot X/Y coordinates using OpenCV homography.

The calibration is stored in:

```text
src/magician_ros2/dobot_vision_yolo/config/camera_to_robot.yaml
```

Calibration does not move the robot automatically. You must record robot X/Y points yourself.

## Safety Notes

- Keep `dry_run=true` while calibrating.
- Do not run real pick until calibration is complete and error is acceptable.
- Use a flat plane: all calibration points and objects should be on the same table plane.
- Use at least four points. More points are allowed and usually improve robustness.

## Recommended 4-Point Layout

Use a rectangle that covers the expected pick area:

```text
image_points:
  top-left
  top-right
  bottom-left
  bottom-right

robot_points:
  same physical points in the same order
```

Example:

```yaml
image_points:
  - [120, 80]
  - [520, 82]
  - [118, 390]
  - [522, 388]
robot_points:
  - [180.0, -120.0]
  - [180.0, 120.0]
  - [300.0, -120.0]
  - [300.0, 120.0]
safe_z: 60.0
pick_z: -35.0
homography: []
```

## Step 1. Open Web UI

```bash
cd /home/jetson/dobot-magician
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch dobot_web_interface dobot_web_interface.launch.py \
  host:=0.0.0.0 \
  port:=8080 \
  camera_device:=/dev/video0
```

Open:

```text
http://<jetson-ip>:8080/
```

## Step 2. Add Calibration Points

In the Vision Pick Calibration panel:

1. Enter pixel `u,v` from the image.
2. Enter matching Dobot `x,y`.
3. Press `Add Point`.
4. Repeat at least four times.

API equivalent:

```bash
curl -X POST http://localhost:8080/api/vision/calibration/add_point \
  -H 'Content-Type: application/json' \
  -d '{"image_point":[120,80],"robot_point":[180.0,-120.0]}'
```

## Step 3. Compute Homography

```bash
curl -X POST http://localhost:8080/api/vision/calibration/compute \
  -H 'Content-Type: application/json' \
  -d '{}'
```

The response includes:

- `homography`
- `validation.mean_error_mm`
- `validation.max_error_mm`
- `validation.warning`

If average or max error is high, recalibrate before running pick.

## Step 4. Test Pixel Conversion

```bash
curl -X POST http://localhost:8080/api/vision/calibration/test_point \
  -H 'Content-Type: application/json' \
  -d '{"u":320,"v":240}'
```

Expected output:

```json
{
  "ok": true,
  "image_point": [320.0, 240.0],
  "robot_xy": [242.246, -0.779],
  "safe_z": 60.0,
  "pick_z": -35.0
}
```

## Step 5. Inspect YAML

```bash
sed -n '1,120p' src/magician_ros2/dobot_vision_yolo/config/camera_to_robot.yaml
```

Expected fields:

```yaml
image_points:
  - [120.0, 80.0]
robot_points:
  - [180.0, -120.0]
safe_z: 60.0
pick_z: -35.0
homography:
  - ...
validation:
  mean_error_mm: 0.0
  max_error_mm: 0.0
  point_errors_mm: []
  warning: ""
```

## Validation Rules

Calibration is not valid until:

- `image_points` and `robot_points` have the same length.
- There are at least four points.
- `homography` has nine numeric values.
- `safe_z` and `pick_z` are numeric.
- Validation warning is empty.

If calibration is incomplete, target selection and pick preview reject with a readable error and do not publish a pick pose.

## Troubleshooting

High calibration error:

- Recheck that pixel and robot points are in the same order.
- Use points farther apart.
- Avoid points that are nearly collinear.
- Keep all points on the same physical plane.
- Make sure the camera is fixed and not moved after calibration.

Robot X/Y appears mirrored:

- Check point ordering.
- Verify Dobot coordinate signs for left/right.
- Recompute with known corner points.

Test pixel gives no robot X/Y:

- Check `homography` is computed.
- Run `curl http://localhost:8080/api/vision/calibration`.
- Confirm validation errors are empty.

Workspace rejects valid-looking points:

- Check `config/workspace.yaml`.
- Check calibration did not map pixels outside expected X/Y.
