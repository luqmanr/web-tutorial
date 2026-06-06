import sqlite3
import random
import os
from datetime import datetime, timedelta

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, 'data')
random.seed(42)

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
    (1, 'Makanan Ringan', None),
    (2, 'Minuman', None),
    (3, 'Bumbu & Saus', None),
    (4, 'Beras & Sembako', None),
    (5, 'Susu & Olahan Susu', None),
    (6, 'Roti & Kue', None),
    (7, 'Produk Beku', None),
    (8, 'Perawatan Diri', None),
    (9, 'Pembersih Rumah', None),
    (10, 'Perlengkapan Bayi', None),
    (11, 'Alat Tulis', None),
    (12, 'Makanan & Perlengkapan Hewan', None),
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

PRODUCT_SUPPLIERS = {
    1: 'PT Indofood Sukses Makmur', 2: 'PT Coca-Cola Indonesia', 3: 'PT Heinz ABC Indonesia',
    4: 'PT Indofood Sukses Makmur', 5: 'PT Frisian Flag Indonesia', 6: 'PT Nippon Indosari',
    7: 'PT Charoen Pokphand', 8: 'PT Unilever Indonesia', 9: 'PT Wings Group',
    10: 'PT Softex Indonesia', 11: 'PT Pabrik Kertas Tjiwi Kimia', 12: 'PT Royal Canin Indonesia',
}

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


def create_master_db():
    db_path = f'{DATA_DIR}/master.db'
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.executescript('''
        CREATE TABLE branches (
            id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL, region TEXT NOT NULL
        );
        CREATE TABLE categories (
            id INTEGER PRIMARY KEY, name TEXT NOT NULL, parent_id INTEGER
        );
        CREATE TABLE products (
            id INTEGER PRIMARY KEY, sku TEXT UNIQUE NOT NULL, name TEXT NOT NULL,
            category_id INTEGER NOT NULL, unit TEXT DEFAULT 'pcs',
            supplier_price INTEGER NOT NULL, retail_price INTEGER NOT NULL,
            supplier_id INTEGER NOT NULL
        );
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY, name TEXT NOT NULL, member_id TEXT UNIQUE,
            phone TEXT, city TEXT, join_date TEXT NOT NULL
        );
        CREATE TABLE sales_headers (
            id INTEGER PRIMARY KEY, branch_id INTEGER NOT NULL, customer_id INTEGER,
            transaction_date TEXT NOT NULL, payment_method TEXT NOT NULL, total_amount INTEGER NOT NULL
        );
        CREATE TABLE sales_items (
            id INTEGER PRIMARY KEY, sale_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL, quantity INTEGER NOT NULL,
            unit_price INTEGER NOT NULL, subtotal INTEGER NOT NULL
        );
        CREATE TABLE suppliers (
            id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT,
            contact TEXT, payment_terms TEXT NOT NULL
        );
        CREATE TABLE purchase_orders (
            id INTEGER PRIMARY KEY, supplier_id INTEGER NOT NULL, branch_id INTEGER NOT NULL,
            order_date TEXT NOT NULL, status TEXT NOT NULL, total_amount INTEGER NOT NULL
        );
        CREATE TABLE inventory (
            id INTEGER PRIMARY KEY, branch_id INTEGER NOT NULL, product_id INTEGER NOT NULL,
            stock_qty INTEGER NOT NULL, last_updated TEXT NOT NULL
        );
    ''')

    cur.executemany('INSERT INTO branches VALUES (?,?,?,?)', BRANCHES)
    cur.executemany('INSERT INTO categories VALUES (?,?,?)', CATEGORIES)

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
    cur.executemany('INSERT INTO products (sku, name, category_id, unit, supplier_price, retail_price, supplier_id) VALUES (?,?,?,?,?,?,?)', products_data)

    customers_data = []
    first_names = ['Ahmad', 'Budi', 'Citra', 'Dedi', 'Eka', 'Fitri', 'Gilang', 'Hana', 'Irfan', 'Juni',
                   'Kartika', 'Lilis', 'Maman', 'Nina', 'Oman', 'Putri', 'Qori', 'Rudi', 'Sari', 'Tono',
                   'Ujang', 'Vina', 'Wawan', 'Yanti', 'Zaki']
    for i in range(1, 1001):
        name = f'{random.choice(first_names)} {random.choice(["S.", "P.", "A.", "Setiawan", "Suryana", "Hidayat", "Wijaya", "Kusuma", "Pratama", "Nugraha"])}'
        member_id = f'MEM-{i:05d}'
        phone = f'08{random.randint(100000000, 999999999)}'
        city = random.choice(CITIES)
        join_date = f'2025-{random.randint(1,12):02d}-{random.randint(1,28):02d}'
        customers_data.append((i, name, member_id, phone, city, join_date))
    cur.executemany('INSERT INTO customers VALUES (?,?,?,?,?,?)', customers_data)

    start_date = datetime(2026, 1, 1)
    end_date = datetime(2026, 3, 31)
    all_dates = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

    print('Generating 10.000 sales transactions...')
    sale_id = 1
    item_id = 1
    sales_batch = []
    items_batch = []
    for date in all_dates:
        num_trans = random.randint(80, 160)
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
            if sale_id % 2000 == 0:
                print(f'  Generated {sale_id} sales...')

    cur.executemany('INSERT INTO sales_headers VALUES (?,?,?,?,?,?)', sales_batch)
    cur.executemany('INSERT INTO sales_items VALUES (?,?,?,?,?,?)', items_batch)

    suppliers_data = [(i+1, *s) for i, s in enumerate(SUPPLIERS_INFO)]
    cur.executemany('INSERT INTO suppliers VALUES (?,?,?,?,?)', suppliers_data)

    po_statuses = ['SELESAI', 'SELESAI', 'SELESAI', 'DIPO', 'DIKIRIM']
    po_data = []
    for i in range(1, 501):
        supplier_id = random.randint(1, len(suppliers_data))
        branch_id = random.randint(1, 10)
        order_date = f'2026-{random.randint(1,3):02d}-{random.randint(1,28):02d}'
        status = random.choice(po_statuses)
        total = random.randint(1000000, 50000000)
        po_data.append((i, supplier_id, branch_id, order_date, status, total))
    cur.executemany('INSERT INTO purchase_orders VALUES (?,?,?,?,?,?)', po_data)

    inv_data = []
    for branch_id in range(1, 11):
        for product_id in range(1, len(products_data) + 1):
            if random.random() < 0.7:
                stock = random.randint(0, 500)
                last_upd = f'2026-{random.randint(1,3):02d}-{random.randint(1,28):02d}'
                inv_data.append((branch_id * 1000 + product_id, branch_id, product_id, stock, last_upd))
    cur.executemany('INSERT INTO inventory VALUES (?,?,?,?,?)', inv_data)

    conn.commit()
    conn.close()
    print(f'Master DB created: {sale_id-1} sales, {item_id-1} items')
    return db_path


def create_reporting_db():
    db_path = f'{DATA_DIR}/reporting.db'
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.executescript('''
        CREATE TABLE daily_sales_by_branch (
            date TEXT NOT NULL, branch_id INTEGER NOT NULL,
            branch_name TEXT NOT NULL, total_sales INTEGER NOT NULL,
            transaction_count INTEGER NOT NULL,
            PRIMARY KEY (date, branch_id)
        );
        CREATE TABLE daily_sales_by_category (
            date TEXT NOT NULL, category_id INTEGER NOT NULL,
            category_name TEXT NOT NULL, total_sales INTEGER NOT NULL,
            qty_sold INTEGER NOT NULL,
            PRIMARY KEY (date, category_id)
        );
        CREATE TABLE monthly_sales_summary (
            year_month TEXT NOT NULL, branch_id INTEGER NOT NULL,
            branch_name TEXT NOT NULL, total_sales INTEGER NOT NULL,
            total_qty INTEGER NOT NULL, avg_transaction REAL NOT NULL,
            PRIMARY KEY (year_month, branch_id)
        );
        CREATE TABLE payment_method_summary (
            date TEXT NOT NULL, payment_method TEXT NOT NULL,
            total_amount INTEGER NOT NULL, transaction_count INTEGER NOT NULL,
            PRIMARY KEY (date, payment_method)
        );
        CREATE TABLE top_products (
            month TEXT NOT NULL, product_id INTEGER NOT NULL,
            product_name TEXT NOT NULL, category_name TEXT NOT NULL,
            qty_sold INTEGER NOT NULL, total_revenue INTEGER NOT NULL,
            rank INTEGER NOT NULL,
            PRIMARY KEY (month, product_id)
        );
    ''')
    conn.commit()
    conn.close()
    print(f'Reporting DB created: {db_path}')
    return db_path


if __name__ == '__main__':
    print('=== SETUP DATABASE ===')
    create_master_db()
    create_reporting_db()
    print('\nSelesai! Jalankan:')
    print('  python 01_sql_basics.py')
    print('  python 02_sql_aggregation.py')
    print('  python 03_sql_joins.py')
