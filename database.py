import mysql.connector
from insert import data_admins, data_users

db = None

def initialize_database():
    global db
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="isiladb"
    )

    return db

def get_database_cursor():
    return db.cursor(dictionary = True)

def create_database():
    cursor = get_database_cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS admins (username VARCHAR(255) PRIMARY KEY, password VARCHAR(255) NOT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS users (username VARCHAR(255) PRIMARY KEY, password VARCHAR(255) NOT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS pengajuan (id_aju VARCHAR(5) PRIMARY KEY, nrp VARCHAR(20), jabatan VARCHAR(50), name VARCHAR(255), age INT, gender CHAR(1), tgl_aju DATE, path_aju VARCHAR(255), status VARCHAR(20))")
    cursor.execute("CREATE TABLE IF NOT EXISTS pengembalian (id_png VARCHAR(5) PRIMARY KEY, nrp VARCHAR(20), jabatan VARCHAR(50), name VARCHAR(255), age INT, gender CHAR(1), tgl_png DATE, path_png VARCHAR(255), status VARCHAR(20))")

    cursor.close()

def insert_admins():
    try:
        cursor = get_database_cursor()

        for admin in data_admins:
            cursor.execute("SELECT COUNT(*) as count FROM admins WHERE username = %s", (admin['username'],))
            result = cursor.fetchone()

            if result and result['count'] == 0:
                cursor.execute(
                    "INSERT INTO admins (username, password) VALUES (%s, %s)",
                    (admin['username'], admin['password'])
                )

        db.commit()

    except Exception as e:
        print("Error:", str(e))
        db.rollback()

    finally:
        cursor.close()

def check_admin_credentials(username, password):
    cursor = get_database_cursor()
    query = "SELECT * FROM admins WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    if result:
        return True
    else:
        return False

def insert_users():
    try:
        cursor = get_database_cursor()

        for admin in data_users:
            cursor.execute("SELECT COUNT(*) as count FROM users WHERE username = %s", (admin['username'],))
            result = cursor.fetchone()

            if result and result['count'] == 0:
                cursor.execute(
                    "INSERT INTO users (username, password) VALUES (%s, %s)",
                    (admin['username'], admin['password'])
                )

        db.commit()

    except Exception as e:
        print("Error:", str(e))
        db.rollback()

    finally:
        cursor.close()

def check_user_credentials(username, password):
    cursor = get_database_cursor()
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    if result:
        return True
    else:
        return False

def id_aj():
    cursor = get_database_cursor()

    cursor.execute("SELECT id_aju FROM pengajuan ORDER BY id_aju DESC LIMIT 1")
    result = cursor.fetchone()

    if result and result['id_aju']:
        last_ipg = result['id_aju']
        prefix = last_ipg[:-2]
        numeric_part = int(last_ipg[-2:]) + 1
        next_ipg = f'{prefix}{numeric_part:02d}'
    else:
        next_ipg = '#01'

    cursor.close()

    return next_ipg


def id_pn():
    cursor = get_database_cursor()

    cursor.execute("SELECT id_png FROM pengembalian ORDER BY id_png DESC LIMIT 1")
    result = cursor.fetchone()

    if result and result['id_png']:
        last_ipgn = result['id_png']
        prefix = last_ipgn[:-2]
        numeric_part = int(last_ipgn[-2:]) + 1
        next_ipgn = f'{prefix}{numeric_part:02d}'
    else:
        next_ipgn = '#01'

    cursor.close()

    return next_ipgn
