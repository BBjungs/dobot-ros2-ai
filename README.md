# dobot-ros2-ai

โปรเจกต์นี้เป็น ROS 2 workspace สำหรับควบคุมแขนกล **Dobot Magician** ผ่าน USB serial พร้อม web interface สำหรับดูภาพกล้องและสั่งงานพื้นฐานจาก browser.

โค้ดหลักอยู่ใน `src/magician_ros2` ซึ่งต่อยอดจาก control stack ของ Dobot Magician บน ROS 2 Humble และ repo นี้เพิ่มไฟล์สำหรับใช้งานบนเครื่อง `/home/jetson/dobot-magician` เช่น web interface, autostart script, config และ systemd user service.

## ความสามารถหลัก

- ควบคุม Dobot Magician ผ่าน ROS 2 action/service
- สั่ง homing, point-to-point motion, gripper และ suction cup
- อ่านสถานะ joint, TCP pose, alarm และสถานะ end effector
- แสดงภาพกล้องแบบ MJPEG ผ่าน browser
- เปิด web control panel ที่ `http://<jetson-ip>:8080/`
- ตั้งค่า autostart ด้วย `systemd --user`

## โครงสร้างโปรเจกต์

```text
.
├── config/
│   └── dobot-autostart.env          # ค่า environment สำหรับ autostart
├── scripts/
│   └── start_dobot_autostart.sh     # script เริ่ม ROS 2 stack + web interface
├── systemd/
│   └── dobot-magician.service       # systemd user service
└── src/magician_ros2/
    ├── dobot_bringup/               # launch หลักของ control stack
    ├── dobot_driver/                # serial driver ไปยัง Dobot
    ├── dobot_motion/                # PointToPoint action server
    ├── dobot_homing/                # homing service
    ├── dobot_end_effector/          # gripper และ suction services
    ├── dobot_web_interface/         # FastAPI web UI + camera stream
    └── ...                          # messages, kinematics, diagnostics, RViz tools
```

`build/`, `install/` และ `log/` เป็น output จาก `colcon build`.

## Requirements

- Ubuntu 22.04
- ROS 2 Humble
- Dobot Magician ต่อผ่าน USB
- กล้อง USB หรือ ROS camera topic ถ้าต้องการ live view
- สิทธิ์ serial port สำหรับผู้ใช้ปัจจุบัน

ติดตั้ง dependency พื้นฐาน:

```bash
sudo apt update
sudo apt install -y \
  python3-colcon-common-extensions \
  python3-rosdep \
  python3-pip \
  python3-fastapi \
  python3-uvicorn \
  python3-opencv \
  ros-humble-cv-bridge \
  ros-humble-diagnostic-aggregator \
  ros-humble-rqt-robot-monitor \
  python3-pykdl
```

เพิ่ม user เข้า group `dialout` เพื่อเปิด serial port โดยไม่ต้องใช้ `sudo`:

```bash
sudo usermod -a -G dialout "$USER"
```

หลังรันคำสั่งนี้ให้ logout/login ใหม่ หรือ reboot เครื่อง.

ค่า serial port เริ่มต้นอยู่ที่ `/dev/ttyUSB0` ใน `src/magician_ros2/dobot_driver/dobot_driver/dobot_handle.py`.

## Build

จาก root ของ repo:

```bash
cd /home/jetson/dobot-magician
source /opt/ros/humble/setup.bash

rosdep install --from-paths src/magician_ros2 --ignore-src -r -y
pip3 install -r src/magician_ros2/requirements.txt

colcon build
source install/setup.bash
```

## Run แบบ manual

ต่อ Dobot Magician กับเครื่องผ่าน USB, เปิดไฟเลี้ยง robot และตั้งค่า tool ที่ติดอยู่กับปลายแขน:

```bash
cd /home/jetson/dobot-magician
source /opt/ros/humble/setup.bash
source install/setup.bash

export MAGICIAN_TOOL=extended_gripper
ros2 launch dobot_bringup dobot_magician_control_system.launch.py
```

ค่า `MAGICIAN_TOOL` ที่รองรับ:

```text
none, pen, suction_cup, gripper, extended_gripper
```

หลังเปิดระบบ ควรทำ homing ก่อนสั่ง motion:

```bash
ros2 service call /dobot_homing_service dobot_msgs/srv/ExecuteHomingProcedure
```

ตัวอย่างสั่ง point-to-point motion:

```bash
ros2 action send_goal /PTP_action dobot_msgs/action/PointToPoint \
  "{motion_type: 1, target_pose: [200.0, 0.0, 100.0, 0.0], velocity_ratio: 0.5, acceleration_ratio: 0.3}" \
  --feedback
```

## Run web interface

ถ้าต้องการเปิดเฉพาะ web interface ให้รัน control stack ในอีก terminal ก่อน แล้วเปิด:

```bash
cd /home/jetson/dobot-magician
source /opt/ros/humble/setup.bash
source install/setup.bash

ros2 launch dobot_web_interface dobot_web_interface.launch.py host:=0.0.0.0 port:=8080
```

เปิด browser:

```text
http://<jetson-ip>:8080/
```

ถ้าต้องการเปิด control stack และ web interface พร้อมกัน:

```bash
cd /home/jetson/dobot-magician
source /opt/ros/humble/setup.bash
source install/setup.bash

ros2 launch dobot_web_interface dobot_auto.launch.py \
  tool:=extended_gripper \
  host:=0.0.0.0 \
  port:=8080 \
  camera_device:=/dev/video0
```

ค่า camera เริ่มต้น:

```text
camera_device=/dev/video0
camera_width=1280
camera_height=720
camera_fps=15.0
stream_fps=12.0
```

web interface จะอ่านภาพจาก `/dev/video0` โดยตรง และรองรับ ROS camera topics:

```text
/camera/color/image_raw
/camera/color/image_raw/compressed
```

## HTTP API

web interface มี endpoint หลักดังนี้:

```text
GET  /api/status
GET  /api/snapshot
GET  /stream
POST /api/homing
POST /api/move
POST /api/cancel
POST /api/gripper
POST /api/suction
```

ตัวอย่างเรียก motion ผ่าน HTTP:

```bash
curl -X POST "http://<jetson-ip>:8080/api/move" \
  -H "Content-Type: application/json" \
  -d '{"motion_type":1,"target_pose":[200,0,100,0],"velocity_ratio":0.5,"acceleration_ratio":0.3}'
```

ตัวอย่างเปิด gripper:

```bash
curl -X POST "http://<jetson-ip>:8080/api/gripper" \
  -H "Content-Type: application/json" \
  -d '{"state":"open","keep_compressor_running":false}'
```

web interface นี้ไม่มี authentication. ควร bind เฉพาะ network ที่เชื่อถือได้เท่านั้น.

## Autostart ด้วย systemd user service

ค่า autostart อยู่ที่:

```text
config/dobot-autostart.env
```

ค่าเริ่มต้น:

```text
MAGICIAN_TOOL=extended_gripper
WEB_HOST=0.0.0.0
WEB_PORT=8080
CAMERA_DEVICE=/dev/video0
CAMERA_WIDTH=1280
CAMERA_HEIGHT=720
CAMERA_FPS=15.0
STREAM_FPS=12.0
ROS_LOG_DIR=/tmp/dobot_ros_logs
```

ติดตั้ง service:

```bash
mkdir -p ~/.config/systemd/user
ln -sf /home/jetson/dobot-magician/systemd/dobot-magician.service ~/.config/systemd/user/dobot-magician.service
systemctl --user daemon-reload
systemctl --user enable --now dobot-magician.service
```

ดูสถานะและ log:

```bash
systemctl --user status dobot-magician.service
journalctl --user -u dobot-magician.service -f
```

restart service:

```bash
systemctl --user restart dobot-magician.service
```

ถ้าต้องการให้ service ทำงานหลัง boot แม้ยังไม่ได้ login:

```bash
loginctl enable-linger "$USER"
```

หมายเหตุ: service และ script มี path แบบ hard-coded เป็น `/home/jetson/dobot-magician`. ถ้าย้าย repo ไป path อื่นให้แก้ `systemd/dobot-magician.service` และ `scripts/start_dobot_autostart.sh`.

## Topics และ interfaces สำคัญ

Published topics:

```text
/dobot_joint_states
/joint_states
/dobot_TCP
/dobot_pose_raw
/dobot_rail_pose
```

Services:

```text
/dobot_homing_service
/dobot_gripper_service
/dobot_suction_cup_service
```

Action:

```text
/PTP_action
```

## Troubleshooting

- ถ้า launch แล้วขึ้นว่า Dobot disconnected ให้เช็ก USB cable, power adapter และผลลัพธ์จาก `lsusb`.
- ถ้าเปิด serial ไม่ได้ ให้เช็กว่า user อยู่ใน group `dialout` แล้ว logout/login ใหม่.
- ถ้า Dobot ไม่ได้อยู่ที่ `/dev/ttyUSB0` ให้แก้ port ใน `dobot_driver/dobot_handle.py`.
- ถ้า web เปิดได้แต่ control ไม่ทำงาน ให้เช็กว่า control stack พร้อมแล้วผ่าน `GET /api/status`.
- ถ้ากล้องไม่ขึ้น ให้เช็ก `/dev/video0`, permission ของ device และลองลด resolution/FPS ใน `config/dobot-autostart.env`.
- ก่อนสั่ง motion หลังเปิดเครื่อง ควรเรียก homing ก่อนเสมอ.

## เอกสารเพิ่มเติม

- README ของ control stack หลัก: `src/magician_ros2/README.md`
- README ของ web interface: `src/magician_ros2/dobot_web_interface/README.md`
- license ของ upstream control stack: `src/magician_ros2/LICENSE`

## Vision Pick-and-Place

เอกสารละเอียด:

- [End-to-end vision pick-and-place](docs/vision_pick_place.md)
- [Camera calibration pixel-to-robot](docs/calibration.md)
- [Jetson TensorRT YOLO](docs/jetson_tensorrt.md)

ค่าเริ่มต้นปลอดภัย:

- `dry_run=true`
- `allow_real_motion=false`
- ถ้า safety ไม่ผ่าน ระบบ Vision จะไม่ส่งคำสั่ง motion
- `Preview Pick` เป็น simulation เท่านั้น

### Install Dependencies

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

### Build

```bash
cd /home/jetson/dobot-magician
source /opt/ros/humble/setup.bash
rosdep install --from-paths src/magician_ros2 --ignore-src -r -y
pip3 install -r src/magician_ros2/requirements.txt
colcon build
source install/setup.bash
```

### Run Web

```bash
cd /home/jetson/dobot-magician
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch dobot_web_interface dobot_web_interface.launch.py \
  host:=0.0.0.0 \
  port:=8080 \
  camera_device:=/dev/video0
```

เปิดเว็บ:

```text
http://<jetson-ip>:8080/
```

### Run Detector

วาง model เองใน:

```text
models/best.engine
models/best.pt
```

รัน detector:

```bash
ros2 run dobot_vision_yolo yolo_detector_node --ros-args \
  -p dry_run:=true \
  -p prefer_tensorrt:=true \
  -p model_path:=models/best.engine \
  -p fallback_model_path:=models/best.pt \
  -p device:=cuda \
  -p imgsz:=640 \
  -p precision:=fp16
```

### Test Detection

```bash
curl -X POST http://localhost:8080/api/vision/detect_once \
  -H 'Content-Type: application/json' \
  -d '{"dry_run":true,"object_class":"all","place_id":"tray_A"}'
curl http://localhost:8080/api/vision/status
curl http://localhost:8080/api/vision/detections
```

### Calibration

```bash
curl -X POST http://localhost:8080/api/vision/calibration/add_point \
  -H 'Content-Type: application/json' \
  -d '{"image_point":[120,80],"robot_point":[180.0,-120.0]}'

curl -X POST http://localhost:8080/api/vision/calibration/compute \
  -H 'Content-Type: application/json' \
  -d '{}'

curl -X POST http://localhost:8080/api/vision/calibration/test_point \
  -H 'Content-Type: application/json' \
  -d '{"u":320,"v":240}'
```

รายละเอียดอยู่ใน [docs/calibration.md](docs/calibration.md)

### Select Target

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

### Preview Pick

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

ผลลัพธ์ต้องเป็น motion sequence แบบ simulated และไม่มีการเรียก `/api/move`.

### Dry Run and Safety

```bash
curl http://localhost:8080/api/vision/safety
curl -X POST http://localhost:8080/api/vision/validate_pick \
  -H 'Content-Type: application/json' \
  -d '{"dry_run":true}'
```

Safety Checklist บนเว็บต้องผ่านก่อน real motion:

- Camera OK
- YOLO OK
- Calibration OK
- Target OK
- Workspace OK
- Dry Run ON/OFF ตรงตามโหมดที่ตั้งใจ

### Enable Real Motion

ค่า default คือปิด real motion:

```yaml
allow_real_motion: false
```

ถ้าจะทดสอบจริง ให้แก้:

```text
src/magician_ros2/dobot_vision_yolo/config/workspace.yaml
```

เป็น:

```yaml
allow_real_motion: true
```

จากนั้น restart web/vision process และใช้ความเร็วต่ำ:

```yaml
velocity_ratio: 0.3
acceleration_ratio: 0.2
```

### Pick Real

ก่อนรันจริงต้องผ่าน checklist:

- Homing แล้ว
- Calibration ผ่าน
- Workspace ถูก
- Dry run ทดสอบผ่าน
- วัตถุอยู่ในพื้นที่
- ไม่มีสิ่งกีดขวาง
- พร้อมกด Cancel

คำสั่ง:

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
curl -X POST http://localhost:8080/api/cancel
```

### System Check Commands

```bash
ros2 topic list
ros2 service list
ros2 action list
curl http://localhost:8080/api/status
curl http://localhost:8080/api/vision/status
curl http://localhost:8080/api/vision/safety
```

### Vision Troubleshooting

กล้องไม่ขึ้น:

- ตรวจ `/dev/video0`: `ls -l /dev/video*`
- ทดสอบ snapshot: `curl http://localhost:8080/api/snapshot --output /tmp/snapshot.jpg`
- เช็ก `camera_device` ใน launch/config

YOLO import ไม่ได้:

- ติดตั้ง: `python3 -m pip install --user --no-deps ultralytics`
- เช็ก: `python3 -c "import ultralytics; print(ultralytics.__version__)"`

ไม่เจอ model:

- วาง `best.engine` หรือ `best.pt` ใน `models/`
- ดู `model_error` จาก `curl http://localhost:8080/api/vision/status`

TensorRT engine ใช้ไม่ได้:

- re-export บน Jetson เครื่องเดียวกัน
- fallback เป็น `best.pt`
- ดู [docs/jetson_tensorrt.md](docs/jetson_tensorrt.md)

Calibration error สูง:

- ใช้จุดกระจายกว้างในพื้นที่ทำงาน
- ตรวจลำดับ `image_points` กับ `robot_points`
- ดู [docs/calibration.md](docs/calibration.md)

พิกัดหลุด workspace:

- ตรวจ `src/magician_ros2/dobot_vision_yolo/config/workspace.yaml`
- เช็กว่า calibration ไม่กลับแกน
- เช็กว่า object/place อยู่ในพื้นที่จริง

API move fail:

- เช็ก `curl http://localhost:8080/api/status`
- เช็ก `ros2 action list` ว่ามี `/PTP_action`
- ทำ homing ก่อน
- ลด velocity/acceleration
