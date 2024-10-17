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
        if os.path.isfile(file_path) and file_name.endswith('.csv'):
            print(f'Processing file: {file_name}')
            
            # Open and read the CSV file
            with open(file_path, mode='r', encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                
                # Write the 'alamat_usaha' column to the output file
                for row in csv_reader:
                    if 'alamat_usaha' in row:
                        alamat_usaha = row['alamat_usaha']
                        # Check if the data already has quotes
                        if alamat_usaha.startswith('"') and alamat_usaha.endswith('"'):
                            formatted_alamat = f'{alamat_usaha}, 1'
                        else:
                            formatted_alamat = f'"{alamat_usaha}", 1'
                        csv_writer.writerow([formatted_alamat])

print('All CSV files processed and alamat_usaha saved.')
