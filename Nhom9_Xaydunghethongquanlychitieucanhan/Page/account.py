import tkinter as tk
from tkinter import messagebox, simpledialog
from Common.constants import TEXT_COLOR


class AccountPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="THÔNG TIN CÁ NHÂN", font=("Arial", 18, "bold")).pack(pady=15)
        self.username_label = tk.Label(self, text="")
        self.username_label.pack()

        tk.Button(self, text="Làm Mới", command=self.refresh, bg="#4CAF50", fg=TEXT_COLOR).pack(pady=5)
        tk.Button(self, text="Sửa", command=self.edit, bg="#FF9800", fg=TEXT_COLOR).pack(pady=5)
        tk.Button(self, text="Xóa", command=self.delete, bg="#F44336", fg=TEXT_COLOR).pack(pady=5)
        tk.Button(self, text="Đăng Xuất", command=self.logout, bg="#9E9E9E", fg=TEXT_COLOR).pack(pady=5)

        tk.Button(self, text="Đổi ngôn ngữ", bg="#9E9E9E", fg=TEXT_COLOR).pack(pady=5)
        tk.Button(self, text="Xuất file CSV", bg="#607D8B", fg=TEXT_COLOR).pack(pady=5)

        self.refresh()

    def refresh(self):
        username = self.controller.model.user['username']
        self.username_label.config(text=f"Username: {username}")

    def edit(self):
        # Giả lập sửa username
        new_username = simpledialog.askstring("Sửa", "Nhập username mới:")
        if new_username:
            self.controller.model.user['username'] = new_username
            self.refresh()
            messagebox.showinfo("Thành công", "Đã cập nhật username")

    def delete(self):
        confirm = messagebox.askyesno("Xóa tài khoản", "Bạn có chắc muốn xóa tài khoản?")
        if confirm:
            # Giả lập xóa
            messagebox.showinfo("Thành công", "Tài khoản đã được xóa")
            self.logout()

    def logout(self):
        # Quay về trang login
        self.master.master.show_login()
