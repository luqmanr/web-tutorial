import psycopg2
import pandas as pd
from pymongo import MongoClient

DB_CONFIG = dict(
    host='localhost', port=5432,
    dbname='reporting_db', user='report_user', password='report_pass',
)

print('=' * 60)
print('PERSIAPAN: Copy data dari PostgreSQL ke MongoDB')
print('Jalankan container: docker compose up -d')
print('=' * 60)

pg_conn = psycopg2.connect(**DB_CONFIG)
mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['retail_db']

branches = pd.read_sql_query('SELECT * FROM branches ORDER BY id', pg_conn)
categories = pd.read_sql_query('SELECT * FROM categories ORDER BY id', pg_conn)
products = pd.read_sql_query('SELECT * FROM products ORDER BY id', pg_conn)
customers = pd.read_sql_query('SELECT * FROM customers ORDER BY id', pg_conn)
suppliers = pd.read_sql_query('SELECT * FROM suppliers ORDER BY id', pg_conn)

print(f'Import {len(branches)} branches...')
mongo_db.branches.delete_many({})
mongo_db.branches.insert_many(branches.to_dict('records'))

print(f'Import {len(categories)} categories...')
mongo_db.categories.delete_many({})
mongo_db.categories.insert_many(categories.to_dict('records'))

print(f'Import {len(products)} products...')
for _, p in products.iterrows():
    cat = mongo_db.categories.find_one({'id': p['category_id']})
    p['category_name'] = cat['name'] if cat else None
mongo_db.products.delete_many({})
mongo_db.products.insert_many(products.to_dict('records'))

print(f'Import {len(customers)} customers...')
mongo_db.customers.delete_many({})
mongo_db.customers.insert_many(customers.to_dict('records'))

print(f'Import {len(suppliers)} suppliers...')
mongo_db.suppliers.delete_many({})
mongo_db.suppliers.insert_many(suppliers.to_dict('records'))

sales_headers = pd.read_sql_query(
    'SELECT * FROM sales_headers ORDER BY id LIMIT 2000', pg_conn
)
sales_ids = tuple(sales_headers['id'].tolist())
sales_items = pd.read_sql_query(
    f'SELECT * FROM sales_items WHERE sale_id IN {sales_ids} ORDER BY id', pg_conn
)

print(f'Build {len(sales_headers)} enriched sales documents...')
sales_docs = []
for _, sh in sales_headers.iterrows():
    items = sales_items[sales_items['sale_id'] == sh['id']]
    item_details = []
    for _, si in items.iterrows():
        prod = mongo_db.products.find_one({'id': si['product_id']})
        item_details.append({
            'product_id': si['product_id'],
            'product_name': prod['name'] if prod else None,
            'category_name': prod['category_name'] if prod else None,
            'quantity': int(si['quantity']),
            'unit_price': int(si['unit_price']),
            'subtotal': int(si['subtotal']),
        })
    branch = mongo_db.branches.find_one({'id': sh['branch_id']})
    customer = mongo_db.customers.find_one({'id': sh['customer_id']})
    doc = {
        'sale_id': int(sh['id']),
        'branch': {
            'id': int(sh['branch_id']),
            'name': branch['name'] if branch else None,
            'city': branch['city'] if branch else None,
        },
        'customer': {
            'id': int(sh['customer_id']),
            'name': customer['name'] if customer else None,
            'member_id': customer['member_id'] if customer else None,
            'city': customer['city'] if customer else None,
        } if customer else None,
        'date': sh['transaction_date'].isoformat() if hasattr(sh['transaction_date'], 'isoformat') else str(sh['transaction_date']),
        'payment_method': sh['payment_method'],
        'total_amount': int(sh['total_amount']),
        'items': item_details,
    }
    sales_docs.append(doc)

mongo_db.sales.delete_many({})
mongo_db.sales.insert_many(sales_docs)
pg_conn.close()

print(f'Imported {len(sales_docs)} enriched sales documents.\n')

print('=' * 60)
print('[Demo] MongoDB Queries')
print('=' * 60)

print('\n1. Transaksi > Rp 500.000 (5 transaksi pertama):')
for r in mongo_db.sales.find(
    {'total_amount': {'$gt': 500000}},
    {'sale_id': 1, 'total_amount': 1, 'branch.name': 1, '_id': 0}
).limit(5):
    print(f"   Sale {r['sale_id']}: Rp {r['total_amount']:,} - {r['branch']['name']}")

print('\n2. Total penjualan per metode pembayaran:')
pipeline = [{'$group': {'_id': '$payment_method', 'total': {'$sum': '$total_amount'}, 'count': {'$sum': 1}}}, {'$sort': {'total': -1}}]
for r in mongo_db.sales.aggregate(pipeline):
    print(f"   {r['_id']}: Rp {r['total']:,} ({r['count']} transaksi)")

print('\n3. Total qty terjual per kategori ($unwind):')
pipeline = [
    {'$unwind': '$items'},
    {'$group': {'_id': '$items.category_name', 'qty': {'$sum': '$items.quantity'}, 'revenue': {'$sum': '$items.subtotal'}}},
    {'$sort': {'revenue': -1}},
]
for r in mongo_db.sales.aggregate(pipeline):
    print(f"   {r['_id']}: {int(r['qty'])} pcs, Rp {int(r['revenue']):,}")

print('\n4. Total penjualan per cabang:')
pipeline = [
    {'$group': {'_id': '$branch.name', 'total': {'$sum': '$total_amount'}, 'count': {'$sum': 1}}},
    {'$sort': {'total': -1}},
]
for r in mongo_db.sales.aggregate(pipeline):
    print(f"   {r['_id']}: Rp {r['total']:,} ({r['count']} transaksi)")

print('\n5. Contoh dokumen embedded (1 transaksi):')
import json
sample = mongo_db.sales.find_one({}, {'_id': 0})
print(json.dumps(sample, indent=2, default=str)[:1500])

mongo_client.close()
print('\nSelesai! Lihat dokumentasi MongoDB Compass untuk eksplorasi visual.')
