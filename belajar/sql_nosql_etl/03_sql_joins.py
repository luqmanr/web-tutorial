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
        print('  ' + '-' * max(40, sum(len(c) for c in cols) + 3 * (len(cols) - 1)))
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
    except Exception as e:
        print(f'  ERROR: {e}')
    finally:
        conn.close()


print('=' * 60)
print('SOAL 1: INNER JOIN (sales_headers + branches)')
print('Tampilkan total penjualan per cabang dengan NAMA cabang')
print('Kolom: nama_cabang, kota, total_penjualan')
print('Urutkan dari total terbesar.')
print('GABUNGKAN sales_headers dengan branches')
print('=' * 60)
sql_soal_1 = """
-- GANTI query di bawah ini
SELECT b.name as nama_cabang, b.city as kota
FROM sales_headers sh
JOIN branches b ON sh.branch_id = b.id
WHERE 1=0
"""
print('\nJawaban kamu:')
q(sql_soal_1)

print('\n' + '=' * 60)
print('SOAL 2: JOIN 3 TABEL (items + products + categories)')
print('Tampilkan total penjualan per kategori produk:')
print('Kolom: nama_kategori, total_qty_terjual, total_revenue')
print('GABUNGKAN sales_items → products → categories')
print('Urutkan dari total revenue terbesar.')
print('=' * 60)
sql_soal_2 = """
-- GANTI query di bawah ini
SELECT c.name as nama_kategori
FROM sales_items si
JOIN products p ON si.product_id = p.id
JOIN categories c ON p.category_id = c.id
WHERE 1=0
"""
print('\nJawaban kamu:')
q(sql_soal_2)

print('\n' + '=' * 60)
print('SOAL 3: JOIN dengan tanggal')
print('Tampilkan penjualan per cabang per hari di bulan Januari 2026:')
print('Kolom: tanggal, nama_cabang, kota, total_penjualan')
print('Urutkan dari tanggal, lalu total terbesar.')
print('=' * 60)
sql_soal_3 = """
-- GANTI query di bawah ini
SELECT sh.transaction_date as tanggal, b.name as nama_cabang, b.city as kota
FROM sales_headers sh
JOIN branches b ON sh.branch_id = b.id
WHERE 1=0
"""
print('\nJawaban kamu:')
q(sql_soal_3)

print('\n' + '=' * 60)
print('SOAL 4: LEFT JOIN (customers yang belanja)')
print('Tampilkan 10 pelanggan dengan total belanja terbanyak:')
print('Kolom: nama_pelanggan, member_id, kota, total_belanja, jumlah_transaksi')
print('HINT: LEFT JOIN customers dengan sales_headers, GROUP BY customer')
print('=' * 60)
sql_soal_4 = """
-- GANTI query di bawah ini
SELECT c.name as nama_pelanggan, c.member_id, c.city as kota
FROM customers c
LEFT JOIN sales_headers sh ON c.id = sh.customer_id
WHERE 1=0
"""
print('\nJawaban kamu:')
q(sql_soal_4)

print('\n' + '=' * 60)
print('SOAL 5: Multi-join lengkap (branch + category)')
print('Tampilkan total penjualan per cabang per kategori:')
print('Kolom: nama_cabang, nama_kategori, total_revenue')
print('GABUNGKAN: sales_headers → branch + sales_items → products → categories')
print('Urutkan: nama_cabang A-Z, total_revenue DESC.')
print('=' * 60)
sql_soal_5 = """
-- GANTI query di bawah ini
SELECT b.name as nama_cabang, c.name as nama_kategori
FROM sales_headers sh
JOIN branches b ON sh.branch_id = b.id
JOIN sales_items si ON sh.id = si.sale_id
JOIN products p ON si.product_id = p.id
JOIN categories c ON p.category_id = c.id
WHERE 1=0
"""
print('\nJawaban kamu:')
q(sql_soal_5)
