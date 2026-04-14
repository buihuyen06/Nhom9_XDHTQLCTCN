import tkinter as tk
from tkinter import messagebox


class RegisterPage(tk.Frame):
    def __init__(self, parent, controller, go_log):
        super().__init__(parent, bg="#F5F5F5")
        self.ctrl = controller

        tk.Label(self, text="ĐĂNG KÝ", font=("Arial", 22, "bold"), fg="#4CAF50", bg="#F5F5F5").pack(pady=50)

        tk.Label(self, text="Tên đăng nhập mới:", bg="#F5F5F5").pack()
        self.u_ent = tk.Entry(self, width=30);
        self.u_ent.pack(pady=5)

        tk.Label(self, text="Mật khẩu mới:", bg="#F5F5F5").pack()
        self.p_ent = tk.Entry(self, width=30, show="*");
        self.p_ent.pack(pady=5)

        def do_reg():
            if self.ctrl.register(self.u_ent.get(), self.p_ent.get()):
                messagebox.showinfo("Xong", "Đăng ký thành công!");
                go_log()
            else:
                messagebox.showerror("Lỗi", "Tài khoản đã tồn tại!")

        tk.Button(self, text="XÁC NHẬN ĐĂNG KÝ", bg="#4CAF50", fg="white", width=20, command=do_reg).pack(pady=20)
        tk.Button(self, text="Quay lại Đăng nhập", fg="gray", relief="flat", bg="#F5F5F5", command=go_log).pack()