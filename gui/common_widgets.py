import tkinter as tk
from tkinter import ttk

def styled_label(master, text):
    return ttk.Label(master, text=text, font=("Arial", 12))

def styled_button(master, text, command):
    return ttk.Button(master, text=text, command=command)

def centered_window(window, width=400, height=300):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width/2) - (width/2))
    y = int((screen_height/2) - (height/2))
    window.geometry(f"{width}x{height}+{x}+{y}")
