# import pyodbc
import mssql_python
import sqlite3
import random
import os
from datetime import datetime, timedelta

"""
TODO: use mssql-python instead of mssql_python for better performance and native support

python3 -m pip install mssql-python
"""


BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, 'data')
random.seed(42)

import config
MSSQL_CONFIG = config.MSSQL_CONFIG

CONN_STR = (
    # f"DRIVER={MSSQL_CONFIG['driver']};"
    f"SERVER={MSSQL_CONFIG['server']},{MSSQL_CONFIG['port']};"
    f"DATABASE={MSSQL_CONFIG['database']};"
    f"UID={MSSQL_CONFIG['username']};"
    f"PWD={MSSQL_CONFIG['password']};"
    "TrustServerCertificate=yes;"
)

BRANCHES = [
    (1, 'Borma Dago', 'Bandung', 'Jawa Barat'),
    (2, 'Borma Dakota', 'Bandung', 'Jawa Barat'),
    (3, 'Borma Setiabudi', 'Bandung', 'Jawa Barat'),
    (4, 'Borma Cimahi', 'Cimahi', 'Jawa Barat'),
    (5, 'Borma Bogor', 'Bogor', 'Jawa Barat'),
    (6, 'Borma Bekasi', 'Bekasi', 'Jawa Barat'),
    (7, 'Borma Tangerang', 'Tangerang', 'Banten'),
    (8, 'Borma Depok', 'Depok', 'Jawa Barat'),
    (9, 'Borma Cirebon', 'Cirebon', 'Jawa Barat'),
    (10, 'Borma Sukabumi', 'Sukabumi', 'Jawa Barat'),
]

CATEGORIES = [
    (1, 'Makanan Ringan', None), (2, 'Minuman', None),
    (3, 'Bumbu & Saus', None), (4, 'Beras & Sembako', None),
    (5, 'Susu & Olahan Susu', None), (6, 'Roti & Kue', None),
    (7, 'Produk Beku', None), (8, 'Perawatan Diri', None),
    (9, 'Pembersih Rumah', None), (10, 'Perlengkapan Bayi', None),
    (11, 'Alat Tulis', None), (12, 'Makanan & Perlengkapan Hewan', None),
]

PRODUCT_NAMES = {
    1: ['Chitato Sapi Panggang', 'Doritos Keju', 'Tango Wafer Coklat', 'Roma Biskuit Kelapa',
        'Oreo Original', 'Pringles BBQ', 'Lays Rumput Laut', 'Qtela Singkong Balado',
        'Kacang Garuda', 'Cheetos Jagung Bakar'],
    2: ['Coca Cola 390ml', 'Fanta Strawberry 390ml', 'Sprite 390ml', 'Teh Botol Sosro 500ml',
        'Pocari Sweat 500ml', 'Aqua 1500ml', 'Ultra Milk Coklat 250ml', 'Nutriboost Jeruk',
        'Floridina Mangga', 'Ale-Ale Leci'],
    3: ['Kecap Bango 520ml', 'Saus Sambal Indofood 340ml', 'Saori Saus Tiram', 'Masako Ayam',
        'Royco Sapi', 'Minyak Goreng Bimoli 1L', 'Garam Dolphin 250gr', 'Gula Pasir Gulaku 1kg',
        'Tepung Segitiga Biru 1kg', 'Saus Tomat ABC'],
    4: ['Beras Ramos 5kg', 'Beras Pandan Wangi 5kg', 'Minyak Kita 2L', 'Telur Ayam 1kg',
        'Mie Indomie Goreng', 'Mie Sedaap Goreng', 'Tepung Beras Rose Brand', 'Kornet Pronas',
        'Sarden ABC Pedas', 'Bihun Jagung'],
    5: ['Indomilk UHT Coklat 1L', 'Ultra Milk Full Cream 1L', 'Yogurt Cimory Stroberi',
        'Keju Kraft Cheddar 200gr', 'Mentega Blue Band 200gr', 'Susu Kental Manis Frisian Flag',
        'Dancow Fortigro', 'Bear Brand', 'Milku Coklat', 'Greenfields Susu Cair'],
    6: ['Sari Roti Tawar', 'Sari Roti Coklat', 'Malkist Roma Kelapa', 'Biskuat Marie',
        'Superman Keju', 'Roma Biskuit Susu', 'Good Time Coklat', 'Sugar Mochi',
        'Nissin Wafer Coklat', 'Egg Roll Dua Kelinci'],
    7: ['Nugget Fiesta 500gr', 'Sosis So Nice 250gr', 'Dimsum Kencana', 'Otak-Otak Bandeng',
        'Pisang Goreng Beku', 'Kerupuk Udang Mentah', 'Bakso Curah 1kg', 'Siomay Ikan'],
    8: ['Sabun Lifebuoy 135gr', 'Pasta Gigi Pepsodent', 'Sampo Clear 170ml', 'Sabun Lux Putih',
        'Deodorant Rexona', 'Pembalut Softex', 'Shampoo Dove 200ml', 'Sabun Nuvo',
        'Sikat Gigi Pepsodent', 'Handbody Citra'],
    9: ['Sabun Cuci Piring Sunlight', 'Deterjen Rinso 900gr', 'Pembersih Lantai So Klin',
        'Pemutih Bayclin', 'Pengharum Ruangan Stella', 'Sapu Lidi', 'Kain Pel Microtex',
        'Spons Cuci Piring', 'Sikat WC', 'Lap Ember'],
    10: ['Popok Merries M', 'Popok Makuku XL', 'Tisu Basah Baby', 'Bedak Bayi Johnson',
         'Minyak Telon Lang', 'Botol Susu Pigeon', 'Dodot Bayi', 'Sabun Mandi Bayi',
         'Shampoo Bayi', 'Gunting Kuku Bayi'],
    11: ['Buku Tulis Sidu 38lembar', 'Pulpen Standard Joy', 'Pensil 2B Faber Castell',
         'Penghapus Joy', 'Penggaris 30cm', 'Crayon 12 Warna', 'Lem Kertas', 'Gunting Joy',
         'Kertas HVS A4 70gr', 'Spidol Whiteboard'],
    12: ['Whiskas Makanan Kucing', 'Pedigree Makanan Anjing', 'Cat Food Royal Canin',
         'Pasir Kucing 5kg', 'Snack Kucing Dreamies', 'Vitamin Ikan', 'Tali Anjing',
         'Kandang Hamster', 'Mainan Kucing', 'Mangkok Hewan'],
}

CITIES = ['Bandung', 'Jakarta', 'Bogor', 'Bekasi', 'Tangerang', 'Depok', 'Cimahi', 'Cirebon', 'Sukabumi', 'Garut']
PAYMENT_METHODS = ['TUNAI', 'DEBIT', 'KREDIT', 'QRIS', 'TRANSFER']

SUPPLIERS_INFO = [
    ('PT Indofood Sukses Makmur', 'Jakarta', 'indofood@email.com', '30 hari'),
    ('PT Coca-Cola Indonesia', 'Jakarta', 'cocacola@email.com', '45 hari'),
    ('PT Heinz ABC Indonesia', 'Jakarta', 'abc@email.com', '30 hari'),
    ('PT Frisian Flag Indonesia', 'Jakarta', 'frisianflag@email.com', '30 hari'),
    ('PT Nippon Indosari', 'Jakarta', 'sariroti@email.com', '14 hari'),
    ('PT Charoen Pokphand', 'Bandung', 'cpfood@email.com', '30 hari'),
    ('PT Unilever Indonesia', 'Jakarta', 'unilever@email.com', '45 hari'),
    ('PT Wings Group', 'Surabaya', 'wings@email.com', '30 hari'),
    ('PT Softex Indonesia', 'Bandung', 'softex@email.com', '30 hari'),
    ('PT Pabrik Kertas Tjiwi Kimia', 'Sidoarjo', 'tjiwi@email.com', '45 hari'),
    ('PT Royal Canin Indonesia', 'Jakarta', 'royalcanin@email.com', '30 hari'),
    ('PT Nestle Indonesia', 'Jakarta', 'nestle@email.com', '30 hari'),
    ('PT Mayora Indah', 'Tangerang', 'mayora@email.com', '30 hari'),
    ('PT Kalbe Farma', 'Jakarta', 'kalbe@email.com', '45 hari'),
    ('PT Borma Retail Indonesia', 'Bandung', 'borma@email.com', '7 hari'),
    ('PT Garudafood Putra Putri Jaya', 'Jakarta', 'garudafood@email.com', '30 hari'),
    ('PT Campina Ice Cream', 'Surabaya', 'campina@email.com', '14 hari'),
    ('PT Kirin Indonesia', 'Jakarta', 'kirin@email.com', '30 hari'),
    ('PT Sido Muncul', 'Semarang', 'sidomuncul@email.com', '30 hari'),
    ('PT Lion Superindo', 'Jakarta', 'lion@email.com', '45 hari'),
]

def ensure_database():
    conn = mssql_python.connect(
        CONN_STR.replace(f"DATABASE={MSSQL_CONFIG['database']};", "DATABASE=master;")
    )
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = '{MSSQL_CONFIG['database']}') CREATE DATABASE [{MSSQL_CONFIG['database']}]")
    cur.close()
    conn.close()

def create_tables(cur):
    cur.execute('''
        CREATE TABLE branches (
            id INT PRIMARY KEY, name VARCHAR(100) NOT NULL,
            city VARCHAR(50) NOT NULL, region VARCHAR(50) NOT NULL
        )
    ''')
    cur.execute('''
        CREATE TABLE categories (
            id INT PRIMARY KEY, name VARCHAR(100) NOT NULL, parent_id INT NULL
        )
    ''')
    cur.execute('''
        CREATE TABLE products (
            id INT IDENTITY(1,1) PRIMARY KEY, 
            sku VARCHAR(20) UNIQUE NOT NULL,
            name VARCHAR(200) NOT NULL, 
            category_id INT NOT NULL,
            unit VARCHAR(20) DEFAULT 'pcs',
            supplier_price INT NOT NULL, 
            retail_price INT NOT NULL,
            supplier_id INT NOT NULL
        )
    ''')
    cur.execute('''
        CREATE TABLE customers (
            id INT PRIMARY KEY, name VARCHAR(100) NOT NULL,
            member_id VARCHAR(20) UNIQUE, phone VARCHAR(20),
            city VARCHAR(50), join_date DATE NOT NULL
        )
    ''')
    cur.execute('''
        CREATE TABLE suppliers (
            id INT PRIMARY KEY, name VARCHAR(200) NOT NULL, city VARCHAR(50),
            contact VARCHAR(100), payment_terms VARCHAR(50) NOT NULL
        )
    ''')
    cur.execute('''
        CREATE TABLE sales_headers (
            id INT PRIMARY KEY, branch_id INT NOT NULL, customer_id INT,
            transaction_date DATE NOT NULL, payment_method VARCHAR(20) NOT NULL,
            total_amount INT NOT NULL
        )
    ''')
    cur.execute('''
        CREATE TABLE sales_items (
            id INT PRIMARY KEY, sale_id INT NOT NULL,
            product_id INT NOT NULL, quantity INT NOT NULL,
            unit_price INT NOT NULL, subtotal INT NOT NULL
        )
    ''')
    cur.execute('''
        CREATE TABLE purchase_orders (
            id INT PRIMARY KEY, supplier_id INT NOT NULL, branch_id INT NOT NULL,
            order_date DATE NOT NULL, status VARCHAR(20) NOT NULL,
            total_amount INT NOT NULL
        )
    ''')
    cur.execute('''
        CREATE TABLE inventory (
            id INT PRIMARY KEY, branch_id INT NOT NULL, product_id INT NOT NULL,
            stock_qty INT NOT NULL, last_updated DATE NOT NULL
        )
    ''')
    cur.execute('''
        CREATE TABLE daily_sales_by_branch (
            date DATE NOT NULL, branch_id INT NOT NULL,
            branch_name VARCHAR(100) NOT NULL, total_sales INT NOT NULL,
            transaction_count INT NOT NULL,
            PRIMARY KEY (date, branch_id)
        )
    ''')
    cur.execute('''
        CREATE TABLE daily_sales_by_category (
            date DATE NOT NULL, category_id INT NOT NULL,
            category_name VARCHAR(100) NOT NULL, total_sales INT NOT NULL,
            qty_sold INT NOT NULL,
            PRIMARY KEY (date, category_id)
        )
    ''')
    cur.execute('''
        CREATE TABLE monthly_sales_summary (
            year_month VARCHAR(7) NOT NULL, branch_id INT NOT NULL,
            branch_name VARCHAR(100) NOT NULL, total_sales INT NOT NULL,
            total_qty INT NOT NULL, avg_transaction FLOAT NOT NULL,
            PRIMARY KEY (year_month, branch_id)
        )
    ''')
    cur.execute('''
        CREATE TABLE payment_method_summary (
            date DATE NOT NULL, payment_method VARCHAR(20) NOT NULL,
            total_amount INT NOT NULL, transaction_count INT NOT NULL,
            PRIMARY KEY (date, payment_method)
        )
    ''')
    cur.execute('''
        CREATE TABLE top_products (
            month VARCHAR(7) NOT NULL, product_id INT NOT NULL,
            product_name VARCHAR(200) NOT NULL, category_name VARCHAR(100) NOT NULL,
            qty_sold INT NOT NULL, total_revenue INT NOT NULL,
            rank INT NOT NULL,
            PRIMARY KEY (month, product_id)
        )
    ''')


def seed_data(cur):
    for b in BRANCHES:
        cur.execute('INSERT INTO branches VALUES (?,?,?,?)', b)
    print(f'  branches: {len(BRANCHES)}')

    for c in CATEGORIES:
        cur.execute('INSERT INTO categories VALUES (?,?,?)', c)
    print(f'  categories: {len(CATEGORIES)}')

    products_data = []
    sku_counter = 1000
    for cat_id, names in PRODUCT_NAMES.items():
        for name in names:
            supplier_price = random.randint(5000, 80000)
            markup = random.uniform(1.15, 1.35)
            retail_price = int(supplier_price * markup / 100) * 100
            supplier_id = (cat_id - 1) % len(SUPPLIERS_INFO) + 1
            products_data.append((sku_counter, name, cat_id, 'pcs', supplier_price, retail_price, supplier_id))
            sku_counter += 1
    for p in products_data:
        cur.execute('INSERT INTO products (sku, name, category_id, unit, supplier_price, retail_price, supplier_id) VALUES (?,?,?,?,?,?,?)', p)
    print(f'  products: {len(products_data)}')

    first_names = ['Ahmad', 'Budi', 'Citra', 'Dedi', 'Eka', 'Fitri', 'Gilang', 'Hana', 'Irfan', 'Juni',
                   'Kartika', 'Lilis', 'Maman', 'Nina', 'Oman', 'Putri', 'Qori', 'Rudi', 'Sari', 'Tono',
                   'Ujang', 'Vina', 'Wawan', 'Yanti', 'Zaki']
    for i in range(1, 1001):
        name = f'{random.choice(first_names)} {random.choice(["S.", "P.", "A.", "Setiawan", "Suryana", "Hidayat", "Wijaya", "Kusuma", "Pratama", "Nugraha"])}'
        member_id = f'MEM-{i:05d}'
        phone = f'08{random.randint(100000000, 999999999)}'
        city = random.choice(CITIES)
        join_date = f'2025-{random.randint(1,12):02d}-{random.randint(1,28):02d}'
        cur.execute('INSERT INTO customers VALUES (?,?,?,?,?,?)', (i, name, member_id, phone, city, join_date))
    print(f'  customers: 1000')

    for i, s in enumerate(SUPPLIERS_INFO, 1):
        cur.execute('INSERT INTO suppliers VALUES (?,?,?,?,?)', (i, *s))
    print(f'  suppliers: {len(SUPPLIERS_INFO)}')

    start_date = datetime(2026, 3, 1)
    end_date = datetime(2026, 3, 31)
    all_dates = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

    print('  Generating sales...')
    sale_id = 1
    item_id = 1
    po_statuses = ['SELESAI', 'SELESAI', 'SELESAI', 'DIPO', 'DIKIRIM']
    sales_batch = []
    items_batch = []

    for date in all_dates:
        num_trans = random.randint(1,10)
        for _ in range(num_trans):
            branch_id = random.randint(1, 10)
            customer_id = random.randint(1, 1000)
            pay_method = random.choice(PAYMENT_METHODS)
            date_str = date.strftime('%Y-%m-%d')
            num_items = random.randint(1, 8)
            total = 0
            for _ in range(num_items):
                product_id = random.randint(1, len(products_data))
                prod = products_data[product_id - 1]
                qty = random.randint(1, 5)
                unit_price = prod[5]
                subtotal = qty * unit_price
                total += subtotal
                items_batch.append((item_id, sale_id, product_id, qty, unit_price, subtotal))
                item_id += 1
            sales_batch.append((sale_id, branch_id, customer_id, date_str, pay_method, total))
            sale_id += 1

    cur.executemany('INSERT INTO sales_headers VALUES (?,?,?,?,?,?)', sales_batch)
    cur.executemany('INSERT INTO sales_items VALUES (?,?,?,?,?,?)', items_batch)
    print(f'  sales: {sale_id - 1} transactions')

    po_data = []
    for i in range(1, 501):
        supplier_id = random.randint(1, len(SUPPLIERS_INFO))
        branch_id = random.randint(1, 10)
        order_date = f'2026-{random.randint(1,3):02d}-{random.randint(1,28):02d}'
        status = random.choice(po_statuses)
        total = random.randint(1000000, 50000000)
        po_data.append((i, supplier_id, branch_id, order_date, status, total))
    cur.executemany('INSERT INTO purchase_orders VALUES (?,?,?,?,?,?)', po_data)
    print(f'  purchase_orders: 500')

    inv_count = 0
    for branch_id in range(1, 11):
        for product_id in range(1, len(products_data) + 1):
            if random.random() < 0.7:
                stock = random.randint(0, 500)
                last_upd = f'2026-{random.randint(1,3):02d}-{random.randint(1,28):02d}'
                cur.execute('INSERT INTO inventory VALUES (?,?,?,?,?)',
                            (branch_id * 1000 + product_id, branch_id, product_id, stock, last_upd))
                inv_count += 1
    print(f'  inventory: {inv_count}')


def populate_reporting(cur):
    cur.execute('''
        INSERT INTO daily_sales_by_branch (date, branch_id, branch_name, total_sales, transaction_count)
        SELECT sh.transaction_date, b.id, b.name,
               SUM(sh.total_amount), COUNT(DISTINCT sh.id)
        FROM sales_headers sh
        JOIN branches b ON sh.branch_id = b.id
        GROUP BY sh.transaction_date, b.id, b.name
    ''')
    print(f'  daily_sales_by_branch: {cur.rowcount}')

    cur.execute('''
        INSERT INTO daily_sales_by_category (date, category_id, category_name, total_sales, qty_sold)
        SELECT sh.transaction_date, c.id, c.name,
               SUM(si.subtotal), SUM(si.quantity)
        FROM sales_headers sh
        JOIN sales_items si ON sh.id = si.sale_id
        JOIN products p ON si.product_id = p.id
        JOIN categories c ON p.category_id = c.id
        GROUP BY sh.transaction_date, c.id, c.name
    ''')
    print(f'  daily_sales_by_category: {cur.rowcount}')

    cur.execute('''
        INSERT INTO monthly_sales_summary (year_month, branch_id, branch_name, total_sales, total_qty, avg_transaction)
        SELECT FORMAT(sh.transaction_date, 'yyyy-MM'), b.id, b.name,
               SUM(si.subtotal), SUM(si.quantity),
               ROUND(AVG(CAST(si.subtotal AS FLOAT)), 2)
        FROM sales_headers sh
        JOIN branches b ON sh.branch_id = b.id
        JOIN sales_items si ON sh.id = si.sale_id
        GROUP BY FORMAT(sh.transaction_date, 'yyyy-MM'), b.id, b.name
    ''')
    print(f'  monthly_sales_summary: {cur.rowcount}')

    cur.execute('''
        INSERT INTO payment_method_summary (date, payment_method, total_amount, transaction_count)
        SELECT transaction_date, payment_method,
               SUM(total_amount), COUNT(*)
        FROM sales_headers
        GROUP BY transaction_date, payment_method
    ''')
    print(f'  payment_method_summary: {cur.rowcount}')

    cur.execute('''
        INSERT INTO top_products (month, product_id, product_name, category_name, qty_sold, total_revenue, rank)
        SELECT FORMAT(sh.transaction_date, 'yyyy-MM'), p.id, p.name, c.name,
               SUM(si.quantity), SUM(si.subtotal),
               RANK() OVER (
                   PARTITION BY FORMAT(sh.transaction_date, 'yyyy-MM')
                   ORDER BY SUM(si.subtotal) DESC
               )
        FROM sales_headers sh
        JOIN sales_items si ON sh.id = si.sale_id
        JOIN products p ON si.product_id = p.id
        JOIN categories c ON p.category_id = c.id
        GROUP BY FORMAT(sh.transaction_date, 'yyyy-MM'), p.id, p.name, c.name
    ''')
    print(f'  top_products: {cur.rowcount}')


# def export_to_sqlite(cur):
#     db_path = os.path.join(DATA_DIR, 'data_retail.db')
#     if os.path.exists(db_path):
#         os.remove(db_path)
#     sl_conn = sqlite3.connect(db_path)
#     sl_cur = sl_conn.cursor()

#     tables = [
#         'branches', 'categories', 'products', 'customers', 'suppliers',
#         'daily_sales_by_branch', 'daily_sales_by_category',
#         'monthly_sales_summary', 'payment_method_summary', 'top_products',
#     ]

#     for table in tables:
#         cur.execute(f'SELECT * FROM [{table}] ORDER BY 1')
#         rows = cur.fetchall()
#         if not rows:
#             print(f'  SKIP {table} (empty)')
#             continue
#         cols = [desc[0] for desc in cur.description]
#         col_types = {}
#         for i, col in enumerate(cols):
#             val = rows[0][i]
#             if isinstance(val, int):
#                 col_types[col] = 'INTEGER'
#             elif isinstance(val, float):
#                 col_types[col] = 'REAL'
#             else:
#                 col_types[col] = 'TEXT'
#         col_defs = ', '.join(f'"{c}" {col_types[c]}' for c in cols)
#         sl_cur.execute(f'DROP TABLE IF EXISTS "{table}"')
#         sl_cur.execute(f'CREATE TABLE "{table}" ({col_defs})')
#         placeholders = ', '.join(['?' for _ in cols])
#         col_names = ', '.join(f'"{c}"' for c in cols)
#         data = [tuple(r[i] for i in range(len(cols))) for r in rows]
#         sl_cur.executemany(f'INSERT INTO "{table}" ({col_names}) VALUES ({placeholders})', data)
#         print(f'  {table}: {len(rows)} rows')

#     sl_conn.commit()
#     sl_conn.close()
#     print(f'\nSQLite intermediary: {db_path}')

def export_to_sqlite(mssql_cur):
    db_path = os.path.join(DATA_DIR, 'data_retail.db')
    if os.path.exists(db_path):
        os.remove(db_path)
    sl_conn = sqlite3.connect(db_path)
    sl_cur = sl_conn.cursor()




if __name__ == '__main__':
    print('Pastikan container MSSQL sudah jalan:')
    ensure_database()

    conn = mssql_python.connect(CONN_STR, fast_executemany=True)
    cur = conn.cursor()

    # for table in ['branches', 'categories', 'products', 'customers', 'suppliers',
    #                'sales_headers', 'sales_items', 'purchase_orders', 'inventory',
    #                'daily_sales_by_branch', 'daily_sales_by_category',
    #                'monthly_sales_summary', 'payment_method_summary', 'top_products']:
    #     cur.execute(f'DROP TABLE IF EXISTS [{table}]')
    # conn.commit()

    # print('1. Membuat tables...')
    # create_tables(cur)

    # print('2. Mengisi master data...')
    # seed_data(cur)
    # conn.commit()

    # print('3. Mengisi reporting data...')
    # populate_reporting(cur)
    # conn.commit()

    # print('4. Export ke SQLite intermediary...')
    # export_to_sqlite(cur)

    # cur.close()
    # conn.close()
    # print('\nSelesai! Sekarang jalankan frontend:')
    # print('  streamlit run 02_frontend_streamlit.py')
    # print('  python 03_frontend_html_bootstrap.py')
