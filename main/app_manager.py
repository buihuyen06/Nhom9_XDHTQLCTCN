import tkinter as tk
from Models.model import SpendingModel
from Controllers.controller import SpendingController
from Views.login import LoginPage
from Views.home_page import HomePage
from Views.account_manager_page import AccountManagerPage
from Views.register_page import RegisterPage
from Views.Inputpage import InputPage
from Views.Historypage import HistoryPage
from Views.Analysispage import AnalysisPage


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("QUẢN LÝ TÀI CHÍNH")
        self.geometry("450x650")

        # Khởi tạo MVC
        self.model = SpendingModel()
        self.controller = SpendingController(self.model)

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
        self.pages["LoginPage"] = LoginPage(
            self.container, self.controller, self.login_ok, lambda: self.show("RegisterPage")
        )
        self.pages["RegisterPage"] = RegisterPage(
            self.container, self.controller, lambda: self.show("LoginPage")
        )
        self.pages["HomePage"] = HomePage(self.container, self)
        self.pages["AccountManagerPage"] = AccountManagerPage(self.container, self)
        self.pages["InputPage"] = InputPage(self.container, self)
        self.pages["HistoryPage"] = HistoryPage(self.container, self)
        self.pages["AnalysisPage"] = AnalysisPage(self.container, self)

        for f in self.pages.values():
            f.grid(row=0, column=0, sticky="nsew")

    def login_ok(self):
        """Xử lý sau khi đăng nhập thành công: Hiện menu điều hướng"""
        # Tránh việc tạo lại nút nhiều lần nếu login/logout
        for widget in self.nav.winfo_children():
            widget.destroy()

        self.nav.pack(side="bottom", fill="x")

        tk.Button(self.nav, text="📊 CHI TIÊU", bg="#81D4FA",
                  command=lambda: self.show("HomePage")).pack(side="left", expand=True, fill="both")

        tk.Button(self.nav, text="👥 TÀI KHOẢN", bg="#A5D6A7",
                  command=lambda: self.show("AccountManagerPage")).pack(side="left", expand=True, fill="both")

        self.show("HomePage")

    def show(self, name):
        """Hiển thị trang dựa trên tên định nghĩa trong self.pages"""
        f = self.pages[name]
        if hasattr(f, 'refresh'):
            f.refresh()
        f.tkraise()