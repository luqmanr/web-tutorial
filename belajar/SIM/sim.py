from flask import Flask, request, render_template
import pandas as pd
from io import StringIO

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

@app.route('/search.html')
def search():
    f = open('search.html', 'r')
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

@app.route('/karyawan') 
def get_karyawan():   
    req_params = dict(request.args)
    queried_user = req_params.get('nama', None)
    queried_age = req_params.get('umur', None)
    queried_city = req_params.get('kota', None)
    
    # converting csv to html  
    db = 'karyawan.csv'
    df = pd.read_csv(db)
    
    if queried_user is not None:
        if len(queried_user) > 1:
            queried_user_index = df[df['nama'].str.lower() == queried_user.lower()].index
            queried_user_row = df.loc[queried_user_index]
            df = queried_user_row
    if queried_age is not None:
        if len(queried_age) > 1:
            try:
               age_query = int(queried_age)
               queried_age_index = df[df['umur'] == age_query].index
               queried_user_row = df.loc[queried_age_index]
               df = queried_user_row
            except:
                pass
    if queried_city is not None:
        if len(queried_city) > 1:
            queried_user_index = df[df['kota'].str.lower() == queried_city.lower()].index
            queried_user_row = df.loc[queried_user_index]
            df = queried_user_row
    
    html = "<body style=\"background:black;color:white;font-family:Verdana;\">"
    html += df.to_html()
    html += "</body>"
    resp = render_template('table.html', tables=[html], titles=['']) 
    return resp
   
@app.route('/karyawan/hapus') 
def del_users(): 
    req_params = dict(request.args)
    nama = req_params.get('nama', None)

    # converting csv to html 
    db = 'karyawan.csv'
    df = pd.read_csv(db)
    new_df = df.copy()
    new_df = new_df[df.nama != nama]
    if len(df.index) == len(new_df.index):
        resp = "tidak ada yang dihapus"
    else:
        resp = f"{nama} dihapus"
    new_df.to_csv(db, index=False)
    return resp

@app.route('/karyawan/update') 
def update_users(): 
    req_params = dict(request.args)
    nama = req_params.get('nama', None)
    umur_baru = req_params.get('umur', None)
    kota_baru = req_params.get('kota', None)

    # converting csv to html 
    db = 'karyawan.csv'
    df = pd.read_csv(db)
   
    umur_updated = False
    if umur_baru is not None:
        if len(umur_baru) > 1:
            num_updated = len(df.loc[df.nama == nama])
            df.loc[df.nama == nama, ['umur']] = umur_baru
            if num_updated != 0:
                umur_updated = True

    kota_updated = False
    if kota_baru is not None:
        if len(kota_baru) > 1:
            num_updated = len(df.loc[df.nama == nama])
            df.loc[df.nama == nama, ['kota']] = kota_baru
            if num_updated == 0:
                kota_updated = True
    
    df.to_csv(db, index=False)
    resp = f"diupdate: {nama} - umur: {umur_updated} - kota: {kota_updated}"
    return resp

@app.route('/report.html')
def report():
    data = pd.read_csv('karyawan.csv')
    resp = render_template('table.html', tables=[data.to_html()], titles=['']) 
    return resp

app.run(debug=True)