import tkinter as tk
from tkinter import messagebox

from Common.button import CustomButton
from Common.constants import PRIMARY_COLOR, TEXT_COLOR


# Create main window


class TaoTKPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.config()
        self.view()

    def config(self):
        self.master.title("Tạo tài khoản")
        self.master.geometry("300x200")

    def view(self):
        # Add a label
        label = tk.Label(self.master, text="Tạo tài khoản", font=("Arial", 20 , "bold"))
        label.pack(pady=10)
        lib_user = tk.Label(self.master, text="Username:")
        lib_user.place(x=20, y=60)

        lib_pass = tk.Label(self.master, text="Password:")
        lib_pass.place(x=20, y=100)

        self.entry_username = tk.Entry(self.master)
        self.entry_username.place(x=90, y=60)

        self.entry_password = tk.Entry(self.master, show="*")
        self.entry_password.place(x=90, y=100)

        btn = CustomButton(self.master, text="Tạo tài khoản", command=self.tao_tk, style_type="primary")
        btn.place(x=40, y=140)

        btn = CustomButton(self.master, text="Quay lại Đăng nhập", command=self.back_login, style_type="success")
        btn.place(x=160, y=140)

    def back_login(self):
        print("Quay lại trang đăng nhập")
        self.app_manager.show_login()

    def tao_tk(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username.strip() == "" or password.strip() == "":
            messagebox.showerror("Thông báo", "Vui lòng nhập đầy đủ thông tin")
            return

        open("database/tk.csv", "a").write(username + "," + password + "\n")
        messagebox.showinfo("Thông báo", "Tạo tài khoản thành công")
        self.app_manager.show_login_page()