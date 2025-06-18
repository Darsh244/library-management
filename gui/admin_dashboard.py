import tkinter as tk
from tkinter import ttk, messagebox
from models import BookModel, IssueModel, UserModel
from datetime import datetime

class AdminDashboard(tk.Frame):
    import tkinter as tk
from tkinter import ttk, messagebox
from models import BookModel, IssueModel, UserModel
from datetime import datetime

class AdminDashboard(tk.Frame):
    def __init__(self, master, db, user, logout_callback):
        super().__init__(master)
        self.master = master
        self.db = db
        self.user = user
        self.logout_callback = logout_callback
        self.book_model = BookModel(db)
        self.issue_model = IssueModel(db)
        self.user_model = UserModel(db)
        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.refresh_books()

    def create_widgets(self):
        self.label = tk.Label(self, text=f"Admin Dashboard - Welcome {self.user['username']}", font=("Arial", 14))
        self.label.pack(pady=10)

        # Book list treeview
        self.tree = ttk.Treeview(self, columns=("ID", "Title", "Author", "Row", "Column"), show='headings')
        for col in ("ID", "Title", "Author", "Row", "Column"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(pady=10)

        # Add book fields
        frame = tk.Frame(self)
        frame.pack(pady=10)

        tk.Label(frame, text="Title").grid(row=0, column=0)
        tk.Label(frame, text="Author").grid(row=0, column=1)
        tk.Label(frame, text="Row").grid(row=0, column=2)
        tk.Label(frame, text="Column").grid(row=0, column=3)

        self.title_entry = tk.Entry(frame)
        self.title_entry.grid(row=1, column=0)

        self.author_entry = tk.Entry(frame)
        self.author_entry.grid(row=1, column=1)

        self.row_entry = tk.Entry(frame, width=5)
        self.row_entry.grid(row=1, column=2)

        self.col_entry = tk.Entry(frame, width=5)
        self.col_entry.grid(row=1, column=3)

        tk.Button(self, text="Add Book", command=self.add_book).pack(pady=5)
        tk.Button(self, text="Delete Selected Book", command=self.delete_book).pack(pady=5)

        # Issue book to user
        issue_frame = tk.LabelFrame(self, text="Issue Book to User")
        issue_frame.pack(pady=15, fill="x", padx=10)

        tk.Label(issue_frame, text="Username:").grid(row=0, column=0)
        self.issue_username_entry = tk.Entry(issue_frame)
        self.issue_username_entry.grid(row=0, column=1)

        tk.Label(issue_frame, text="Book ID:").grid(row=0, column=2)
        self.issue_book_id_entry = tk.Entry(issue_frame, width=10)
        self.issue_book_id_entry.grid(row=0, column=3)

        tk.Button(issue_frame, text="Issue Book", command=self.issue_book).grid(row=0, column=4, padx=5)

        # Logout button
        tk.Button(self, text="Logout", fg="red", command=self.logout).pack(pady=10)

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.logout_callback()


    def refresh_books(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        books = self.book_model.get_all_books()
        for book in books:
            self.tree.insert('', 'end', values=book)

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        try:
            row_loc = int(self.row_entry.get())
            col_loc = int(self.col_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Row and Column must be integers.")
            return
        if not title:
            messagebox.showerror("Input Error", "Title is required.")
            return
        success = self.book_model.add_book(title, author, row_loc, col_loc)
        if success:
            messagebox.showinfo("Success", "Book added.")
            self.refresh_books()
            self.title_entry.delete(0, 'end')
            self.author_entry.delete(0, 'end')
            self.row_entry.delete(0, 'end')
            self.col_entry.delete(0, 'end')
        else:
            messagebox.showerror("Error", "Failed to add book.")

    def delete_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a book to delete.")
            return
        book_id = self.tree.item(selected[0])['values'][0]
        confirm = messagebox.askyesno("Confirm Delete", f"Delete book ID {book_id}?")
        if confirm:
            success = self.book_model.delete_book(book_id)
            if success:
                messagebox.showinfo("Deleted", "Book deleted.")
                self.refresh_books()
            else:
                messagebox.showerror("Error", "Failed to delete book.")

    def issue_book(self):
        username = self.issue_username_entry.get()
        book_id = self.issue_book_id_entry.get()
        if not username or not book_id:
            messagebox.showerror("Input Error", "Enter username and book ID.")
            return
        # get user id by username
        query = "SELECT id FROM users WHERE username=%s"
        self.db.cursor.execute(query, (username,))
        user_data = self.db.cursor.fetchone()
        if not user_data:
            messagebox.showerror("Error", "User not found.")
            return
        user_id = user_data[0]

        try:
            book_id_int = int(book_id)
        except ValueError:
            messagebox.showerror("Input Error", "Book ID must be an integer.")
            return

        # Issue book
        success = self.issue_model.issue_book(user_id, book_id_int)
        if success:
            messagebox.showinfo("Success", "Book issued.")
            self.issue_username_entry.delete(0, 'end')
            self.issue_book_id_entry.delete(0, 'end')
        else:
            messagebox.showerror("Error", "Failed to issue book.")
