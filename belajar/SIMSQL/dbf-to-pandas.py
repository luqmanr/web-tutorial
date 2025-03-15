import dbfread
import csv
import os
import pandas as pd

def dbf_to_csv(dbf_filepath, csv_filepath):
    """
    Converts a .dbf (dBase IV) file to a .csv file.

    Args:
        dbf_filepath (str): Path to the input .dbf file.
        csv_filepath (str): Path to the output .csv file.
    """
    try:
        table = dbfread.DBF(dbf_filepath, encoding='latin1') # common encoding for dbf
        df = pd.DataFrame([list(r.values()) for r in table], columns = table.field_names)
        print(df)
        # save to CSV
        with open(csv_filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(table.field_names)  # Write header row
            for record in table:
                writer.writerow(list(record.values()))
        
        # TODO:
        # save to sqlite
        print(f"Successfully converted '{dbf_filepath}' to '{csv_filepath}'")

    except dbfread.DBFNotFound as e:
        print(f"Error: DBF file not found: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def convert_all_dbf_in_folder(input_folder, output_folder):
    """
    Converts all .dbf files in a folder to .csv files in another folder.

    Args:
        input_folder (str): Path to the folder containing .dbf files.
        output_folder (str): Path to the folder where .csv files will be saved.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".dbf"):
            dbf_filepath = os.path.join(input_folder, filename)
            csv_filepath = os.path.join(output_folder, os.path.splitext(filename)[0] + ".csv")
            dbf_to_csv(dbf_filepath, csv_filepath)

# Example usage (single file):
dbf_to_csv("input.dbf", "output.csv")

#Example usage (folder conversion):
# convert_all_dbf_in_folder("input_folder", "output_folder")