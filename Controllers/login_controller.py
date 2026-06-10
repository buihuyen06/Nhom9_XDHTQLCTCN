from tkinter import messagebox


class LoginController:
    def __init__(self, app):
        self.app = app

        self.SECURE_USER = "nhom9"
        self.SECURE_PASS = "123456"

    def check_login(self, username, password):
        if username == self.SECURE_USER and password == self.SECURE_PASS:
            self.app.login_ok()
        else:
            messagebox.showerror("Truy cập bị từ chối", "Sai tên đăng nhập hoặc mật khẩu bảo vệ!")