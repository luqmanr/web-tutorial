import psycopg2
import random
import os
from datetime import datetime, timedelta

BASE = os.path.dirname(os.path.abspath(__file__))
random.seed(42)

DB_CONFIG = dict(
    host='localhost', port=5432,
    dbname='reporting_db', user='report_user', password='report_pass',
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


def get_conn():
    return psycopg2.connect(**DB_CONFIG)


def create_tables(conn):
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS branches (
            id INTEGER PRIMARY KEY, name TEXT NOT NULL,
            city TEXT NOT NULL, region TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY, name TEXT NOT NULL, parent_id INTEGER
        );
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY, sku TEXT UNIQUE NOT NULL, name TEXT NOT NULL,
            category_id INTEGER NOT NULL, unit TEXT DEFAULT 'pcs',
            supplier_price INTEGER NOT NULL, retail_price INTEGER NOT NULL,
            supplier_id INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY, name TEXT NOT NULL, member_id TEXT UNIQUE,
            phone TEXT, city TEXT, join_date DATE NOT NULL
        );
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT,
            contact TEXT, payment_terms TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS sales_headers (
            id INTEGER PRIMARY KEY, branch_id INTEGER NOT NULL, customer_id INTEGER,
            transaction_date DATE NOT NULL, payment_method TEXT NOT NULL,
            total_amount INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS sales_items (
            id INTEGER PRIMARY KEY, sale_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL, quantity INTEGER NOT NULL,
            unit_price INTEGER NOT NULL, subtotal INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS purchase_orders (
            id INTEGER PRIMARY KEY, supplier_id INTEGER NOT NULL, branch_id INTEGER NOT NULL,
            order_date DATE NOT NULL, status TEXT NOT NULL, total_amount INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY, branch_id INTEGER NOT NULL, product_id INTEGER NOT NULL,
            stock_qty INTEGER NOT NULL, last_updated DATE NOT NULL
        );
    ''')
    conn.commit()


def seed_master_data(conn):
    cur = conn.cursor()

    cur.execute('TRUNCATE branches, categories, products, customers, suppliers, sales_headers, sales_items, purchase_orders, inventory RESTART IDENTITY CASCADE')

    for b in BRANCHES:
        cur.execute('INSERT INTO branches VALUES (%s,%s,%s,%s)', b)
    print(f'  branches: {len(BRANCHES)}')

    for c in CATEGORIES:
        cur.execute('INSERT INTO categories VALUES (%s,%s,%s)', c)
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
        cur.execute('INSERT INTO products (sku, name, category_id, unit, supplier_price, retail_price, supplier_id) VALUES (%s,%s,%s,%s,%s,%s,%s)', p)
    print(f'  products: {len(products_data)}')

    first_names = ['Ahmad', 'Budi', 'Citra', 'Dedi', 'Eka', 'Fitri', 'Gilang', 'Hana', 'Irfan', 'Juni',
                   'Kartika', 'Lilis', 'Maman', 'Nina', 'Oman', 'Putri', 'Qori', 'Rudi', 'Sari', 'Tono',
                   'Ujang', 'Vina', 'Wawan', 'Yanti', 'Zaki']
    customers_data = []
    for i in range(1, 1001):
        name = f'{random.choice(first_names)} {random.choice(["S.", "P.", "A.", "Setiawan", "Suryana", "Hidayat", "Wijaya", "Kusuma", "Pratama", "Nugraha"])}'
        member_id = f'MEM-{i:05d}'
        phone = f'08{random.randint(100000000, 999999999)}'
        city = random.choice(CITIES)
        join_date = f'2025-{random.randint(1,12):02d}-{random.randint(1,28):02d}'
        customers_data.append((i, name, member_id, phone, city, join_date))
    for c in customers_data:
        cur.execute('INSERT INTO customers VALUES (%s,%s,%s,%s,%s,%s)', c)
    print(f'  customers: {len(customers_data)}')

    for i, s in enumerate(SUPPLIERS_INFO, 1):
        cur.execute('INSERT INTO suppliers VALUES (%s,%s,%s,%s,%s)', (i, *s))
    print(f'  suppliers: {len(SUPPLIERS_INFO)}')

    start_date = datetime(2026, 1, 1)
    end_date = datetime(2026, 3, 31)
    all_dates = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

    print('  Generating sales transactions...')
    sale_id = 1
    item_id = 1
    po_statuses = ['SELESAI', 'SELESAI', 'SELESAI', 'DIPO', 'DIKIRIM']

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
                cur.execute('INSERT INTO sales_items VALUES (%s,%s,%s,%s,%s,%s)',
                            (item_id, sale_id, product_id, qty, unit_price, subtotal))
                item_id += 1
            cur.execute('INSERT INTO sales_headers VALUES (%s,%s,%s,%s,%s,%s)',
                        (sale_id, branch_id, customer_id, date_str, pay_method, total))
            sale_id += 1

    print(f'  sales_headers: {sale_id - 1}')

    po_data = []
    for i in range(1, 501):
        supplier_id = random.randint(1, len(SUPPLIERS_INFO))
        branch_id = random.randint(1, 10)
        order_date = f'2026-{random.randint(1,3):02d}-{random.randint(1,28):02d}'
        status = random.choice(po_statuses)
        total = random.randint(1000000, 50000000)
        po_data.append((i, supplier_id, branch_id, order_date, status, total))
    for p in po_data:
        cur.execute('INSERT INTO purchase_orders VALUES (%s,%s,%s,%s,%s,%s)', p)
    print(f'  purchase_orders: {len(po_data)}')

    inv_count = 0
    for branch_id in range(1, 11):
        for product_id in range(1, len(products_data) + 1):
            if random.random() < 0.7:
                stock = random.randint(0, 500)
                last_upd = f'2026-{random.randint(1,3):02d}-{random.randint(1,28):02d}'
                cur.execute('INSERT INTO inventory VALUES (%s,%s,%s,%s,%s)',
                            (branch_id * 1000 + product_id, branch_id, product_id, stock, last_upd))
                inv_count += 1
    print(f'  inventory: {inv_count}')

    conn.commit()


def create_reporting_tables(conn):
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS daily_sales_by_branch (
            date DATE NOT NULL, branch_id INTEGER NOT NULL,
            branch_name TEXT NOT NULL, total_sales INTEGER NOT NULL,
            transaction_count INTEGER NOT NULL,
            PRIMARY KEY (date, branch_id)
        );
        CREATE TABLE IF NOT EXISTS daily_sales_by_category (
            date DATE NOT NULL, category_id INTEGER NOT NULL,
            category_name TEXT NOT NULL, total_sales INTEGER NOT NULL,
            qty_sold INTEGER NOT NULL,
            PRIMARY KEY (date, category_id)
        );
        CREATE TABLE IF NOT EXISTS monthly_sales_summary (
            year_month TEXT NOT NULL, branch_id INTEGER NOT NULL,
            branch_name TEXT NOT NULL, total_sales INTEGER NOT NULL,
            total_qty INTEGER NOT NULL, avg_transaction REAL NOT NULL,
            PRIMARY KEY (year_month, branch_id)
        );
        CREATE TABLE IF NOT EXISTS payment_method_summary (
            date DATE NOT NULL, payment_method TEXT NOT NULL,
            total_amount INTEGER NOT NULL, transaction_count INTEGER NOT NULL,
            PRIMARY KEY (date, payment_method)
        );
        CREATE TABLE IF NOT EXISTS top_products (
            month TEXT NOT NULL, product_id INTEGER NOT NULL,
            product_name TEXT NOT NULL, category_name TEXT NOT NULL,
            qty_sold INTEGER NOT NULL, total_revenue INTEGER NOT NULL,
            rank INTEGER NOT NULL,
            PRIMARY KEY (month, product_id)
        );
    ''')
    conn.commit()


def populate_reporting(conn):
    cur = conn.cursor()

    cur.execute('TRUNCATE daily_sales_by_branch, daily_sales_by_category, monthly_sales_summary, payment_method_summary, top_products')

    cur.execute('''
        INSERT INTO daily_sales_by_branch (date, branch_id, branch_name, total_sales, transaction_count)
        SELECT sh.transaction_date, b.id, b.name,
               SUM(sh.total_amount), COUNT(DISTINCT sh.id)
        FROM sales_headers sh
        JOIN branches b ON sh.branch_id = b.id
        GROUP BY sh.transaction_date, b.id
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
        GROUP BY sh.transaction_date, c.id
    ''')
    print(f'  daily_sales_by_category: {cur.rowcount}')

    cur.execute('''
        INSERT INTO monthly_sales_summary (year_month, branch_id, branch_name, total_sales, total_qty, avg_transaction)
        SELECT TO_CHAR(sh.transaction_date, 'YYYY-MM'), b.id, b.name,
               SUM(si.subtotal), SUM(si.quantity),
               ROUND(AVG(si.subtotal)::numeric, 2)::real
        FROM sales_headers sh
        JOIN branches b ON sh.branch_id = b.id
        JOIN sales_items si ON sh.id = si.sale_id
        GROUP BY TO_CHAR(sh.transaction_date, 'YYYY-MM'), b.id
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
        SELECT TO_CHAR(sh.transaction_date, 'YYYY-MM'), p.id, p.name, c.name,
               SUM(si.quantity), SUM(si.subtotal),
               RANK() OVER (
                   PARTITION BY TO_CHAR(sh.transaction_date, 'YYYY-MM')
                   ORDER BY SUM(si.subtotal) DESC
               )
        FROM sales_headers sh
        JOIN sales_items si ON sh.id = si.sale_id
        JOIN products p ON si.product_id = p.id
        JOIN categories c ON p.category_id = c.id
        GROUP BY TO_CHAR(sh.transaction_date, 'YYYY-MM'), p.id
    ''')
    print(f'  top_products: {cur.rowcount}')

    conn.commit()


if __name__ == '__main__':
    print('=== SETUP POSTGRESQL ===')
    print('Pastikan container PostgreSQL sudah jalan:')
    print('  docker compose up -d\n')

    try:
        conn = get_conn()
    except Exception as e:
        print(f'ERROR: Tidak bisa konek ke PostgreSQL: {e}')
        print('Jalankan: docker compose up -d')
        exit(1)

    print('1. Membuat tables...')
    create_tables(conn)

    print('2. Mengisi master data...')
    seed_master_data(conn)

    print('3. Membuat reporting tables...')
    create_reporting_tables(conn)

    print('4. Mengisi reporting data...')
    populate_reporting(conn)

    conn.close()
    print('\nSelesai! Sekarang jalankan frontend:')
    print('  streamlit run 02_frontend_streamlit.py')
    print('  python 03_frontend_html_bootstrap.py')
