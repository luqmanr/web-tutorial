import jsonpickle
import pandas as pd 

from aioflask import Flask, Response, request, redirect, url_for, render_template 
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app)

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
async def serve_index():
    f = open('index.html', 'r')
    return f.read()
# '''
@app.route('/contoh_function', methods = ['GET'])
async def contoh_function():
    response = {
        "status": 200,
        "status_message": "contoh_function OK"
    }
    print(response)
    return Response(jsonpickle.encode(response), mimetype="application/json", status=response['status'])

@app.route('/submit_form', methods = ['GET', 'POST'])
async def submit_form():
    req_headers = dict(request.headers)
    print(f'headers: {req_headers}')

    req_params = dict(request.args)
    print(f'params: {req_params}')

    req_data = request.data
    print(f'data/body: {req_data}')

    # we can then do something with the variable `req_headers` & `req_params`

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
async def table(): 
    # converting csv to html 
    data = pd.read_csv('sample_data.csv') 
    print(data.to_html())
    resp = await render_template('table.html', tables=[data.to_html()], titles=['']) 
    return resp
  
if __name__ == '__main__':
    print("Starting server...")
    port = "9999"
    app.run(host='0.0.0.0', port=port, threaded=True, debug=True)