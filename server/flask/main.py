from flask import Flask, request

app = Flask(__name__)

@app.route('/index.html')
def serve_index():
    f = open('index.html', 'r')
    return f.read()

@app.route('/assets/cat.jpg')
def serve_cat():
    return open('./assets/cat.jpg', 'rb').read()

@app.route('/text')
def text():
    return "sebuah plaintext juga bisa dikembalikan"

@app.route('/terima_data', methods = ['GET'])
def terima_data():
    headers = dict(request.headers)
    print(f'headers: {headers}')

    params = dict(request.args)
    print(f'params: {params}')

    body = request.data
    print(f'data: {body}')

    response = "ok"
    print(f'response: {response}')
    return response
  
print("Starting server...")
app.run()