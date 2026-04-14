import tkinter as tk
from tkinter import messagebox


class LoginPage(tk.Frame):
    def __init__(self, parent, controller, on_login, go_reg):
        super().__init__(parent, bg="#F5F5F5")
        self.ctrl = controller

        tk.Label(self, text="ĐĂNG NHẬP", font=("Arial", 22, "bold"), fg="#2196F3", bg="#F5F5F5").pack(pady=50)

        tk.Label(self, text="Tên đăng nhập:", bg="#F5F5F5").pack()
        self.u_ent = tk.Entry(self, width=30);
        self.u_ent.pack(pady=5)

        tk.Label(self, text="Mật khẩu:", bg="#F5F5F5").pack()
        self.p_ent = tk.Entry(self, width=30, show="*");
        self.p_ent.pack(pady=5)

        tk.Button(self, text="ĐĂNG NHẬP", bg="#2196F3", fg="white", width=20,
                  command=lambda: on_login() if self.ctrl.check_login(self.u_ent.get(), self.p_ent.get())
                  else messagebox.showerror("Lỗi", "Sai thông tin!")).pack(pady=20)

        tk.Button(self, text="Chưa có tài khoản? Đăng ký", fg="blue", relief="flat", bg="#F5F5F5",
                  command=go_reg).pack()