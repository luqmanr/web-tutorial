# SQL & NoSQL + Frontend (PostgreSQL, MongoDB, Streamlit, HTML/Bootstrap)

## Flow Belajar

```
docker compose up -d          ─→ PostgreSQL (port 5432) + MongoDB (27017)
    │
    ├── 00_setup_postgresql.py  ─→ Buat tabel + seed data + reporting tables
    │
    ├── 01_setup_mongodb.py     ─→ Copy data ke MongoDB (document model)
    │
    ├── 02_frontend_streamlit.py  ─→ Dashboard Streamlit (query PostgreSQL)
    │
    └── 03_frontend_html_bootstrap.py  ─→ Web Flask + Bootstrap (query PostgreSQL)
```

## Setup

### 1. Jalankan Docker

```bash
docker compose up -d
```

### 2. Install Dependencies

```bash
pip install psycopg2-binary pandas streamlit flask pymongo
```

### 3. Setup Database + Seed Data

```bash
python 00_setup_postgresql.py
```

Ini akan:
- Buat 9 tabel master (branches, categories, products, customers, sales_headers, sales_items, suppliers, purchase_orders, inventory)
- Seed data: 10 cabang, 12 kategori, 118 produk, 1000 pelanggan, ~10.800 transaksi
- Buat 5 reporting tables (pre-aggregated, siap pakai untuk frontend)
- Isi reporting data dari master

### 4. Setup MongoDB (Opsional)

```bash
python 01_setup_mongodb.py
```

Copy data dari PostgreSQL ke MongoDB dengan struktur **embedded document** (denormalized). Menunjukkan perbedaan:
- SQL: JOIN 4-5 tabel untuk 1 laporan
- NoSQL: 1 dokumen sudah berisi semua data (branch, customer, items dengan nama produk)

## Frontend

### Streamlit Dashboard

```bash
streamlit run 02_frontend_streamlit.py
```

4 tab: per Cabang, per Kategori, Metode Pembayaran, Top Produk.
Membaca dari reporting tables PostgreSQL (cepat, tanpa JOIN).

### HTML + Bootstrap (Flask)

```bash
python 03_frontend_html_bootstrap.py
# Buka: http://localhost:5000
```

4 halaman dengan Bootstrap 5:
- `/` — Dashboard ringkasan (total cabang, penjualan, transaksi)
- `/branches` — Penjualan per cabang (filter tanggal)
- `/products` — Top 10 produk + penjualan per kategori
- `/sales` — 100 transaksi terbaru

## Arsitektur

```
PostgreSQL (normalized)
    │
    ├── Master tables (9 tabel, banyak JOIN)
    │
    └── Reporting tables (pre-aggregated)
            │
            ├── Streamlit Dashboard (Python)
            └── Flask + Bootstrap 5 (Browser)

MongoDB (denormalized, embedded documents)
    └── 1 collection `sales` sudah包含 semua data
```

## File Reference (lama)

File-file berikut masih ada tapi tidak dipakai di flow utama:
- `01-04_sql_*.py` — Latihan SQL dasar (jawaban di `answers/`)
- `06_etl_pipeline.py` — ETL SQLite (ATTACH)
- `07_scheduler.py` — Cronjob scheduler
- `08_streamlit_dashboard.py` — Streamlit versi SQLite
- `09_export_data.py` — Export CSV/HTML
