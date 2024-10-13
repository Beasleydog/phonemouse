from flask import Flask, render_template, url_for
from flask_socketio import SocketIO
from flask_cors import CORS
import logging
import pyautogui
from collections import deque
from time import time
import numpy as np

SENSITIVITY = 5
CALIBRATION_TIME = 3
MOVEMENT_THRESHOLD = 0.5
SMOOTHING_FACTOR = 0.2
Z_THRESHOLD = 0.5
VELOCITY_DECAY = 0.8
MAX_VELOCITY = 50

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

calibration_data = {'x': deque(maxlen=100), 'y': deque(maxlen=100), 'z': deque(maxlen=100)}
calibration_start_time = None
offset = {'x': 0, 'y': 0, 'z': 0}
last_movement = {'x': 0, 'y': 0}
is_lifted = False
last_z = 0
velocity = {'x': 0, 'y': 0}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('accelerometer_data')
def handle_accelerometer_data(data):
    global calibration_start_time, offset, velocity, is_lifted, last_z

    if calibration_start_time is None:
        calibration_start_time = time()

    if time() - calibration_start_time <= CALIBRATION_TIME:
        for axis in ['x', 'y', 'z']:
            calibration_data[axis].append(data[axis])
    elif not offset['x'] and not offset['y'] and not offset['z']:
        for axis in ['x', 'y', 'z']:
            offset[axis] = sum(calibration_data[axis]) / len(calibration_data[axis])
        logger.info(f"Calibration complete. Offset: {offset}")
    else:
        logger.info(f"Received accelerometer data: {data}")
        
        z_movement = data['z'] - offset['z']
        if abs(z_movement) > Z_THRESHOLD:
            if z_movement > 0 and not is_lifted:
                is_lifted = True
                logger.info("Device lifted")
            elif z_movement < 0 and is_lifted:
                is_lifted = False
                logger.info("Device set down")
        
        if not is_lifted:
            accel_x = (data['x'] - offset['x']) * SENSITIVITY
            accel_y = (data['y'] - offset['y']) * SENSITIVITY
            
            velocity['x'] = velocity['x'] * VELOCITY_DECAY + accel_x
            velocity['y'] = velocity['y'] * VELOCITY_DECAY + accel_y
            
            velocity['x'] = 0 if abs(velocity['x']) < MOVEMENT_THRESHOLD else velocity['x']
            velocity['y'] = 0 if abs(velocity['y']) < MOVEMENT_THRESHOLD else velocity['y']
            
            velocity['x'] = np.clip(velocity['x'], -MAX_VELOCITY, MAX_VELOCITY)
            velocity['y'] = np.clip(velocity['y'], -MAX_VELOCITY, MAX_VELOCITY)
            
            if abs(velocity['x']) > MOVEMENT_THRESHOLD or abs(velocity['y']) > MOVEMENT_THRESHOLD:
                current_x, current_y = pyautogui.position()
                
                new_x = int(current_x + velocity['x'])
                new_y = int(current_y - velocity['y'])
                
                screen_width, screen_height = pyautogui.size()
                new_x = max(0, min(new_x, screen_width - 1))
                new_y = max(0, min(new_y, screen_height - 1))
                
                pyautogui.moveTo(new_x, new_y)
        
        last_z = data['z']

@socketio.on('mouse_click')
def handle_mouse_click(data):
    button = data['button']
    if button == 'left':
        pyautogui.click()
        logger.info("Left click performed")
    elif button == 'right':
        pyautogui.rightClick()
        logger.info("Right click performed")

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, ssl_context='adhoc')
