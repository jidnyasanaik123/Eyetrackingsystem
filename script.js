document.getElementById("startTest").addEventListener("click", function() {
    document.getElementById("startScreen").classList.add("hidden");
    document.getElementById("eyeTrackingScreen").classList.remove("hidden");

    // Start User's Webcam in Circular Mode
    navigator.mediaDevices.getUserMedia({ video: true }) 
        .then(function(stream) {
            let videoElement = document.getElementById("video");
            videoElement.srcObject = stream;
        })
        .catch(function(error) {
            alert("Camera access denied. Please allow camera permissions in your browser.");
            console.error("Camera error:", error);
        });
});

document.getElementById("startTracking").addEventListener("click", function() {
    document.getElementById("eyeTrackingScreen").classList.add("hidden");
    document.getElementById("cameraAccessScreen").classList.remove("hidden");

    // Stop User's Webcam (to switch to Flask stream)
    let videoElement = document.getElementById("video");
    if (videoElement.srcObject) {
        videoElement.srcObject.getTracks().forEach(track => track.stop());
        videoElement.srcObject = null;
    }

    // Start Flask Video Stream (Real-time Eye Tracking)
    let streamElement = document.getElementById("videoStream");
    streamElement.src = "http://127.0.0.1:5000/video_feed"; // Change to your Flask server URL if needed
});

document.getElementById("finishTest").addEventListener("click", function() {
    alert("Test Completed!");
    
    // Stop Flask Stream by resetting src
    let streamElement = document.getElementById("videoStream");
    streamElement.src = "";
});
