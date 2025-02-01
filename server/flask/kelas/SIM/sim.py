from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/index.html')
def index():
    f = open('index.html', 'r')
    return f.read()

@app.route('/entry.html')
def entry():
    f = open('entry.html', 'r')
    return f.read()

@app.route('/report.html')
def report():
    data = pd.read_csv('karyawan.csv')
    resp = render_template('table.html', tables=[data.to_html()], titles=['']) 
    return resp

@app.route('/tambahdata')
def tambahdata():
    params = request.args
    nama = params.get('nama', None)
    umur = params.get('umur', None)
    kota = params.get('kota', None)

    f = open('karyawan.csv', 'a')
    f.write(nama + ',' + umur + ',' + kota +'\n')
    f.close()
    return 

app.run(debug=True)