import cv2
import os

# Check for aruco availability
if not hasattr(cv2, 'aruco'):
    raise ImportError("cv2.aruco module is not available. Please install opencv-contrib-python.")

from cv2 import aruco

# Configuration
output_dir = "../markers"
dictionary_id = aruco.DICT_6X6_250
num_markers = 10  # Adjust to number of pages you want

# Create marker images
aruco_dict = aruco.getPredefinedDictionary(dictionary_id)
os.makedirs(output_dir, exist_ok=True)

try:
    for marker_id in range(num_markers):
              marker_img = aruco.drawMarker(aruco_dict, marker_id, 700)
        filepath = os.path.join(output_dir, f"marker_{marker_id}.png")
        cv2.imwrite(filepath, marker_img)
    print(f"Saved {num_markers} markers to {output_dir}")
except AttributeError as e:
    print("Failed to generate markers. Your OpenCV version might not support aruco.drawMarker.")
    print("Please ensure you have opencv-contrib-python installed.")
    raise e
