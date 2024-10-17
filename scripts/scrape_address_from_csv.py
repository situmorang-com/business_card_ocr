import os
import csv

# Define the folder path for input files
input_folder = os.path.join(os.path.dirname(__file__), '..', 'input')
output_folder = os.path.join(os.path.dirname(__file__), '..', 'data')
output_file = os.path.join(output_folder, 'alamat_usaha.csv')

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Open the output file for writing
with open(output_file, mode='w', encoding='utf-8', newline='') as out_csv:
    csv_writer = csv.writer(out_csv, quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['alamat_usaha'])  # Write the header row

    # Loop through all files in the input folder
    for file_name in os.listdir(input_folder):
        # Construct full file path
        file_path = os.path.join(input_folder, file_name)
        
        # Check if the file is a CSV file
        if os.path.isfile(file_path) and file_name.endswith('.