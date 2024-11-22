import jsonpickle
import pandas as pd 
import csv
import os

from flask import Flask, Response, request, redirect, url_for, render_template, send_from_directory

app = Flask(__name__)

# @app.route('/')
# async def main():
#     return redirect(url_for('serve_index'))

# @app.route('/index.html', methods = ['GET'])
# async def serve_index():
#     html_template = """
        # <body>
        #     <h1>Title</h1>
        #     <p>paragraph</p>
        #     <a href="http://localhost:9999/contoh_function">link ke sebuah tempat</a>
        # </body>
#     """
#     return html_template

@app.route('/<path:path>')
def index(path):
    return send_from_directory('templates', path) # must be in `./templates` folder


@app.route('/index.html', methods = ['GET'])
def serve_index():
    f = open('index.html', 'r')
    return f.read()

@app.route('/submit_form', methods = ['GET', 'POST'])
@app.route('/process', methods = ['GET', 'POST'])
def submit_form():
    req_headers = dict(request.headers)
    print(f'headers: {req_headers}')

    req_params = dict(request.args)
    print(f'params: {req_params}')

    req_data = request.data
    print(f'data/body: {req_data}')
    print(f'{",".join(list(req_params.keys()))}')

    # we can then do something with the variable `req_headers` & `req_params`
    csv_path = 'csv_file.csv'
    if not os.path.exists(csv_path):
        csv_file = open(csv_path, 'w')
        csv_file.write(f'{",".join(list(req_params.keys()))}\n')
        csv_file.close()
    csv_file = open(csv_path, 'a')
    row = ""
    for key in req_params.keys():
        row += req_params[key] + ','
    csv_file.write(f'{row[:-2]}\n')
    csv_file.close()

    response = {
        "status": 200,
        "status_message": "post_data OK",
        "req_headers": req_headers,
        "req_params": req_params,
        "req_data": req_data
    }
    print(response)
    return Response(jsonpickle.encode(response), mimetype="application/json", status=response['status'])

@app.route('/registration')
def registration_form():
    f = open('templates/registration.html', 'r')
    return f.read()

@app.route('/register', methods = ['GET', 'POST'])
def register():
    req_params = dict(request.args)
    username = req_params.get('username', None)
    password = req_params.get('pass', None)

    # we can then do something with the variable `req_headers` & `req_params`
    csv_path = 'registered_users.csv'
    if not os.path.exists(csv_path):
        csv_file = open(csv_path, 'w')
        csv_file.write('username,password\n')
        csv_file.close()
    
    csv_file = open(csv_path, 'r')
    rows = csv_file.read().split('\n')
    for row in rows:
        data = row.split(',')
        registered_username = data[0]
        if username == registered_username:
            response = {
                "status": 400,
                "status_message": "user already exists!"
            }
            print(response)
            return response

    csv_file = open(csv_path, 'a')
    csv_file.write(username + ',' + password + '\n')
    csv_file.close()
    response = {
        "status": 200,
        "status_message": "post_data OK",
        "req_params": req_params
    }
    print(response)
    return response

@app.route('/users') 
@app.route('/users/get') 
def get_registered_users(): 
    # converting csv to html  
    db = 'registered_users.csv'
    df = pd.read_csv(db)
    html = "<body style=\"background:black;color:white;font-family:Verdana;\">"
    html += df.to_html()
    html += "</body>"
    resp = render_template('table.html', tables=[html], titles=['']) 
    return resp

@app.route('/users/delete') 
def del_registered_users(): 
    req_params = dict(request.args)
    username = req_params.get('username', None)

    # converting csv to html 
    db = 'registered_users.csv'
    df = pd.read_csv(db)
    tmp_df = df.copy()
    tmp_df = tmp_df[df.username != username]
    if len(df.index) == len(tmp_df.index):
        resp = {"status": 400, "message": "no users deleted"}
    else:
        resp = {"status": 200, "message": f'user deleted: {username}'}
    tmp_df.to_csv(db, index=False)
    return resp

@app.route('/users/update_password') 
def update_registered_users(): 
    req_params = dict(request.args)
    username = req_params.get('username', None)
    password = req_params.get('pass', None)
    old_password = req_params.get('old_pass', None)

    # converting csv to html 
    db = 'registered_users.csv'
    df = pd.read_csv(db)
    num_updated = len(df.loc[(df.username == username) & (df.password == old_password)])
    df.loc[(df.username == username) & (df.password == old_password), ['password']] = password
    if num_updated == 0:
        resp = {"status": 400, "message": "no users updated"}
        return resp
    
    df.to_csv(db, index=False)
    resp = {"status": 200, "message": "ok"}
    return resp
  
if __name__ == '__main__':
    print("Starting server...")
    port = "5000"
    app.run(host='0.0.0.0', port=port, threaded=True, debug=True)