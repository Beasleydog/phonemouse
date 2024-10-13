const socket = io();
let isTracking = false;

function handleOrientation(event) {
  const x = event.accelerationIncludingGravity.x;
  const y = event.accelerationIncludingGravity.y;
  const z = event.accelerationIncludingGravity.z;

  document.getElementById("x").textContent = x ? x.toFixed(2) : "N/A";
  document.getElementById("y").textContent = y ? y.toFixed(2) : "N/A";
  document.getElementById("z").textContent = z ? z.toFixed(2) : "N/A";

  socket.emit("accelerometer_data", { x, y, z });
}

function handleVolumeButton(event) {
  if (event.key === "VolumeUp") {
    socket.emit("mouse_click", { button: "left" });
  } else if (event.key === "VolumeDown") {
    socket.emit("mouse_click", { button: "right" });
  }
}

function requestAccelerometerPermission() {
  if (typeof DeviceMotionEvent.requestPermission === "function") {
    // iOS 13+ devices
    DeviceMotionEvent.requestPermission()
      .then((permissionState) => {
        if (permissionState === "granted") {
          window.addEventListener("devicemotion", handleOrientation);
          window.addEventListener("keyup", handleVolumeButton);
          isTracking = true;
          document.getElementById("start-button").textContent =
            "Stop Sending Data";
        } else {
          console.error("Permission denied for accessing motion data");
        }
      })
      .catch(console.error);
  } else {
    // Non iOS 13+ devices
    window.addEventListener("devicemotion", handleOrientation);
    window.addEventListener("keyup", handleVolumeButton);
    isTracking = true;
    document.getElementById("start-button").textContent = "Stop Sending Data";
  }
}

function stopTracking() {
  if (!isTracking) return;

  window.removeEventListener("devicemotion", handleOrientation);
  window.removeEventListener("keyup", handleVolumeButton);
  isTracking = false;
  document.getElementById("start-button").textContent = "Start Sending Data";
}

document.getElementById("start-button").addEventListener("click", () => {
  if (isTracking) {
    stopTracking();
  } else {
    requestAccelerometerPermission();
  }
});
