"""
Export data dari REPORTING DB ke berbagai format:
1. CSV (.csv)
2. HTML table (.html)
3. Embedded HTML (iframe-ready)
"""

import sqlite3
import os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
REPORTING_DB = os.path.join(BASE, 'data/reporting.db')
EXPORT_DIR = os.path.join(BASE, 'exports')
os.makedirs(EXPORT_DIR, exist_ok=True)


def get_rows(table, limit=None):
    conn = sqlite3.connect(REPORTING_DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    if limit:
        cur.execute(f'SELECT * FROM {table} LIMIT {limit}')
    else:
        cur.execute(f'SELECT * FROM {table}')
    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]
    conn.close()
    return cols, rows


def val_str(v):
    if v is None:
        return ''
    if isinstance(v, float):
        return f'{v:,.2f}'
    if isinstance(v, int):
        return f'{v:,}'
    return str(v)


def export_csv(table_name, filename=None):
    if filename is None:
        filename = f'{table_name}.csv'
    filepath = os.path.join(EXPORT_DIR, filename)
    cols, rows = get_rows(table_name)

    with open(filepath, 'w') as f:
        f.write(','.join(cols) + '\n')
        for row in rows:
            vals = [val_str(row[c]).replace(',', ';') for c in cols]
            f.write(','.join(vals) + '\n')

    print(f'CSV exported: {filepath} ({len(rows)} rows)')


def export_html(table_name, filename=None, title=None):
    if filename is None:
        filename = f'{table_name}.html'
    if title is None:
        title = f'Laporan: {table_name.replace("_", " ").title()}'
    filepath = os.path.join(EXPORT_DIR, filename)
    cols, rows = get_rows(table_name)

    thead = ''
    for c in cols:
        thead += f'<th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{c}</th>'

    tbody = ''
    for row in rows:
        tbody += '<tr class="hover:bg-gray-50">'
        for c in cols:
            tbody += f'<td class="px-4 py-2 text-sm text-gray-700">{val_str(row[c])}</td>'
        tbody += '</tr>\n'

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    html = f'''<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 p-8">
<div class="max-w-6xl mx-auto">
<h1 class="text-2xl font-bold mb-4 text-gray-800">{title}</h1>
<div class="bg-white rounded-lg shadow overflow-x-auto">
<table class="min-w-full divide-y divide-gray-200">
<thead class="bg-gray-50">
<tr>
{thead}
</tr>
</thead>
<tbody class="bg-white divide-y divide-gray-200">
{tbody}
</tbody>
</table>
</div>
<p class="text-sm text-gray-500 mt-4">Generated: {now} | {len(rows)} rows</p>
</div>
</body>
</html>'''

    with open(filepath, 'w') as f:
        f.write(html)
    print(f'HTML exported: {filepath} ({len(rows)} rows)')


def export_embedded_html(table_name, filename=None):
    if filename is None:
        filename = f'{table_name}_embedded.html'
    filepath = os.path.join(EXPORT_DIR, filename)
    cols, rows = get_rows(table_name, limit=50)

    thead = ''
    for c in cols:
        thead += f'<th style="padding: 8px 12px; text-align: left; border-bottom: 2px solid #e5e7eb; font-size: 11px; color: #6b7280; text-transform: uppercase;">{c}</th>'

    tbody = ''
    for row in rows:
        tbody += '<tr style="border-bottom: 1px solid #e5e7eb;">'
        for c in cols:
            tbody += f'<td style="padding: 8px 12px; color: #374151;">{val_str(row[c])}</td>'
        tbody += '</tr>\n'

    html = f'''<!-- EMBEDDED HTML: Copy-paste ini ke halaman web / email -->
<div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto;">
<table style="width: 100%; border-collapse: collapse; font-size: 13px;">
<thead>
<tr style="background-color: #f3f4f6;">
{thead}
</tr>
</thead>
<tbody>
{tbody}
</tbody>
</table>
<p style="font-size: 11px; color: #9ca3af; margin-top: 8px;">{len(rows)} rows &middot; Updated automatically</p>
</div>'''

    with open(filepath, 'w') as f:
        f.write(html)
    print(f'Embedded HTML exported: {filepath} ({len(rows)} rows)')


def export_all():
    tables = [
        'daily_sales_by_branch',
        'daily_sales_by_category',
        'monthly_sales_summary',
        'payment_method_summary',
        'top_products',
    ]

    print('=== EXPORT ALL ===')
    for table in tables:
        try:
            export_csv(table)
            export_html(table)
            export_embedded_html(table)
        except Exception as e:
            print(f'  SKIP {table}: {e}')
    print(f'\nAll exports saved to: {EXPORT_DIR}/')


if __name__ == '__main__':
    import sys
    args = sys.argv[1:]

    if not args:
        export_all()
    elif args[0] == 'csv' and len(args) > 1:
        export_csv(args[1])
    elif args[0] == 'html' and len(args) > 1:
        export_html(args[1])
    elif args[0] == 'embedded' and len(args) > 1:
        export_embedded_html(args[1])
    else:
        export_all()
