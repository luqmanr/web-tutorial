import mssql_python
import sqlite3
import os

import config
MSSQL_CONFIG = config.MSSQL_CONFIG

"""
https://pastebin.com/2vPqS0e2
"""

CONN_STR = (
    f"SERVER={MSSQL_CONFIG['server']},{MSSQL_CONFIG['port']};"
    f"DATABASE={MSSQL_CONFIG['database']};"
    f"UID={MSSQL_CONFIG['username']};"
    f"PWD={MSSQL_CONFIG['password']};"
    "TrustServerCertificate=yes;"
)

DATA_DIR = './data'
os.makedirs(DATA_DIR, exist_ok=True)

def export_to_sqlite(mssql_cur):
    db_path = os.path.join(DATA_DIR, 'data_retail.db')
    sl_conn = sqlite3.connect(db_path)
    sl_cur = sl_conn.cursor()
    sqlite_insert_query = """
        select * from transformed_inventory where product_id=24"""
    try:
        sl_cur.execute(sqlite_insert_query)
        rows = sl_cur.fetchall()
        # print(f'berhasil query sqlite, jumlah rows: {len(rows)}')
        for r in rows:
            print(r)
    except Exception as e:
        print(f'error inserting into sqlite: {e}')
        return

if __name__ == '__main__':
    print('Pastikan container MSSQL sudah jalan:')
    conn = mssql_python.connect(CONN_STR, fast_executemany=True)
    cur = conn.cursor()

    export_to_sqlite(cur)