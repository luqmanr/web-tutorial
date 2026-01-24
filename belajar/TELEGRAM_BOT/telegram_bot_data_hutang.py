import logging
import sqlite3
import duckdb

from datetime import datetime
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

import config

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
table_name = 'hutang'

def init_db():
    conn = sqlite3.connect(f'{table_name}.db')
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            branch TEXT,
            tanggal_pembelian TEXT,
            tanggal_jatuh_tempo TEXT,
            nama_supplier TEXT,
            doc_no TEXT,
            pr_no TEXT,
            amount FLOAT
        )
    ''')
    cursor.execute(f'DELETE FROM {table_name}')
    today = datetime.now().strftime('%Y-%m-%d')
    dummy_data = [
        ('05sb', '2026-01-25', '2026-02-25', 'bsp', '05-123456', 'PR-001', 1500000.0),
        ('05sb', '2026-01-21', '2026-02-21', 'abcd', '05-343423', 'PR-009', 500000.0),
        ('08mg', '2025-01-25', '2026-02-25', 'sayap mas', '08-325576', 'PR-003', 10000000.0),
        ('07kp', '2025-12-12', '2026-01-12', 'indomarko', '07-098765', 'PR-002', 21500000.500),
        ('08mg', '2025-10-03', '2025-11-03', 'sayap mas', '08-325576', 'PR-003', 10000000.0),
        ('11an', '2025-07-09', '2025-08-09', 'unilever', '11-883474', 'PR-004', 1056000.0),
    ]
    cursor.executemany(f'INSERT INTO {table_name} VALUES (?, ?, ?, ?, ?, ?, ?)', dummy_data)
    conn.commit()
    conn.close()

def format_report_table(rows, date_str):
    if not rows:
        return f"No data found for {date_str}."

    table_header = f"<b>Omset Report ({date_str})</b>\n\n"
    table_content = f"<pre>{'Cabang':<10} | {'Total (Rp)':>12}\n"
    table_content += "-" * 25 + "\n"
    
    grand_total = 0
    for cabang, tanggal, total in rows:
        table_content += f"{cabang:<10} | {total:>12,}\n"
        grand_total += total
        
    table_content += "-" * 25 + "\n"
    table_content += f"{'TOTAL':<10} | {grand_total:>12,}\n"
    table_content += "</pre>"
    return table_header + table_content

async def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}!\n\n"
        f"Commands:\n"
        f"/query_daily - Today's report\n"
        f"/query_omset_by_date YYYY-MM-DD - Report for specific date",
    )

async def query_by_branch_date(update: Update, context: CallbackContext) -> None:
    if not context.args:
        await update.message.reply_text("Please provide a date. Usage: /query_by_date 2023-10-27")
        return

    raw_string = context.args[0]
    arguments = raw_string.split(',')
    branch = arguments[0]
    date_str = arguments[1]

    try:
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        await update.message.reply_text("Invalid date format. Please use YYYY-MM-DD.")
        return
    
    if branch == 'all':
        branch = ''

    conn = sqlite3.connect(f'{table_name}.db')
    cursor = conn.cursor()
    cursor.execute(f'''
        SELECT 
            branch,
            tanggal_jatuh_tempo, 
            amount
        FROM {table_name} 
        WHERE 
            branch LIKE '%{branch}%'
        AND
            tanggal_jatuh_tempo = '{date_str}'
            ''')
            
    rows = cursor.fetchall()
    conn.close()
    print(rows)

    response = format_report_table(rows, date_str)
    await update.message.reply_html(response)

async def query_by_branch(update: Update, context: CallbackContext) -> None:
    if not context.args:
        await update.message.reply_text("Please provide a date. Usage: /query_by_date 2023-10-27")
        return

    branch = context.args[0]
    
    if branch == 'all':
        branch = ''

    conn = sqlite3.connect(f'{table_name}.db')
    cursor = conn.cursor()
    cursor.execute(f'''
        SELECT 
            branch,
            SUM(amount) as total_amount
        FROM {table_name} 
        WHERE 
            branch LIKE '%{branch}%'
        GROUP BY branch    
            ''')
            
    rows = cursor.fetchall()
    conn.close()

    ## format response to table
    csv_data = "```csv\nbranch,total_amount\n"
    for row in rows:
        csv_data += f"{row[0]},{row[1]}\n```"

    await update.message.reply_text(csv_data, parse_mode=ParseMode.MARKDOWN_V2)

async def echo(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(update.message.text)

def main() -> None:
    init_db()
    BOT_TOKEN = config.BOT_TOKEN

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("query_by_branch_date", query_by_branch_date))
    application.add_handler(CommandHandler("query_by_branch", query_by_branch))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    logger.info("Bot started. Press Ctrl-C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()