import cv2
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
from io import BytesIO

# Function to load content from a text file
def load_content(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error loading content from {filepath}: {e}")
        return None


# Function to load coordinates from a text file
def load_coordinates(filepath):
    coordinates = []
    with open(filepath, 'r') as file:
        for line in file:
            coord = tuple(map(int, line.strip().split(',')))
            coordinates.append(coord)
    print(coordinates)
    return coordinates


def create_text_image(text, font_scale, font_color=(0, 0, 0), font_thickness=5, line_spacing=30):
    # Set font, scale, and thickness
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    # Split the input text into lines
    lines = text.split('\n')
    
    # Determine the maximum width and total height of the text image
    max_width = 0
    total_height = 0
    for line in lines:
        text_size = cv2.getTextSize(line, font, font_scale, font_thickness)[0]
        max_width = max(max_width, text_size[0])
        total_height += text_size[1]

    # Add extra space between lines
    total_height += (len(lines) - 1) * line_spacing

    # Create a blank image with white background
    text_image = np.ones((total_height, max_width, 3), dtype=np.uint8) * 255
    
    # Write text onto the image line by line
    y_offset = 0
    for line in lines:
        text_size = cv2.getTextSize(line, font, font_scale, font_thickness)[0]
        x_offset = (max_width - text_size[0]) // 2
        cv2.putText(text_image, line, (x_offset, y_offset + text_size[1]), font, font_scale, font_color, font_thickness)
        y_offset += text_size[1] + line_spacing  # Add line spacing

    return text_image


def resize_image(image, width, height):
    return cv2.resize(image, (width, height))

# Function to replace processed images with content from text files
def replace_images(input_coordinates_dir, input_images_dir, input_math_dir, output_img_dir):
    for txt_file in os.listdir(input_coordinates_dir):
        if txt_file.endswith('.txt'):
            image_name = os.path.splitext(os.path.basename(txt_file))[0].split('_')[1] + '.png'
            image_path = os.path.join(input_images_dir, image_name)
            coordinates = load_coordinates(os.path.join(input_coordinates_dir, txt_file))
            # Load the image
            image = cv2.imread(image_path)

            # Replace processed images with content from text files
            for idx, (x, y, w, h) in enumerate(coordinates, start=1):
                math_filename = os.path.splitext(os.path.basename(txt_file))[0].split('_')[1] + f'_{idx}.txt'
                math_filepath = os.path.join(input_math_dir, math_filename)
                content = load_content(math_filepath)
                math_image = create_text_image(content, 10)
                cv2.imwrite('math_image.png', math_image)
                math_image_resized = resize_image(math_image, w, h)
                image[y:y+h, x:x+w] = math_image_resized
            # Save the modified image
            cv2.imwrite(os.path.join(output_img_dir, image_name), image)
            
if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python script.py input_txt_directory output_image_directory")
        sys.exit(1)

    input_coordinates_dir = sys.argv[1]
    input_images_dir = sys.argv[2]
    input_math_dir = sys.argv[3]
    output_image_dir = sys.argv[4]
    

    # Replace processed images with content from text files
    os.makedirs(output_image_dir, exist_ok=True)
    replace_images(input_coordinates_dir, input_images_dir, input_math_dir, output_image_dir)
