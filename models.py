from database import Database
from utils import hash_password, verify_password
from datetime import date

class UserModel:
    def __init__(self, db: Database):
        self.db = db

    def create_user(self, username, password, role):
        hashed = hash_password(password)
        hashed_str = hashed.decode('utf-8') 
        query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
        try:
            self.db.cursor.execute(query, (username, hashed_str, role))
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False

    def authenticate(self, username, password):
        query = "SELECT id, password, role FROM users WHERE username=%s"
        self.db.cursor.execute(query, (username,))
        result = self.db.cursor.fetchone()
        if result:
            user_id, hashed_pw, role = result
            if verify_password(password, hashed_pw):
                return {'id': user_id, 'username': username, 'role': role}
        return None

class BookModel:
    def __init__(self, db: Database):
        self.db = db

    def add_book(self, title, author, row_loc, col_loc):
        query = "INSERT INTO books (title, author, row_loc, col_loc) VALUES (%s, %s, %s, %s)"
        try:
            self.db.cursor.execute(query, (title, author, row_loc, col_loc))
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding book: {e}")
            return False

    def delete_book(self, book_id):
        query = "DELETE FROM books WHERE id=%s"
        try:
            self.db.cursor.execute(query, (book_id,))
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting book: {e}")
            return False

    def get_all_books(self):
        query = "SELECT id, title, author, row_loc, col_loc FROM books"
        self.db.cursor.execute(query)
        return self.db.cursor.fetchall()

    def search_books_by_title(self, title_search):
        query = "SELECT id, title, author, row_loc, col_loc FROM books WHERE title LIKE %s"
        like_pattern = f"%{title_search}%"
        self.db.cursor.execute(query, (like_pattern,))
        return self.db.cursor.fetchall()

class IssueModel:
    def __init__(self, db: Database):
        self.db = db

    def issue_book(self, user_id, book_id):
        query = "INSERT INTO issued_books (user_id, book_id, issue_date) VALUES (%s, %s, %s)"
        try:
            self.db.cursor.execute(query, (user_id, book_id, date.today()))
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error issuing book: {e}")
            return False

    def return_book(self, issue_id):
        query = "UPDATE issued_books SET return_date = %s WHERE id = %s"
        try:
            self.db.cursor.execute(query, (date.today(), issue_id))
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error returning book: {e}")
            return False

    def get_issued_books_by_user(self, user_id):
        query = """
            SELECT ib.id, b.title, b.author, ib.issue_date, ib.return_date
            FROM issued_books ib
            JOIN books b ON ib.book_id = b.id
            WHERE ib.user_id = %s
        """
        self.db.cursor.execute(query, (user_id,))
        return self.db.cursor.fetchall()
