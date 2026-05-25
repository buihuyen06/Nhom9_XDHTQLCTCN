import tkinter as tk
from tkinter import messagebox, ttk


class LoginPage(tk.Frame):
    def __init__(self, parent, controller, on_user_login, on_admin_login, go_reg):
        super().__init__(parent, bg="#F5F5F5")
        self.ctrl = controller
        self.on_user_login = on_user_login
        self.on_admin_login = on_admin_login

        tk.Label(self, text="ĐĂNG NHẬP", font=("Arial", 22, "bold"), fg="#2196F3", bg="#F5F5F5").pack(pady=50)

        # --- MENU CHỌN LOẠI TÀI KHOẢN ---
        tk.Label(self, text="Loại tài khoản:", bg="#F5F5F5").pack()
        self.role_cb = ttk.Combobox(self, width=27, state="readonly")
        self.role_cb["values"] = ("Người dùng", "Quản trị hệ thống")
        self.role_cb.current(0)  # Chọn sẵn dòng đầu tiên (Người dùng)
        self.role_cb.pack(pady=5)

        tk.Label(self, text="Tên đăng nhập:", bg="#F5F5F5").pack()
        self.u_ent = tk.Entry(self, width=30)
        self.u_ent.pack(pady=5)

        tk.Label(self, text="Mật khẩu:", bg="#F5F5F5").pack()
        self.p_ent = tk.Entry(self, width=30, show="*")
        self.p_ent.pack(pady=5)

        tk.Button(self, text="ĐĂNG NHẬP", bg="#2196F3", fg="white", width=20,
                  command=self.handle_login).pack(pady=20)

        tk.Button(self, text="Chưa có tài khoản? Đăng ký", fg="blue", relief="flat", bg="#F5F5F5",
                  command=go_reg).pack()

    def handle_login(self):
        username = self.u_ent.get()
        password = self.p_ent.get()
        role = self.role_cb.get()

        if self.ctrl.check_login(username, password, role):
            if role == "Quản trị hệ thống":
                self.on_admin_login()
            else:
                self.on_user_login()
        else:
            messagebox.showerror("Lỗi", "Sai thông tin đăng nhập hoặc loại tài khoản!")