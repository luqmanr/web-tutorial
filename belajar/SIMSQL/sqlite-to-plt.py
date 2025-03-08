import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

import sqlite3

def query_rows(con):
    statement = """
        SELECT
            cabang, tanggal, penjualan
        FROM
            sales;
    """

    try:
        cur = con.cursor()
        cur.execute(statement)
        rows = cur.fetchall()
        return rows
    except Exception as e:
        print(f'failed to fetch rows: {e}')
        return []

# connect to sqlite database
con = sqlite3.connect('./db/sim.db')

rows = query_rows(con)
# print(rows)

df = pd.DataFrame(columns=['store', 'tanggal', 'sales'])
print(df)
for row in rows:
    df.loc[len(df)] = [row[0], row[1], row[2]]
df = df.sort_values(by=['sales'], ascending=True)
print(df)

plt.figure(figsize=(15, 8))
sns.barplot(x='tanggal', y='sales', hue='store', data=df)

# Set plot labels and title
plt.xlabel('Tanggal')
plt.ylabel('Sales')
plt.title('Sales for All Stores (Grouped by Date)')
plt.xticks(rotation=0, ha='right')  # Rotate x-axis labels
plt.legend(title='Store')  # Add a legend with a title
plt.tight_layout()
plt.savefig('./result.png')

# create sum of sales
sumdf = df.sort_values(by=['store'], ascending=True)
sumdf = sumdf.groupby('store').sum()
sumdf.reset_index(inplace=True)
# sumdf['tanggal'] = df["tanggal"].max()
sumdf['tanggal'] = pd.Series([df["tanggal"].max() for x in range(len(sumdf.index))])

plt.figure(figsize=(15, 8))
sns.barplot(x='store', y='sales', hue='store', data=sumdf)


# Set plot labels and title
plt.xlabel('Store Name')
plt.ylabel('Sales')
plt.title(f'Sales for All Stores (per {sumdf["tanggal"].max()})')
# plt.xticks(rotation=0, ha='right')  # Rotate x-axis labels
plt.legend(title='Store')  # Add a legend with a title
plt.tight_layout()
plt.savefig('./totalsales.png')