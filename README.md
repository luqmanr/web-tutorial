# Web Tutorial

## Ever wonder how the web works?
![http request](./assets/http_communication.bmp)

## What is a WebServer
A web server has to store the website's files, namely all HTML documents and their related assets, including images, CSS stylesheets, JavaScript files, fonts, etc.

## HTML templates
Refresh lagi tentang html
```html
<!DOCTYPE html>                     <!-->definisikan bahwa ini adalah sebuah dokumen html<-->
<html>                              <!-->definisi dokumen `root` / `paling atas`<-->
    <body>                          <!-->konten dari html page<-->
        <h1>Title</h1>              <!-->Sebuah title<-->
        <p>paragraph</p>            <!-->Sebuah paragraf<-->
        <a href="http://localhost:9999/index.html">link ke sebuah tempat</a>
        <br></br>                   <!-->sebuah line break<-->
        <img src="/assets/cat.jpg"> <!-->mengembalikan sebuah image<-->
    </body>
</html>
```

## Flask pt.1
[Flask](https://flask.palletsprojects.com/en/stable/) is a web framework written in Python. Jadi bukan hanya webserver, tapi sebuah tool untuk membuat web applications.

1. import `flask`
```python
import flask
```

2. inisialisasi object `Flask`
```python
app = Flask(__name__)
```

3. definisikan sebuah `route` atau `path` dengan `function` atau `endpoint` yang akan kita jalankan
```python
@app.route('/')
def text():
    return "kembalikan sebuah text"
```

4. jalankan aplikasi
```python
app.run()
```

## Flask pt.2
Selain text, kita juga bisa return sebuah `html`

1. return sebuah `index.html`
```python
@app.route('/index.html')
def serve_index():
    f = open('index.html', 'rb')
    return f.read()
```

2. Quiz, coba kembalikan sebuah gambar kucing

3. Quiz, coba kembalikan sebuah dokumen singkat, berisikan:
    - Gambar personil band favorit anda
    - Judul lagu favorit dari mereka
    - Cuplikan lirik favorit

## Anatomy of an HTTP request
![http req anatomy](./assets/http_req_anatomy.bmp)
![http req anatomy 2](./assets/http_req_anatomy2.bmp)

- URL/URI = Uniform Resource Identifier/Locator
- Method = Mengindikasikan request intent
- Headers = Metadata, key-value pair data
- Body = Data dalam request
- Query / Parameters = Data dalam bentuk URL
