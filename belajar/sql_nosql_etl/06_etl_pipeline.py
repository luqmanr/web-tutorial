"""
ETL Pipeline: Master DB → Reporting DB
Menggunakan ATTACH agar bisa query master & insert ke reporting dalam 1 koneksi.
"""

import sqlite3
import os

BASE = os.path.dirname(os.path.abspath(__file__))
MASTER_DB = os.path.join(BASE, 'data/master.db')
REPORTING_DB = os.path.join(BASE, 'data/reporting.db')


def run_etl():
    print('=== ETL PIPELINE ===')

    conn = sqlite3.connect(REPORTING_DB)
    conn.execute(f"ATTACH DATABASE '{MASTER_DB}' AS master")
    cur = conn.cursor()

    # 1. daily_sales_by_branch
    print('  daily_sales_by_branch...')
    cur.execute('DELETE FROM daily_sales_by_branch')
    cur.execute('''
        INSERT INTO daily_sales_by_branch (date, branch_id, branch_name, total_sales, transaction_count)
        SELECT sh.transaction_date, b.id, b.name,
               SUM(sh.total_amount), COUNT(DISTINCT sh.id)
        FROM master.sales_headers sh
        JOIN master.branches b ON sh.branch_id = b.id
        GROUP BY sh.transaction_date, b.id
    ''')

    # 2. daily_sales_by_category
    print('  daily_sales_by_category...')
    cur.execute('DELETE FROM daily_sales_by_category')
    cur.execute('''
        INSERT INTO daily_sales_by_category (date, category_id, category_name, total_sales, qty_sold)
        SELECT sh.transaction_date, c.id, c.name,
               SUM(si.subtotal), SUM(si.quantity)
        FROM master.sales_headers sh
        JOIN master.sales_items si ON sh.id = si.sale_id
        JOIN master.products p ON si.product_id = p.id
        JOIN master.categories c ON p.category_id = c.id
        GROUP BY sh.transaction_date, c.id
    ''')

    # 3. monthly_sales_summary
    print('  monthly_sales_summary...')
    cur.execute('DELETE FROM monthly_sales_summary')
    cur.execute('''
        INSERT INTO monthly_sales_summary (year_month, branch_id, branch_name, total_sales, total_qty, avg_transaction)
        SELECT substr(sh.transaction_date, 1, 7), b.id, b.name,
               SUM(si.subtotal), SUM(si.quantity),
               ROUND(AVG(si.subtotal), 2)
        FROM master.sales_headers sh
        JOIN master.branches b ON sh.branch_id = b.id
        JOIN master.sales_items si ON sh.id = si.sale_id
        GROUP BY substr(sh.transaction_date, 1, 7), b.id
    ''')

    # 4. payment_method_summary
    print('  payment_method_summary...')
    cur.execute('DELETE FROM payment_method_summary')
    cur.execute('''
        INSERT INTO payment_method_summary (date, payment_method, total_amount, transaction_count)
        SELECT transaction_date, payment_method,
               SUM(total_amount), COUNT(*)
        FROM master.sales_headers
        GROUP BY transaction_date, payment_method
    ''')

    # 5. top_products
    print('  top_products...')
    cur.execute('DELETE FROM top_products')
    cur.execute('''
        INSERT INTO top_products (month, product_id, product_name, category_name, qty_sold, total_revenue, rank)
        SELECT substr(sh.transaction_date, 1, 7), p.id, p.name, c.name,
               SUM(si.quantity), SUM(si.subtotal),
               RANK() OVER (
                   PARTITION BY substr(sh.transaction_date, 1, 7)
                   ORDER BY SUM(si.subtotal) DESC
               )
        FROM master.sales_headers sh
        JOIN master.sales_items si ON sh.id = si.sale_id
        JOIN master.products p ON si.product_id = p.id
        JOIN master.categories c ON p.category_id = c.id
        GROUP BY substr(sh.transaction_date, 1, 7), p.id
    ''')

    conn.commit()

    for table in ['daily_sales_by_branch', 'daily_sales_by_category',
                   'monthly_sales_summary', 'payment_method_summary', 'top_products']:
        count = cur.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
        print(f'  {table}: {count} rows')

    conn.execute("DETACH DATABASE master")
    conn.close()
    print('=== ETL COMPLETE ===')


if __name__ == '__main__':
    run_etl()
