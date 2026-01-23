import logging
import sqlite3
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

import config

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

def init_db():
    conn = sqlite3.connect('sales.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS omset (
            cabang TEXT,
            tanggal TEXT,
            total_rupiah INTEGER
        )
    ''')
    cursor.execute('DELETE FROM omset')
    today = datetime.now().strftime('%Y-%m-%d')
    dummy_data = [
        ('Jakarta', today, 5000000),
        ('Bandung', today, 3500000),
        ('Surabaya', today, 4200000),
        ('Jakarta', '2023-10-26', 1000000)
    ]
    cursor.executemany('INSERT INTO omset VALUES (?, ?, ?)', dummy_data)
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

async def query_daily(update: Update, context: CallbackContext) -> None:
    today = datetime.now().strftime('%Y-%m-%d')
    conn = sqlite3.connect('sales.db')
    cursor = conn.cursor()
    cursor.execute('SELECT cabang, tanggal, total_rupiah FROM omset WHERE tanggal = ?', (today,))
    rows = cursor.fetchall()
    conn.close()

    response = format_report_table(rows, today)
    await update.message.reply_html(response)

async def query_omset_by_date(update: Update, context: CallbackContext) -> None:
    if not context.args:
        await update.message.reply_text("Please provide a date. Usage: /query_omset_by_date 2023-10-27")
        return

    date_str = context.args[0]
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        await update.message.reply_text("Invalid date format. Please use YYYY-MM-DD.")
        return

    conn = sqlite3.connect('sales.db')
    cursor = conn.cursor()
    cursor.execute('SELECT cabang, tanggal, total_rupiah FROM omset WHERE tanggal = ?', (date_str,))
    rows = cursor.fetchall()
    conn.close()

    response = format_report_table(rows, date_str)
    await update.message.reply_html(response)

async def echo(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(update.message.text)

def main() -> None:
    init_db()
    BOT_TOKEN = config.BOT_TOKEN

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("query_daily", query_daily))
    application.add_handler(CommandHandler("query_omset_by_date", query_omset_by_date))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    logger.info("Bot started. Press Ctrl-C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()