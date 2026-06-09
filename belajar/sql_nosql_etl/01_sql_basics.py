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
        print('  ' + '-' * (sum(len(c) for c in cols) + 3 * (len(cols) - 1)))
        for row in rows:
            print('  ' + ' | '.join(str(v) if v is not None else 'NULL' for v in row))
        print(f'  ({len(rows)} rows)')
    except Exception as e:
        print(f'  ERROR: {e}')
    finally:
        conn.close()


print('=' * 60)
print('SOAL 1: SELECT & WHERE')
print('Tampilkan semua produk yang harga jualnya (retail_price)')
print('di atas Rp 50.000. Tampilkan kolom: id, name, retail_price.')
print('Urutkan dari termahal ke termurah.')
print('=' * 60)
sql_soal_1 = """
-- GANTI query di bawah ini
SELECT id, name, retail_price FROM products WHERE 1=0
"""
print('\nJawaban kamu:')
q(sql_soal_1)

print('\n' + '=' * 60)
print('SOAL 2: LIKE / Pencarian')
print('Cari semua produk yang namanya mengandung kata "Kecap"')
print('Tampilkan: id, name, category_id, retail_price')
print('=' * 60)
sql_soal_2 = """
-- GANTI query di bawah ini
SELECT id, name, category_id, retail_price FROM products WHERE 1=0
"""
print('\nJawaban kamu:')
q(sql_soal_2)

print('\n' + '=' * 60)
print('SOAL 3: IN / BETWEEN')
print('Tampilkan produk dengan category_id 1, 3, atau 5')
print('dan harga jual antara Rp 10.000 sampai Rp 30.000')
print('Tampilkan: id, name, category_id, retail_price')
print('Urutkan berdasarkan category_id, lalu harga naik.')
print('=' * 60)
sql_soal_3 = """
-- GANTI query di bawah ini
SELECT id, name, category_id, retail_price FROM products WHERE 1=0
"""
print('\nJawaban kamu:')
q(sql_soal_3)

print('\n' + '=' * 60)
print('SOAL 4: DISTINCT & COUNT')
print('Ada berapa kota asal pelanggan (customers) yang berbeda?')
print('Tampilkan: jumlah_kota')
print('=' * 60)
sql_soal_4 = """
-- GANTI query di bawah ini
SELECT 0 as jumlah_kota
"""
print('\nJawaban kamu:')
q(sql_soal_4)

print('\n' + '=' * 60)
print('SOAL 5: ORDER BY & LIMIT')
print('Tampilkan 10 transaksi (sales_headers) dengan total_amount')
print('terbesar. Tampilkan: id, branch_id, total_amount, payment_method')
print('=' * 60)
sql_soal_5 = """
-- GANTI query di bawah ini
SELECT id, branch_id, total_amount, payment_method FROM sales_headers WHERE 1=0
"""
print('\nJawaban kamu:')
q(sql_soal_5)
