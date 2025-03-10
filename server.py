import cv2
import dlib
import numpy as np
import base64
from flask import Flask, Response
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Load dlib's face detector and landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

def get_eye_center(landmarks, eye_points):
    """ Calculate the center of the eye based on dlib's facial landmarks. """
    x = sum([landmarks.part(n).x for n in eye_points]) // len(eye_points)
    y = sum([landmarks.part(n).y for n in eye_points]) // len(eye_points)
    return (x, y)

@socketio.on('video_frame')
def process_frame(data):
    try:
        # Convert base64 to OpenCV image
        img_data = base64.b64decode(data.split(',')[1])
        np_img = np.frombuffer(img_data, dtype=np.uint8)
        frame = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        eye_positions = {}

        for face in faces:
            landmarks = predictor(gray, face)

            # Get left and right eye centers
            left_eye_center = get_eye_center(landmarks, range(36, 42))
            right_eye_center = get_eye_center(landmarks, range(42, 48))

            # Normalize coordinates to screen size
            frame_height, frame_width = frame.shape[:2]
            screen_width = 1920  # Adjust according to screen size
            screen_height = 1080

            norm_x = int((left_eye_center[0] + right_eye_center[0]) / 2 / frame_width * screen_width)
            norm_y = int((left_eye_center[1] + right_eye_center[1]) / 2 / frame_height * screen_height)

            eye_positions = {
                "left_eye": [left_eye_center[0], left_eye_center[1]],
                "right_eye": [right_eye_center[0], right_eye_center[1]],
                "screen_x": norm_x,
                "screen_y": norm_y
            }
            print("Detected Eyes:", eye_positions)

        # Send eye positions back to frontend
        socketio.emit('eye_tracking_data', eye_positions)

    except Exception as e:
        print("Error processing frame:", e)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

