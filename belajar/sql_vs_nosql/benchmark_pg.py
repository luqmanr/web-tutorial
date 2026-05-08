import psycopg2
import csv
import time
import os

# Konfigurasi Database (Sesuaikan dengan kredensial Anda)
DB_CONFIG = {
    "host": "localhost",
    "database": "benchmark_db",
    "user": "postgres",
    "password": "password"
}

def benchmark_postgresql():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Setup Table
        cur.execute("DROP TABLE IF EXISTS sales_data;")
        cur.execute("""
            CREATE TABLE sales_data (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP,
                category_id INT,
                product_sku VARCHAR(50),
                branch_id INT,
                quantity INT,
                price NUMERIC
            );
        """)
        conn.commit()

        # 1. Benchmark Insertion (Bulk)
        print("Starting PostgreSQL Bulk Insert...")
        start_time = time.time()
        
        files = [
            'benchmark_data/sales_transactions.csv',
            'benchmark_data/product_metadata.csv',
            'benchmark_data/stock_metrics.csv'
        ]
        
        for file in files:
            with open(file, 'r') as f:
                next(f) # skip header
                cur.copy_from(f, 'sales_data', sep=',', columns=('timestamp', 'category_id', 'product_sku', 'branch_id', 'quantity', 'price'))
        
        conn.commit()
        insert_duration = time.time() - start_time
        print(f"PostgreSQL Insert Duration (3M rows): {insert_duration:.2f} seconds")

        # 2. Benchmark Query (Aggregation)
        print("Starting PostgreSQL Aggregation Query...")
        start_time = time.time()
        cur.execute("SELECT branch_id, SUM(price * quantity) FROM sales_data GROUP BY branch_id ORDER BY 2 DESC;")
        cur.fetchall()
        query_duration = time.time() - start_time
        print(f"PostgreSQL Query Duration: {query_duration:.4f} seconds")

        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    benchmark_postgresql()
