import sqlite3
import os

if os.path.exists('belajar.db'):
    os.remove('belajar.db')
con = sqlite3.connect('belajar.db')

# statement create table karyawan
statement = """
    CREATE TABLE
        karyawan(
            id   INTEGER PRIMARY KEY NOT NULL,
            nama TEXT NOT NULL,
            umur INTEGER NOT NULL,
            kota TEXT NOT NULL
        );
"""

cur = con.cursor()
cur.execute(statement)
con.commit()

# statement insert ke table
statement = """
    INSERT INTO
        karyawan (
            id, nama, umur, kota
        ) VALUES (?, ?, ?, ?);
"""
cur.execute(statement, (1, 'Luqman', 30, 'Bandung'))
con.commit()