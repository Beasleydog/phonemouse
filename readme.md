# Phone Mouse Experiment

This project is an experimental implementation of a "phone mouse" that uses a smartphone's accelerometer to mimic the functionality of a real computer mouse. By leveraging the phone's motion sensors, users can control their computer's cursor movements simply by tilting and moving their phone. Additionally, users can perform mouse clicks using the phone's volume buttons.

## Features

- Real-time cursor control using phone's accelerometer data
- Calibration system for improved accuracy
- Lift detection to pause/resume cursor movement
- Velocity-based movement for smoother cursor control
- Web-based interface for easy connection between phone and computer
- Mouse click functionality using phone's volume buttons

## Technologies Used

- **Backend:**

  - Python
  - Flask (Web framework)
  - Flask-SocketIO (Real-time communication)

- **Frontend:**
  - HTML/JavaScript (Web interface)
  - Socket.IO client (Real-time communication with server)

## How It Works

1. The Flask server runs on the computer you want to control.
2. Connect your phone to the same network and access the web interface.
3. The phone sends accelerometer data to the server via WebSocket.
4. The server processes the data, applying calibration, smoothing, and velocity calculations.
5. PyAutoGUI moves the computer's cursor based on the processed accelerometer data.
6. Volume up button triggers a left click, while volume down button triggers a right click.

## Notes

This project is experimental and may require fine-tuning of sensitivity and threshold values for optimal performance. The current implementation uses HTTPS with a self-signed certificate for secure communication.
