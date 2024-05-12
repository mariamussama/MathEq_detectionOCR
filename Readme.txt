# Mathematical Equation Detection Tool

## Introduction
The Mathematical Equation Detection Tool is designed to assist visually impaired individuals by converting mathematical equations in PDF documents into a format readable by screen readers. This tool detects equations in PDFs, extracts them, and converts them into a format suitable for accessibility purposes.

Installation
- Clone the repository:
   https://github.com/mariamussama/MathEq_detectionOCR.git


To use the tool, execute the run.py script:
python run.py input.pdf output.pdf

Script Details
convert_pdf_to_image.py: Converts the PDF document to images for processing.
Detect_YOLO.py: Utilizes YOLO object detection to identify regions containing mathematical equations within the images.
detect_toMathPix.py: Converts the detected equation images into a format suitable for input to the MathPix API.
replace_math_pdf.py: Replaces the detected equations in the PDF document with the output from the MathPix API.