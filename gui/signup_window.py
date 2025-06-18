import tkinter as tk
from tkinter import messagebox
from models import UserModel

class SignupWindow(tk.Toplevel):
    def __init__(self, master, db):
        super().__init__(master)
        self.title("Signup")
        self.geometry("300x300")
        self.db = db
        self.user_model = UserModel(db)
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Label(self, text="Role:").pack(pady=5)
        self.role_var = tk.StringVar(value="user")
        tk.Radiobutton(self, text="User", variable=self.role_var, value="user").pack()
        tk.Radiobutton(self, text="Admin", variable=self.role_var, value="admin").pack()

        tk.Button(self, text="Create Account", command=self.create_account).pack(pady=10)

    def create_account(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_var.get()
        if username and password:
            success = self.user_model.create_user(username, password, role)
            if success:
                messagebox.showinfo("Success", "Account created! You can now login.")
                self.destroy()
            else:
                messagebox.showerror("Error", "Could not create account. Username might be taken.")
        else:
            messagebox.showerror("Error", "Please enter all fields.")
