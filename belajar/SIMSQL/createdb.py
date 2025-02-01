import sqlite3

con = sqlite3.connect('karyawan.db')
statement = """
    CREATE TABLE karyawan (
        id   INTEGER    PRIMARY KEY NOT NULL,
        nama TEXT       NOT NULL,
        umur INTEGER    NOT NULL,
        kota TEXT       NOT NULL
    );
"""

cur = con.cursor()
cur.execute('DROP TABLE karyawan;')
cur.execute(statement)
con.commit()
