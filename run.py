import subprocess

def call_script(script_path, args):
    """
    Call a Python script with arguments.
    :param script_path: Path to the Python script.
    :param args: Arguments to pass to the script.
    """
    subprocess.run(["python", script_path] + args)
    
if __name__ == "__main__":
    # List of Python scripts to execute with their respective arguments
    scripts_to_execute_1 = [
        ("convert_pdf_to_image.py", ["test.pdf", "images"]),
        # ("detect_toMathPix.py", ["YOLO_output","MathPix_input"]),
        # ("replace_math.py", ["MathPix_input", "images", "MathPix_output", "With_MathML"]),
        # Add more scripts as needed with their arguments
    ]
    scripts_to_execute_2 = [
        ("detect_toMathPix.py", ["YOLO_output","MathPix_input"]),
        ("replace_math.py", ["MathPix_input", "images", "MathPix_output", "With_MathML"]),
        # Add more scripts as needed with their arguments
    ]
    # Execute each script sequentially
    for script_info in scripts_to_execute_1:
        script_path, args = script_info
        print(f"Executing {script_path} with arguments: {args}")
        call_script(script_path, args)
    subprocess.run("yolo task=detect mode=predict model=best.pt conf=0.25 source='images/*' save=true show_labels=False")
    for script_info in scripts_to_execute_2:
        script_path, args = script_info
        print(f"Executing {script_path} with arguments: {args}")
        call_script(script_path, args)
