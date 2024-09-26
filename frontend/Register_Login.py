import os
import hashlib
import sqlite3
from os.path import join, dirname, abspath

db_path = join(dirname(dirname(abspath(__file__))), 'AegisAudit.db')

def create_db():
    try:
        mydb = sqlite3.connect(db_path)
        cursor = mydb.cursor()
        print("Connection established")
        cursor.execute('''CREATE TABLE IF NOT EXISTS accounts(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                salt TEXT NOT NULL,
                profile_picture TEXT NOT NULL,
                role TEXT NOT NULL)''')
        print(f"Database- AegisAudit and tables 'accounts' created successfully")

        # Create user profile pics directory
        user_images_path = r"..\\profile_pictures"
        if not os.path.exists(user_images_path):
            os.makedirs(user_images_path)
            print("User profile picture Directory created successfully!")
        else:
            print("User profile picture Directory already exists!")

        create_admin()
        mydb.commit()
        mydb.close()

    except sqlite3.Error as err:
        print("An error occurred:", err)


def create_secure_password(password, salt=os.urandom(16).hex()):
    password_hash = hashlib.sha256((salt + password).encode()).hexdigest()
    return [password_hash, salt]

def create_user(username, password, profile_picture = None, role = "user"):
    mydb = sqlite3.connect(db_path)
    cursor = mydb.cursor()
    if not profile_picture:
        profile_picture = r"..\profile_pictures\user_icon.png"
    try:
        secure_password_with_salt = create_secure_password(password)
        secure_password, salt = secure_password_with_salt[0], secure_password_with_salt[1]
        cursor.execute('INSERT INTO accounts (name, password, salt, profile_picture, role) VALUES (?, ?, ?, ?, ?)',
                       (username, secure_password, salt, profile_picture, role))
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
    mydb = sqlite3.connect(db_path)
    cursor = mydb.cursor()
    cursor.execute('SELECT EXISTS(SELECT name FROM accounts WHERE name = ?)', (username,))
    exists = cursor.fetchone()
    if exists:
        cursor.execute('SELECT password, salt FROM accounts WHERE name = ?', (username,))
        stored_password, stored_salt = cursor.fetchone()
        if stored_password == create_secure_password(input_password, stored_salt)[0]:
            print(f"Welcome, {username}")
            return True
    return False
    mydb.close()

def create_admin():
    mydb = sqlite3.connect(db_path)
    cursor = mydb.cursor()
    cursor.execute('SELECT COUNT(*) from accounts')
    exists = cursor.fetchone()
    if not exists[0]:
        # print("Empty table")
        admin_name, password, profile_pic = "AegisAdmin", "1234", r"..\profile_pictures\pfp.png"
        create_user(admin_name, password, profile_pic, "Admin")
        print("Admin created successfully")
    else:
        print("Table not empty")
    mydb.close()
