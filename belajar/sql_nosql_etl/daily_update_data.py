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
    
    sqlite_ensure_db = """
        CREATE TABLE IF NOT EXISTS transformed_inventory (
            id INT PRIMARY KEY, 
            product_name TEXT,
            branch_id INT, 
            branch_name TEXT, 
            product_id INT, 
            product_category TEXT, 
            stock_qty INT, 
            last_updated DATETIME)"""
    
    try:
        sl_cur.execute(sqlite_ensure_db)
        print(f'successfully ensured sqlite table exists')
    except Exception as e:
        print(f'error ensuring sqlitedb exist: {e}')
        return
    
    sqlite_get_last_updated = """
        SELECT MAX(last_updated) FROM transformed_inventory"""
    try:
        last_updated = sl_cur.execute(sqlite_get_last_updated).fetchone()[0]
        print(f'last_updated: {last_updated}')
    except Exception as e:
        print(f'error getting last_updated from sqlite: {e}')
        return

    query = """
        SELECT 
            inventory.id,
            products.name as product_name,
            inventory.branch_id,
            branches.name AS branch_name,
            inventory.product_id,
            categories.name AS product_category,
            inventory.stock_qty,
            inventory.last_updated
            FROM 
                inventory 
            JOIN 
                branches ON inventory.branch_id = branches.id
            JOIN
                products ON inventory.product_id = products.id 
            JOIN
                categories ON products.category_id = categories.id
            WHERE
                inventory.last_updated >= ?"""
    try:
        rows = mssql_cur.execute(query, (last_updated)).fetchall()
        print(f'berhasil query mssql, jumlah rows: {len(rows)}')
    except Exception as e:
        print(f'error querying mssql: {e}')
        return
    
    # delete rows that have same id as rows from mssql
    if rows:
        ids = [row[0] for row in rows]
        sqlite_delete_query = f"""
            DELETE FROM 
                transformed_inventory 
                WHERE id IN ({','.join(['?']*len(ids))})"""
        try:
            sl_cur.execute(sqlite_delete_query, ids)
            sl_conn.commit()
            print(f'successfully deleted {len(ids)} rows from sqlite')
        except Exception as e:
            print(f'error deleting from sqlite: {e}')
            return

    sqlite_insert_query = """
        INSERT INTO transformed_inventory (
            id, 
            product_name,
            branch_id, 
            branch_name, 
            product_id, 
            product_category, 
            stock_qty, 
            last_updated)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
    try:
        sl_cur.executemany(sqlite_insert_query, rows)
        sl_conn.commit()
        print(f'successfully inserted {len(rows)} rows into sqlite')
    except Exception as e:
        print(f'error inserting into sqlite: {e}')
        return

if __name__ == '__main__':
    print('Pastikan container MSSQL sudah jalan:')
    conn = mssql_python.connect(CONN_STR, fast_executemany=True)
    cur = conn.cursor()

    export_to_sqlite(cur)