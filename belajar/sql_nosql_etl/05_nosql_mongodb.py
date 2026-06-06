import sqlite3
import os
import pandas as pd
from pymongo import MongoClient
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))

print('=' * 60)
print('PERSIAPAN: Copy data dari SQLite ke MongoDB')
print('Jalankan container: docker compose up -d')
print('=' * 60)

client = MongoClient('mongodb://localhost:27017/')
db = client['retail_db']

sql_conn = sqlite3.connect(os.path.join(BASE, 'data/master.db'))

branches = pd.read_sql_query('SELECT * FROM branches', sql_conn)
categories = pd.read_sql_query('SELECT * FROM categories', sql_conn)
products = pd.read_sql_query('SELECT * FROM products', sql_conn)
customers = pd.read_sql_query('SELECT * FROM customers', sql_conn)
suppliers = pd.read_sql_query('SELECT * FROM suppliers', sql_conn)

print(f'Importing {len(branches)} branches...')
db.branches.delete_many({})
db.branches.insert_many(branches.to_dict('records'))

print(f'Importing {len(categories)} categories...')
db.categories.delete_many({})
db.categories.insert_many(categories.to_dict('records'))

print(f'Importing {len(products)} products...')
for _, p in products.iterrows():
    cat = db.categories.find_one({'id': p['category_id']})
    p['category_name'] = cat['name'] if cat else None
db.products.delete_many({})
db.products.insert_many(products.to_dict('records'))

print(f'Importing {len(customers)} customers...')
db.customers.delete_many({})
db.customers.insert_many(customers.to_dict('records'))

print(f'Importing {len(suppliers)} suppliers...')
db.suppliers.delete_many({})
db.suppliers.insert_many(suppliers.to_dict('records'))

sales_headers = pd.read_sql_query(
    'SELECT * FROM sales_headers LIMIT 2000', sql_conn
)
sales_items = pd.read_sql_query(
    'SELECT * FROM sales_items WHERE sale_id <= 2000', sql_conn
)

print(f'Building {len(sales_headers)} enriched sales documents...')
sales_docs = []
for _, sh in sales_headers.iterrows():
    items = sales_items[sales_items['sale_id'] == sh['id']]
    item_details = []
    for _, si in items.iterrows():
        prod = db.products.find_one({'id': si['product_id']})
        item_details.append({
            'product_id': si['product_id'],
            'product_name': prod['name'] if prod else None,
            'category_name': prod['category_name'] if prod else None,
            'quantity': int(si['quantity']),
            'unit_price': int(si['unit_price']),
            'subtotal': int(si['subtotal']),
        })
    branch = db.branches.find_one({'id': sh['branch_id']})
    customer = db.customers.find_one({'id': sh['customer_id']})
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
        'date': sh['transaction_date'],
        'payment_method': sh['payment_method'],
        'total_amount': int(sh['total_amount']),
        'items': item_details,
    }
    sales_docs.append(doc)

db.sales.delete_many({})
db.sales.insert_many(sales_docs)
sql_conn.close()

print(f'Imported {len(sales_docs)} enriched sales documents.\n')

print('=' * 60)
print('SOAL 1: Basic MongoDB find()')
print('Tampilkan 5 transaksi dengan total_amount > Rp 500.000')
print('Tampilkan: sale_id, total_amount, branch.name')
print('Gunakan: collection.find({"total_amount": {"$gt": 500000}}).limit(5)')
print('=' * 60)
print('\nJalankan di MongoDB shell atau Compass:')
print('''
db.sales.find(
    {"total_amount": {"$gt": 500000}},
    {"sale_id": 1, "total_amount": 1, "branch.name": 1, "_id": 0}
).limit(5)
''')

print('\nAtau dari Python:')
result = list(db.sales.find(
    {'total_amount': {'$gt': 500000}},
    {'sale_id': 1, 'total_amount': 1, 'branch.name': 1, '_id': 0}
).limit(5))
for r in result:
    print(f"  Sale {r['sale_id']}: Rp {r['total_amount']:,} - {r['branch']['name']}")

print('\n' + '=' * 60)
print('SOAL 2: Aggregation Pipeline - GROUP BY')
print('Hitung total penjualan per metode pembayaran.')
print('Gunakan $group + $sum, hasilnya seperti GROUP BY di SQL.')
print('=' * 60)
pipeline_2 = [
    {'$group': {
        '_id': '$payment_method',
        'total_penjualan': {'$sum': '$total_amount'},
        'jumlah_transaksi': {'$sum': 1},
    }},
    {'$sort': {'total_penjualan': -1}},
]
print('\nPipeline:')
import json
print(json.dumps(pipeline_2, indent=2))
print('\nHasil:')
for r in db.sales.aggregate(pipeline_2):
    print(f"  {r['_id']}: Rp {r['total_penjualan']:,} ({r['jumlah_transaksi']} transaksi)")

print('\n' + '=' * 60)
print('SOAL 3: Aggregation - Unwind items')
print('Hitung total qty terjual per kategori produk')
print('Gunakan $unwind items → $group by items.category_name')
print('=' * 60)
pipeline_3 = [
    {'$unwind': '$items'},
    {'$group': {
        '_id': '$items.category_name',
        'total_qty': {'$sum': '$items.quantity'},
        'total_revenue': {'$sum': '$items.subtotal'},
    }},
    {'$sort': {'total_revenue': -1}},
]
print('\nHasil:')
for r in db.sales.aggregate(pipeline_3):
    print(f"  {r['_id']}: {int(r['total_qty'])} pcs, Rp {int(r['total_revenue']):,}")

print('\n' + '=' * 60)
print('SOAL 4: Embedded document vs Reference')
print('Perhatikan struktur dokumen sales:')
print('- Data BRANCH di-embed langsung di dokumen (denormalized)')
print('- Data CUSTOMER juga di-embed')
print('- Item produk dengan nama kategori di-embed')
print('\nKeuntungan embedded: 1 query dapat semua data (no JOIN!)')
print('Kekurangan: ukuran dokumen besar, update harus di banyak tempat')
print('\nBandingkan dengan SQL yang perlu JOIN 4-5 tabel')
print('untuk mendapatkan data yang sama.')
print('=' * 60)
print('\nCek 1 dokumen sample:')
sample = db.sales.find_one({}, {'_id': 0})
print(json.dumps(sample, indent=2, default=str)[:2000])

print('\n' + '=' * 60)
print('SOAL 5: Visualize - Aggregation by Branch')
print('Total penjualan per cabang via aggregation pipeline')
print('=' * 60)
pipeline_5 = [
    {'$group': {
        '_id': '$branch.name',
        'total_sales': {'$sum': '$total_amount'},
        'count': {'$sum': 1},
    }},
    {'$sort': {'total_sales': -1}},
]
for r in db.sales.aggregate(pipeline_5):
    print(f"  {r['_id']}: Rp {r['total_sales']:,} ({r['count']} transaksi)")

client.close()
