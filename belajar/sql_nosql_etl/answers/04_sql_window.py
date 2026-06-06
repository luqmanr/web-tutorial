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
                vals.append(f'{v:,.2f}')
            elif isinstance(v, int):
                vals.append(f'{v:,}')
            else:
                vals.append(str(v) if v is not None else 'NULL')
        print('  ' + ' | '.join(vals))
    print(f'  ({len(rows)} rows)')
    conn.close()


print('=== JAWABAN: SQL Window Functions ===\n')

print('Soal 1: Peringkat cabang berdasarkan total penjualan')
q('''
    WITH branch_sales AS (
        SELECT b.name as nama_cabang,
               SUM(sh.total_amount) as total_penjualan
        FROM sales_headers sh
        JOIN branches b ON sh.branch_id = b.id
        GROUP BY b.name
    )
    SELECT nama_cabang, total_penjualan,
           RANK() OVER (ORDER BY total_penjualan DESC) as peringkat
    FROM branch_sales
    ORDER BY peringkat
''')

print('\nSoal 2: Running total penjualan harian (Jan 2026)')
q('''
    WITH daily AS (
        SELECT transaction_date as tanggal,
               SUM(total_amount) as penjualan_harian
        FROM sales_headers
        WHERE transaction_date >= '2026-01-01' AND transaction_date < '2026-02-01'
        GROUP BY transaction_date
    )
    SELECT tanggal, penjualan_harian,
           SUM(penjualan_harian) OVER (ORDER BY tanggal) as running_total
    FROM daily
    ORDER BY tanggal
''')

print('\nSoal 3: TOP 3 produk terlaris per kategori')
q('''
    WITH product_sales AS (
        SELECT p.category_id, p.name as nama_produk,
               SUM(si.quantity) as total_qty,
               RANK() OVER (PARTITION BY p.category_id ORDER BY SUM(si.quantity) DESC) as peringkat_di_kategori
        FROM sales_items si
        JOIN products p ON si.product_id = p.id
        GROUP BY p.category_id, p.name
    )
    SELECT c.name as nama_kategori, ps.nama_produk, ps.total_qty, ps.peringkat_di_kategori
    FROM product_sales ps
    JOIN categories c ON ps.category_id = c.id
    WHERE ps.peringkat_di_kategori <= 3
    ORDER BY c.name, ps.peringkat_di_kategori
''')

print('\nSoal 4: Selisih penjualan dengan hari sebelumnya')
q('''
    WITH daily AS (
        SELECT transaction_date as tanggal,
               SUM(total_amount) as penjualan_harian
        FROM sales_headers
        WHERE transaction_date >= '2026-01-01' AND transaction_date < '2026-02-01'
        GROUP BY transaction_date
    )
    SELECT tanggal, penjualan_harian,
           LAG(penjualan_harian) OVER (ORDER BY tanggal) as penjualan_kemarin,
           penjualan_harian - LAG(penjualan_harian) OVER (ORDER BY tanggal) as selisih
    FROM daily
    ORDER BY tanggal
    LIMIT 10
''')
