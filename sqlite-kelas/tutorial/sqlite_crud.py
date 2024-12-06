import sqlite3

def sql_connection():
    """Create a connection with SQLite database specified
        by the mytest.db file
    :param con: the connection object
    :return: connection object or Error"""
    try:
        db = sqlite3.connect('mytest.db')
        return db
    except Exception as e:
        print(e)

def create_table(con):
    """Create the table with given columns"""
    try:
        cur = con.cursor()
        cur.execute('''CREATE TABLE employees(
        id INTEGER PRIMARY KEY,
        name TEXT,
        surname TEXT,
        department TEXT,
        position TEXT,
        salary REAL,
        date TEXT);''')
        con.commit()
        print('The table is created successfully')
    except Exception as e:
        print(e)

def insert_data(con, entities):
    """Insert records into the table"""
    query = """INSERT INTO employees (id, name, surname, department, position,
            salary, date) VALUES(?,?,?,?,?,?,?)"""

    try:
        cur = con.cursor()
        cur.execute(query, entities)
        con.commit()
        print("The record added successfully")
    except Exception as e:
        print(e)

def add_data(con):
    """ The second method to add records into the table"""
    try:
        cur = con.cursor()
        cur.execute("INSERT INTO employees VALUES(2, 'David', 'Anderson', 'IT', 'Dev', 3000, '2020-06-01')")
        cur.execute("INSERT INTO employees VALUES(3, 'Tom', 'Roger', 'IT', 'Manager', 3000, '2018-03-02')")
        cur.execute("INSERT INTO employees VALUES(4, 'Alan', 'Meyer', 'IT', 'Dev', 5000, '2019-04-15')")
        con.commit()
        print("The records added successfully")
    except Exception as e:
        print(e)

def select_all(con):
    """Selects all rows from the table to display"""
    try:
        cur = con.cursor()
        cur.execute('SELECT * FROM employees')
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        print(e)


def update_data(con, salary, id):
    """Update the table with given new values"""
    try:
        cur = con.cursor()
        cur.execute("UPDATE employees SET salary = ?  WHERE id = ?", (salary,
                                                                      id))
        con.commit()
        print("The record updated successfully")
    except Exception as e:
        print(e)


def delete_record(con, surname):
    """Delete the given record"""
    query = "DELETE FROM employees WHERE surname = ?;"
    try:
        cur = con.cursor()
        cur.execute(query, (surname,))
        con.commit()
        print("The record deleted successfully")
    except Exception as e:
        print(e)

def main():
    con = sql_connection()
    create_table(con)
    entities = (1, 'Anna', 'Smith', 'IT', 'Dev', 2000, '2020-02-09')
    insert_data(con, entities)
    add_data(con)
    select_all(con)
    update_data(con, 3000, 1)
    delete_record(con, "Smith")
    select_all(con)
    con.close()

if __name__ == "__main__":
    main()