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
    print('  ' + '-' * max(50, sum(len(c) for c in cols) + 3 * (len(cols) - 1)))
    for row in rows:
        vals = []
        for v in row:
            if isinstance(v, float):
                vals.append(f'{v:,.0f}')
            elif isinstance(v, int):
                vals.append(f'{v:,}')
            else:
                vals.append(str(v) if v is not None else 'NULL')
        print('  ' + ' | '.join(vals))
    print(f'  ({len(rows)} rows)')
    conn.close()


print('=== JAWABAN: SQL Joins ===\n')

print('Soal 1: Total penjualan per cabang (dengan nama)')
q('''
    SELECT b.name as nama_cabang, b.city as kota,
           SUM(sh.total_amount) as total_penjualan
    FROM sales_headers sh
    JOIN branches b ON sh.branch_id = b.id
    GROUP BY b.name, b.city
    ORDER BY total_penjualan DESC
''')

print('\nSoal 2: Total penjualan per kategori')
q('''
    SELECT c.name as nama_kategori,
           SUM(si.quantity) as total_qty_terjual,
           SUM(si.subtotal) as total_revenue
    FROM sales_items si
    JOIN products p ON si.product_id = p.id
    JOIN categories c ON p.category_id = c.id
    GROUP BY c.name
    ORDER BY total_revenue DESC
''')

print('\nSoal 3: Penjualan per cabang per hari (Jan 2026)')
q('''
    SELECT sh.transaction_date as tanggal,
           b.name as nama_cabang, b.city as kota,
           SUM(sh.total_amount) as total_penjualan
    FROM sales_headers sh
    JOIN branches b ON sh.branch_id = b.id
    WHERE sh.transaction_date >= '2026-01-01' AND sh.transaction_date < '2026-02-01'
    GROUP BY sh.transaction_date, b.name, b.city
    ORDER BY tanggal, total_penjualan DESC
''')

print('\nSoal 4: Top 10 pelanggan dengan total belanja terbanyak')
q('''
    SELECT c.name as nama_pelanggan, c.member_id, c.city as kota,
           COALESCE(SUM(sh.total_amount), 0) as total_belanja,
           COUNT(sh.id) as jumlah_transaksi
    FROM customers c
    LEFT JOIN sales_headers sh ON c.id = sh.customer_id
    GROUP BY c.id
    ORDER BY total_belanja DESC
    LIMIT 10
''')

print('\nSoal 5: Total penjualan per cabang per kategori')
q('''
    SELECT b.name as nama_cabang, c.name as nama_kategori,
           SUM(si.subtotal) as total_revenue
    FROM sales_headers sh
    JOIN branches b ON sh.branch_id = b.id
    JOIN sales_items si ON sh.id = si.sale_id
    JOIN products p ON si.product_id = p.id
    JOIN categories c ON p.category_id = c.id
    GROUP BY b.name, c.name
    ORDER BY b.name, total_revenue DESC
''')
