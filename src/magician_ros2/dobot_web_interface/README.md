# Dobot Web Interface

Browser control panel for Dobot Magician with a live MJPEG camera view.

## Run

```bash
cd /home/jetson/dobot-magician
source /opt/ros/humble/setup.bash
source install/setup.bash

ros2 launch dobot_web_interface dobot_web_interface.launch.py host:=0.0.0.0 port:=8080
```

Open:

```text
http://<jetson-ip>:8080/
```

## Dobot Control Stack

Run the Dobot control stack in another terminal before using motion or tool buttons:

```bash
cd /home/jetson/dobot-magician
source /opt/ros/humble/setup.bash
source install/setup.bash

export MAGICIAN_TOOL=extended_gripper
ros2 launch dobot_bringup dobot_magician_control_system.launch.py
```

## Camera Topics

The web interface listens to both topics below and uses whichever publishes frames:

```text
/camera/color/image_raw
/camera/color/image_raw/compressed
```

It also opens a direct USB camera device by default:

```text
/dev/video0
```

For Intel RealSense, run the camera driver in another terminal if it is installed:

```bash
source /opt/ros/humble/setup.bash
ros2 launch realsense2_camera rs_launch.py
```

For another camera driver, either publish one of the default topics above or override the
launch arguments:

```bash
ros2 launch dobot_web_interface dobot_web_interface.launch.py \
  camera_raw_topic:=/my_camera/image_raw \
  camera_compressed_topic:=/my_camera/image_raw/compressed
```

For a USB camera without a ROS driver, set the device directly:

```bash
ros2 launch dobot_web_interface dobot_web_interface.launch.py \
  camera_device:=/dev/video0
```

## Autostart

Autostart settings live in:

```text
/home/jetson/dobot-magician/config/dobot-autostart.env
```

The user service file is:

```text
/home/jetson/dobot-magician/systemd/dobot-magician.service
```

After installing the user service:

```bash
systemctl --user status dobot-magician.service
systemctl --user restart dobot-magician.service
journalctl --user -u dobot-magician.service -f
```

## HTTP API

```text
GET  /api/status
GET  /stream
GET  /api/snapshot
POST /api/homing
POST /api/move
POST /api/cancel
POST /api/gripper
POST /api/suction
```

This interface has no authentication. Bind it only on a trusted network.
