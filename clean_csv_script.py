import csv

def clean_csv(input_file, output_file):
    try:
        # Open input CSV file for reading
        with open(input_file, mode='r', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            # Skip header
            header = next(reader)

            # Open output CSV file for writing
            with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
                writer = csv.writer(outfile)
                writer.writerow(header)  # Write header back

                # Iterate through rows
                for row in reader:
                    cleaned_row = []
                    for value in row:
                        # Strip leading/trailing spaces
                        cleaned_value = value.strip()
                        # Remove commas and dots
                        cleaned_value = cleaned_value.replace(',', '')
                        cleaned_value = cleaned_value.replace('.', '')
                        cleaned_row.append(cleaned_value)
                    writer.writerow(cleaned_row)

        print("CSV file cleaned successfully!")

    except Exception as e:
        print("Error cleaning CSV file:", e)

if __name__ == "__main__":
    input_file = "acpc 21.csv"  # Path to your input CSV file
    output_file = "cleaned_acpc.csv"  # Path to save the cleaned CSV file
    clean_csv(input_file, output_file)
