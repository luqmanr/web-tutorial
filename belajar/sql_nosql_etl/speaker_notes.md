# Speaker Notes — SQL & NoSQL + Frontend

## Ringkasan Sesi

**Tujuan**: Peserta bisa setup MSSQL + MongoDB, seed data, export ke SQLite intermediary, dan menampilkan data di web browser via Streamlit maupun HTML/Bootstrap.

**Durasi**: ~120 menit (1 sesi penuh atau 2x60 menit)

**Flow**:
```
Docker → MSSQL → Seed Data → export SQLite → MongoDB → Streamlit → Flask + Bootstrap
```

---

## Bagian 1: Setup Infrastruktur (15 menit)

### Docker Compose

```bash
docker compose up -d
```

**Jelaskan ke peserta:**
- `docker-compose.yml` mendefinisikan 3 service: `mssql`, `mongodb`, `postgres`
- MSSQL di port 1433 (user: `sa` / `YourStrong!Password123`), MongoDB di port 27017
- PostgreSQL (port 5432) sebagai alternatif — tidak dipakai di flow utama
- Volume data tetap ada meskipun container di-restart

**Cek apakah container sudah jalan:**
```bash
docker ps
docker compose logs postgres
docker compose logs mongodb
```

**Troubleshooting umum:**
- Port 1433/27017 sudah dipakai → ganti port di `docker-compose.yml`
- Docker daemon belum jalan → `sudo systemctl start docker`
- MSSQL butuh ~10-15 detik untuk pertama kali start (initialization)
- Cek log: `docker compose logs mssql`
- ODBC Driver 18 belum terinstall → `pip install pyodbc` saja tidak cukup, perlu driver dari Microsoft
- Di Ubuntu: `curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list && sudo apt update && sudo ACCEPT_EULA=Y apt install -y msodbcsql18`

---

## Bagian 2: Setup MSSQL + Export SQLite — 00_setup_mssql.py (25 menit)

### Jalankan:
```bash
python 00_setup_mssql.py
```

### Yang terjadi di belakang layar:

**Step 1 — Koneksi MSSQL:**
```python
pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost;DATABASE=retail_db;"
    "UID=sa;PWD=YourStrong!Password123;"
    "TrustServerCertificate=yes;"
)
```
- Library `pyodbc` = ODBC bridge untuk Python
- Butuh ODBC Driver 18 from Microsoft (install terpisah)
- `TrustServerCertificate=yes` karena pakai self-signed cert (localhost)
- Bandingkan dengan SQLite (tanpa server, tanpa auth)

**Step 2 — Create Database:**
```python
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'retail_db')
    CREATE DATABASE [retail_db]
```
- MSSQL require explicit database creation (beda dengan PostgreSQL `CREATE DATABASE` atau SQLite yang auto-create file)
- `sys.databases` = system catalog view

**Step 3 — Create Tables:**
- 9 tabel master + 5 reporting tables
- Perbedaan tipe data dengan SQL lain:
  - `INT IDENTITY(1,1)` = auto-increment (seperti `SERIAL` di PG)
  - `VARCHAR(n)` = string dengan panjang tetap
  - `DATE` = tanggal
  - `FLOAT` = desimal

**Step 4 — Seed Data:**
- Data dummy: 10 cabang Borma, 12 kategori, 118 produk, 1000 pelanggan
- ~10.800 transaksi (Jan-Mar 2026), ~48.700 item
- `random.seed(42)` → hasil konsisten

**Step 5 — Reporting Tables (di MSSQL):**
- `FORMAT(tanggal, 'yyyy-MM')` = MSSQL version of `TO_CHAR` / `strftime`
- `RANK() OVER (PARTITION BY ...)` = window function (sama di semua SQL)
- `CAST(si.subtotal AS FLOAT)` = explicit type cast

**Step 6 — Export ke SQLite Intermediary:**
```python
# Baca dari MSSQL → tulis ke SQLite
cur.execute('SELECT * FROM branches')
rows = cur.fetchall()
# Buat table di SQLite + insert
```
- Kenapa SQLite? Frontend (Streamlit/Flask) baca dari SQLite
- SQLite lebih ringan, tanpa koneksi jaringan, cocok untuk read-only dashboard
- Ini pola ETL sederhana: source (MSSQL) → intermediary (SQLite) → frontend

### Slide/Visual:
```
┌──────────────────────────────────────────────────┐
│  Arsitektur Data Flow                            │
│                                                  │
│  MSSQL (master data)                             │
│  ┌─────────────────────────────────────┐         │
│  │ 9 master tables (normalized)        │         │
│  │ 5 reporting tables (aggregated)     │         │
│  └──────────┬──────────────────────────┘         │
│             │ export                             │
│             ▼                                    │
│  SQLite (data/data_retail.db)                    │
│  ┌─────────────────────────────────────┐         │
│  │ reporting tables (read-only)        │         │
│  │ ← untuk Streamlit & Flask           │         │
│  └─────────────────────────────────────┘         │
│                                                  │
│  MongoDB (document model)                        │
│  ┌─────────────────────────────────────┐         │
│  │ embedded documents (denormalized)   │         │
│  │ ← untuk demo NoSQL                  │         │
│  └─────────────────────────────────────┘         │
└──────────────────────────────────────────────────┘
```

### Perbandingan: MSSQL vs PostgreSQL vs SQLite

| Aspek | MSSQL | PostgreSQL | SQLite |
|-------|-------|------------|--------|
| Setup | Server + ODBC driver | Server + psycopg2 | File saja |
| Port | 1433 | 5432 | — |
| Auto-increment | `IDENTITY(1,1)` | `SERIAL` | `INTEGER PRIMARY KEY` |
| Format date | `FORMAT(d, 'yyyy-MM')` | `TO_CHAR(d, 'YYYY-MM')` | `strftime('%Y-%m', d)` |
| Use case | Production OLTP | Production OLTP | Embedded / mobile |

### Pertanyaan untuk peserta:
1. "Kenapa kita pakai SQLite sebagai intermediary?" (ringan, tanpa server, cocok untuk read-only dashboard)
2. "Apa bedanya IDENTITY di MSSQL dengan SERIAL di PostgreSQL?" (IDENTITY = auto-increment pada column, SERIAL = shortcut untuk sequence)
3. "Kalau ada transaksi baru di MSSQL, gimana caranya update SQLite?" (re-run export_to_sqlite / setup cronjob)

---

## Bagian 3: Setup MongoDB — 01_setup_mongodb.py (15 menit)

### Jalankan:
```bash
python 01_setup_mongodb.py
```

Membaca data dari **MSSQL**, lalu membangun enriched documents di MongoDB.

### Konsep Kunci:

**SQL vs NoSQL — Struktur Data:**
- SQL: data dipecah ke banyak tabel (branches, customers, items terpisah)
- NoSQL (MongoDB): data digabung jadi 1 dokumen besar (embedded)

**Contoh perbandingan:**

SQL di MSSQL (butuh JOIN):
```sql
SELECT b.name, c.name, p.name, si.quantity
FROM sales_headers sh
JOIN branches b ON sh.branch_id = b.id
JOIN customers c ON sh.customer_id = c.id
JOIN sales_items si ON sh.sale_id = si.sale_id
JOIN products p ON si.product_id = p.id
WHERE sh.id = 1;
```

NoSQL (1 query): 
```javascript
db.sales.findOne({sale_id: 1})
// Langsung dapat: branch, customer, items dengan nama produk
```

**Keuntungan embedded document:**
- 1 query dapat semua data (no JOIN!)
- Lebih cepat untuk read-heavy workload
- Cocok untuk dashboard / API response

**Kekurangan:**
- Ukuran dokumen besar
- Update harus di banyak tempat (kalau nama branch berubah)
- Kurang fleksibel untuk ad-hoc query

**Hasil di MongoDB:**
```
retail_db.sales → 2000 dokumen, masing-masing包含:
  ├── sale_id, date, total_amount, payment_method
  ├── branch: {id, name, city}
  ├── customer: {id, name, member_id, city}
  └── items: [{product_id, product_name, category_name, quantity, unit_price, subtotal}]
```

### Pertanyaan untuk peserta:
1. "Kapan sebaiknya pakai embedded document vs reference?" (embedded: data dibaca bersama, reference: data sering berubah sendiri)
2. "Apa yang terjadi kalau kita merge semua tabel SQL jadi 1 dokumen MongoDB?" (ukuran besar, update lambat, tapi query cepat)
3. "Coba bandingkan query SQL vs MongoDB untuk: 'tampilkan 5 transaksi dengan total > 500rb'" 

---

## Bagian 4: Streamlit Dashboard — 02_frontend_streamlit.py (20 menit)

### Jalankan:
```bash
streamlit run 02_frontend_streamlit.py
```

### Yang Didemonstrasikan:

**1. Koneksi ke SQLite dari Streamlit:**
```python
@st.cache_data(ttl=60)
def load_data(query):
    conn = sqlite3.connect('data/data_retail.db')
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
```

- `@st.cache_data(ttl=60)`: cache query selama 60 detik
- Kenapa? Karena reporting tables jarang berubah, tidak perlu query setiap re-render
- **Tidak perlu koneksi jaringan** — SQLite adalah file lokal, jadi ekstrem cepat
- Bandingkan dengan MSSQL yang perlu TCP/IP + auth setiap query

**2. 4 Tab Dashboard:**
- **Penjualan per Cabang**: filter tanggal, tabel + bar chart
- **Penjualan per Kategori**: aggregasi total, tabel + bar chart
- **Metode Pembayaran**: breakdown TUNAI/DEBIT/KREDIT/QRIS/TRANSFER
- **Top Produk**: peringkat produk terlaris per bulan

**3. Kenapa cepat?**
- Query ke reporting tables (pre-aggregated), bukan master
- 1 query = 1 tabel, no JOIN
- Dataframe Langsung dari pandas

**4. Pola Streamlit:**
- `st.dataframe()` — tampilkan tabel interaktif
- `st.bar_chart()` — chart dari dataframe
- `st.selectbox()` — filter interaktif
- `st.columns()` — layout 2 kolom

### Demo interaktif:
1. Tanya peserta: "Cabang mana yang penjualannya paling tinggi hari ini?"
2. Ganti tanggal → lihat perubahannya
3. Tanya: "Metode pembayaran apa yang paling populer?"

### Error handling:
- Kalau PostgreSQL belum di-setup → tampilkan error message
- Kalau reporting tables kosong → tampilkan warning untuk run `00_setup_postgresql.py`

---

## Bagian 5: Flask + Bootstrap — 03_frontend_html_bootstrap.py (25 menit)

### Jalankan:
```bash
python 03_frontend_html_bootstrap.py
# Buka browser: http://localhost:5000
```

### Arsitektur Flask:

```
03_frontend_html_bootstrap.py
  ├── Routes: /, /branches, /products, /sales
  ├── Function query() — reusable PostgreSQL query
  └── Render template → templates/*.html

templates/
  ├── base.html       — Layout, navbar Bootstrap, footer
  ├── dashboard.html  — Halaman utama (summary cards + tables)
  ├── branches.html   — Penjualan per cabang (filter date)
  ├── products.html   — Top 10 produk + kategori
  └── sales.html      — Recent 100 transaksi
```

### Konsep yang diajarkan:

**1. Koneksi ke SQLite dari Flask:**
```python
def query(sql, params=None):
    conn = sqlite3.connect('data/data_retail.db')
    conn.row_factory = sqlite3.Row
    ...
```
- `sqlite3.Row` → akses kolom seperti dictionary (`row['branch_name']`)
- Parameter binding pakai `?` (placeholder SQLite), bukan `%s` (PostgreSQL) atau `?` (MSSQL via pyodbc)

**2. Flask Route:**
```python
@app.route('/')
def dashboard():
    data = query("SELECT ...")
    return render_template('dashboard.html', data=data)
```

- Decorator `@app.route()` → mapping URL ke function
- `render_template()` → render HTML file dengan data dari backend
- Template engine: Jinja2 (bawaan Flask)

**2. Template Inheritance (Jinja2):**
```html
{% extends "base.html" %}
{% block content %}
  ... halaman spesifik ...
{% endblock %}
```

- `base.html`: navbar, footer, CSS/JS includes
- Child template: cukup isi `{% block content %}`
- DRY (Don't Repeat Yourself): navbar cukup ditulis 1x

**3. Bootstrap 5:**
- CDN: `bootstrap.min.css` + `bootstrap.bundle.min.js`
- Grid: `<div class="row">` + `<div class="col-md-6">`
- Components: `card`, `table table-hover`, `badge`, `navbar`
- Icons: `bootstrap-icons`

**4. Server-Side Rendering:**
- Data diquery di backend (Python + PostgreSQL)
- Dikirim ke template sebagai variable
- Jinja2 render HTML string → dikirim ke browser
- Berbeda dengan SPA (React/Vue) yang pake API JSON + client-side render

### Perbandingan Streamlit vs Flask:

| Aspek | Streamlit | Flask + Bootstrap |
|-------|-----------|-------------------|
| Setup | 1 file Python | Python + HTML templates |
| UI | Auto-generated | Manual HTML + CSS |
| Interaktivitas | Widget Python | Form submit / JS |
| Use case | Data exploration, prototyping | Production web app |
| Kecepatan开发 | Cepat | Sedang |

### Pertanyaan untuk peserta:
1. "Apa bedanya server-side rendering (Flask) dengan client-side rendering (React)?" 
2. "Kenapa kita pisahkan HTML ke file terpisah (templates/)?" (separation of concerns)
3. "Coba tambahin 1 halaman baru: `/customers` yang menampilkan daftar pelanggan!"

---

## Bonus: Eksplorasi Database Langsung (15 menit)

### sqlcmd (MSSQL CLI):
```bash
docker exec -it mssql_retail /opt/mssql-tools18/bin/sqlcmd \
  -S localhost -U sa -P 'YourStrong!Password123' -C

# Di dalam sqlcmd:
SELECT name FROM sys.databases;
USE retail_db;
SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES;
SELECT * FROM branches;
SELECT branch_name, total_sales FROM daily_sales_by_branch;
GO
exit
```

### MongoDB Compass / mongosh:
```bash
docker exec -it nosql_mongo mongosh

# Di dalam mongosh:
use retail_db
db.sales.findOne()
db.sales.aggregate([{$group: {_id: "$payment_method", total: {$sum: "$total_amount"}}}])
exit
```

### DBeaver / TablePlus:
- Konek ke PostgreSQL: host localhost, port 5432, user report_user, db reporting_db
- Konek ke MongoDB: host localhost, port 27017

---

## Ringkasan Akhir

### Yang sudah dipelajari:
1. **Infrastruktur**: Docker, MSSQL, MongoDB
2. **Database Design**: Normalized vs Denormalized, OLTP vs OLAP
3. **SQL**: CREATE TABLE, INSERT, SELECT, JOIN, GROUP BY, RANK() — di MSSQL
4. **ETL Pattern**: MSSQL → SQLite intermediary → Frontend
5. **NoSQL**: Document model, embedded documents, aggregation pipeline — di MongoDB
6. **Frontend**: Streamlit dashboard, Flask + Bootstrap web app
7. **Pola**: Cache query, pre-aggregated reporting tables, server-side rendering

### Latihan untuk peserta (kalau ada waktu):
1. Tambah halaman `/customers` di Flask app yang menampilkan 100 pelanggan terbaru
2. Tambah filter tanggal di halaman Streamlit tab "Penjualan per Kategori"
3. Export data MongoDB ke JSON: `mongoexport --db retail_db --collection sales --out sales.json`
4. Buat materialized view di PostgreSQL: `CREATE MATERIALIZED VIEW ...`

### Referensi:
- [MSSQL ODBC Driver](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server)
- [pyodbc Documentation](https://github.com/mkleehammer/pyodbc)
- [MongoDB Manual](https://www.mongodb.com/docs/manual/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [Flask Tutorial](https://flask.palletsprojects.com/)
- [Bootstrap 5](https://getbootstrap.com/docs/5.3/)
