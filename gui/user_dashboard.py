import tkinter as tk
from tkinter import ttk, messagebox
from models import BookModel, IssueModel

class UserDashboard(tk.Frame):
    import tkinter as tk
from tkinter import ttk, messagebox
from models import BookModel, IssueModel

class UserDashboard(tk.Frame):
    def __init__(self, master, db, user, logout_callback):
        super().__init__(master)
        self.master = master
        self.db = db
        self.user = user
        self.logout_callback = logout_callback
        self.book_model = BookModel(db)
        self.issue_model = IssueModel(db)
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text=f"User Dashboard - Welcome {self.user['username']}", font=("Arial", 14))
        self.label.pack(pady=10)

        search_frame = tk.Frame(self)
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Search Book by Title:").pack(side="left")
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side="left", padx=5)
        tk.Button(search_frame, text="Search", command=self.search_books).pack(side="left")

        self.tree = ttk.Treeview(self, columns=("ID", "Title", "Author", "Row", "Column"), show='headings')
        for col in ("ID", "Title", "Author", "Row", "Column"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(pady=10)

        tk.Button(self, text="Request Issue Selected Book", command=self.request_issue).pack(pady=5)

        # Issued books list
        tk.Label(self, text="Your Issued Books:").pack(pady=5)
        self.issued_tree = ttk.Treeview(self, columns=("IssueID", "Title", "Author", "Issue Date", "Return Date"), show='headings')
        for col in ("IssueID", "Title", "Author", "Issue Date", "Return Date"):
            self.issued_tree.heading(col, text=col)
            self.issued_tree.column(col, width=100)
        self.issued_tree.pack(pady=10)

        # Logout button
        tk.Button(self, text="Logout", fg="red", command=self.logout).pack(pady=10)

        self.refresh_issued_books()

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.logout_callback()


    def search_books(self):
        search_text = self.search_entry.get()
        results = self.book_model.search_books_by_title(search_text)
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in results:
            self.tree.insert('', 'end', values=row)

    def request_issue(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a book to issue.")
            return
        book_id = self.tree.item(selected[0])['values'][0]

        success = self.issue_model.issue_book(self.user['id'], book_id)
        if success:
            messagebox.showinfo("Success", "Book issue requested.")
            self.refresh_issued_books()
        else:
            messagebox.showerror("Error", "Failed to issue book.")

    def refresh_issued_books(self):
        for item in self.issued_tree.get_children():
            self.issued_tree.delete(item)
        issued = self.issue_model.get_issued_books_by_user(self.user['id'])
        for row in issued:
            # id, title, author, issue_date, return_date
            issue_id = row[0]
            title = row[1]
            author = row[2]
            issue_date = row[3].strftime("%Y-%m-%d") if row[3] else ""
            return_date = row[4].strftime("%Y-%m-%d") if row[4] else ""
            self.issued_tree.insert('', 'end', values=(issue_id, title, author, issue_date, return_date))
