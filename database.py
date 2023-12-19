import mysql.connector
from insert import data_admins

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
