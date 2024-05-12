import cv2
import numpy as np
import os
import sys

# Function to save coordinates to a text file
def save_coordinates(filepath, coordinates):
    with open(filepath, 'w') as file:
        for coord in coordinates:
            file.write(','.join(map(str, coord)) + '\n')

# Function to process an image
def process_image(image_path, output_dir):
    # Load the image
    image = cv2.imread(image_path)
    image_name = os.path.splitext(os.path.basename(image_path))[0]

    # Convert image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define range of red color in HSV
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    # Threshold the HSV image to get only red colors
    mask = cv2.inRange(hsv_image, lower_red, upper_red)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # List to store bounding box coordinates
    bounding_boxes = []

    # Iterate through contours and find bounding box
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        # Draw bounding box
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Save bounding box coordinates
        bounding_boxes.append((x, y, w, h))

        # Extract content framed with red color and save it
        content = image[y:y+h, x:x+w]
        cv2.imwrite(os.path.join(output_dir, f'{image_name}_{len(bounding_boxes)}.jpg'), content)

    # Save coordinates to a text file
    save_coordinates(os.path.join(output_dir, f'coordinates_{image_name}.txt'), bounding_boxes)

    # Display the image with detected red areas and bounding boxes
    # cv2.imshow('Detected Red Color', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input_directory output_directory")
        sys.exit(1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Process each image in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith('.jpg') or filename.endswith('.png'):  # Process only image files
            image_path = os.path.join(input_dir, filename)
            process_image(image_path, output_dir)
