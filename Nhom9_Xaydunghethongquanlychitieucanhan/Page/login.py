import tkinter as tk
from tkinter import messagebox
from Common.button import CustomButton


class LoginPage(tk.Frame):
    def __init__(self, parent, controller, on_success):
        super().__init__(parent)
        self.controller = controller
        self.on_success = on_success

        tk.Label(self, text="ĐĂNG NHẬP", font=("Arial", 18, "bold")).pack(pady=20)

        tk.Label(self, text="Tên đăng nhập:").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Mật khẩu:").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Button(self, text="Đăng Nhập", command=self.login).pack(pady=10)

        tk.Button(self, text="Đăng Ký", command=self.go_to_register).pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Giả lập kiểm tra đăng nhập
        if username == "admin" and password == "123":
            messagebox.showinfo("Thành công", "Đăng nhập thành công!")
            self.on_success()
        else:
            messagebox.showerror("Lỗi", "Sai tên đăng nhập hoặc mật khẩu")

    def go_to_register(self):
        # Chuyển sang trang đăng ký
        self.master.master.show_register()
