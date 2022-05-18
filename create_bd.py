import sqlite3


DB_PATH = 'results/san_francisco.sqlite3'
SQL_FILE_PATH = 'create_bd.sql'

def run_sql_script(cursor, path):
    with open(path, 'r') as file:
        sql_script = file.read()

    cursor.executescript(sql_script)
    print("SQL script is done")

def connect_and_run_execute(execute, *args):
    try:
        connection = sqlite3.connect(DB_PATH)
        print("Successfull connection")
        cursor = connection.cursor()

        execute(cursor, *args)

        connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("SQLite error", error)

    finally:
        if (connection):
            connection.close()
            print("Connection close")

if __name__ == '__main__':
    connect_and_run_execute(run_sql_script, SQL_FILE_PATH)
