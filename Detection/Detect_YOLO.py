import cv2
import numpy as np
import os
import sys
from ultralytics import YOLO

# Function to process an image
def detect(image_path, output_dir):
    filename = os.path.basename(output_dir)
    foldername = os.path.dirname(output_dir)
    model = YOLO("best.pt")
    model.predict(source = image_path, show = False, save=True, project = output_dir, name = 'images', show_labels=False)
    cv2.waitKey(0)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python Detect_YOLO.py input_directory output_directory")
        sys.exit(1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    detect(input_dir, output_dir)
