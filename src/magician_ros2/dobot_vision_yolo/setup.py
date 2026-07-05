import os
from glob import glob

from setuptools import setup


package_name = "dobot_vision_yolo"
model_files = glob("models/*.pt") + glob("models/*.engine")
data_files = [
    ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
    ("share/" + package_name, ["package.xml", "README.md"]),
    (os.path.join("share", package_name, "launch"), glob("launch/*.launch.py")),
    (os.path.join("share", package_name, "config"), glob("config/*.yaml")),
]
if model_files:
    data_files.append((os.path.join("share", package_name, "models"), model_files))

setup(
    name=package_name,
    version="0.1.0",
    packages=[package_name],
    data_files=data_files,
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="jetson",
    maintainer_email="jetson@example.com",
    description="Dry-run YOLO vision pick-and-place skeleton for Dobot Magician.",
    license="MIT",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "yolo_detector_node = dobot_vision_yolo.yolo_detector_node:main",
            "target_selector_node = dobot_vision_yolo.target_selector_node:main",
            "pixel_to_robot_node = dobot_vision_yolo.pixel_to_robot_node:main",
            "vision_pick_place_node = dobot_vision_yolo.vision_pick_place_node:main",
            "camera_calibration_tool = dobot_vision_yolo.camera_calibration_tool:main",
            "safety_guard_node = dobot_vision_yolo.safety_guard:main",
        ],
    },
)
