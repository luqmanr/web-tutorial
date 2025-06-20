# Github
[**github.com**](https://github.com)

# Markdown
Mirip dengan HTML (Hyper Text Markup Language)

Kalau HTML pakai `<tags>` kalau markdown bisa dua-duanya, tapi lebih common pakai simbol-simbol lain

# String Matching

RegEx, atau Regular Expression, adalah serangkaian karakter yang membentuk pola pencarian.

RegEx dapat digunakan untuk memeriksa apakah suatu string berisi pola pencarian yang ditentukan.

```python
import re

txt = "The rain in Spain"
x = re.search("^The.*Spain$", txt)

if x:
  print("YES! We have a match!")
else:
  print("No match")
```

alt.2
```python
txt = "The rain in Spain"
print(txt[0:3])
print(txt[-5:len(txt)])
if (txt[0:3] == 'The') & (txt[-5:len(txt)] == 'Spain'):
  print("YES! We have a match!")
else:
  print("No match")
```

# Date Formatting

Dalam programming language apapun, kita juga selalu berhubungan dengan tipe data `time`. Di python ada dua library umum/utama yang digunakan untuk melakukan pemrosesan dengan waktu, yaitu modul `datetime` & `time`

Salah satu fungsi yang sering digunakan adalah `.strftime()` & `datetime.datetime.strptime()`

Contoh, jika kita ingin membuat sebuah datetime object baru, kita bisa seperti ini
```python
import datetime

now = datetime.datetime.now()
print(now)
>> 2025-05-16 14:36:33.597258
```

Nah kalau ingin kita buat print dengan format tertentu, kita bisa pakai method `.strftime`

```python
now_str = now.strftime("%Y-%m-%d %H:%M:%S")
print(now_str)
>> 2025-05-16 14:36:33
```
[ref](https://www.w3schools.com/python/python_datetime.asp)
| fmt | corresponds |
| -- | -- |
| %Y | Year |
| %m | month |
| %d | day |
| %H | hour |
| %M | minute |
| %S | second |
