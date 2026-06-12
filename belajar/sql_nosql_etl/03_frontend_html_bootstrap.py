from flask import Flask, render_template, request
import psycopg2
import psycopg2.extras

app = Flask(__name__)

DB_CONFIG = dict(
    host='localhost', port=5432,
    dbname='reporting_db', user='report_user', password='report_pass',
)


def query(sql, params=None):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(sql, params)
    rows = cur.fetchall()
    conn.close()
    return rows


@app.route('/')
def dashboard():
    summary = query('''
        SELECT COUNT(DISTINCT branch_id) as total_branches,
               SUM(total_sales) as grand_total,
               SUM(transaction_count) as total_transactions
        FROM daily_sales_by_branch
    '')[0]

    sales_by_branch = query('''
        SELECT branch_name, SUM(total_sales) as total, SUM(transaction_count) as count
        FROM daily_sales_by_branch
        GROUP BY branch_name
        ORDER BY total DESC
    ''')

    sales_by_payment = query('''
        SELECT payment_method, SUM(total_amount) as total, SUM(transaction_count) as count
        FROM payment_method_summary
        GROUP BY payment_method
        ORDER BY total DESC
    ''')

    return render_template('dashboard.html',
                           summary=summary,
                           sales_by_branch=sales_by_branch,
                           sales_by_payment=sales_by_payment)


@app.route('/branches')
def branches():
    dates = query('SELECT DISTINCT date FROM daily_sales_by_branch ORDER BY date DESC')

    selected = request.args.get('date', dates[0]['date']) if dates else None

    branch_data = query('''
        SELECT branch_name, total_sales, transaction_count
        FROM daily_sales_by_branch
        WHERE date = %s
        ORDER BY total_sales DESC
    ''', (selected,)) if selected else []

    return render_template('branches.html', dates=[d['date'] for d in dates],
                           selected=selected, branch_data=branch_data)


@app.route('/products')
def products():
    top = query('''
        SELECT month, product_name, category_name, qty_sold, total_revenue, rank
        FROM top_products
        WHERE rank <= 10
        ORDER BY month DESC, rank ASC
    ''')

    by_category = query('''
        SELECT category_name, SUM(total_sales) as total, SUM(qty_sold) as total_qty
        FROM daily_sales_by_category
        GROUP BY category_name
        ORDER BY total DESC
    ''')

    return render_template('products.html', top=top, by_category=by_category)


@app.route('/sales')
def sales():
    recent = query('''
        SELECT sh.id, b.name as branch_name, sh.transaction_date,
               sh.payment_method, sh.total_amount, COUNT(si.id) as item_count
        FROM sales_headers sh
        JOIN branches b ON sh.branch_id = b.id
        JOIN sales_items si ON sh.id = si.sale_id
        GROUP BY sh.id, b.name
        ORDER BY sh.id DESC
        LIMIT 100
    ''')

    return render_template('sales.html', recent=recent)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
