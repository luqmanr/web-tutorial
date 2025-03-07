import sqlite3

namax = input('nama: ')

con = sqlite3.connect('karyawan.db')
statement = """
    SELECT 
        id, nama, umur, kota
    FROM karyawan
    WHERE nama = ?;
"""
cur = con.cursor()
rows = cur.execute(statement, (namax,))
for r in rows:
    print(r)
