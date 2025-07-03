import cv2
import sys
from pythonosc import udp_client
import subprocess

# For OSC
client = udp_client.SimpleUDPClient("127.0.0.1", 5005)


# Check for aruco availability
if not hasattr(cv2, 'aruco'):
    raise ImportError("cv2.aruco module is not available. Please install opencv-contrib-python.")

from cv2 import aruco

# Setup
dictionary_id = aruco.DICT_6X6_250
aruco_dict = aruco.getPredefinedDictionary(dictionary_id)
parameters = aruco.DetectorParameters_create()
for i in range(3):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Webcam gevonden op index {i}")
        break
else:
    print("Geen werkende webcam gevonden")
    sys.exit(1)

capture = cap

if not capture.isOpened():
    print("Error: Could not access webcam. Is it already in use or missing?")
    sys.exit(1)
    
last_id = None

print("Starting webcam. Press 'q' to quit.")

while True:
    ret, frame = capture.read()
    if not ret:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejected = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    if ids is not None:
        id_list = ids.flatten().tolist()
        detected_id = id_list[0]  # Simplified: just use first detected marker

        if detected_id != last_id:
            print(f"Detected marker: {detected_id}")
            client.send_message("/marker_id", detected_id)
            last_id = detected_id

            # Stop precious VLC-instantion
            subprocess.call(["pkill", "-f", "VLC"])
            
            # Path to file
            video_path = f"/Users/kristienpeeters/Desktop/videos/marker_{detected_id}.MOV"
            
            # Start VLC with file, quiet and no interface
            subprocess.Popen([
                "/Applications/VLC.app/Contents/MacOS/VLC",
                #"--intf", "dummy",  # No interface
                "--play-and-exit",  # Play en exit
                #"--no-video",       # No video
                video_path
                ])

    aruco.drawDetectedMarkers(frame, corners, ids)
    cv2.imshow("Aruco Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()