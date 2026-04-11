import tkinter as tk
from tkinter import messagebox
from Common.constants import PRIMARY_COLOR, TEXT_COLOR


class RegisterPage(tk.Frame):
    def __init__(self, parent, controller, on_success):
        super().__init__(parent)
        self.controller = controller
        self.on_success = on_success

        tk.Label(self, text="ĐĂNG KÝ", font=("Arial", 18, "bold"), fg=PRIMARY_COLOR).pack(pady=20)

        tk.Label(self, text="Tên đăng nhập:").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Mật khẩu:").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Label(self, text="Xác nhận mật khẩu:").pack()
        self.confirm_entry = tk.Entry(self, show="*")
        self.confirm_entry.pack()

        tk.Button(self, text="Đăng Ký", command=self.register, bg=PRIMARY_COLOR, fg=TEXT_COLOR).pack(pady=10)

        tk.Button(self, text="Quay lại Đăng Nhập", command=self.go_to_login).pack()

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm = self.confirm_entry.get()
        if not username or not password or not confirm:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin")
            return
        if password != confirm:
            messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp")
            return
        # Giả lập đăng ký thành công
        messagebox.showinfo("Thành công", "Đăng ký thành công! Vui lòng đăng nhập.")
        self.go_to_login()

    def go_to_login(self):
        self.master.master.show_login()
