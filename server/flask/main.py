import jsonpickle
import os
import sys
import json
import asyncio

from aioflask import Flask, Response, request, render_template, send_from_directory
from flask_cors import CORS

app = Flask(__name__)

@app.route('/<path:path>')
async def index(path):
    # await asyncio.sleep(1)
    return  send_from_directory('templates', path) # must be in `./templates` folder

@app.route('/function_one', methods = ['GET'])
async def function_one():
    response = {
        "status": 200,
        "status_message": "function_one OK"
    }
    print(response)
    return Response(jsonpickle.encode(response), mimetype="application/json", status=response['status'])
  
if __name__ == '__main__':
    print("Starting server...")
    port = "9999"
    app.run(host='0.0.0.0', port=port, threaded=True, debug=True)