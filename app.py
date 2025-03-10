from flask import Flask, Response
import cv2
import dlib
import numpy as np

app = Flask(__name__)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

LEFT_EYE_POINTS = [36, 37, 38, 39, 40, 41]
RIGHT_EYE_POINTS = [42, 43, 44, 45, 46, 47]

def get_eye_region(landmarks, eye_points):
    return np.array([(landmarks.part(n).x, landmarks.part(n).y) for n in eye_points], np.int32)

def get_pupil_center(gray, eye_region):
    mask = np.zeros_like(gray)
    cv2.fillPoly(mask, [eye_region], 255)
    eye = cv2.bitwise_and(gray, gray, mask=mask)
    x, y, w, h = cv2.boundingRect(eye_region)
    eye = eye[y:y+h, x:x+w]
    
    _, threshold_eye = cv2.threshold(eye, 30, 255, cv2.THRESH_BINARY_INV)
    moments = cv2.moments(threshold_eye, binaryImage=True)
    if moments["m00"] != 0:
        cx = int(moments["m10"] / moments["m00"]) + x
        cy = int(moments["m01"] / moments["m00"]) + y
        return (cx, cy)
    return None

def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face in faces:
            landmarks = predictor(gray, face)

            left_eye = get_eye_region(landmarks, LEFT_EYE_POINTS)
            right_eye = get_eye_region(landmarks, RIGHT_EYE_POINTS)

            cv2.polylines(frame, [left_eye], True, (0, 255, 0), 2)
            cv2.polylines(frame, [right_eye], True, (0, 255, 0), 2)

            left_pupil = get_pupil_center(gray, left_eye)
            right_pupil = get_pupil_center(gray, right_eye)

            if left_pupil:
                cv2.circle(frame, left_pupil, 3, (0, 0, 255), -1)
            if right_pupil:
                cv2.circle(frame, right_pupil, 3, (0, 0, 255), -1)

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
    cv2.destroyAllWindows()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
