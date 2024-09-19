import os
import hashlib
import sqlite3

def create_db():
    try:
        mydb = sqlite3.connect("../../AegisAudit/frontend/AegisAudit.db")
        cursor = mydb.cursor()
        print("Connection established")
        cursor.execute('''CREATE TABLE IF NOT EXISTS Admin(
                Admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
                admin_name TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                salt TEXT NOT NULL)''')
        print(f"Database- AegisAudit and tables 'Admin' created successfully")
        mydb.commit()
        mydb.close()

    except sqlite3.Error as err:
        print("An error occurred:", err)


def create_secure_password(password, salt=os.urandom(16).hex()):
    password_hash = hashlib.sha256((salt + password).encode()).hexdigest()
    return [password_hash, salt]

def create_user(username, password):
    mydb = sqlite3.connect("../../AegisAudit/frontend/AegisAudit.db")
    cursor = mydb.cursor()
    try:
        secure_password_with_salt = create_secure_password(password)
        secure_password, salt = secure_password_with_salt[0], secure_password_with_salt[1]
        cursor.execute('INSERT INTO Admin (admin_name, password, salt) VALUES (?, ?, ?)',
                       (username, secure_password, salt))
        mydb.commit()
        return True
    except sqlite3.IntegrityError:
        # print(f"Error: User '{name}' already exists.")
        return False
    except sqlite3.Error as err:
        # print(f"Error: {err}")
        return False
    finally:
        mydb.close()


def login_user(username, input_password):
    mydb = sqlite3.connect("../../AegisAudit/frontend/AegisAudit.db")
    cursor = mydb.cursor()
    cursor.execute('SELECT EXISTS(SELECT admin_name FROM Admin WHERE admin_name = ?)', (username,))
    exists = cursor.fetchone()
    if exists:
        cursor.execute('SELECT password, salt FROM Admin WHERE admin_name = ?', (username,))
        stored_password, stored_salt = cursor.fetchone()
        if stored_password == create_secure_password(input_password, stored_salt)[0]:
            print(f"Welcome, {username}")
            return True
    return False
    mydb.close()
