import pyodbc

DB_CONFIG = {
    "server": "192.168.86.104",
    "database": "belajar_db",
    "username": "siswa",
    "password": "python6an!",
    "driver": "{ODBC Driver 18 for SQL Server}",
}

'''
sudo apt install -y curl gnupg2
https://pastebin.com/qSHZCiRA
'''

CONN_STR = (
    f"DRIVER={DB_CONFIG['driver']};"
    f"SERVER={DB_CONFIG['server']};"
    f"DATABASE={DB_CONFIG['database']};"
    f"UID={DB_CONFIG['username']};"
    f"PWD={DB_CONFIG['password']};"
    "TrustServerCertificate=yes;"
)

def get_conn():
    conn = pyodbc.connect(CONN_STR, fast_executemany=True)
    return conn

if __name__ == '__main__':
    print('=== TEST MSSQL ===')
    try:
        conn = get_conn()
        print(f'{conn} - KONEKSI BERHASIL')
    except Exception as e:
        print(f'ERROR: Tidak bisa konek ke MSSQL: {e}')
        print('Jalankan: docker compose up -d')
        exit(1)

    conn.close()