import sqlite3

con = sqlite3.connect('./sim.db')

statement = """
    CREATE TABLE sales(
        cabang TEXT,
        tanggal TEXT,
        penjualan FLOAT
    );
"""

try:
    cur = con.cursor()
    cur.execute(statement)
    con.commit()
except Exception as e:
    print(f'failed to create table: {e}')

statement = """
    INSERT INTO sales(
        cabang, tanggal, penjualan
    ) VALUES (?, ?, ?);
"""

try:
    cur = con.cursor()
    # cur.execute(statement, ('dakota', '2025-03-07', 827391000))
    con.commit()
except Exception as e:
    print(f'failed to insert into table: {e}')
