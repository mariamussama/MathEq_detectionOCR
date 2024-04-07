from pdf2image import convert_from_path
import sys
import os


def create_images_from_pdf(input_pdf, output_dir):

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # pdf_name = os.path.basename(input_pdf).split(".pdf")[0]
    # output_path = os.path.join(output_dir, pdf_name)
    # if not os.path.exists(output_path):
    #     os.makedirs(output_path)
    
    pages = convert_from_path(input_pdf, 600)
    for i, page in enumerate(pages):
        page.save(os.path.join(output_dir, f"{i + 1}.png"), 'PNG')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 convert_pdf_to_image.py <input_pdf_file> <output_dir>")
        sys.exit(1)
    input_pdf = sys.argv[1]
    output_dir = sys.argv[2]
    create_images_from_pdf(input_pdf, output_dir)
