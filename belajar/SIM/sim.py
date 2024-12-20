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


@app.route('/users') 
@app.route('/users/get') 
def get_registered_users():   
    req_params = dict(request.args)
    queried_user = req_params.get('nama', None)
    
    # converting csv to html  
    db = 'karyawan.csv'
    df = pd.read_csv(db)
    
    if queried_user is not None:
        if len(queried_user) > 1:
            queried_user_index = df[df['nama'].str.lower() == queried_user.lower()].index
            queried_user_row = df.loc[queried_user_index]
            df = queried_user_row
    
    html = "<body style=\"background:black;color:white;font-family:Verdana;\">"
    html += df.to_html()
    html += "</body>"
    resp = render_template('table.html', tables=[html], titles=['']) 
    return resp

@app.route('/report.html')
def report():
   data = pd.read_csv('karyawan.csv')
   resp = render_template('table.html', tables=[data.to_html()], titles=['']) 
   return resp

app.run(debug=True)