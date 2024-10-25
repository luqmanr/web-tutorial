import jsonpickle
import os
import sys
import json
import asyncio

from aioflask import Flask, redirect, url_for
from flask_cors import CORS

app = Flask(__name__)

@app.route('/redirect')
async def redirect_to():
    return redirect(url_for('tujuan'))

@app.route('/tujuan')
async def tujuan(path):
    return "ini redirect dari index"
  
if __name__ == '__main__':
    print("Starting server...")
    port = "9999"
    app.run(host='0.0.0.0', port=port, threaded=True, debug=True)