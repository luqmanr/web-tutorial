# Speaker Notes — SQL & NoSQL + Frontend

## Ringkasan Sesi

**Tujuan**: Peserta bisa setup PostgreSQL + MongoDB, seed data, dan menampilkan data di web browser via Streamlit maupun HTML/Bootstrap.

**Durasi**: ~120 menit (1 sesi penuh atau 2x60 menit)

**Flow**:
```
Docker → PostgreSQL → Seed Data → MongoDB → Streamlit → Flask + Bootstrap
```

---

## Bagian 1: Setup Infrastruktur (15 menit)

### Docker Compose

```bash
docker compose up -d
```

**Jelaskan ke peserta:**
- `docker-compose.yml` mendefinisikan 2 service: `postgres` dan `mongodb`
- PostgreSQL di port 5432, MongoDB di port 27017
- Volume data tetap ada meskipun container di-restart
- Kredensial: `report_user` / `report_pass`, database: `reporting_db`

**Cek apakah container sudah jalan:**
```bash
docker ps
docker compose logs postgres
docker compose logs mongodb
```

**Troubleshooting umum:**
- Port 5432/27017 sudah dipakai → ganti port di `docker-compose.yml`
- Docker daemon belum jalan → `sudo systemctl start docker`
- Peserta di Windows → pastikan Docker Desktop sudah running

---

## Bagian 2: Setup PostgreSQL — 00_setup_postgresql.py (20 menit)

### Jalankan:
```bash
python 00_setup_postgresql.py
```

### Yang terjadi di belakang layar:

**Step 1 — Koneksi:**
```python
psycopg2.connect(host='localhost', port=5432, dbname='reporting_db', ...)
```
- Perhatikan: library `psycopg2` adalah PostgreSQL adapter untuk Python
- Parameter connection = host, port, dbname, user, password
- Beda dengan SQLite yang cuma perlu path file

**Step 2 — Create Tables:**
- 9 tabel master: `branches, categories, products, customers, sales_headers, sales_items, suppliers, purchase_orders, inventory`
- 5 reporting tables: `daily_sales_by_branch, daily_sales_by_category, monthly_sales_summary, payment_method_summary, top_products`
- Tabel master = normalized (data dipecah kecil-kecil, perlu JOIN)
- Reporting tables = denormalized / pre-aggregated (data sudah siap pakai)

**Kenapa reporting tables terpisah?**
```
Query ke master: butuh JOIN 4-5 tabel → lambat untuk dashboard
Query ke reporting: SELECT langsung dari 1 tabel → cepat
Ini pola umum di BI / data warehouse: ETL dari OLTP ke OLAP
```

**Step 3 — Seed Data:**
- Data dummy: 10 cabang Borma (Jawa Barat + Banten), 12 kategori, 118 produk
- ~10.800 transaksi selama Jan-Mar 2026
- ~48.700 item transaksi
- random.seed(42) → hasilnya konsisten setiap run

**Step 4 — Reporting Tables:**
- `daily_sales_by_branch`: total penjualan per cabang per hari
- `daily_sales_by_category`: total penjualan per kategori per hari
- `monthly_sales_summary`: ringkasan bulanan per cabang
- `payment_method_summary`: breakdown metode bayar per hari
- `top_products`: peringkat produk terlaris per bulan (pakai RANK() window function)

### Slide/Visual:
```
┌──────────────────────────────────────────────┐
│  PostgreSQL (reporting_db)                    │
│                                              │
│  Master Tables (normalized)                  │
│  ┌────────┐ ┌──────────┐ ┌──────────┐       │
│  │branches│ │products  │ │sales_hdr │       │
│  │ 10 rows│ │ 118 rows │ │ 10.8k    │       │
│  └────────┘ └──────────┘ └──────────┘       │
│                                              │
│  Reporting Tables (pre-aggregated)           │
│  ┌──────────────────┐ ┌──────────────────┐  │
│  │daily_by_branch   │ │monthly_summary   │  │
│  │daily_by_category │ │payment_method    │  │
│  │top_products      │ │                  │  │
│  └──────────────────┘ └──────────────────┘  │
└──────────────────────────────────────────────┘
```

### Pertanyaan untuk peserta:
1. "Apa bedanya PRIMARY KEY di SQLite vs PostgreSQL?" (SERIAL vs INTEGER)
2. "Kenapa reporting tables perlu dibuat terpisah?" (performance, no JOIN)
3. "Kalau ada transaksi baru, gimana cara update reporting tables?" (re-run populate_reporting)

---

## Bagian 3: Setup MongoDB — 01_setup_mongodb.py (15 menit)

### Jalankan:
```bash
python 01_setup_mongodb.py
```

### Konsep Kunci:

**SQL vs NoSQL — Struktur Data:**
- SQL: data dipecah ke banyak tabel (branches, customers, items terpisah)
- NoSQL (MongoDB): data digabung jadi 1 dokumen besar (embedded)

**Contoh perbandingan:**

SQL (butuh JOIN):
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

**1. Koneksi ke PostgreSQL dari Streamlit:**
```python
@st.cache_data(ttl=60)
def load_data(query):
    conn = psycopg2.connect(**DB_CONFIG)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
```

- `@st.cache_data(ttl=60)`: cache query selama 60 detik
- Kenapa? Karena reporting tables jarang berubah, tidak perlu query setiap re-render
- Ini best practice Streamlit: cache semuanya

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

**1. Flask Route:**
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

### psql (PostgreSQL CLI):
```bash
docker exec -it nosql_pg psql -U report_user -d reporting_db

# Di dalam psql:
\d                    # daftar semua tables
\d daily_sales_by_branch  # lihat struktur table
SELECT * FROM branches;
SELECT branch_name, total_sales FROM daily_sales_by_branch LIMIT 10;
\q
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
1. **Infrastruktur**: Docker, PostgreSQL, MongoDB
2. **Database Design**: Normalized vs Denormalized, OLTP vs OLAP
3. **SQL**: CREATE TABLE, INSERT, SELECT, JOIN, GROUP BY, RANK()
4. **NoSQL**: Document model, embedded documents, aggregation pipeline
5. **Frontend**: Streamlit dashboard, Flask + Bootstrap web app
6. **Pola**: Cache query, pre-aggregated reporting tables, server-side rendering

### Latihan untuk peserta (kalau ada waktu):
1. Tambah halaman `/customers` di Flask app yang menampilkan 100 pelanggan terbaru
2. Tambah filter tanggal di halaman Streamlit tab "Penjualan per Kategori"
3. Export data MongoDB ke JSON: `mongoexport --db retail_db --collection sales --out sales.json`
4. Buat materialized view di PostgreSQL: `CREATE MATERIALIZED VIEW ...`

### Referensi:
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [MongoDB Manual](https://www.mongodb.com/docs/manual/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [Flask Tutorial](https://flask.palletsprojects.com/)
- [Bootstrap 5](https://getbootstrap.com/docs/5.3/)
