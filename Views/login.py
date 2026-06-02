import tkinter as tk


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F5F5F5")
        self.controller = controller

        # Giao diện màn hình khóa bảo mật (Đẩy khoảng cách rộng rãi)
        tk.Label(self, text="QUẢN LÝ CHI TIÊU CÁ NHÂN", font=("Arial", 26, "bold"), fg="#2c3e50", bg="#F5F5F5").pack(
            pady=(140, 10)) # Font 20 -> 26, pady (80, 5) -> (140, 10)
        tk.Label(self, text="Vui lòng xác thực quyền truy cập để xem dữ liệu chi tiêu", font=("Arial", 14, "italic"),
                 fg="#7f8c8d", bg="#F5F5F5").pack(pady=(0, 50)) # Font 11 -> 14

        tk.Label(self, text="Tên đăng nhập:", font=("Arial", 13), bg="#F5F5F5").pack(pady=(5, 4))
        self.u_ent = tk.Entry(self, width=35, font=("Arial", 14)) # Rộng 30 font 11 -> rộng 35 font 14
        self.u_ent.pack(pady=8)

        tk.Label(self, text="Mật khẩu bảo vệ:", font=("Arial", 13), bg="#F5F5F5").pack(pady=(15, 4))
        self.p_ent = tk.Entry(self, width=35, font=("Arial", 14), show="*") # Rộng 30 font 11 -> rộng 35 font 14
        self.p_ent.pack(pady=8)

        tk.Button(self, text="MỞ KHÓA 🔓", bg="#2196F3", fg="white", font=("Arial", 14, "bold"), width=22, height=2,
                  command=self.handle_login).pack(pady=40) # Font 11 -> 14, rộng 18 -> 22

    def handle_login(self):
        username = self.u_ent.get().strip()
        password = self.p_ent.get().strip()

        self.controller.check_login(username, password)

        self.u_ent.delete(0, tk.END)
        self.p_ent.delete(0, tk.END)