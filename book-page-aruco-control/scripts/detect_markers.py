import cv2
import json
import time
import sys

# Check for aruco availability
if not hasattr(cv2, 'aruco'):
    raise ImportError("cv2.aruco module is not available. Please install opencv-contrib-python.")

from cv2 import aruco

# Setup
dictionary_id = aruco.DICT_6X6_250
aruco_dict = aruco.getPredefinedDictionary(dictionary_id)
parameters = aruco.DetectorParameters_create()
capture = cv2.VideoCapture(0)

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
            last_id = detected_id

            with open("../chataigne/trigger.json", "w") as f:
                json.dump({"marker_id": detected_id}, f)

    aruco.drawDetectedMarkers(frame, corners, ids)
    cv2.imshow("Aruco Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()