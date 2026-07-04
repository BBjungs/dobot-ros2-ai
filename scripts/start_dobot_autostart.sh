#!/usr/bin/env bash
set -eo pipefail

cd /home/jetson/dobot-magician

set +u
source /opt/ros/humble/setup.bash
source install/setup.bash
set -u

: "${MAGICIAN_TOOL:=extended_gripper}"
: "${WEB_HOST:=0.0.0.0}"
: "${WEB_PORT:=8080}"
: "${CAMERA_DEVICE:=/dev/video0}"
: "${CAMERA_WIDTH:=1280}"
: "${CAMERA_HEIGHT:=720}"
: "${CAMERA_FPS:=15.0}"
: "${STREAM_FPS:=12.0}"
: "${ROS_LOG_DIR:=/tmp/dobot_ros_logs}"

export MAGICIAN_TOOL
export ROS_LOG_DIR
export WEB_HOST WEB_PORT
export CAMERA_DEVICE CAMERA_WIDTH CAMERA_HEIGHT CAMERA_FPS STREAM_FPS

mkdir -p "${ROS_LOG_DIR}"

exec ros2 launch dobot_web_interface dobot_auto.launch.py \
  tool:="${MAGICIAN_TOOL}" \
  host:="${WEB_HOST}" \
  port:="${WEB_PORT}" \
  camera_device:="${CAMERA_DEVICE}" \
  camera_width:="${CAMERA_WIDTH}" \
  camera_height:="${CAMERA_HEIGHT}" \
  camera_fps:="${CAMERA_FPS}" \
  stream_fps:="${STREAM_FPS}"
