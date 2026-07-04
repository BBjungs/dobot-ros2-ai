const $ = (id) => document.getElementById(id);

const eventLog = $("eventLog");
const commandStatus = $("commandStatus");
const statusEls = {
  camera: $("cameraStatus"),
  action: $("actionStatus"),
  homing: $("homingStatus"),
  tool: $("toolStatus"),
};

function log(message) {
  const time = new Date().toLocaleTimeString();
  eventLog.textContent = `[${time}] ${message}\n` + eventLog.textContent;
  commandStatus.textContent = message;
}

function setBusy(button, busy) {
  button.classList.toggle("busy", busy);
  button.disabled = busy;
}

function setPill(element, label, ready, warn = false) {
  element.textContent = label;
  element.classList.toggle("ready", ready);
  element.classList.toggle("warn", warn && !ready);
}

async function api(path, body = null) {
  const options = { method: "POST" };
  if (body !== null) {
    options.headers = { "Content-Type": "application/json" };
    options.body = JSON.stringify(body);
  }

  const response = await fetch(path, options);
  const data = await response.json();
  if (!response.ok) {
    const detail = data.detail || response.statusText;
    throw new Error(detail);
  }
  return data;
}

async function refreshStatus() {
  try {
    const status = await fetch("/api/status").then((response) => response.json());
    const hasFrame = status.camera.has_frame;
    const frameAge = status.camera.frame_age_sec;
    const toolReady = status.ros.gripper_ready || status.ros.suction_ready;

    setPill(
      statusEls.camera,
      hasFrame ? `Camera ${frameAge}s` : "Camera waiting",
      hasFrame,
      true
    );
    setPill(statusEls.action, "PTP", status.ros.ptp_action_ready, true);
    setPill(statusEls.homing, "Homing", status.ros.homing_ready, true);
    setPill(statusEls.tool, "Tool", toolReady, true);

    $("cameraTopic").textContent =
      status.camera.frame_source ||
      status.camera.device ||
      `${status.camera.raw_topic} or ${status.camera.compressed_topic}`;

    $("motionState").textContent = status.motion.active_goal
      ? "Motion goal active"
      : "No active goal";

    if (status.motion.last_feedback) {
      $("poseFeedback").textContent = `Pose ${status.motion.last_feedback.join(", ")}`;
    } else if (status.motion.last_result) {
      $("poseFeedback").textContent =
        `Result ${status.motion.last_result.achieved_pose.join(", ")}`;
    } else {
      $("poseFeedback").textContent = "Feedback unavailable";
    }

    syncAxisControls(status.motion.joints_deg);
  } catch (error) {
    setPill(statusEls.camera, "Offline", false, true);
    log(`Status error: ${error.message}`);
  }
}

function targetPose() {
  return [
    Number($("poseX").value),
    Number($("poseY").value),
    Number($("poseZ").value),
    Number($("poseR").value),
  ];
}

const axisControls = {
  x: {
    label: "J1",
    index: 0,
    slider: "axisXSlider",
    value: "axisXValue",
    minus: "axisXMinus",
    plus: "axisXPlus",
  },
  y: {
    label: "J2",
    index: 1,
    slider: "axisYSlider",
    value: "axisYValue",
    minus: "axisYMinus",
    plus: "axisYPlus",
  },
  z: {
    label: "J3",
    index: 2,
    slider: "axisZSlider",
    value: "axisZValue",
    minus: "axisZMinus",
    plus: "axisZPlus",
  },
  r: {
    label: "J4",
    index: 3,
    slider: "axisRSlider",
    value: "axisRValue",
    minus: "axisRMinus",
    plus: "axisRPlus",
  },
};

const axisLiveStatus = $("axisLiveStatus");
let axisLiveTimer = null;
let axisMoveInFlight = false;
let axisMoveQueued = false;
let lastAxisPoseKey = "";
let axisInitialized = false;
let axisTargetPose = [0, 0, 0, 0];

function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max);
}

function writeAxis(axis, value) {
  const control = axisControls[axis];
  const slider = $(control.slider);
  const next = clamp(Number(value), Number(slider.min), Number(slider.max));

  slider.value = String(next);
  $(control.value).textContent = String(next);
  axisTargetPose[control.index] = next;
}

function syncAxisControls(jointsDeg) {
  if (!Array.isArray(jointsDeg) || jointsDeg.length < 4 || axisInitialized) {
    return;
  }

  Object.keys(axisControls).forEach((axis) => {
    const control = axisControls[axis];
    writeAxis(axis, jointsDeg[control.index]);
  });
  axisInitialized = true;
  lastAxisPoseKey = axisTargetPose.join(",");
  setAxisLiveStatus("Live", false);
}

function setAxisLiveStatus(message, waiting = false) {
  axisLiveStatus.textContent = message;
  axisLiveStatus.classList.toggle("waiting", waiting);
  commandStatus.textContent = message;
}

function axisMovePayload() {
  return {
    motion_type: 4,
    target_pose: axisTargetPose,
    velocity_ratio: Number($("velocity").value),
    acceleration_ratio: Number($("acceleration").value),
  };
}

function scheduleAxisMove(delayMs = 300) {
  if (!axisInitialized) {
    setAxisLiveStatus("Waiting", true);
    log("Waiting for current joint state...");
    return;
  }

  clearTimeout(axisLiveTimer);
  setAxisLiveStatus("Live wait", true);
  axisLiveTimer = setTimeout(sendAxisMove, delayMs);
}

async function sendAxisMove() {
  if (axisMoveInFlight) {
    axisMoveQueued = true;
    return;
  }

  axisMoveInFlight = true;
  const payload = axisMovePayload();
  const poseKey = payload.target_pose.join(",");

  try {
    if (poseKey === lastAxisPoseKey) {
      setAxisLiveStatus("Live", false);
      return;
    }

    const status = await fetch("/api/status").then((response) => response.json());
    if (status.motion.active_goal) {
      axisMoveQueued = true;
      setAxisLiveStatus("Moving...", true);
      return;
    }

    setAxisLiveStatus("Sending", true);
    const result = await api("/api/move", payload);
    lastAxisPoseKey = poseKey;
    log(`Axis live MOVJ ANGLE: J1=${payload.target_pose[0]}, J2=${payload.target_pose[1]}, J3=${payload.target_pose[2]}, J4=${payload.target_pose[3]}`);
    if (result.message) {
      commandStatus.textContent = result.message;
    }
  } catch (error) {
    axisMoveQueued = true;
    setAxisLiveStatus("Retry", true);
    commandStatus.textContent = `Axis live: ${error.message}`;
  } finally {
    axisMoveInFlight = false;
    if (axisMoveQueued) {
      axisMoveQueued = false;
      clearTimeout(axisLiveTimer);
      axisLiveTimer = setTimeout(sendAxisMove, 550);
    }
  }
}

Object.entries(axisControls).forEach(([axis, control]) => {
  $(control.slider).addEventListener("input", () => {
    writeAxis(axis, $(control.slider).value);
    scheduleAxisMove();
  });

  $(control.minus).addEventListener("click", () => {
    writeAxis(axis, Number($(control.slider).value) - Number($("axisStep").value));
    scheduleAxisMove(120);
  });

  $(control.plus).addEventListener("click", () => {
    writeAxis(axis, Number($(control.slider).value) + Number($("axisStep").value));
    scheduleAxisMove(120);
  });
});

$("moveButton").addEventListener("click", async () => {
  const button = $("moveButton");
  try {
    setBusy(button, true);
    log("Sending motion goal...");
    const result = await api("/api/move", {
      motion_type: Number($("motionType").value),
      target_pose: targetPose(),
      velocity_ratio: Number($("velocity").value),
      acceleration_ratio: Number($("acceleration").value),
    });
    log(result.message);
  } catch (error) {
    log(`Move failed: ${error.message}`);
  } finally {
    setBusy(button, false);
  }
});

$("cancelButton").addEventListener("click", async () => {
  const button = $("cancelButton");
  try {
    setBusy(button, true);
    log("Cancel requested...");
    const result = await api("/api/cancel");
    log(result.message || `Cancel requested: ${result.goals_canceling}`);
  } catch (error) {
    log(`Cancel failed: ${error.message}`);
  } finally {
    setBusy(button, false);
  }
});

$("homeButton").addEventListener("click", async () => {
  const button = $("homeButton");
  try {
    setBusy(button, true);
    log("Homing requested...");
    const result = await api("/api/homing");
    log(`Homing: ${result.message}`);
  } catch (error) {
    log(`Homing failed: ${error.message}`);
  } finally {
    setBusy(button, false);
  }
});

async function setGripper(state) {
  const button = state === "open" ? $("gripperOpen") : $("gripperClose");
  try {
    setBusy(button, true);
    log(`Gripper ${state} requested...`);
    const result = await api("/api/gripper", {
      state,
      keep_compressor_running: $("keepCompressor").checked,
    });
    log(`Gripper ${state}: ${result.message}`);
  } catch (error) {
    log(`Gripper failed: ${error.message}`);
  } finally {
    setBusy(button, false);
  }
}

async function setSuction(enable) {
  const button = enable ? $("suctionOn") : $("suctionOff");
  try {
    setBusy(button, true);
    log(`Suction ${enable ? "on" : "off"} requested...`);
    const result = await api("/api/suction", { enable_suction: enable });
    log(`Suction ${enable ? "on" : "off"}: ${result.message}`);
  } catch (error) {
    log(`Suction failed: ${error.message}`);
  } finally {
    setBusy(button, false);
  }
}

$("gripperOpen").addEventListener("click", () => setGripper("open"));
$("gripperClose").addEventListener("click", () => setGripper("close"));
$("suctionOn").addEventListener("click", () => setSuction(true));
$("suctionOff").addEventListener("click", () => setSuction(false));

refreshStatus();
setInterval(refreshStatus, 1000);
