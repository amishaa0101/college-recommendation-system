import csv

# Define the path to the cleaned CSV file
input_file = 'cleaned_data.csv'
output_file = 'cleaned_data_fixed.csv'

# Open the CSV file and create a new CSV file for writing
with open(input_file, mode='r', encoding='utf-8', newline='') as file, \
        open(output_file, mode='w', encoding='utf-8', newline='') as output:
    
    csv_reader = csv.reader(file)
    csv_writer = csv.writer(output)
    
    header = next(csv_reader)  # Get the header row
    num_fields_header = len(header)  # Get the number of fields in the header row
    
    csv_writer.writerow(header)  # Write the header to the new file
    
    for line_num, row in enumerate(csv_reader, start=2):  # Start from line 2 (after header)
        if len(row) == num_fields_header:  # Check if the row has the correct number of fields
            csv_writer.writerow(row)  # Write the row to the new file

print("CSV file cleaned and saved to:", output_file)
