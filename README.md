# Library Management System

A simple desktop Library Management System built with Python (Tkinter) and MySQL.  
Features role-based login for Admin and User, book management, issue tracking, and a GUI interface.

---

## Features

- User authentication with roles (Admin, User)  
- Admin dashboard to add, delete, and issue books  
- User dashboard to search books and request book issues  
- Secure password storage (hashed)  
- Persistent data storage using MySQL  

---

## Installation & Setup

1. **Clone the repository**  
   ```bash
   git clone https://github.com/yourusername/library-management.git
   cd library-management

2. **Set up the Python environment**
   Ensure Python 3.7+ is installed. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
  source venv/bin/activate  # macOS/Linux
  venv\Scripts\activate     # Windows

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt

4. **Setup MYSQL database**
- Download and install MySQL Community Server from the official website:
https://dev.mysql.com/downloads/mysql/
- Install and start MySQL server on your machine.
- The app will automatically create the required database and tables on first run.

5. **Run the application**
   ```bash
   python3 main.py

---

## Usage
- Launch the app and login as Admin or User.
- Admin can manage books and issue them to users.
- Users can search books and request book issues.
- Use the Signup option on the login screen to create new users.


## License
This project is licensed under the MIT license.


Developed by Darsh Mishra.


