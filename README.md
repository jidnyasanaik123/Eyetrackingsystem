# Eye Tracking System
A real-time eye-tracking application using Flask (Python backend) and JavaScript (frontend) to detect facial landmarks and track pupil movements.

## 🚀Features
- ✅ Real-time eye tracking using dlib and OpenCV
- ✅ Frontend integration with a Flask video stream
- ✅ User-friendly web interface
- ✅ Supports multiple devices over a network

## 📌 Setup Instructions
### 1. Clone the Repository  
git clone https://github.com/yourusername/eye-tracking.git  cd eye-tracking

### 2. Install Dependencies 
- Install Python Packages
- Make sure you have Python 3.9+ installed.
- Run the following command to install required libraries: **pip install flask opencv-python dlib numpy**

### 3. Download the Pre-Trained Model
- [PreTrained Model](https://github.com/davisking/dlib-models/blob/master/shape_predictor_68_face_landmarks.dat.bz2/)
- After downloading
- Extract the .bz2 file using 7-Zip or any extraction tool.
- Move shape_predictor_68_face_landmarks.dat to the project folder.

### 4. Run the Backend (Flask Server)
- python app.py
### 📌 Expected Output:
 - Running on http://127.0.0.1:5000
 -  Running on http://192.168.X.X:5000 (For local network access)
- 🚀 Open http://127.0.0.1:5000/video_feed in a browser to check the camera feed.

### 5.Run the Frontend
- Simply open index.html in your browser.
- ✅ Click "Start Test" → Starts the user's webcam.
- ✅ Click "Start Tracking Now" → Switches to Flask eye-tracking feed.
- ✅ Click "Finish Test" → Stops tracking.

