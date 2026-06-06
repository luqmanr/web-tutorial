import pyodbc
import csv
import time
from datetime import datetime

DB_CONFIG = {
    "server": "localhost",
    "database": "benchmark_db",
    "username": "sa",
    "password": "YourStrong!Password123",
    "driver": "{ODBC Driver 18 for SQL Server}",
}

CONN_STR = (
    f"DRIVER={DB_CONFIG['driver']};"
    f"SERVER={DB_CONFIG['server']};"
    f"DATABASE={DB_CONFIG['database']};"
    f"UID={DB_CONFIG['username']};"
    f"PWD={DB_CONFIG['password']};"
    "TrustServerCertificate=yes;"
)

def ensure_database():
    conn = pyodbc.connect(
        f"DRIVER={DB_CONFIG['driver']};"
        f"SERVER={DB_CONFIG['server']};"
        f"UID={DB_CONFIG['username']};"
        f"PWD={DB_CONFIG['password']};"
        "TrustServerCertificate=yes;"
    )
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = '{DB_CONFIG['database']}') CREATE DATABASE {DB_CONFIG['database']};")
    cur.close()
    conn.close()

def benchmark_mssql():
    try:
        ensure_database()
        conn = pyodbc.connect(CONN_STR, fast_executemany=True)
        cur = conn.cursor()

        cur.execute("DROP TABLE IF EXISTS sales_data;")
        cur.execute("""
            CREATE TABLE sales_data (
                id INT IDENTITY(1,1) PRIMARY KEY,
                timestamp DATETIME2,
                category_id INT,
                product_sku VARCHAR(50),
                branch_id INT,
                quantity INT,
                price DECIMAL(18,2)
            );
        """)
        conn.commit()

        print("Starting MSSQL Bulk Insert...")
        start_time = time.time()

        files = [
            'benchmark_data/sales_transactions.csv',
            'benchmark_data/product_metadata.csv',
            'benchmark_data/stock_metrics.csv'
        ]

        for file in files:
            batch = []
            with open(file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    batch.append((
                        row['timestamp'],
                        int(row['category_id']),
                        row['product_sku'],
                        int(row['branch_id']),
                        int(row['quantity']),
                        float(row['price']),
                    ))
                    if len(batch) >= 10000:
                        cur.executemany(
                            "INSERT INTO sales_data (timestamp, category_id, product_sku, branch_id, quantity, price) VALUES (?, ?, ?, ?, ?, ?)",
                            batch
                        )
                        conn.commit()
                        batch = []
                if batch:
                    cur.executemany(
                        "INSERT INTO sales_data (timestamp, category_id, product_sku, branch_id, quantity, price) VALUES (?, ?, ?, ?, ?, ?)",
                        batch
                    )
                    conn.commit()

        insert_duration = time.time() - start_time
        print(f"MSSQL Insert Duration (3M rows): {insert_duration:.2f} seconds")

        print("Starting MSSQL Aggregation Query...")
        start_time = time.time()
        cur.execute("SELECT branch_id, SUM(price * quantity) FROM sales_data GROUP BY branch_id ORDER BY 2 DESC;")
        cur.fetchall()
        query_duration = time.time() - start_time
        print(f"MSSQL Query Duration: {query_duration:.4f} seconds")

        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    benchmark_mssql()
