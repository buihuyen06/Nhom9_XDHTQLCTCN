import tkinter as tk
from tkinter import messagebox

class View:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Quản lý chi tiêu cá nhân")
        self.root.geometry("600x400")

    def start_mainloop(self):
        self.root.mainloop()

    def show_message(self, msg):
        messagebox.showinfo("Thông báo", msg)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()