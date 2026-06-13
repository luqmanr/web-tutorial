# SQL & NoSQL + Frontend (MSSQL, MongoDB, Streamlit, HTML/Bootstrap)

## Flow

```
docker compose up -d  ─→ MSSQL (1433) + MongoDB (27017)
    │
    ├── 00_setup_mssql.py      ─→ seed data ke MSSQL + export ke SQLite
    │
    ├── 01_setup_mongodb.py     ─→ copy data dari MSSQL ke MongoDB
    │
    ├── 02_frontend_streamlit.py  ─→ baca dari SQLite intermediary
    │
    └── 03_frontend_html_bootstrap.py  ─→ baca dari SQLite intermediary
```

## Setup

### 1. Jalankan Docker

```bash
docker compose up -d
```

| Container | Port | DB | User | Password |
|-----------|------|----|------|----------|
| `mssql_retail` | 1433 | `retail_db` | `sa` | `YourStrong!Password123` |
| `mongo_retail` | 27017 | `retail_db` | — | — |

### 2. Install Dependencies

```bash
pip install pyodbc pandas streamlit flask pymongo
```

> **Note pyodbc**: Di Linux perlu `sudo apt install unixodbc-dev`, di macOS `brew install unixodbc`.
> Driver ODBC 18: [Install dari Microsoft](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server).

### 3. Setup MSSQL + Seed Data + Export ke SQLite

```bash
python 00_setup_mssql.py
```

Ini akan:
- Buat database `retail_db` di MSSQL
- Buat 9 tabel master + 5 reporting tables
- Seed data: 10 cabang, 12 kategori, 118 produk, 1000 pelanggan, ~10.800 transaksi
- Export reporting data ke `data/data_retail.db` (SQLite) — untuk frontend

### 4. Setup MongoDB (Opsional)

```bash
python 01_setup_mongodb.py
```

Copy data dari MSSQL ke MongoDB dengan struktur **embedded document**.
Menunjukkan perbedaan SQL (JOIN) vs NoSQL (1 dokumen sudah包含 semua data).

## Frontend

### Streamlit Dashboard

```bash
streamlit run 02_frontend_streamlit.py
```

4 tab: per Cabang, per Kategori, Metode Pembayaran, Top Produk.
Membaca dari **SQLite intermediary** (`data/data_retail.db`) — cepat, tanpa JOIN.

### HTML + Bootstrap (Flask)

```bash
python 03_frontend_html_bootstrap.py
# Buka: http://localhost:5000
```

4 halaman: Dashboard, Cabang (filter tanggal), Produk, Penjualan.
Juga membaca dari SQLite intermediary yang sama.

## Arsitektur

```
MSSQL (master data — normalized)
    │
    ├── 00_setup_mssql.py  (seed + reporting + export)
    │         │
    │         ▼
    │   SQLite intermediary (data/data_retail.db)
    │         │
    │         ├── Streamlit Dashboard
    │         └── Flask + Bootstrap
    │
    └── 01_setup_mongodb.py  →  MongoDB (document model)
```

## File Reference (lama)

File berikut masih ada tapi tidak dipakai di flow utama:
- `00_setup_postgresql.py` — Alternatif setup PostgreSQL
- `01-04_sql_*.py` — Latihan SQL dasar (jawaban di `answers/`)
- `05_nosql_mongodb.py` — MongoDB versi PostgreSQL
- `06_etl_pipeline.py` — ETL SQLite
- `07_scheduler.py` — Cronjob
- `08_streamlit_dashboard.py` — Streamlit versi SQLite langsung
- `09_export_data.py` — Export CSV/HTML
