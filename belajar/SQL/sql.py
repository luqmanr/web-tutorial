import sqlite3
import os

if os.path.exists('belajar.db'):
    os.remove('belajar.db')

con = sqlite3.connect('belajar.db')
# con = mssql.connect('')

statement = """
    CREATE TABLE
        buku (
            id               INTEGER    PRIMARY KEY NOT NULL,
            judul            TEXT       NOT NULL,
            tahun            INTEGER    NOT NULL,
            status_dipinjam  TEXT       NOT NULL,
            tanggal_diinput  TEXT       NOT NULL,
            tanggal_diupdate TEXT       NOT NULL
        );
"""

cur = con.cursor()
cur.execute(statement)
con.commit()

statement = """
    INSERT INTO
        buku (
            id,
            judul,
            tahun,
            status_dipinjam,
            tanggal_diinput,
            tanggal_diupdate
    ) VALUES (?, ?, ?, ?, ?, ?);
"""
cur.execute(statement, (1, 'Lord of The Rings', 1940, 'true', '2025-01-25', '2025-01-25'))
cur.execute(statement, (2, 'DUNE', 1940, 'true', '2025-01-25', '2025-01-25'))
cur.execute(statement, (3, 'Mistborn', 2000, 'true', '2025-01-25', '2025-01-25'))
cur.execute(statement, (4, 'Harry Potter', 1940, 'true', '2025-01-25', '2025-01-25'))

con.commit()