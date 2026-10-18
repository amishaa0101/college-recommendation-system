import pandas as pd
import PyPDF2
from tabula import read_pdf

def clean_college_data(df):
    """
    Cleans the college data extracted from the Excel file.
    """
    # Extracting the parts of "College Name"
    df[['College Name', 'Address', 'Contact No', 'Email', 'Website']] = df['name of institutes'].str.split("\n", 4, expand=True)

    # Split "Provisional Intake as per ACIET /University" into separate columns
    df[['Civil Engineering', 'Computer Engineering', 'Electrical Engineering',
        'E&C Engineering', 'E&I Engineering', 'Environmental Engineering', 'Mechanical Engineering', 'Total Intake']] = df['Intake'].str.split(" ", expand=True)

    # Split "Facilities" into separate columns
    df[['Boys Hostel', 'Girls Hostel', 'Mess', 'Transportation']] = df['facilities'].str.split("\n", expand=True)

    # Clean up columns
    df['Address'] = df['Address'].str.strip()
    df['Contact No'] = df['Contact No'].str.extract(r'Contact No:(\d+)', expand=False)
    df['Email'] = df['Email'].str.extract(r'Email\s*:\s*(\S+@\S+)', expand=False)
    df['Website'] = df['Website'].str.extract(r'Website\s*:\s*(http\S+)', expand=False)
    df['District'] = df['district'].str.strip()
    df['Tuition Fees'] = df['tution fees'].str.extract(r'(\d+)').astype(float)

    # Drop intermediate columns
    df = df.drop(columns=['name of institutes', 'Intake', 'facilities', 'district', 'tution fees'])

    return df


def main():
    # Path to your Excel file
    excel_file = "cdata.xlsx"
    
    # Read Excel file into DataFrame
    df = pd.read_excel(excel_file)
    
    # Clean the extracted college data
    cleaned_df = clean_college_data(df)
    
    # Save the cleaned DataFrame to a CSV file
    csv_file = "converted_colleges.csv"
    cleaned_df.to_csv(csv_file, index=False)
    
    print("CSV file saved successfully:", csv_file)

if __name__ == "__main__":
    main()
