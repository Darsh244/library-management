import tkinter as tk
from database import Database
from gui.login_window import LoginWindow
from gui.admin_dashboard import AdminDashboard
from gui.user_dashboard import UserDashboard

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Library Management System")
        self.geometry("800x600")
        self.db = Database()
        self.db.connect()
        self.user = None
        self.current_frame = None
        self.login_window = None
        self.show_login()

    def show_login(self):
        # Destroy any existing dashboard frame
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None

        # If login window is already open, don't open another
        if self.login_window and self.login_window.winfo_exists():
            return

        # Create LoginWindow (Toplevel popup), no packing needed
        self.login_window = LoginWindow(self, self.db, self.on_login_success)

    def on_login_success(self, user):
        self.user = user

        # Destroy login popup window after successful login
        if self.login_window and self.login_window.winfo_exists():
            self.login_window.destroy()
            self.login_window = None

        # Destroy old dashboard frame if any
        if self.current_frame:
            self.current_frame.destroy()

        # Create dashboard frame based on user role
        if user['role'] == 'admin':
            self.current_frame = AdminDashboard(self, self.db, user, self.logout)
        else:
            self.current_frame = UserDashboard(self, self.db, user, self.logout)

        self.current_frame.pack(fill="both", expand=True)

    def logout(self):
        self.user = None
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None
        self.show_login()

if __name__ == "__main__":
    app = App()
    app.mainloop()
