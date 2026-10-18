import pandas as pd

def excel_to_csv(input_excel_file, output_csv_file):
    try:
        # Read Excel file
        df = pd.read_excel(input_excel_file)

        # Write to CSV file
        df.to_csv(output_csv_file, index=False)
        print(f"CSV file '{output_csv_file}' created successfully.")
    except Exception as e:
        print("Error converting Excel to CSV:", e)

if __name__ == "__main__":
    # Input Excel file path
    input_excel_file = "ncdata.xlsx"

    # Output CSV file path
    output_csv_file = "ncdata.csv"

    # Call the function to convert Excel to CSV
    excel_to_csv(input_excel_file, output_csv_file)
