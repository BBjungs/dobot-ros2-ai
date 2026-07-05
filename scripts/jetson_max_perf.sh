#!/usr/bin/env bash
set -euo pipefail

echo "[jetson] Jetson max performance helper"
echo "[jetson] This script will request sudo for nvpmodel and jetson_clocks."
echo "[jetson] It does not install packages or modify model files."

echo "[jetson] Step 1/2: setting max performance mode with: sudo nvpmodel -m 0"
sudo nvpmodel -m 0

echo "[jetson] Step 2/2: locking clocks with: sudo jetson_clocks"
sudo jetson_clocks

echo "[jetson] Max performance commands completed."
echo "[jetson] Optional monitor: install/run jtop manually if desired:"
echo "[jetson]   sudo -H pip3 install -U jetson-stats"
echo "[jetson]   jtop"
