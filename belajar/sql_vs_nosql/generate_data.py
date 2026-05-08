import random
import csv
import os
from datetime import datetime, timedelta

def generate_random_string(length):
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choice(letters) for _ in range(length))

def generate_csv_category(filename, category_id, total_rows):
    print(f"Generating {total_rows} records for {filename}...")
    start_date = datetime(2023, 1, 1)
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'category_id', 'product_sku', 'branch_id', 'quantity', 'price'])
        
        for i in range(total_rows):
            timestamp = start_date + timedelta(seconds=random.randint(0, 31536000))
            row = [
                timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                category_id,
                f"SKU-{generate_random_string(8)}",
                random.randint(1, 100),
                random.randint(1, 500),
                round(random.uniform(5000, 1000000), 2)
            ]
            writer.writerow(row)
            if (i + 1) % 250000 == 0:
                print(f"Progress: {i + 1} rows written...")

if __name__ == "__main__":
    # Total 3 Juta data: 1jt per file/kategori
    os.makedirs('benchmark_data', exist_ok=True)
    generate_csv_category('benchmark_data/sales_transactions.csv', 1, 1000000)
    generate_csv_category('benchmark_data/product_metadata.csv', 2, 1000000)
    generate_csv_category('benchmark_data/stock_metrics.csv', 3, 1000000)
    print("--- Data Preparation Complete ---")
