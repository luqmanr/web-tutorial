import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

import sqlite3

def insert_row(con, cabang, tanggal, penjualan):
    statement = """
        INSERT INTO sales(
            cabang, tanggal, penjualan
        ) VALUES (?, ?, ?);
    """

    try:
        cur = con.cursor()
        cur.execute(statement, (cabang, tanggal, penjualan))
        con.commit()
        return True
    except Exception as e:
        print(f'failed to insert into table: {e}')
        return False

# connect to sqlite database
con = sqlite3.connect('./db/sim.db')

# Directory containing CSV files
directory = 'data'

# List to store dataframes
dataframes = []

# Iterate through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        print('filename:', filename)

        filepath = os.path.join(directory, filename)
        print('filepath:', filepath)
        try:
            # Read CSV file into DataFrame
            df = pd.read_csv(filepath)
            # Add 'store' column with filename minus '.csv'
            df['store'] = filename.replace('.csv', '')
            dataframes.append(df)
            print(f"Successfully read {filename}")
        except Exception as e:
            print(f"Error reading {filepath}: {e}")

# Optionally, concatenate all DataFrames into one
if len(dataframes) == 0:
    print('tidak ada csv yang bisa dijadikan dataframe')
else:
    combined_df = pd.concat(dataframes, ignore_index=True)
    combined_df = combined_df.sort_values(by=['tanggal'], ascending=True)

    # insert to sqlite
    for i,row in combined_df.iterrows():
        inserted = insert_row(con, row['store'], row['tanggal'], row['sales'])
