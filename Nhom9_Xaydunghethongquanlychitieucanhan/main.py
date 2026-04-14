import tkinter as tk
from MVC.Controller import SpendingController
from Common.constants import APP_NAME
from Page.login import LoginPage
from Page.register import RegisterPage
from Page.home import HomePage
from Page.add import AddPage
from Page.stats import StatsPage
from Page.account import AccountPage

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("400x500")  # Kích thước cửa sổ

        self.ctrl = SpendingController()

        # Nơi chứa các trang
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # Nơi chứa menu điều hướng
        self.menu_frame = tk.Frame(self, bg="#E0E0E0")

        self.pages = {}
        self.init_pages()

        # Bắt đầu với trang Login
        self.show_page(LoginPage)

    def init_pages(self):
        # Khởi tạo các trang và lưu vào dict
        for PageClass in (HomePage, AddPage, StatsPage, AccountPage):
            page_name = PageClass.__name__
            frame = PageClass(self.container, self.ctrl)
            self.pages[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")  # Xếp chồng lên nhau

    def show_page(self, page_class_or_obj):
        # Ẩn menu nếu là trang Login hoặc Register
        if page_class_or_obj == LoginPage:
            # Khởi tạo login page riêng
            login_frame = LoginPage(self.container, self.ctrl, self.on_login_success)
            login_frame.grid(row=0, column=0, sticky="nsew")
            login_frame.tkraise()  # Đưa lên trên cùng
            return
        elif page_class_or_obj == RegisterPage:
            # Khởi tạo register page riêng
            register_frame = RegisterPage(self.container, self.ctrl, self.on_login_success)
            register_frame.grid(row=0, column=0, sticky="nsew")
            register_frame.tkraise()  # Đưa lên trên cùng
            return

        # Hiển thị trang bình thường
        page_name = page_class_or_obj.__name__
        frame = self.pages[page_name]
        frame.tkraise()

    def on_login_success(self):
        # Đăng nhập xong thì hiện menu và hiện trang chủ
        self.show_page(HomePage)
        self.show_menu()

    def show_menu(self):
        self.menu_frame.pack(fill="x", side="bottom")  # Hiện menu ở dưới
        tk.Button(self.menu_frame, text="Trang Chủ", command=lambda: self.show_page(HomePage)).pack(side="left")
        tk.Button(self.menu_frame, text="Thêm Mới", command=lambda: self.show_page(AddPage)).pack(side="left")
        tk.Button(self.menu_frame, text="Thống Kê", command=lambda: self.show_page(StatsPage)).pack(side="left")
        tk.Button(self.menu_frame, text="Cá Nhân", command=lambda: self.show_page(AccountPage)).pack(side="left")

    def show_login(self):
        self.show_page(LoginPage)

    def show_register(self):
        self.show_page(RegisterPage)


if __name__ == "__main__":
    app = App()
    app.mainloop()