import sqlite3
import os

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, 'data/master.db')


def q(sql):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    try:
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
    except Exception as e:
        print(f'  ERROR: {e}')
    finally:
        conn.close()


print('=' * 60)
print('SOAL 1: RANK() penjualan per cabang')
print('Buat peringkat cabang berdasarkan total penjualan:')
print('Kolom: nama_cabang, total_penjualan, peringkat')
print('Gunakan RANK() ORDER BY total_penjualan DESC')
print('HINT: bikin subquery dulu untuk total per cabang,')
print('      lalu RANK di outer query')
print('=' * 60)
sql_soal_1 = """
-- GANTI query di bawah ini
WITH ranked AS (
    SELECT b.name as nama_cabang
    FROM sales_headers sh
    JOIN branches b ON sh.branch_id = b.id
    WHERE 1=0
)
SELECT * FROM ranked
"""
print('\nJawaban kamu:')
q(sql_soal_1)

print('\n' + '=' * 60)
print('SOAL 2: Running total penjualan harian')
print('Tampilkan akumulasi penjualan harian di bulan Januari 2026:')
print('Kolom: tanggal, penjualan_harian, running_total')
print('Gunakan SUM() OVER (ORDER BY tanggal)')
print('=' * 60)
sql_soal_2 = """
-- GANTI query di bawah ini
WITH daily AS (
    SELECT transaction_date as tanggal, SUM(total_amount) as penjualan_harian
    FROM sales_headers
    WHERE 1=0
)
SELECT tanggal, penjualan_harian FROM daily
ORDER BY tanggal
"""
print('\nJawaban kamu:')
q(sql_soal_2)

print('\n' + '=' * 60)
print('SOAL 3: TOP produk terlaris per kategori')
print('Tampilkan peringkat produk dalam setiap kategori:')
print('Kolom: nama_kategori, nama_produk, total_qty, peringkat_di_kategori')
print('Gunakan RANK() PARTITION BY category_id')
print('=' * 60)
sql_soal_3 = """
-- GANTI query di bawah ini
WITH product_sales AS (
    SELECT p.category_id, p.name as nama_produk, SUM(si.quantity) as total_qty
    FROM sales_items si
    JOIN products p ON si.product_id = p.id
    WHERE 1=0
)
SELECT c.name as nama_kategori, ps.nama_produk, ps.total_qty
FROM product_sales ps
JOIN categories c ON ps.category_id = c.id
ORDER BY c.name, ps.total_qty DESC
LIMIT 15
"""
print('\nJawaban kamu:')
q(sql_soal_3)

print('\n' + '=' * 60)
print('SOAL 4: Selisih penjualan dengan hari sebelumnya')
print('Kolom: tanggal, penjualan_harian, penjualan_kemarin, selisih')
print('Gunakan LAG() untuk ambil nilai hari sebelumnya.')
print('=' * 60)
sql_soal_4 = """
-- GANTI query di bawah ini
WITH daily AS (
    SELECT transaction_date as tanggal, SUM(total_amount) as penjualan_harian
    FROM sales_headers
    WHERE 1=0
)
SELECT tanggal, penjualan_harian FROM daily
ORDER BY tanggal
LIMIT 10
"""
print('\nJawaban kamu:')
q(sql_soal_4)
