import os
import subprocess

def generate_pylint_report(directory):
    print("--------------------------------------------------------")
    """
    Generate PyLint reports for all Python files in the specified directory.
    Args:
        directory (str): The path to the directory containing Python files.
    """
    for root, dirs, files in os.walk(directory):
        print("-------------------------------------------")
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                pylint_report_path = file_path.replace(".py", "_pylint_report.txt")
                # Run PyLint and save the report to a file
                subprocess.run(["pylint", file_path, "--output-format=text", "--exit-zero"],
                               stdout=open(pylint_report_path, "w"),
                               stderr=subprocess.PIPE)
                print(f"PyLint report generated for {file_path} at {pylint_report_path}")

# Specify the directory containing your project's Python files
project_directory = os.getcwd()

# Generate PyLint reports for the project
generate_pylint_report(project_directory)
