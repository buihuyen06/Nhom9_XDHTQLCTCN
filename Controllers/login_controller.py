from tkinter import messagebox


class LoginController:
    def __init__(self, app):
        self.app = app  # Giữ tham chiếu tới MainApp để ra lệnh chuyển trang khi đăng nhập đúng

        # THÔNG TIN BẢO MẬT CỐ ĐỊNH
        self.SECURE_USER = "nhom9"
        self.SECURE_PASS = "123456"

    def check_login(self, username, password):
        """Xử lý logic kiểm tra tài khoản"""
        if username == self.SECURE_USER and password == self.SECURE_PASS:
            self.app.login_ok()  # Đúng mật khẩu -> Bảo MainApp mở khóa ứng dụng
        else:
            messagebox.showerror("Truy cập bị từ chối", "Sai tên đăng nhập hoặc mật khẩu bảo vệ!")