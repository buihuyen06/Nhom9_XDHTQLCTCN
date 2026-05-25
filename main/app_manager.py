import tkinter as tk
from Controllers.controller import SpendingController
from Views.login import LoginPage
from Views.home_page import HomePage
from Views.register_page import RegisterPage
from Views.Inputpage import InputPage
from Views.Historypage import HistoryPage
from Views.Analysispage import AnalysisPage
from Views.Admin_page import AdminPage


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("QUẢN LÝ TÀI CHÍNH")
        self.geometry("500x520")
        self.controller = SpendingController()
        # Thanh điều hướng (Navigation Bar)
        self.nav = tk.Frame(self, bg="#333", height=50)

        # Container chứa các trang
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.pages = {}
        self._init_frames()
        self.show("LoginPage")

    def _init_frames(self):
        """Khởi tạo tất cả các View và đưa vào stack grid"""
        self.page = LoginPage(
            parent=self.container,
            controller=self.controller,
            on_user_login=self.login_ok,  # Gọi hàm xử lý đăng nhập cho user bình thường
            on_admin_login=lambda: self.show("AdminPage"),
            go_reg=lambda: self.show("RegisterPage")
        )

        self.pages["LoginPage"] = self.page
        self.pages["RegisterPage"] = RegisterPage(
            self.container, self.controller, lambda: self.show("LoginPage"))
        self.pages["HomePage"] = HomePage(self.container, self)
        self.pages["InputPage"] = InputPage(self.container, self)
        self.pages["HistoryPage"] = HistoryPage(self.container, self)
        self.pages["AnalysisPage"] = AnalysisPage(self.container, self)
        # --- SỬA LẠI ĐOẠN KHỞI TẠO ADMINPAGE TRONG MAINAPP ---
        self.pages["AdminPage"] = AdminPage(
            parent=self.container,
            controller=self,  # Truyền chính MainApp vào làm controller điều hướng
            go_login=lambda: self.logout()  # Dùng lambda để gọi chính xác hàm logout của MainApp
        )
        for f in self.pages.values():
            f.grid(row=0, column=0, sticky="nsew")

    def login_ok(self):
        """Xử lý sau khi đăng nhập thành công: Hiện menu điều hướng"""
        # Tránh việc tạo lại nút nhiều lần nếu login/logout
        for widget in self.nav.winfo_children():
            widget.destroy()

        self.nav.pack(side="bottom", fill="x")

        tk.Button(self.nav, text="📊 TRANG CHỦ", bg="#81D4FA",
                  command=lambda: self.show("HomePage")).pack(side="left", expand=True, fill="both")

        tk.Button(self.nav, text="🚪 ĐĂNG XUẤT", bg="#A5D6A7",
                  command=lambda: self.show("LoginPage")).pack(side="left", expand=True, fill="both")

        self.show("HomePage")

    def logout(self):
        """Hàm xử lý quy trình đăng xuất sạch sẽ"""
        self.nav.pack_forget()  # Ẩn thanh menu điều hướng đi
        self.show("LoginPage")  # Hiển thị lại trang Đăng nhập
    def show(self, name):
        """Hiển thị trang dựa trên tên định nghĩa trong self.pages"""
        f = self.pages[name]
        if hasattr(f, 'refresh'):
            f.refresh()
        f.tkraise()

