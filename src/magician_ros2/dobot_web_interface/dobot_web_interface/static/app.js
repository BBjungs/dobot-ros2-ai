const $ = (id) => document.getElementById(id);

const eventLog = $("eventLog");
const commandStatus = $("commandStatus");
const statusEls = {
  camera: $("cameraStatus"),
  action: $("actionStatus"),
  homing: $("homingStatus"),
  tool: $("toolStatus"),
};
let lastSelectedTarget = null;
let allowRealMotion = false;

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

async function getJson(path) {
  const response = await fetch(path);
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

function setVisionError(message) {
  const errorEl = $("visionError");
  errorEl.hidden = !message;
  errorEl.textContent = message || "";
}

function setCalibrationError(message) {
  const errorEl = $("calibrationError");
  errorEl.hidden = !message;
  errorEl.textContent = message || "";
}

function setSafetyError(message) {
  const errorEl = $("safetyError");
  errorEl.hidden = !message;
  errorEl.textContent = message || "";
}

function setRealPickError(message) {
  const errorEl = $("realPickError");
  errorEl.hidden = !message;
  errorEl.textContent = message || "";
}

function setSelectOptions(select, values, fallback = []) {
  const current = select.value;
  const unique = [...new Set([...fallback, ...values].filter(Boolean))];
  select.textContent = "";
  unique.forEach((value) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value;
    select.appendChild(option);
  });
  if (unique.includes(current)) {
    select.value = current;
  }
}

function formatPoint(value) {
  return Array.isArray(value)
    ? value.map((item) => Number(item).toFixed(3)).join(", ")
    : "-";
}

function updateVisionStatus(status) {
  const pill = $("visionStatusPill");
  const ok = Boolean(status.ok);
  pill.textContent = ok ? "Detect only" : "Vision error";
  pill.classList.toggle("waiting", !ok);

  $("visionFps").textContent = Number(status.fps || 0).toFixed(2);
  $("visionModel").textContent =
    status.model_path ||
    status.configured_model_path ||
    status.fallback_model_path ||
    "No model";
  $("visionConfidence").textContent =
    status.confidence_threshold === null || status.confidence_threshold === undefined
      ? "n/a"
      : Number(status.confidence_threshold).toFixed(2);

  $("visionDryRun").checked = true;

  const details = [];
  if (!status.detector_running) {
    details.push("Detector is not publishing status.");
  }
  if (status.error) {
    details.push(status.error);
  }
  if (!status.source_ok && status.detector_running) {
    details.push(`Source unavailable (${status.source_type || "unknown"}).`);
  }
  setVisionError(details.join(" "));
}

function renderVisionDetections(detections) {
  const body = $("visionDetectionsBody");
  body.textContent = "";

  if (!Array.isArray(detections) || detections.length === 0) {
    const row = document.createElement("tr");
    const cell = document.createElement("td");
    cell.colSpan = 5;
    cell.textContent = "No detections";
    row.appendChild(cell);
    body.appendChild(row);
    return;
  }

  detections.forEach((detection) => {
    const row = document.createElement("tr");
    [
      detection.id,
      detection.class_name,
      Number(detection.confidence || 0).toFixed(2),
      Array.isArray(detection.center_pixel)
        ? detection.center_pixel.join(", ")
        : "",
      Array.isArray(detection.bbox) ? detection.bbox.join(", ") : "",
    ].forEach((value) => {
      const cell = document.createElement("td");
      cell.textContent = String(value ?? "");
      row.appendChild(cell);
    });
    body.appendChild(row);
  });
}

function renderSelectedTarget(result) {
  const panel = $("selectedTargetPanel");
  const status = $("selectedTargetStatus");
  panel.hidden = false;
  lastSelectedTarget = result || null;

  const selected = Boolean(result?.selected);
  status.textContent = selected ? "Selected" : "Rejected";
  status.classList.toggle("waiting", !selected);

  if (!selected) {
    $("selectedTargetId").textContent = "-";
    $("selectedTargetClass").textContent = "-";
    $("selectedTargetConfidence").textContent = "-";
    $("selectedTargetPixel").textContent = "-";
    $("selectedTargetRobot").textContent = "-";
    $("selectedTargetPick").textContent = "-";
    $("selectedTargetPlace").textContent = result?.reason || "-";
    return;
  }

  $("selectedTargetId").textContent = String(result.id ?? "-");
  $("selectedTargetClass").textContent = result.class_name || "-";
  $("selectedTargetConfidence").textContent =
    result.confidence === undefined ? "-" : Number(result.confidence).toFixed(3);
  $("selectedTargetPixel").textContent = formatPoint(result.center_pixel);
  $("selectedTargetRobot").textContent = formatPoint(result.robot_xy);
  $("selectedTargetPick").textContent = formatPoint(result.pick_pose);
  $("selectedTargetPlace").textContent =
    `${result.place_id || "-"}: ${formatPoint(result.place_pose)}`;
}

function renderSafety(report) {
  const allowed = Boolean(report?.allowed);
  const pill = $("safetyStatusPill");
  pill.textContent = allowed ? "Safe" : "Blocked";
  pill.classList.toggle("waiting", !allowed);
  allowRealMotion = Boolean(report?.config?.allow_real_motion);
  $("visionPickSelected").disabled = !allowRealMotion;
  $("realPickStatusPill").textContent = allowRealMotion ? "Armed" : "Locked";
  $("realPickStatusPill").classList.toggle("waiting", !allowRealMotion);

  const checks = Array.isArray(report?.checks) ? report.checks : [];
  checks.forEach((check) => {
    const row = document.querySelector(
      `.safety-check[data-check="${check.name}"]`
    );
    if (!row) {
      return;
    }
    row.classList.toggle("ready", Boolean(check.ok));
    row.classList.toggle("warn", !check.ok && check.severity === "warning");
    row.classList.toggle("waiting", !check.ok && check.severity !== "warning");
    const strong = row.querySelector("strong");
    strong.textContent = check.ok ? "OK" : check.reason;
    strong.title = check.reason;
  });

  const messages = [];
  if (Array.isArray(report?.errors) && report.errors.length) {
    messages.push(report.errors.join("; "));
  }
  if (Array.isArray(report?.warnings) && report.warnings.length) {
    messages.push(report.warnings.join("; "));
  }
  setSafetyError(messages.join(" "));
}

function renderMotionPreview(result) {
  const body = $("motionPreviewBody");
  const pill = $("previewStatusPill");
  const sequence = Array.isArray(result?.motion_sequence)
    ? result.motion_sequence
    : [];

  body.textContent = "";
  pill.textContent = result?.accepted ? "Preview ready" : "No preview";
  pill.classList.toggle("waiting", !result?.accepted);

  if (sequence.length === 0) {
    const row = document.createElement("tr");
    const cell = document.createElement("td");
    cell.colSpan = 5;
    cell.textContent = result?.reason || "No preview";
    row.appendChild(cell);
    body.appendChild(row);
    return;
  }

  sequence.forEach((step) => {
    const row = document.createElement("tr");
    const safety = step.safety_result || {};
    [
      step.step,
      step.command,
      formatPoint(step.pose),
      step.simulated ? "yes" : "no",
      safety.allowed ? "OK" : safety.reason || "blocked",
    ].forEach((value) => {
      const cell = document.createElement("td");
      cell.textContent = String(value ?? "");
      row.appendChild(cell);
    });
    body.appendChild(row);
  });
}

function renderCalibration(calibration) {
  const pill = $("calibrationStatusPill");
  const complete = Boolean(calibration.is_complete);
  pill.textContent = complete ? "Ready" : `${calibration.point_count || 0}/4 points`;
  pill.classList.toggle("waiting", !complete);

  const body = $("calibrationPointsBody");
  body.textContent = "";
  const imagePoints = calibration.image_points || [];
  const robotPoints = calibration.robot_points || [];
  if (imagePoints.length === 0) {
    const row = document.createElement("tr");
    const cell = document.createElement("td");
    cell.colSpan = 3;
    cell.textContent = "No calibration points";
    row.appendChild(cell);
    body.appendChild(row);
  } else {
    imagePoints.forEach((imagePoint, index) => {
      const row = document.createElement("tr");
      [
        index + 1,
        imagePoint.join(", "),
        Array.isArray(robotPoints[index]) ? robotPoints[index].join(", ") : "",
      ].forEach((value) => {
        const cell = document.createElement("td");
        cell.textContent = String(value);
        row.appendChild(cell);
      });
      body.appendChild(row);
    });
  }

  const validation = calibration.validation || {};
  const meanError = validation.mean_error_mm;
  const maxError = validation.max_error_mm;
  const maxErrorText =
    maxError === null || maxError === undefined
      ? "n/a"
      : Number(maxError).toFixed(3);
  $("calMeanError").textContent =
    meanError === null || meanError === undefined
      ? "Mean error n/a"
      : `Mean ${Number(meanError).toFixed(3)} mm / Max ${maxErrorText} mm`;

  const messages = [];
  if (Array.isArray(calibration.validation_errors) && calibration.validation_errors.length) {
    messages.push(calibration.validation_errors.join("; "));
  }
  if (validation.warning) {
    messages.push(validation.warning);
  }
  setCalibrationError(messages.join(" "));
}

function refreshVisionAnnotated() {
  $("visionAnnotated").src = `/api/vision/annotated?t=${Date.now()}`;
}

async function refreshVisionStatus() {
  try {
    const status = await getJson("/api/vision/status");
    updateVisionStatus(status);
  } catch (error) {
    $("visionStatusPill").textContent = "Vision error";
    $("visionStatusPill").classList.add("waiting");
    setVisionError(`Vision status failed: ${error.message}`);
  }
}

async function refreshVisionDetections() {
  try {
    const result = await getJson("/api/vision/detections");
    renderVisionDetections(result.detections);
    if (result.error) {
      setVisionError(result.error);
    }
  } catch (error) {
    renderVisionDetections([]);
    setVisionError(`Vision detections failed: ${error.message}`);
  }
}

async function refreshVisionOptions() {
  try {
    const [classes, places] = await Promise.all([
      getJson("/api/vision/classes"),
      getJson("/api/vision/places"),
    ]);
    setSelectOptions($("visionObjectClass"), classes.classes || [], ["all"]);
    setSelectOptions($("visionPlacePosition"), places.place_ids || []);
  } catch (error) {
    setVisionError(`Vision options failed: ${error.message}`);
  }
}

async function refreshCalibration() {
  try {
    const calibration = await getJson("/api/vision/calibration");
    renderCalibration(calibration);
  } catch (error) {
    setCalibrationError(`Calibration failed: ${error.message}`);
  }
}

async function refreshSafety() {
  try {
    const report = await getJson("/api/vision/safety");
    renderSafety(report);
  } catch (error) {
    setSafetyError(`Safety failed: ${error.message}`);
  }
}

async function refreshVision() {
  await refreshVisionOptions();
  await refreshVisionStatus();
  await refreshVisionDetections();
  await refreshCalibration();
  await refreshSafety();
  refreshVisionAnnotated();
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

$("restartConnectionButton").addEventListener("click", async () => {
  const button = $("restartConnectionButton");
  try {
    setBusy(button, true);
    log("Restarting Dobot connection...");
    const result = await api("/api/restart_connection");
    log(result.message || "Dobot restart requested. Reconnect in a few seconds.");
  } catch (error) {
    log(`Restart failed: ${error.message}`);
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

function visionSelectionPayload() {
  const manualId = $("visionManualId").value;
  return {
    object_class: $("visionObjectClass").value,
    place_id: $("visionPlacePosition").value,
    selection_mode: $("visionSelectionMode").value,
    manual_id: manualId === "" ? null : Number(manualId),
    dry_run: true,
  };
}

function visionRealPickPayload() {
  return {
    ...visionSelectionPayload(),
    dry_run: false,
    confirm_real_motion: $("visionConfirmRealMotion").checked,
    tool_type: $("visionToolType").value,
    velocity_ratio: Number($("visionVelocityRatio").value),
    acceleration_ratio: Number($("visionAccelerationRatio").value),
  };
}

async function visionDetectOnce() {
  const button = $("visionDetectOnce");
  $("visionDryRun").checked = true;

  try {
    setBusy(button, true);
    log("Vision detect once requested in dry-run mode...");
    const result = await api("/api/vision/detect_once", {
      dry_run: true,
      object_class: $("visionObjectClass").value,
      place_id: $("visionPlacePosition").value,
      place_position: $("visionPlacePosition").value,
    });
    updateVisionStatus(result.status);
    renderVisionDetections(result.detections.detections);
    refreshVisionAnnotated();
    log(result.message);
  } catch (error) {
    setVisionError(`Detect once failed: ${error.message}`);
    log(`Vision detect once failed: ${error.message}`);
  } finally {
    setBusy(button, false);
  }
}

async function selectVisionTarget() {
  const button = $("visionSelectTarget");
  $("visionDryRun").checked = true;
  const payload = visionSelectionPayload();

  try {
    setBusy(button, true);
    const result = await api("/api/vision/select_target", payload);
    renderSelectedTarget(result);
    await refreshSafety();
    if (result.selected) {
      setVisionError("");
      log(
        `Selected ${result.class_name} id=${result.id} for ${result.place_id}.`
      );
    } else {
      setVisionError(result.reason || "Target selection rejected.");
      log(`Target selection rejected: ${result.reason || "no target"}`);
    }
  } catch (error) {
    setVisionError(`Select target failed: ${error.message}`);
    log(`Target selection failed: ${error.message}`);
  } finally {
    setBusy(button, false);
  }
}

async function validateVisionPick() {
  const button = $("visionValidatePick");
  try {
    setBusy(button, true);
    const report = await api("/api/vision/validate_pick", {
      selected_target: lastSelectedTarget,
      dry_run: true,
    });
    renderSafety(report);
    log(report.allowed ? "Safety validation passed." : `Safety blocked: ${report.reason}`);
  } catch (error) {
    setSafetyError(`Validate pick failed: ${error.message}`);
    log(`Safety validation failed: ${error.message}`);
  } finally {
    setBusy(button, false);
  }
}

async function previewVisionPick() {
  const button = $("visionPreviewPick");
  $("visionDryRun").checked = true;

  try {
    setBusy(button, true);
    const result = await api("/api/vision/preview_pick", visionSelectionPayload());
    if (result.selected_target) {
      renderSelectedTarget(result.selected_target);
    }
    if (result.safety) {
      renderSafety(result.safety);
    } else {
      await refreshSafety();
    }
    renderMotionPreview(result);
    log(
      result.accepted
        ? "Dry-run motion preview generated."
        : `Preview blocked: ${result.reason || "not accepted"}`
    );
  } catch (error) {
    renderMotionPreview({ accepted: false, reason: error.message });
    log(`Preview failed: ${error.message}`);
  } finally {
    setBusy(button, false);
  }
}

async function pickSelectedVisionTarget() {
  const button = $("visionPickSelected");
  if (!allowRealMotion) {
    setRealPickError("allow_real_motion=false; real pick is locked.");
    return;
  }

  try {
    setBusy(button, true);
    setRealPickError("");
    const result = await api("/api/vision/pick_selected", visionRealPickPayload());
    if (result.selected_target) {
      renderSelectedTarget(result.selected_target);
    }
    if (result.safety) {
      renderSafety(result.safety);
    }
    if (result.motion_sequence) {
      renderMotionPreview({ accepted: Boolean(result.accepted), motion_sequence: result.motion_sequence });
    }
    if (!result.accepted) {
      setRealPickError(result.reason || "Real pick rejected.");
      log(`Real pick rejected: ${result.reason || "not accepted"}`);
      return;
    }
    log(result.message || "Real pick executed.");
  } catch (error) {
    setRealPickError(`Pick selected failed: ${error.message}`);
    log(`Pick selected failed: ${error.message}`);
  } finally {
    setBusy(button, false);
  }
}

async function cancelVisionPick() {
  const button = $("visionCancelPick");
  try {
    setBusy(button, true);
    const result = await api("/api/vision/cancel", {});
    log(result.message || `Cancel requested. goals_canceling=${result.goals_canceling}`);
  } catch (error) {
    setRealPickError(`Cancel failed: ${error.message}`);
    log(`Cancel failed: ${error.message}`);
  } finally {
    setBusy(button, false);
  }
}

async function addCalibrationPoint() {
  const button = $("calAddPoint");
  try {
    setBusy(button, true);
    const calibration = await api("/api/vision/calibration/add_point", {
      image_point: [Number($("calImageU").value), Number($("calImageV").value)],
      robot_point: [Number($("calRobotX").value), Number($("calRobotY").value)],
    });
    renderCalibration(calibration);
    log("Calibration point added.");
  } catch (error) {
    setCalibrationError(`Add point failed: ${error.message}`);
    log(`Calibration add point failed: ${error.message}`);
  } finally {
    setBusy(button, false);
  }
}

async function computeCalibration() {
  const button = $("calCompute");
  try {
    setBusy(button, true);
    const calibration = await api("/api/vision/calibration/compute", {});
    renderCalibration(calibration);
    const meanError = calibration.validation?.mean_error_mm;
    log(`Homography computed. Mean error ${meanError ?? "n/a"} mm.`);
  } catch (error) {
    setCalibrationError(`Compute failed: ${error.message}`);
    log(`Calibration compute failed: ${error.message}`);
  } finally {
    setBusy(button, false);
  }
}

async function testCalibrationPoint() {
  const button = $("calTestPoint");
  try {
    setBusy(button, true);
    const result = await api("/api/vision/calibration/test_point", {
      u: Number($("calTestU").value),
      v: Number($("calTestV").value),
    });
    $("calTestResult").textContent =
      `Robot X=${Number(result.robot_xy[0]).toFixed(3)}, ` +
      `Y=${Number(result.robot_xy[1]).toFixed(3)}`;
    const warning = result.validation?.warning || "";
    setCalibrationError(warning);
    log("Calibration test point converted.");
  } catch (error) {
    setCalibrationError(`Test point failed: ${error.message}`);
    log(`Calibration test failed: ${error.message}`);
  } finally {
    setBusy(button, false);
  }
}

$("gripperOpen").addEventListener("click", () => setGripper("open"));
$("gripperClose").addEventListener("click", () => setGripper("close"));
$("suctionOn").addEventListener("click", () => setSuction(true));
$("suctionOff").addEventListener("click", () => setSuction(false));
$("visionDetectOnce").addEventListener("click", visionDetectOnce);
$("visionSelectTarget").addEventListener("click", selectVisionTarget);
$("visionValidatePick").addEventListener("click", validateVisionPick);
$("visionPreviewPick").addEventListener("click", previewVisionPick);
$("visionPickSelected").addEventListener("click", pickSelectedVisionTarget);
$("visionCancelPick").addEventListener("click", cancelVisionPick);
$("visionRefresh").addEventListener("click", refreshVision);
$("calAddPoint").addEventListener("click", addCalibrationPoint);
$("calCompute").addEventListener("click", computeCalibration);
$("calTestPoint").addEventListener("click", testCalibrationPoint);
$("calRefresh").addEventListener("click", refreshCalibration);
$("visionDryRun").addEventListener("change", () => {
  if (!$("visionDryRun").checked) {
    $("visionDryRun").checked = true;
    setVisionError("Vision Pick is dry-run only in this phase.");
    log("Vision Pick remains dry-run only.");
  }
});

refreshStatus();
refreshVision();
setInterval(refreshStatus, 1000);
setInterval(refreshVision, 2500);
