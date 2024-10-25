from flask import Flask, request, send_file

app = Flask(__name__)

@app.route('/assets/cat.jpg')
def serve_cat():
    return send_file('./assets/cat.jpg')
  
if __name__ == '__main__':
    print("Starting server...")
    port = "9999"
    app.run(host='0.0.0.0', port=port, threaded=True, debug=True)