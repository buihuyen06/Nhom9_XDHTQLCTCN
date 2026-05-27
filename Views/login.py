import tkinter as tk


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F5F5F5")
        self.controller = controller  # Chính là LoginController

        # Giao diện màn hình khóa bảo mật
        tk.Label(self, text="QUẢN LÝ TÀI CHÍNH CÁ NHÂN", font=("Arial", 20, "bold"), fg="#2c3e50", bg="#F5F5F5").pack(
            pady=(80, 5))
        tk.Label(self, text="Vui lòng xác thực quyền truy cập để xem dữ liệu chi tiêu", font=("Arial", 11, "italic"),
                 fg="#7f8c8d", bg="#F5F5F5").pack(pady=(0, 40))

        tk.Label(self, text="Tên đăng nhập:", font=("Arial", 11), bg="#F5F5F5").pack(pady=(5, 2))
        self.u_ent = tk.Entry(self, width=30, font=("Arial", 11))
        self.u_ent.pack(pady=5)

        tk.Label(self, text="Mật khẩu bảo vệ:", font=("Arial", 11), bg="#F5F5F5").pack(pady=(10, 2))
        self.p_ent = tk.Entry(self, width=30, font=("Arial", 11), show="*")
        self.p_ent.pack(pady=5)

        tk.Button(self, text="MỞ KHÓA 🔓", bg="#2196F3", fg="white", font=("Arial", 11, "bold"), width=18, height=2,
                  command=self.handle_login).pack(pady=30)

    def handle_login(self):
        username = self.u_ent.get().strip()
        password = self.p_ent.get().strip()

        # Ủy quyền xử lý logic cho LoginController
        self.controller.check_login(username, password)

        # Xóa trắng form để đảm bảo an toàn bảo mật
        self.u_ent.delete(0, tk.END)
        self.p_ent.delete(0, tk.END)