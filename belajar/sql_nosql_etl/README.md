# SQL & NoSQL Exercises + ETL + Automation + Visualization

## Flow
```
Master Database (master.db) — normalized, 10.804 transaksi, 48.700 item
    |
    ├── SQL Exercises (01-04): query langsung ke master
    ├── MongoDB (05): document model via Docker
    ├── ETL Pipeline (06): master → reporting DB (aggregated, fast)
    ├── Scheduler (07): auto-jalankan ETL tiap N menit
    ├── Streamlit Dashboard (08): baca dari reporting DB (cepat!)
    ├── Export (09): CSV / HTML / embedded HTML dari reporting DB
    └── Grafana (bonus): konek ke SQLite/PostgreSQL reporting DB
```

## Setup

### Install
```bash
# Core (tanpa dependensi eksternal — pake sqlite3 bawaan Python)
# Sudah bisa jalan: 00_setup, 01-04, 06, 07, 09

# Untuk MongoDB & Streamlit (opsional):
pip install pymongo streamlit pandas
```

### Generate Data
```bash
python 00_setup.py
python 06_etl_pipeline.py   # Isi reporting DB
```

### Docker (untuk MongoDB & PostgreSQL)
```bash
docker compose up -d
```

---

## Sesi 1 (2026-06-13) — SQL & NoSQL Exercises + ETL Pipeline

| # | File | Durasi | Topik |
|---|------|--------|-------|
| 1 | `00_setup.py` | 10m | Generate master DB & reporting DB |
| 2 | `01_sql_basics.py` | 15m | SELECT, WHERE, LIKE, IN, BETWEEN, ORDER BY, LIMIT |
| 3 | `02_sql_aggregation.py` | 20m | GROUP BY, SUM, COUNT, AVG, HAVING |
| 4 | `03_sql_joins.py` | 20m | INNER JOIN, LEFT JOIN, multi-table JOIN |
| 5 | `04_sql_window.py` | 15m | RANK, OVER, PARTITION BY, running total, LAG |
| 6 | `05_nosql_mongodb.py` | 20m | Document model, $unwind, aggregation pipeline |
| 7 | `06_etl_pipeline.py` | 20m | ETL: transform master → reporting (ATTACH) |

**Total: ~120 menit (2 jam)**

### Answer Keys
Semua jawaban ada di folder `answers/`:
```bash
python answers/01_sql_basics.py
python answers/02_sql_aggregation.py
python answers/03_sql_joins.py
python answers/04_sql_window.py
```

---

## Sesi 2 (2026-06-20) — Automation + Visualization + Export

| # | File | Durasi | Topik |
|---|------|--------|-------|
| 1 | `07_scheduler.py` | 25m | 3 cara: Python loop, cronjob, systemd service |
| 2 | `08_streamlit_dashboard.py` | 30m | Dashboard dari reporting DB (tab: cabang, kategori, payment, top produk) |
| 3 | `09_export_data.py` | 15m | CSV, HTML, embedded HTML |
| 4 | **Grafana Bonus** | 20m | Setup Grafana + PostgreSQL/SQLite data source |

**Total: ~90 menit**

---

## Detail Setiap File

### `00_setup.py`
Generate master DB dengan 10 cabang, 12 kategori, 118 produk, 1.000 pelanggan, 10.804 transaksi (Jan-Mar 2026).

### Exercises (01-05)
Setiap file berisi soal dengan comment `-- GANTI query di bawah ini`. Student mengisi SQL, lalu run:
```bash
python 01_sql_basics.py
```

### `06_etl_pipeline.py`
Menggunakan SQLite ATTACH untuk transformasi data master → reporting.
Agregasi yang dihasilkan: daily sales per branch, per category, monthly summary, payment method, top products.

### `07_scheduler.py`
Tiga mode:
```bash
# Loop mode (development) — jalan tiap 15 menit
python 07_scheduler.py loop

# Once mode (untuk cronjob) — jalan sekali lalu exit
python 07_scheduler.py once

# Cronjob (production)
# crontab -e
0 * * * * cd /path && python 07_scheduler.py once

# systemd service — file .service sudah dijelaskan di docstring
```

### `08_streamlit_dashboard.py`
```bash
streamlit run 08_streamlit_dashboard.py
```
Dashboard membaca dari **reporting DB** (bukan master), jadi query-nya cepat.
Ada 4 tab: penjualan per cabang, per kategori, metode pembayaran, top produk.

### `09_export_data.py`
```bash
# Export semua tabel ke semua format
python 09_export_data.py

# Export spesifik
python 09_export_data.py csv daily_sales_by_branch
python 09_export_data.py html monthly_sales_summary
python 09_export_data.py embedded top_products
```

---

## Kenapa Reporting DB Terpisah?

```
            MASTER DB (normalized)             REPORTING DB (aggregated)
            ┌─────────────────┐               ┌──────────────────────┐
            │ sales_headers   │               │ daily_sales_by_       │
            │ sales_items     │──ETL──►        │   branch             │
            │ products        │   cron         │ daily_sales_by_      │
            │ branches        │               │   category           │
            │ customers       │               │ monthly_summary      │
            └─────────────────┘               │ top_products         │
                    │                         └──────────────────────┘
                    │                                 │
                    ▼                                 ▼
              Query lambat                     Query super cepat
              (JOIN 5 tabel)                   (1 tabel, pre-aggregated)
```

- **Master DB**: query lambat karena perlu JOIN & aggregate di runtime
- **Reporting DB**: data sudah siap pakai, tinggal SELECT — cocok untuk dashboard
- **ETL cronjob**: update reporting DB periodik (tiap 15 menit / 1 jam)
- **Setiap student manage reporting DB sendiri**

## Dataset

### Master DB Tables
| Table | Rows | Deskripsi |
|-------|------|-----------|
| branches | 10 | Cabang Borma se-Jawa Barat & Banten |
| categories | 12 | Makanan Ringan, Minuman, Susu, dll |
| products | 118 | Produk dengan SKU, harga modal & jual |
| customers | 1.000 | Pelanggan dengan member ID |
| sales_headers | 10.804 | Transaksi Jan-Mar 2026 |
| sales_items | 48.700 | Item per transaksi |
| suppliers | 20 | Supplier dengan terms pembayaran |
| purchase_orders | 500 | PO ke supplier |
| inventory | 816 | Stok per cabang per produk |

### Reporting DB Tables
| Table | Rows | Deskripsi |
|-------|------|-----------|
| daily_sales_by_branch | 900 | Penjualan harian per cabang |
| daily_sales_by_category | 1.080 | Penjualan harian per kategori |
| monthly_sales_summary | 30 | Ringkasan bulanan per cabang |
| payment_method_summary | 450 | Penjualan per metode bayar per hari |
| top_products | 354 | Peringkat produk terlaris per bulan |

## Grafana (Bonus)

### Option A: Grafana + SQLite (via sqlite3datasource)
```bash
docker run -d -p 3000:3000 --name=grafana grafana/grafana
# Install plugin: grafana-sqlite3-datasource
# Add data source → SQLite → path ke reporting.db
```

### Option B: Grafana + PostgreSQL
```bash
# Di docker-compose.yml sudah ada service postgres
python migrate_to_pg.py  # (akan dibuat terpisah)
# Add data source → PostgreSQL → host: localhost, db: reporting_db
```
