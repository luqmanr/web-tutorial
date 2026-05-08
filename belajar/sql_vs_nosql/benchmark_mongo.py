from pymongo import MongoClient
import csv
import time
from datetime import datetime

# Konfigurasi
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "benchmark_db"

def benchmark_mongodb():
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db["sales_data"]
        
        # Cleanup
        collection.drop()

        # 1. Benchmark Insertion
        print("Starting MongoDB Bulk Insert...")
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
                    # Konversi tipe data agar fair
                    row['timestamp'] = datetime.strptime(row['timestamp'], "%Y-%m-%d %H:%M:%S")
                    row['category_id'] = int(row['category_id'])
                    row['branch_id'] = int(row['branch_id'])
                    row['quantity'] = int(row['quantity'])
                    row['price'] = float(row['price'])
                    batch.append(row)
                    
                    if len(batch) >= 10000:
                        collection.insert_many(batch)
                        batch = []
                if batch:
                    collection.insert_many(batch)
        
        insert_duration = time.time() - start_time
        print(f"MongoDB Insert Duration (3M rows): {insert_duration:.2f} seconds")

        # 2. Benchmark Query (Aggregation)
        print("Starting MongoDB Aggregation Query...")
        start_time = time.time()
        pipeline = [
            {"$group": {
                "_id": "$branch_id",
                "total_sales": {"$sum": {"$multiply": ["$price", "$quantity"]}}
            }},
            {"$sort": {"total_sales": -1}}
        ]
        list(collection.aggregate(pipeline))
        query_duration = time.time() - start_time
        print(f"MongoDB Query Duration: {query_duration:.4f} seconds")

        client.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    benchmark_mongodb()
