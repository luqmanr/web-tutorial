from aioflask import Flask, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

@app.route('/<path:path>')
async def index(path):
    # await asyncio.sleep(1)
    return  send_from_directory('templates', path) # must be in `./templates` folder
  
if __name__ == '__main__':
    print("Starting server...")
    port = "9999"
    app.run(host='0.0.0.0', port=port, threaded=True, debug=True)