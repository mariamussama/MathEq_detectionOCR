import cv2
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
from io import BytesIO
import PyPDF2
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from PIL import Image

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


def get_image_dpi(image_path):
    with Image.open(image_path) as img:
        dpi = img.info.get("dpi")
        if dpi is not None:
            return dpi
        else:
            return None


def image_to_pdf_coordinates(image_x, image_y, image_resolution, pdf_width, pdf_height):
    # Determine scaling factors
    pdf_width_pt = pdf_width * 72  # Convert width from inches to points (1 inch = 72 points)
    pdf_height_pt = pdf_height * 72  # Convert height from inches to points (1 inch = 72 points)
    scaling_factor_x = pdf_width_pt / image_resolution[0]  # Scale factor for x-coordinate
    scaling_factor_y = pdf_height_pt / image_resolution[1]  # Scale factor for y-coordinate
    
    # Apply scaling factors to convert image coordinates to PDF coordinates
    pdf_x = image_x * scaling_factor_x
    pdf_y = pdf_height_pt - (image_y * scaling_factor_y)  # Invert y-coordinate as PDF coordinates start from bottom-left
    
    return pdf_x, pdf_y


def get_pdf_page_size(pdf_path, page_number=0):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        page = pdf_reader.pages[page_number]
        page_width = page.mediabox.width
        page_height = page.mediabox.height
        return page_width, page_height
    

# Function to replace processed images with content from text files
def replace_inPDF(input_coordinates_dir, input_pdf_path, input_math_dir, output_path):
    pdf_width, pdf_height = get_pdf_page_size(input_pdf_path)
    with open(input_pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        pdf_writer = PyPDF2.PdfWriter()
        
        for txt_file in os.listdir(input_coordinates_dir):
            if txt_file.endswith('.txt') :
                page_num = int(os.path.splitext(os.path.basename(txt_file))[0].split('_')[1])
                coordinates = load_coordinates(os.path.join(input_coordinates_dir, txt_file))
                page = pdf_reader.pages[page_num-1]
                n = 0
                packet = BytesIO()
                can = canvas.Canvas(packet, pagesize=letter)
                # Replace processed images with content from text files
                for idx, (x, y, w, h) in enumerate(coordinates, start=1):
                    y_content = y + (h/2)
                    math_filename = os.path.splitext(os.path.basename(txt_file))[0].split('_')[1] + f'_{idx}.txt'
                    math_filepath = os.path.join(input_math_dir, math_filename)
                    if not os.path.exists(math_filepath):
                        print(f"Math file not found: {math_filepath}")
                        continue
                    else:
                        content = load_content(math_filepath)
                    
                        # Draw the text onto the canvas
                        scaling_factor_x = int(pdf_width) / 4961
                        scaling_factor_y = int(pdf_height) / 7016
                        pdf_x = x * scaling_factor_x
                        pdf_y = int(pdf_height) -( y * scaling_factor_y)
                        pdf_y_content = int(pdf_height) -(y_content * scaling_factor_y)
                        pdf_h= h * scaling_factor_y
                        pdf_w = w * scaling_factor_x
                        print(pdf_x, pdf_y)
                        # can.drawString(10, 10 + (n*15), content)
                        can.setFillColor(colors.white) 
                        can.setStrokeColor(colors.white)
                        can.rect(pdf_x, pdf_y, pdf_w, -pdf_h, fill=1)
                        can.setFillColor(colors.black)
                        can.drawString(pdf_x, pdf_y_content, content)
                        n = n +1
                    
                # Close the canvas
                # can.drawString(10, 100, "Hello world")
                can.save()

                # Move to the beginning of the StringIO buffer
                packet.seek(0)
                new_pdf_reader = PyPDF2.PdfReader(packet)
                if new_pdf_reader is None or len(new_pdf_reader.pages) == 0:
                    print(f"No content found in {math_filepath}")
                    continue
                else:
                    new_page = new_pdf_reader.pages[0]

                # Merge the modified page with the original page
                page.merge_page(new_page)
                pdf_writer.add_page(page)

                # Save the modified image
        with open(output_path, 'wb') as output_file:
                    pdf_writer.write(output_file)     
                
                
                       
if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python script.py input_coordinates_dir input_pdf_path input_math_dir output_path")
        sys.exit(1)

    input_coordinates_dir = sys.argv[1]
    input_pdf_path = sys.argv[2]
    input_math_dir = sys.argv[3]
    output_path = sys.argv[4]
    

    # Replace processed images with content from text files
    # os.makedirs(output_image_dir, exist_ok=True)
    replace_inPDF(input_coordinates_dir, input_pdf_path, input_math_dir, output_path)
