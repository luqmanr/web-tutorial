from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
   f = open('index.html', 'r')
   return f.read()

@app.route('/index.html')
def index2():
   f = open('index.html', 'r')
   return f.read()

@app.route('/entry.html')
def entry():
   f = open('entry.html', 'r')
   return f.read()

@app.route('/update.html')
def update():
   f = open('update.html', 'r')
   return f.read()

@app.route('/hapus.html')
def hapus():
   f = open('hapus.html', 'r')
   return f.read()

@app.route('/tambahdata')
def tambahdata():
   params = request.args
   nama = params.get('nama', None)
   umur = params.get('umur', None)
   kota = params.get('kota', None)

   f = open('karyawan.csv', 'a')
   f.write(nama + ',' + umur + ',' + kota +'\n')
   f.close()

   g = open('entry.html', 'r')
   return g.read()

@app.route('/updatedata')
def updatedata():
   # QUERY berdasarkan Nama
   # yang diupdate: umur
   params = request.args
   nama = params.get('nama', None)
   umur = params.get('umur', None)
   print(nama, umur)

   f = open('karyawan.csv', 'r')
   csv_text = f.read()
   f.close()
   rows = csv_text.split('\n')

   # check if rows terakhir = baris kosong
   if rows[-1] == '':
      print('baris kosong')
      del rows[-1]
   
   # for loop to each items in variable `rows`
   f = open('karyawan.csv', 'w')
   found = False
   for row in rows:
      row_data = row.split(',')
      nama_row = row_data[0]
      usia_row = row_data[1]
      kota_row = row_data[2]
      # GeMoy -> gemoy | Gemoy -> gemoy
      if nama.lower() != nama_row.lower():
         print(nama, 'tidak sama', nama_row)
         f.write(nama_row + ',' + usia_row + ',' + kota_row +'\n')
      else:
         print(nama, 'sama', nama_row)
         f.write(nama_row + ',' + umur + ',' + kota_row +'\n')
         found = True
   f.close()

   msg = f"nama '{nama}' not found"
   if found is True:
      msg = f"nama '{nama}' is found and updated!"
   return msg

@app.route('/deletedata')
def deletedata():
   # delete sebuah row, dimana nama = $nama
   params = request.args
   nama = params.get('nama', None)
   print(nama)

   f = open('karyawan.csv', 'r')
   csv_text = f.read()
   f.close()
   rows = csv_text.split('\n')

   # check if rows terakhir = baris kosong
   if rows[-1] == '':
      print('baris kosong')
      del rows[-1]
   
   # for loop to each items in variable `rows`
   f = open('karyawan.csv', 'w')
   found = False
   for row in rows:
      row_data = row.split(',')
      nama_row = row_data[0]
      usia_row = row_data[1]
      kota_row = row_data[2]
      # GeMoy -> gemoy | Gemoy -> gemoy
      if nama.lower() != nama_row.lower():
         print(nama, 'tidak sama', nama_row)
         f.write(nama_row + ',' + usia_row + ',' + kota_row +'\n')
      else:
         print(nama, 'sama', nama_row)
         found = True
   f.close()

   msg = f"nama '{nama}' not found"
   if found is True:
      msg = f"nama '{nama}' is found and deleted!"
   return msg

@app.route('/report.html')
def report():
   data = pd.read_csv('karyawan.csv')
   resp = render_template('table.html', tables=[data.to_html()], titles=['']) 
   return resp

app.run(debug=True)