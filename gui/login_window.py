import tkinter as tk
from tkinter import messagebox
from models import UserModel
from gui.signup_window import SignupWindow

class LoginWindow(tk.Toplevel):
    def __init__(self, master, db, on_login_success):
        super().__init__(master)
        self.title("Login")
        self.geometry("300x250")
        self.db = db
        self.user_model = UserModel(db)
        self.on_login_success = on_login_success
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Button(self, text="Login", command=self.login).pack(pady=10)
        tk.Button(self, text="Signup", command=self.signup).pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = self.user_model.authenticate(username, password)
        if user:
            messagebox.showinfo("Success", f"Welcome {user['username']}!")
            self.on_login_success(user)
            self.destroy()
        else:
            messagebox.showerror("Failed", "Invalid username or password")

    def signup(self):
        self.grab_release()           
        signup_win = SignupWindow(self.master, self.db)  
        signup_win.grab_set()         
        signup_win.wait_window()      
        self.grab_set()              
