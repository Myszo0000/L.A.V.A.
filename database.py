import sqlite3

def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn

def create_table(conn):
    sql_create_tasks_table = """ CREATE TABLE IF NOT EXISTS tasks (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        completed boolean NOT NULL
                                    ); """
    try:
        c = conn.cursor()
        c.execute(sql_create_tasks_table)
    except Exception as e:
        print(e)

def insert_task(conn, task):
    sql = ''' INSERT INTO tasks(name, completed)
              VALUES(?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()
    return cur.lastrowid

def get_tasks(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")
    return cur.fetchall()
  #python-database
