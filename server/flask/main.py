import jsonpickle
import pandas as pd 
import csv
import os

from flask import Flask, Response, request, redirect, url_for, render_template 

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
# '''
@app.route('/index.html', methods = ['GET'])
def serve_index():
    f = open('index.html', 'r')
    return f.read()
# '''
@app.route('/contoh_function', methods = ['GET'])
def contoh_function():
    response = {
        "status": 200,
        "status_message": "contoh_function OK"
    }
    print(response)
    return Response(jsonpickle.encode(response), mimetype="application/json", status=response['status'])

@app.route('/submit_form', methods = ['GET', 'POST'])
@app.route('/process', methods = ['GET', 'POST'])
def submit_form():
    req_headers = dict(request.headers)
    print(f'headers: {req_headers}')

    req_params = dict(request.args)
    print(f'params: {req_params}')

    req_data = request.data
    print(f'data/body: {req_data}')

    # we can then do something with the variable `req_headers` & `req_params`
    csv_path = 'csv_file.csv'
    if not os.path.exists(csv_path):
        csv_file = open(csv_path, 'w')
        csv_file.write('fname,lname\n')
        csv_file.close()
    else:
        csv_file = open(csv_path, 'r')
        csv_data = csv_file.read()
        if len(csv_data) == 0:
            csv_file.close()
            csv_file = open(csv_path, 'w')
            csv_file.write('fname,lname\n')
        csv_file.close()

    csv_file = open(csv_path, 'a')
    csv_file.write(f'{req_params["fname"]},{req_params["lname"]}\n')
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

@app.route('/table') 
def table(): 
    # converting csv to html 
    data = pd.read_csv('sample_data.csv') 
    print(data.to_html())
    resp = render_template('table.html', tables=[data.to_html()], titles=['']) 
    return resp

@app.route('/csv') 
def csv_read(): 
    # we can then do something with the variable `req_headers` & `req_params`
    csv_path = 'csv_file.csv'
    if not os.path.exists(csv_path):
        return 'doesn\'t exist'
    csv_data = open(csv_path, 'r').read()
    csv_headers = []
    rows = []
    l = 0
    for line in csv_data.split('\n'):
        print(line)
        if l == 0:
            csv_headers = line.split(',')
        else:
            rows.append(line.split(','))
        l += 1
    print(csv_headers)
    print(rows)
    resp = csv_data
    return resp
  
if __name__ == '__main__':
    print("Starting server...")
    port = "5000"
    app.run(host='0.0.0.0', port=port, threaded=True, debug=True)