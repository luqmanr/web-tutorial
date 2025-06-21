nama, umur, kota
<a href='http://some-ip:80/data-orang/budi>budi</a>, 60, bandung


# contoh data dari sql
rows = 
```
nama, umur, kota
budi, 60, bandung
```

for row in rows:
    nama = f'<a href='http://some-ip:80/data-orang/{nama}>{nama}</a>'


row = sql.query('''select * from table where name='budi'''')
