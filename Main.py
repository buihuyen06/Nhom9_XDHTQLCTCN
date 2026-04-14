import tkinter as tk
from Models.model import SpendingModel
from Controllers.controller import SpendingController
from Views.login import LoginPage
from Views.home_page import HomePage
from Views.account_manager_page import AccountManagerPage
from Views.register_page import RegisterPage


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("QUẢN LÝ TÀI CHÍNH")
        self.geometry("450x650")

        self.model = SpendingModel()
        self.controller = SpendingController(self.model)

        self.nav = tk.Frame(self, bg="#333", height=50)
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1);
        self.container.grid_columnconfigure(0, weight=1)

        self.pages = {}
        # Init Pages
        self.pages["LoginPage"] = LoginPage(self.container, self.controller, self.login_ok,
                                            lambda: self.show("RegisterPage"))
        self.pages["RegisterPage"] = RegisterPage(self.container, self.controller, lambda: self.show("LoginPage"))
        self.pages["HomePage"] = HomePage(self.container, self.controller)
        self.pages["AccountManagerPage"] = AccountManagerPage(self.container, self.controller)

        for f in self.pages.values(): f.grid(row=0, column=0, sticky="nsew")
        self.show("LoginPage")

    def login_ok(self):
        self.nav.pack(side="bottom", fill="x")
        tk.Button(self.nav, text="📊 CHI TIÊU", bg="#81D4FA", command=lambda: self.show("HomePage")).pack(side="left",
                                                                                                         expand=True,
                                                                                                         fill="both")
        tk.Button(self.nav, text="👥 TÀI KHOẢN", bg="#A5D6A7", command=lambda: self.show("AccountManagerPage")).pack(
            side="left", expand=True, fill="both")
        self.show("HomePage")

    def show(self, name):
        f = self.pages[name]
        if hasattr(f, 'refresh'): f.refresh()
        f.tkraise()


if __name__ == "__main__":
    MainApp().mainloop()