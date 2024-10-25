import jsonpickle
import os
import sys
import json
import asyncio

from aioflask import Flask, Response, request, redirect, url_for
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

@app.route('/')
async def root():
    return redirect(url_for('serve_index'))

@app.route('/index.html')
async def serve_index():
    f = open('index.html', 'r')
    return f.read()

@app.route('/terima_data', methods = ['GET'])
async def terima_data():
    headers = dict(request.headers)
    print(f'headers: {headers}')

    params = dict(request.args)
    print(f'params: {params}')

    body = request.data
    print(f'data: {body}')

    response = {
        "status": 200,
        "status_message": "terima_data OK",
        "headers": headers,
        "params": params,
        "body": body
    }
    print(response)
    return Response(jsonpickle.encode(response), mimetype="application/json", status=response['status'])

  
if __name__ == '__main__':
    print("Starting server...")
    port = "9999"
    app.run(host='0.0.0.0', port=port, threaded=True, debug=True)