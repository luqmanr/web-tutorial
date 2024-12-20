import sqlite3

def sql_connection():
    """Create a connection with SQLite database specified
        by the mytest.db file
    :param con: the connection object
    :return: connection object or Error"""
    try:
        db = sqlite3.connect('karyawan.db')
        return db
    except Exception as e:
        print(e)

def create_table(con):
    # Create the table with given columns
    try:
        cur = con.cursor()
        cur.execute('''
            CREATE TABLE karyawan(
                id INTEGER PRIMARY KEY,
                nama TEXT,
                umur INTEGER,
                kota TEXT);
        ''')
        con.commit()
        print('The table is created successfully')
    except Exception as e:
        print(e)

def insert_data(con, id, nama, umur, kota):
    # Insert records into the table
    query = """INSERT INTO karyawan(
            id, 
            nama, 
            umur, 
            kota) 
        VALUES(?,?,?,?);"""

    try:
        cur = con.cursor()
        cur.execute(query, (id, nama, umur, kota,))
        con.commit()
        print("The record added successfully")
    except Exception as e:
        print(e)

def add_data(con):
    # The second method to add records into the table
    try:
        cur = con.cursor()
        cur.execute("INSERT INTO karyawan VALUES(2, 'David', 77, 'Amsterdam')")
        cur.execute("INSERT INTO karyawan VALUES(3, 'Thomas', 30, 'Jakarta')")
        cur.execute("INSERT INTO karyawan VALUES(4, 'Tintin', 21 , 'Bekasi')")
        con.commit()
        print("The records added successfully")
    except Exception as e:
        print(e)

def select_all(con):
    # Selects all rows from the table to display
    try:
        cur = con.cursor()
        cur.execute('SELECT * FROM karyawan')
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        print(e)


def update_data(con, umur_baru, id):
    # Update the table with given new values
    try:
        cur = con.cursor()
        cur.execute("UPDATE karyawan SET umur = ?  WHERE id = ?", (umur_baru, id))
        con.commit()
        print("The record updated successfully")
    except Exception as e:
        print(e)


def delete_record(con, id):
    # Delete the given record
    query = "DELETE FROM karyawan WHERE id = ?;"
    try:
        cur = con.cursor()
        cur.execute(query, (id,))
        con.commit()
        print("The record deleted successfully")
    except Exception as e:
        print(e)

def main():
    con = sql_connection()
    create_table(con)
    insert_data(con, 1, 'Luqman', 30, 'Bandung')
    add_data(con)
    select_all(con)
    update_data(con, 55, 4)
    delete_record(con, 2)
    select_all(con)
    con.close()

if __name__ == "__main__":
    main()