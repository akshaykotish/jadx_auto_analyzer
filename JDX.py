import os
import subprocess
import openpyxl
from openpyxl import Workbook

# Function to decompile APKs using Jadx
def decompile_apk(jadx_path, apk_path, output_dir):
    cmd = f"{jadx_path} -d {output_dir} {apk_path}"
    subprocess.run(cmd, shell=True)

# Function to search for a specific string in decompiled files
def search_string_in_files(directory, search_string):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".java") or file.endswith(".xml"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    if search_string in f.read():
                        return True
    return False

# Main function to process APKs
def process_apks(apk_folder, jadx_path, search_string, output_excel):
    apks = [f for f in os.listdir(apk_folder) if f.endswith(".apk")]
    results = []

    for apk in apks:
        apk_path = os.path.join(apk_folder, apk)
        decompiled_dir = os.path.join(apk_folder, f"decompiled_{apk}")
        
        # Decompile the APK
        decompile_apk(jadx_path, apk_path, decompiled_dir)
        
        # Search for the string in decompiled files
        found = search_string_in_files(decompiled_dir, search_string)
        
        # Append the result
        results.append((apk, "Yes" if found else "No"))
        
        # Clean up the decompiled files
        subprocess.run(f"rm -rf {decompiled_dir}", shell=True)

    # Write results to an Excel file
    wb = Workbook()
    ws = wb.active
    ws.append(["APK Name", "String Found"])
    for result in results:
        ws.append(result)

    wb.save(output_excel)

# Configuration
apk_folder = "/path/to/apk/folder"
jadx_path = "/path/to/jadx/bin/jadx"
search_string = "your_search_string"
output_excel = "results.xlsx"

# Run the script
process_apks(apk_folder, jadx_path, search_string, output_excel)


# Copy code
# pip install openpyxl
# Download and set up Jadx:
# Ensure you have Jadx installed on your system. If not, download it from the Jadx GitHub repository.
# The Python script: