import sqlite3
import os

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, '..', 'data/master.db')


def q(sql):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]
    print('  ' + ' | '.join(cols))
    print('  ' + '-' * max(40, sum(len(c) for c in cols) + 3 * (len(cols) - 1)))
    for row in rows:
        vals = [f'{v:,}' if isinstance(v, int) else str(v) for v in row]
        print('  ' + ' | '.join(vals))
    print(f'  ({len(rows)} rows)')
    conn.close()


print('=== JAWABAN: SQL Basics ===\n')

print('Soal 1: Produk dengan retail_price > 50000')
q('''
    SELECT id, name, retail_price
    FROM products
    WHERE retail_price > 50000
    ORDER BY retail_price DESC
''')

print('\nSoal 2: Produk mengandung "Kecap"')
q('''
    SELECT id, name, category_id, retail_price
    FROM products
    WHERE name LIKE '%Kecap%'
''')

print('\nSoal 3: category_id IN (1,3,5) dan harga 10000-30000')
q('''
    SELECT id, name, category_id, retail_price
    FROM products
    WHERE category_id IN (1, 3, 5)
      AND retail_price BETWEEN 10000 AND 30000
    ORDER BY category_id, retail_price
''')

print('\nSoal 4: Jumlah kota unik pelanggan')
q('''
    SELECT COUNT(DISTINCT city) as jumlah_kota
    FROM customers
''')

print('\nSoal 5: Top 10 transaksi terbesar')
q('''
    SELECT id, branch_id, total_amount, payment_method
    FROM sales_headers
    ORDER BY total_amount DESC
    LIMIT 10
''')
