import mysql.connector
from getpass import getpass

class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        print("Enter MySQL root credentials:")
        user = input("Username (usually 'root'): ")
        password = getpass("Password: ")
        try:
            self.conn = mysql.connector.connect(
                host='localhost',
                user=user,
                password=password
            )
            self.cursor = self.conn.cursor()
            self.create_database()
            self.conn.database = 'library_db'
            self.create_tables()
            print("Connected and database ready.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            exit(1)

    def create_database(self):
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS library_db")

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password BLOB NOT NULL,
            role ENUM('admin','user') NOT NULL
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author VARCHAR(255),
            row_loc INT,
            col_loc INT
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS issued_books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            book_id INT,
            issue_date DATE,
            return_date DATE,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (book_id) REFERENCES books(id)
        )
        """)
        self.conn.commit()
