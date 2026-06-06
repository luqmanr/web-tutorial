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


print('=== JAWABAN: SQL Aggregation ===\n')

print('Soal 1: Total penjualan per cabang')
q('''
    SELECT branch_id, SUM(total_amount) as total_penjualan
    FROM sales_headers
    GROUP BY branch_id
    ORDER BY total_penjualan DESC
''')

print('\nSoal 2: Statistik per cabang')
q('''
    SELECT branch_id,
           COUNT(*) as jumlah_transaksi,
           AVG(total_amount) as rata_rata_transaksi,
           SUM(total_amount) as total_penjualan
    FROM sales_headers
    GROUP BY branch_id
    ORDER BY total_penjualan DESC
''')

print('\nSoal 3: Cabang dengan rata-rata > 200000')
q('''
    SELECT branch_id, AVG(total_amount) as avg_transaksi
    FROM sales_headers
    GROUP BY branch_id
    HAVING AVG(total_amount) > 200000
''')

print('\nSoal 4: Total penjualan per tanggal (Jan 2026)')
q('''
    SELECT transaction_date as tanggal,
           SUM(total_amount) as total_penjualan,
           COUNT(*) as jumlah_transaksi
    FROM sales_headers
    WHERE transaction_date >= '2026-01-01' AND transaction_date < '2026-02-01'
    GROUP BY transaction_date
    ORDER BY tanggal
''')

print('\nSoal 5: Metode pembayaran')
q('''
    SELECT payment_method,
           SUM(total_amount) as total_penjualan,
           COUNT(*) as jumlah_transaksi
    FROM sales_headers
    GROUP BY payment_method
    ORDER BY total_penjualan DESC
''')
