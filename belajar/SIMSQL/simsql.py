import sqlite3
from flask import Flask, request, redirect, send_from_directory

app = Flask(__name__)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory('images', path)

@app.route('/')
@app.route('/index.html')
def root():
    return open('./index.html', 'r').read()

@app.route('/tambah.html')
def tambah():
    return open('./tambah.html', 'r').read()

@app.route('/update.html')
def update():
    return open('./update.html', 'r').read()

@app.route('/hapus.html')
def hapus():
    return open('./hapus.html', 'r').read()

@app.route('/cari.html')
def cari():
    return open('./cari.html', 'r').read()

@app.route('/tambahdata')
def tambahdata():
    params = request.args
    w = params.get('id', None)
    x = params.get('nama', None)
    y = params.get('umur', None)
    z = params.get('kota', None)

    con = sqlite3.connect('karyawan.db')
    cur = con.cursor()
    statement = """
        INSERT INTO karyawan (
            id, nama, umur, kota
        ) VALUES (?, ?, ?, ?);
    """
    cur.execute(statement, (w,x,y,z))
    con.commit()
    return redirect('/tambah.html')

app.run(debug=True)
