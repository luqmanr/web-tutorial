# app.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'ini versi 2'

@app.route('/test')
def test():
    return """
    <html>
        <h1>ROUTE /test also works!</h1>
        <p>
        sebuah paragraf
        </p>
    <html>
    """

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
