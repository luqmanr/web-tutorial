# Database Lanjutan: SQL vs NoSQL

## Pendahuluan
Sesi ini akan membahas berbagai aspek database, perbedaan mendasar antara SQL (relational) dan NoSQL (non-relational), kapan menggunakan masing-masing, serta praktik langsung dalam membuat dan mengelola database.

**Durasi:** 2 Jam

## Prasyarat
- Pemahaman dasar Python programming
- Pengetahan minimal tentang struktur data (list, dict, tuple)
- Komputer dengan akses internet untuk instalasi

## Tujuan Pembelajaran
Setelah sesi ini, Anda diharapkan dapat:
1. Memahami perbedaan mendasar SQL vs NoSQL
2. Memilih database yang tepat untuk berbagai use case
3. Membangun koneksi ke database SQLite dan PostgreSQL
4. Membuat skema database yang sesuai dengan kebutuhan aplikasi
5. Melakukan operasi CRUD (Create, Read, Update, Delete)
6. Mendemonstrasikan kelebihan dan kekurangan masing-masing jenis database

---

### 🎓 Pengalaman Praktis Database Saya (Kenapa SQL > NoSQL untuk most use cases)

Saya punya pengalaman praktis dengan berbagai database engine:

1. **PostgreSQL** - Paling performant untuk production (lihat benchmark2 online)
2. **Elasticsearch** - Pakai sebagai frontend search engine untuk Kibana, data utama masih di PostgreSQL  
3. **Milvus** - Pernah cek untuk vector search, tapi pgvector sudah cukup dipakai di PostgreSQL jadi Milvus obsolete
4. **SQLite** - Untuk aplikasi ringan/embedded atau development quick start
5. **ObjectBox** - Sedang explore (lightweight NoSQL Python)

### Kenapa Pakai SQL/PostgreSQL sebagai Primary?

✅ **Performant**: Dengan perkembangan teknologi, PostgreSQL terbukti paling performant dibanding MySQL/MariaDB  
✅ **Jsonb Support**: Powerful untuk query semi-structured data + relasi kompleks dalam satu database  
✅ **Familiarity**: Tidak perlu pindah ke NoSQL jika sudah familiar dengan PostgreSQL

### Personal Pattern Saya:

Jika belum tau apakah data butuh relasi atau tidak, saya mostly pakai cuma 2 kolom:
    ```python
    # timestampz + jsonb untuk flexible storage:
    CREATE TABLE flexible_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP AT TIME ZONE 'utc',
        data JSONB NOT NULL  -- Bisa query isi jsonb-nya langsung!
    )
    ```

**Kesimpulan**: Jika project butuh reliable + performant dan sudah familiar PostgreSQL, pakai PostgreSQL + jsonb. Tidak perlu repot ke NoSQL untuk kebanyakan modern use cases.

---

## 🎯 Choose NoSQL Over SQL? (Khi Naik Pilih)

Pilih **NoSQL over SQL** ketika Anda butuhkan:
- ✅ Handle massive, rapidly changing datasets yang butuh high speed & scalability
- ✅ BIKIN strict data consistency & complex relationships itu prioritas utama

Sementara SQL (relational) databases rely auf rigid, predefined tables, NoSQL (non-relational) databases offer flexible structures like documents or key-value pairs yang easier to scale horizontally across multiple servers.

### Key Reasons to Choose NoSQL:

#### 📦 Massive Horizontal Scalability
NoSQL databases designed to "scale out" by adding more servers ke cluster, making them more cost-effective untuk big data applications dibandingkan vertical "scale up" (lebih powerful hardware) typically required buat SQL.

#### 🔧 Schema Flexibility  
Do not need define rigid data structure upfront. This "schema-less" nature allows rapid development & frequent changes to data model tanpa downtime atau complex migrations.

#### ⚡ High Performance untuk Simple Queries
By avoiding complex table joins & normalizing data, NoSQL can offer faster read/write speeds buat large-scale, high-velocity workloads like real-time analytics atau social media feeds.

#### 📝 Diverse Data Types
NoSQL excels storing unstructured or semi-structured data (e.g., JSON, XML, images, atau sensor data) yang does not fit neatly into rows & columns traditional table.

#### 🔄 High Availability  
Many NoSQL systems prioritize system responsiveness & availability over immediate consistency, using distributed architectures that have no single point of failure.

### Common Use Cases untuk NoSQL:

| Application Type | Why NoSQL is Preferred |
|------------------|------------------------|
| Real-Time Big Data | Handles high-velocity data dari IoT sensors atau log files |
| Content Management | Flexible enough store varied metadata buat videos, images, & posts |
| Social Networks | Graph databases efficiently map complex, interconnected user relationships |
| E-commerce Catalogs | Accommodates products dengan highly varying attributes (e.g., shirt vs. laptop) |
| Mobile Apps | Supports rapid iteration & offline data syncing with flexible JSON documents |

### NoSQL vs SQL Comparison Summary:

| Feature | SQL (Relational) | NoSQL (Non-Relational) |
|---------|------------------|------------------------|
| **Data Model** | Predefined, fixed schema | Dynamic, flexible schema |
| **Scaling** | Vertical (bigger server) | Horizontal (more servers) |
| **Consistency** | Strong (ACID properties) | Often eventual (BASE properties) |
| **Complexity** | Best for complex joins/queries | Best for simple, fast access |
| **Examples** | MySQL, PostgreSQL | MongoDB, Cassandra |


### 1.1 Apa itu Database?

**Database** adalah tempat menyimpan data secara terstruktur yang dapat diakses melalui program komputer. Dua pendekatan utama:

#### Relational Databases (SQL)
- Data disimpan dalam **tables dengan rows dan columns**
- Menggunakan **schema/fixed structure** - struktur harus ditentukan sebelum menyimpan
- Mengikuti **ACID principles**: Atomicity, Consistency, Isolation, Durability
- Contoh: MySQL, PostgreSQL, SQLite, SQL Server

#### Non-Relational Databases (NoSQL)
- Data disimpan dalam format **flexible/unstructured**
- Beberapa memiliki **dynamic schema** - bisa berubah setiap saat
- Mengutamakan **scalability** dan performa read-intensive
- Jenis-jenis NoSQL:
  - **Document**: MongoDB, CouchDB
  - **Key-Value**: Redis, DynamoDB
  - **Column-family**: Cassandra, HBase
  - **Graph**: Neo4j, Amazon Neptune

### 1.2 Perbandingan Mendalam

| Aspek | SQL (Relational) | NoSQL |
|-------|------------------|---------|
| **Konsistensi** | High consistency (ACID) | Eventual consistency |
| **Scalability** | Vertical scaling (tambah RAM/CPU) | Horizontal scaling (tambah node) |
| **Query Language** | SQL (standardized) | API spesifik / query sendiri |
| **Schema** | Fixed, rigid schema | Flexible/dynamic schema |
| **Use Case** | Data dengan relasi kompleks, transaksi finansial, laporan analytical | Big data, real-time analytics, content management |

### 1.3 Metaphor untuk Memahami Perbedaannya

#### SQL seperti Buku Katalog Perpustakaan
```sql
-- Anda harus membuat struktur dulu
CREATE TABLE books (
    isbn VARCHAR(20) PRIMARY KEY,
    title TEXT NOT NULL,
    author VARCHAR(100) NOT NULL,
    published_year INTEGER
);

INSERT INTO books VALUES (
    '1234567890', 
    'Harry Potter', 
    'J.K. Rowling', 
    1997
);
```

**Keuntungan**: Terstruktur rapi semua data ada di tempat yang jelas
**Kekurangan**: Sulit mengubah struktur jika format berubah (misal: sekarang kita mau tambah kolom "number_of_pages")

#### NoSQL seperti Kardus Stok Barang
```python
# MongoDB style - setiap document bebas punya field berbeda
books = [
    {
        "_id": ObjectId("5f8d1234..."),
        "title": "Harry Potter",
        "author": "J.K. Rowling"
    },
    {
        "_id": ObjectId("5f8d1234..."),
        "title": "Lord of the Rings",
        "author": "J.R.R. Tolkien",
        "genre": ["Fiction", "Fantasy"],  # bisa lebih dari satu
        "pages": 1178,
        "publisher": "Allen & Unwin"
    }
]
```

**Keuntungan**: Sangat fleksibel - setiap dokumen bisa beda-beda
**Kekurangan**: Sulit untuk query yang membutuhkan relasi data antar dokumen

### 1.4 Use Cases Pilihan

#### Pilih SQL jika:
- ✅ Aplikasi e-commerce (order processing, transactions)
- ✅ Social media dengan feed timeline (relasi user-content-comments)
- ✅ Sistem finansial/banking (kepentingan konsistensi tinggi)
- ✅ Aplikasi enterprise dengan data yang terstruktur
- ✅ **PostgreSQL**: Seiring perkembangan teknologi, PostgreSQL terbukti paling performant sebagai engine database (lihat benchmark2 online untuk perbandingan performa vs MySQL/SQLite)

#### Pilih NoSQL jika:
- ✅ Content Management System (blog, CMS)
- ✅ Real-time analytics & monitoring
- ✅ Big Data / IoT data collection
- ✅ Prototype cepat atau startup MVP
- ✅ Data format berubah-ubah frekuenstinya besar

---

## Modul 2: SQL dengan SQLite - Database File-Based Ringan (± 45 menit)

### 2.1 Instalasi Python SQLite

```bash
# SQLite biasanya sudah included dalam Python standar library
# Tidak perlu instalasi tambahan!
python -c "import sqlite3; print(sqlite3.sqlite_version)"
```

### 2.2 Membuat Database Pertama Anda

```python
import sqlite3

# Connect ke database (file dibuat otomatis jika belum ada)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Buat tabel
cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT NOT NULL UNIQUE,
    full_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1
)
''')

# Tambah user pertama
cursor.execute(
    'INSERT INTO users (username, email, full_name) VALUES (?, ?, ?)',
    ('budi_santa', 'budi@luqmanr.xyz', 'Budi Santoso')
)

conn.commit()

# Verify data
cursor.execute('SELECT * FROM users WHERE is_active = 1')
print(cursor.fetchall())

conn.close()
```

### 2.3 Membuat Database Relasional Lengkap E-Commerce Sederhana

```python
import sqlite3

def create_ecommerce_database():
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    
    # Tabel Users
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Tabel Posts/Kommenter (bukan owner)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        author_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (author_id) REFERENCES users(id)
    )
    ''')
    
    # Tabel Comments dengan relasi
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER NOT NULL,
        author_username TEXT NOT NULL,
        content TEXT NOT NULL,
        likes_count INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (post_id) REFERENCES posts(id)
    )
    ''')
    
    # Tabel untuk menyimpan tags artikel
    cursor.execute('''
    CREATE TABLE IF_not EXISTS post_tags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER NOT NULL,
        tag_name TEXT NOT NULL,
        FOREIGN KEY (post_id) REFERENCES posts(id)
    )
    ''')
    
    conn.commit()
    return conn
    
# Buat database
db = create_ecommerce_database()

# Insert sample data
cursor = db.cursor()

# Tambah user
cursor.execute(
    'INSERT INTO users (username, email, password_hash, full_name) VALUES (?, ?, ?, ?)',
    ('john_doe', 'john@example.com', '$2b$12$ABC...', 'John Doe')
)

# Insert post
cursor.execute('''
INSERT INTO posts (title, content, author_id) 
VALUES (?, ?, ?)
''',
('Belajar Python dengan SQLite',
'`SQLite` adalah database file-based yang ringan dan mudah digunakan. Dalam tutorial ini, kita akan belajar berbagai aspek dari SQL vs NoSQL.',
1)
)

# Insert comments
cursor.execute('''
INSERT INTO comments (post_id, author_username, content, likes_count)
VALUES (?, ?, ?, ?)
''',
(post_id: db.lastrowid,
'Ini tutorial pertama saya!',
'Tutorial ini sangat bagus!')
)

db.close()
```

### 2.4 Operasi CRUD Lengkap dengan SQL

#### Create (CREATE & INSERT)
```python
import sqlite3

conn = sqlite3.connect('blog.db')
cursor = conn.cursor()

# Buat tabel baru
cursor.execute('''
CREATE TABLE articles IF NOT EXISTS (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    summary TEXT,
    body TEXT NOT NULL,
    author TEXT NOT NULL,
    published BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# INSERT dengan parameterized query (security!)
cursor.execute(
    'INSERT INTO articles (title, summary, body, author, published) VALUES (?, ?, ?, ?, ?)',
    (
        'Tutorial Database Python',
        'Belajar SQL menggunakan SQLite3',  
        '''SQLite adalah embedded database yang sangat powerful...''',
        'Tutorial Team',
        0
    )
)

conn.commit()
new_id = cursor.lastrowid  # ID dari data baru yang ditambahkan
print(f"Data berhasil ditambahkan dengan ID: {new_id}")
```

#### Read (SELECT - Berbagai Jenis Query)
```python
cursor = conn.cursor()

# BASIC SELECT
cursor.execute('SELECT * FROM articles ORDER BY created_at DESC LIMIT 10')
rows = cursor.fetchall()

# WITH COLUMN NAMES
for row in rows:
    print({
        'id': row[0],
        'title': row[1],
        'summary': row[2] if len(row) > 2 else None,  
    })

# SELECT DENGAN FILTER
cursor.execute('SELECT * FROM articles WHERE published = 1')
published_articles = cursor.fetchall()

# INNER JOIN - Menggabungkan data dari beberapa tabel
cursor.execute('''
SELECT a.title, u.full_name AS author
FROM articles a
LEFT JOIN users u ON a.author_id = u.id
WHERE a.published = 1
LIMIT 20
''')
```

#### Update (SQL UPDATE)
```python
# UPDATE SATU FIELD
cursor.execute(
    'UPDATE articles SET published = 1 WHERE id = ?',
    (new_id,)
)

# UPDATE DENGAN CONDITION COMPLEX
cursor.execute('''
UPDATE articles 
SET views = views + 1, last_read_at = CURRENT_TIMESTAMP
WHERE title LIKE '%Python%'
''')

# MASS UPDATE dengan multiple statements
updates = [
    {'id': 1, 'views': 99},
    {'id': 2, 'views': 85}
]
cursor.executemany(
    'UPDATE articles SET views = ? WHERE id = ?',
    [(u['views'], u['id']) for u in updates]
)

# ROLLBACK jika error (good practice!)
try:
    # lakukan update/transaction
except Exception as e:
    cursor.execute('ROLLBACK')  # kembalikan semua perubahan
```

#### Delete (SQL DELETE)
```python
# HAPUS DENGAN ID
cursor.execute('DELETE FROM articles WHERE id = ?', (new_id,))

# HAPUS BERBASIS CONDITION
cursor.execute('DELETE FROM comments WHERE likes_count < ?', (5,))

# SOFT DELETE - Tandai sebagai deleted_instead dari hapus benar-benar
cursor.execute('''
UPDATE articles 
SET is_deleted = 1, deleted_at = CURRENT_TIMESTAMP 
WHERE id = ?
''', (some_id,)
)

# PERMANENT DELETE HANYAK BARU DILAKUKAN jika:
if cursor.rowcount != 0:
    conn.commit()
```

### 2.5 Advanced SQLite Features

#### Transactions Management
```python
conn.row_factory = sqlite3.Row  # Access by column name

# AUTO TRANSACTION MANAGEMENT
conn = sqlite3.connect('db.sqlite', timeout=10)

try:
    cursor = conn.cursor()
    
    # Begin transaction (automatic)
    cursor.execute(
        'INSERT INTO users (username, email) VALUES (?, ?)',
        ('test_user', 'test@test.com')
    )
    cursor.execute('SELECT last_insert_rowid()')  # Get the ID
    
    conn.commit()  # Commit changes
    print(f"User created with ID: {cursor.fetchone()[0]}")
    
except Exception as e:
    conn.rollback()  # Rollback on error
    raise e

finally:
    conn.close()
```

#### Indexing untuk Performance
```python
# Tambah index untuk query yang sering dilakukan
cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_articles_title ON articles(title)')

# Composite Index (untuk multiple columns)
cursor.execute('''
CREATE INDEX IF NOT EXISTS idx_posts_author_date 
ON posts(author_id, created_at DESC)
''')

# Partial Index (SQLite 3.8+)
cursor.execute('''
CREATE INDEX IF NOT EXISTS idx_published_articles 
ON articles(created_at) 
WHERE published = 1
''')
```

#### Views - Query dengan Logic Fixed
```python
# CREATE VIEW untuk query yang kompleks
cursor.execute('''
CREATE VIEW AS active_users_summary AS
SELECT 
    username,
    COUNT(DISTINCT posts.id) AS post_count,
    SUM(likes_count) AS total_likes
FROM users u
LEFT JOIN comments ON u.username = comments.author_username
WHERE is_active = 1
GROUP BY u.id
ORDER BY total_likes DESC
''')

# Query view seperti query tabel biasa
cursor.execute('SELECT * FROM active_users_summary LIMIT 5')
```

#### JSON Support di SQLite (Modern SQLite)
```python
# SQLite 3.38+ support JSON functions

cursor.execute('''
-- Menyimpan data sebagai JSON string dalam satu field
INSERT INTO products (name, specs, price) 
VALUES (?, ?, ?)
''', ('Laptop XYZ', '{"ram": 16, "ssd": true}', 7500000))

cursor.execute("""
-- Parse JSON dan ambil nilai
SELECT name, json_extract(specs, '$.ram'), json_extract(specs, '$.ssd')
FROM products;
""")

cursor.execute("""
-- Filter data berdasarkan JSON content
SELECT * FROM products WHERE json_extract(specs, '$.ram') > 12
""")
```

---

## Modul 3: Best Practices dan Production Ready (± 30 menit)

### 3.1 Database Connection Pooling

```python
import sqlite3
from queue import Queue
import threading

class SQLiteConnectionPool:
    """Simple connection pool untuk production"""
    
    def __init__(self, db_path, max_size=10):
        self.db_path = db_path
        self.max_size = max_size
        self.queue = Queue(maxsize=max_size)
        
        # Pre-create and initialize connections
        for _ in range(max(max_size % 2, 1)):  
            try:
                conn = sqlite3.connect(db_path, check_same_thread=False)
                conn.create_execution()
                pool._pool.append(conn)
            except Exception as e:
                print(f"Could not create connection: {e}")
    
    def get_connection(self):
        return self.connections.pop() if self.connections else self._create_new_connection()
    
    def return_connection(self, conn):
        # Return to pool or close if too many connections
```

### 3.2 SQL Injection Prevention (WAJIB BACA!)

```python
# BAD - SQL INJECTION VULNERABLE!
username = input("Enter username: ")
cursor.execute(f"SELECT * FROM users WHERE email LIKE '%{username}%'",)  # VULNERABLE!

# GOOD - Using Parameterized Queries (PREVENTS SQL INJECTION!)
email_search_term = "%" + username + "%"  # Clean input first if needed
cursor.execute('SELECT * FROM users WHERE email LIKE ?', (email_search_term,))

# GOOD - Multiple parameters
user_id = 5
search_pattern = "%Python%"
cursor.execute(
    'SELECT title FROM articles WHERE id = ? AND title LIKE ?',
    (user_id, search_pattern)
)

# BAD vs GOOD Comparison
print(f"Bad:   SELECT * FROM users WHERE email = '{email}'")          # INJECTION!
print(f"Good:  SELECT * FROM users WHERE email = ?")                   # Safe with placeholders
```

### 3.3 Database Migrations (Simple Version)

```python
import sqlite3
jsonschema

class DatabaseMigrator:
    """Simple database migration system"""
    
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
    
    def _get_current_schema(self):
        """Get current database schema"""
        cursor.execute("
            SELECT name FROM sqlite_master WHERE type='table' ORDER BY name
        ")
        tables = set([row[0] for row in cursor.fetchall()])
        
        results = {table: self._get_table_schema(table) for table in tables}
        return results
    
    def _get_table_schema(self, table_name):
        """Get table columns and constraints"""
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        schema = {
            "columns": [(col['cid'], col['name'], col['type']) for col in columns],
            "row_count": len(self.cursor)('SELECT COUNT(*) FROM' + table_name, table_name))
        )
        return schema
    
    def migrate(self, target_version):
        '''
        Simple migration logic
        Implement your own migration steps here
        '''
        print(f"Migrating database to version {target_version}")

# Usage example
migrator = DatabaseMigrator('myapp.db')
current_schema = migrator._get_current_schema()
print("Current schema:", current_schema)
```

---

## Modul 4: Latihan & Eksperimen (± 15 menit)

### Exercise 1: Build Your First Social Media Database

```python
# TASK: Buat database social media sederhana
import sqlite3

conn = sqlite3.connect('social_media.db')
cursor = conn.cursor()

def create_social_database():
    """Create all necessary tables for mini social network"""
    
    # Users table
    cursor.execute('''CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name TEXT,
        bio TEXT,
        avatar_url TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Posts table
    cursor.execute('''CREATE TABLE posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        author_id INTEGER NOT NULL REFERENCES users(id),
        title TEXT,
        content TEXT NOT NULL,
        image_url TEXT,
        likes_count INTEGER DEFAULT 0,
        views_count INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Comments table
    cursor.execute('''CREATE TABLE comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER NOT NULL REFERENCES posts(id),
        author_id INTEGER NOT NULL REFERENCES users(id),
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Hashtags table
    cursor.execute('''CREATE TABLE hashtags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tag_name TEXT UNIQUE NOT NULL
    )''')
    
    # Post-Hashtag junction table
    cursor.execute('''CREATE TABLE post_hashtags (
        post_id INTEGER REFERENCES posts(id),
        hashtag_id INTEGER REFERENCES hashtags(id),
        PRIMARY KEY (post_id, hashtag_id)
    )''')
    
    conn.commit()

create_social_database()
```

**Challenge**: Implement these features:
1. User dapat login dan membuat akun baru
2. Publish feed dengan likes dan views tracking
3. Comment system pada posts
4. Hashtag filtering untuk search posts

### Exercise 2: Data Analytics Query Patterns

```python
# ANALYTICS QUERY 1: User Engagement Score
cursor.execute('''
SELECT 
    users.id,
    users.username,
    COUNT(posts.id) as total_posts,
    SUM(posts.likes_count) as total_likes,
    AVG(CASE WHEN posts.content LIKE '%Python%' THEN 1 ELSE 0 END) as python_talk_percentage
FROM users
LEFT JOIN posts ON users.id = posts.author_id
GROUP BY users.id
HAVING total_posts > 5
ORDER BY total_likes DESC
''')

# ANALYTICS QUERY 2: Most Popular Content
cursor.execute('''
SELECT 
    post.title,
    COUNT(DISTINCT comments.post_id) as comment_count,
    SUM(comments.likes_count) as total_comment_likes
FROM posts p
JOIN comments c ON p.id = c.post_id
GROUP BY p.id, p.title
ORDER BY total_comment_likes DESC
LIMIT 10
''')
```

### Exercise 3: Complex Data Transformation

Tugas: Buat script yang merangkum data users dengan pola seperti ini:

```python
# Group by activity period
cursor.execute('''
SELECT 
    strftime('%Y', created_at) as year,
    COUNT(*) as new_users_this_year,
    AVG(CASE WHEN is_active = 1 THEN 1 ELSE 0 END) * 100 as active_percentage
FROM users
GROUP BY year
ORDER BY year DESC
''')

# Top performing tags per post
cursor.execute('''
SELECT 
    t.tag_name,
    COUNT(ph.post_id) as used_count,
    GROUP_CONCAT(DISTINCT u.username) as authors_using
FROM post_hashtags ph
JOIN hashtags t ON ph.hashtag_id = t.id
JOIN posts p ON ph.post_id = p.id
JOIN users u ON p.author_id = u.id
WHERE t.tag_name IN ('#python', '#sqlite', '#tutorial')
GROUP BY t.tag_name
ORDER BY used_count DESC
''')

print(cursor.fetchall())
```

---

## Modul 5: NoSQL dengan SQLite JSON (± 15 menit)

### 5.1 Embedding Complex Data dalam JSON Field

Walaupun kita menggunakan SQL database, kita bisa menyimpan data kompleks dalam format JSON di satu field! Ini mirip seperti NoSQL document storage!

```python
import sqlite3
from datetime import datetime

conn = sqlite3.connect('ecommerce_nosql_style.db')
cursor = conn.cursor()

# Schema yang mendukung "NoSQL-like" flexibility
cursor.execute('''CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    stock INTEGER DEFAULT 0,
    -- JSON field untuk specs yang kompleks berubah-ubah
    specifications TEXT DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')

# Insert products dengan spesifikasi berbeda-beda (seperti NoSQL doc)
cursor.execute('''INSERT INTO products 
(name, description, price, stock, specifications) 
VALUES (?, ?, ?, ?, ?)''',

('Smartphone XYZ', 'Phone flagship 2026', 15000000, 50, '{"ram": 8, "storage": "256GB", "camera_megapixels": [48, 12, 13], "battery": 4700}')
)

cursor.execute('''INSERT INTO products
(name, description, price, stock, specifications) 
VALUES (?, ?, ?, ?, ?)',

('Laptop Pro', 'Professional grade laptop', 25000000, 15, 
'{"cpu_model": "Core i7-13700H", "ram": 32, "ssd_type": "NVMe Gen4", "screen_resolution": "QHD"',
'')

# Query dan parse JSON
cursor.execute('''WITH product_specs AS (
    SELECT 
        id, name, price, 
        json_extract(specifications, $.ram) as ram_gb,
        json_extract(specifications, '$.ssd_type') as ssd_type,
        json_array_length(json_extract(specifications, $cameras)) as camera_count
    FROM products
)
SELECT * FROM product_specs WHERE ram_gb > 24 ORDER BY price DESC LIMIT 5
''')

print(cursor.fetchall())

# Aggregate data inside JSON
cursor.execute('''INSERT INTO products (name, specifications) 
VALUES ('Raspberry Pi',?)''', 

json.dumps({
    'cpu': 'ARM Cortex-A72',
    'gpio_pins': 40,
    'memory_options': ['512MB SD Card', '4GB RAM'],
    'compatible_boards': ['Raspberry Pi 3', 'Raspberry Pi 4']
}))

```

### 5.2 NoSQL Patterns dengan SQLite JSON Functions (SQLite 3.38+)

```python
# INDEX untuk query berdasarkan JSON field
cursor.execute('''CREATE INDEX idx_product_specs RAM 
ON products( json_extract(specifications, '$.ram') )''')

# Search array elements inside JSON
cursor.execute('''SELECT * FROM products WHERE specifications IS NOT NULL AND json_extract(specifications, '$.cpu_cores') > 8''')

# Array operations (SQLite 3.37+)
cursor.execute('SELECT id, name FROM sqlite_master WHERE tbl_name = ?', ('products',))

# UPDATE JSON field without re-creating entire document
cursor.execute('''UPDATE products 
SET specifications = json_set(specifications, '$.battery', ?)
WHERE id = 1''')

# Nested path extraction (dot notation works!)
cursor.execute('SELECT product_id, json_extract(json_extract(specifications, $"storage"), '.capacity') FROM products;')

---

## Ringkasan & Next Steps (± 5 menit)

### Summary: SQL vs NoSQL Decision Matrix

| Situasi Gunakan | Database Pilihan | Alasan |
|----------------|-----------------|--------|
| **E-commerce platform** | **SQL (PostgreSQL/MySQL)** | Transaction integrity, multi-table joins untuk order processing |
| **Content Management System** | **NoSQL (MongoDB/Couchbase)** | Flexible schema untuk berbagai content types, cepat write |
| **Real-time analytics dashboard** | **NoSQL (Redis/DynamoDB)** | High-speed reads, eventual consistency ok |
| **Data warehousing / BI** | **SQL (PostgreSQL with extensions)** | Query capability dan JOINs untuk aggregation |
| **Prototyping startup MVP** | **SQLite/PostgreSQL** | Fast development, ACID compliance penting nanti |
| **IoT / sensor data** | **NoSQL (InfluxDB/Cassandra)** | Time-series optimization, massive write throughput |

### Cheat Sheet: Pergi ke SQL SQLite jika:
- ✅ Anda punya relasi data yang kompleks
- ✅ Data perlu transactional integrity
- ✅ Butuh reporting/analytical query kuat
- ✅ Tim teknis familiar dengan SQL
- ✅ Scalability vertikal lebih mudah daripada horizontal

## Penulis Personal tentang Database Experience

### Why I Prefer PostgreSQL over NoSQL (dan pengalaman pribadi saya):

Saya punya pengalaman praktis dengan berbagai database engine:

1. **PostgreSQL** - Sudah pakai lama, paling performant untuk production
2. **Elasticsearch** - Pakai sebagai frontend search engine untuk Kibana dashboard, data utama masih di PostgreSQL
3. **Milvus** - Pernah cek untuk vector search, tapi menemukan `pgvector` sudah bisa dipakai langsung di PostgreSQL jadi Milvus jadi obsolete
4. **SQLite** - Untuk aplikasi ringan/embedded atau development quick start
5. **ObjectBox** - Sedang explore saat ini (untuk lightweight NoSQL Python)

### Kenapa pakai PostgreSQL sebagai primary database?

✅ **Performant**: Seiring perkembangannya, PostgreSQL terbukti paling performant sebagai engine database untuk berbagai workload. Cek benchmark online untuk perbandingan vs MySQL/MariaDB.

✅ **Jsonb Support**: PostgreSQL punya `jsonb` yang powerful! Ini memungkinkan hybrid approach:
- Gunakan schema relational tradisional (tabel) untuk relasi kompleks
- Atau pakai JSONB untuk data semi-structured
- Bisa query dan filter isi jsonb tanpa harus migrate ke NoSQL murni

### Personal Pattern Saya:
Alasan tidak prefer NoSQL karena sudah sangat familiar dengan PostgreSQL. Pola yang saya gunakan mostly cuma 2 kolom jika belum tau data akan punya relasi seperti apa:

```python
# Pola simpel: timestampz + jsonb untuk flexible storage
cursor.execute('''
CREATE TABLE flexible_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP AT TIME ZONE 'utc',  -- Selalu track waktu
    data JSONB NOT NULL   -- JSONB bisa query/filter di dalamnya!
)
''')

# Bisa insert berbagai format:
cursor.execute('INSERT INTO flexible_data (data) VALUES (?)', 
    json.dumps({'user_id': 123, 'settings': {'theme': 'dark', 'notifications': True}}))

# Dan masih bisa query isi JSONB nya:
cursor.execute('''
SELECT id, data->>'theme' as theme_setting
FROM flexible_data
WHERE data->>'theme' = 'dark'
'''
```

---

## Latihan Tambahan untuk Haus Pengetahuan Lebih

### Project Ide 1: Blog Platform Full Stack
- User authentication (users table)
- Create, Read, Update, Delete (CRUD) posts 
- Comment system dengan nested structure
- Tag filtering dengan multiple categories
- Search by title/content keyword
- Views/likes tracking per post

### Project Ide 2: Inventory Management System  
- Products dengan JSON specs yang flexible
- Stock management with batch updates
- Suppliers and orders relational tables
- Low stock alerts with queries
- Historical data tracking

### Project Ide 3: E-commerce Database Architecture
- Users, products, carts, orders, order_items
- Reviews dan ratings system
- Search indexing dengan indexes
- Analytics untuk sales reporting
- Product recommendations (join patterns)

--- 

## Resources Lanjutan

- 📚 **[PostgreSQL Documentation](https://www.postgresql.org/** - Reference lengkap SQL
- 📚 **[SQLite Tutorial](https://sqlite.org/tutorial.html)** - SQLite basics  
- 📚 **[SQLZoo](https://sqlzoosql.zoo)/tutorial](https://sqlzoo.net/text/)** - Interactive SQL practice
- 📚 **[MongoDB Guide](https://www.mongodb.com/learn/introduction)** - NoSQL introduction
- 🔌 **Video references**: [FreeCodeCamp SQLite Course](https://youtube/watch?v=Z54y9uV6J7E)

---

## 📝 Catatan Tambahan & Pertanyaan (FAQ)

### Kenapa NoSQL lebih mudah di-scale horizontally?

**Short answer**: NoSQL designed for **horizontal scaling (scale-out)**, sedangkan SQL designed untuk **vertical scaling (scale-up)**.

#### Vertical Scaling (SQL - traditional):
- Tambah RAM, CPU, disk ke server yang sama
- Limitasi: Ada batas maksimal satu mesin physical
- Example: Server 8-core → upgrade ke 32-core  
- Biaya terus naik seiring hardware power naik

#### Horizontal Scaling (NoSQL - built-in):
- Tambah **banyak server/node sederhana** ke cluster  
- Setiap node bisa lebih sederhana/kurang powerful
- Data didistribusikan ke multiple servers secara otomatis atau manual

##### Karena itu NoSQL mudah horizontal-scale:
1. **Architecture distributed by default** - multi-node cluster adalah design standard
2. **No complex joins needed** - each node handle its own data tanpa cross-node complexity  
3. **Dynamic schema** - setiap dokumen bisa beda structure → easier distribute
4. **Sharding built-in** - partitioning strategies automatic/manual untuk split data ke multiple nodes

---

### Kalau mau scaling horizontally untuk PostgreSQL, gimana caranya?

Short answer: **Tidak se-"natural" NoSQL**, tapi ada beberapa opsi:

#### 1. Read Replicas (Mudah - paling umum)
- Primary node handles **writes**
- Replica nodes handle **reads only**
```python
# Architecture:
Primary Node (write) ←→ Replica Nodes (read only) → Clients
                          ↓                    ↓
                    Query Routing           Analytics
```

#### 2. PgBouncer + Multiple Replicas (Connection pooling)
- pgbouncer untuk connection pool ke multiple replicas
- Write queries → primary
- Read queries → connect ke random replica dari pool

#### 3. Citus Extension (Full horizontal scaling - kompleks)
[Citus](https://github.com/citusdata/citus) extension untuk distributed PostgreSQL.

```python
CREATE EXTENSION citus;
CREATE TABLE distributed_users AS 
SELECT * FROM users WITH (distrib_key=user_id);
```

#### 4. TimescaleDB (Time-series horizontal scaling)
Untuk workload time-series heavy, partitioned berdasarkan waktu.

```python
CREATE HYPERTABLE weather_data(
    timestamp, location_id, temp, pressure
);
```

#### 5. PostgreSQL + External Search Engine Pattern (my favorite 😄)
```
PostgreSQL (write-heavy) ←→ ElasticSearch/Lambda DB (read-heavy)
# Data sync dengan pg_search atau aplikasi level
```

##### Limitasi Horizontal Scaling PostgreSQL:
| Challenge | Lösung |
|-----------|--------|
| Single point of failure | HA cluster + failover |
| No native sharding | Citus/external sharders |
| Complex joins across nodes | Application-level routing |
| Data consistency | Two-phase commit, synchronous replication |

**TLDR**: PostgreSQL bukan "horizontal scaling ready" seperti NoSQL. Kalau butuh pure horizontal scale-out untuk data besar + complex reads/query, consider MongoDB (dengan JSONB pattern) daripada Citus.

--- 
