import sqlite3

con = sqlite3.connect('karyawan.db')
statement = """
    UPDATE karyawan 
    SET 
        umur = ?,
        kota = ?
    WHERE nama = ? ;
"""
nama = input('nama: ')
umur = input('umur: ')
kota = input('kota: ')
cur = con.cursor()
rows = cur.execute(statement, (umur, kota, nama,))
print(rows.rowcount)
con.commit()
