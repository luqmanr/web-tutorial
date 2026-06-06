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
print('SOAL 1: GROUP BY dengan SUM')
print('Tampilkan total penjualan per cabang (branch_id)')
print('Kolom: branch_id, total_penjualan')
print('Urutkan dari total terbesar.')
print('=' * 60)
sql_soal_1 = """
-- GANTI query di bawah ini
SELECT branch_id, SUM(total_amount) as total_penjualan
FROM sales_headers
WHERE 1=0
"""
print('\nJawaban kamu:')
q(sql_soal_1)

print('\n' + '=' * 60)
print('SOAL 2: GROUP BY dengan COUNT, AVG')
print('Tampilkan statistik per cabang:')
print('- jumlah_transaksi (COUNT)')
print('- rata_rata_transaksi (AVG total_amount)')
print('- total_penjualan (SUM)')
print('Urutkan dari total penjualan terbesar.')
print('=' * 60)
sql_soal_2 = """
-- GANTI query di bawah ini
SELECT branch_id FROM sales_headers WHERE 1=0
"""
print('\nJawaban kamu:')
q(sql_soal_2)

print('\n' + '=' * 60)
print('SOAL 3: HAVING')
print('Cabang mana saja yang memiliki rata-rata transaksi')
print('di atas Rp 200.000?')
print('Tampilkan: branch_id, avg_transaksi')
print('=' * 60)
sql_soal_3 = """
-- GANTI query di bawah ini
SELECT branch_id FROM sales_headers WHERE 1=0
"""
print('\nJawaban kamu:')
q(sql_soal_3)

print('\n' + '=' * 60)
print('SOAL 4: Aggregation per Tanggal')
print('Tampilkan total penjualan per tanggal di bulan Januari 2026')
print('Kolom: tanggal, total_penjualan, jumlah_transaksi')
print('Urutkan dari tanggal paling awal.')
print('=' * 60)
sql_soal_4 = """
-- GANTI query di bawah ini
SELECT transaction_date as tanggal FROM sales_headers WHERE 1=0
"""
print('\nJawaban kamu:')
q(sql_soal_4)

print('\n' + '=' * 60)
print('SOAL 5: Metode Pembayaran')
print('Tampilkan total penjualan per metode pembayaran')
print('Kolom: payment_method, total_penjualan, jumlah_transaksi')
print('Urutkan dari total penjualan terbesar.')
print('=' * 60)
sql_soal_5 = """
-- GANTI query di bawah ini
SELECT payment_method FROM sales_headers WHERE 1=0
"""
print('\nJawaban kamu:')
q(sql_soal_5)
