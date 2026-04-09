from model import AccountModel
from view import View
import tkinter as tk

class Controller:
    def __init__(self):
        self.model = AccountModel()
        self.view = View()
        self.current_user = None
        self.show_main_menu()

    def show_main_menu(self):
        self.view.clear_window()
        # Background pastel
        self.view.root.configure(bg="#FFF0F5")  # Lavender blush

        # Tiêu đề cute
        tk.Label(
            self.view.root,
            text=" QUẢN LÝ CHI TIÊU CÁ NHÂN ",
            font=("Kristen ITC", 22, "bold"),
            fg="#FF69B4",
            bg="#FFF0F5",
            pady=10
        ).pack()

        # Nhãn mô tả trước nút Tạo tài khoản
        tk.Label(
            self.view.root,
            text="Bạn chưa có tài khoản? Hãy tạo ngay:",
            font=("Chalkboard SE", 12),
            fg="#333",
            bg="#FFF0F5"
        ).pack(pady=(20,5))

        # Nút Tạo tài khoản
        tk.Button(
            self.view.root,
            text="✨ Tạo tài khoản ✨",
            width=25,
            bg="#FFB6C1",  # hồng nhạt
            fg="white",
            font=("Kristen ITC", 14, "bold"),
            command=self.show_create_account
        ).pack(pady=5)

        # Nhãn mô tả trước nút Đăng nhập
        tk.Label(
            self.view.root,
            text="Đã có tài khoản? Đăng nhập tại đây:",
            font=("Chalkboard SE", 12),
            fg="#333",
            bg="#FFF0F5"
        ).pack(pady=(20,5))

        # Nút Đăng nhập
        tk.Button(
            self.view.root,
            text="🌸 Đăng nhập 🌸",
            width=25,
            bg="#87CEFA",  # xanh pastel
            fg="white",
            font=("Kristen ITC", 14, "bold"),
            command=self.show_login
        ).pack(pady=5)

        # Nút Thoát
        tk.Button(
            self.view.root,
            text="❌ Thoát ❌",
            width=25,
            bg="#FF6F61",  # đỏ pastel
            fg="white",
            font=("Kristen ITC", 14, "bold"),
            command=self.view.root.quit
        ).pack(pady=(30,10))

    def show_create_account(self):
        self.view.clear_window()
        tk.Label(self.view.root, text="Tạo tài khoản", font=("Arial", 14)).pack(pady=10)
        username_entry = tk.Entry(self.view.root)
        username_entry.pack(pady=5)
        username_entry.insert(0, "Tên tài khoản")
        password_entry = tk.Entry(self.view.root, show="*")
        password_entry.pack(pady=5)
        password_entry.insert(0, "Mật khẩu")

        def create():
            username = username_entry.get()
            password = password_entry.get()
            if self.model.create_account(username, password):
                self.view.show_message("Tạo tài khoản thành công!")
                self.show_main_menu()
            else:
                self.view.show_message("Tên tài khoản đã tồn tại!")

        tk.Button(self.view.root, text="Tạo", command=create).pack(pady=5)
        tk.Button(self.view.root, text="Quay lại", command=self.show_main_menu).pack(pady=5)

    def show_login(self):
        self.view.clear_window()
        tk.Label(self.view.root, text="Đăng nhập", font=("Arial", 14)).pack(pady=10)
        username_entry = tk.Entry(self.view.root)
        username_entry.pack(pady=5)
        username_entry.insert(0, "Tên tài khoản")
        password_entry = tk.Entry(self.view.root, show="*")
        password_entry.pack(pady=5)
        password_entry.insert(0, "Mật khẩu")

        def login():
            username = username_entry.get()
            password = password_entry.get()
            if self.model.authenticate(username, password):
                self.current_user = username
                self.view.show_message("Đăng nhập thành công!")
                self.show_user_menu()
            else:
                self.view.show_message("Sai tên tài khoản hoặc mật khẩu!")

        tk.Button(self.view.root, text="Đăng nhập", command=login).pack(pady=5)
        tk.Button(self.view.root, text="Quay lại", command=self.show_main_menu).pack(pady=5)

    def show_user_menu(self):
        self.view.clear_window()
        tk.Label(self.view.root, text=f"Xin chào, {self.current_user}", font=("Arial", 14)).pack(pady=10)
        tk.Button(self.view.root, text="Xem số dư", width=20, command=self.show_balance).pack(pady=5)
        tk.Button(self.view.root, text="Thêm thu/chi", width=20, command=self.show_add_transaction).pack(pady=5)
        tk.Button(self.view.root, text="Xem lịch sử giao dịch", width=20, command=self.show_transactions).pack(pady=5)
        tk.Button(self.view.root, text="Đăng xuất", width=20, command=self.logout).pack(pady=5)

    def show_balance(self):
        balance = self.model.get_balance(self.current_user)
        self.view.show_message(f"Số dư hiện tại: {balance}")

    def show_add_transaction(self):
        self.view.clear_window()
        tk.Label(self.view.root, text="Thêm thu/chi", font=("Arial", 14)).pack(pady=10)
        amount_entry = tk.Entry(self.view.root)
        amount_entry.pack(pady=5)
        amount_entry.insert(0, "Nhập số tiền (+ thu / - chi)")
        note_entry = tk.Entry(self.view.root)
        note_entry.pack(pady=5)
        note_entry.insert(0, "Ghi chú")

        def add():
            try:
                amount = float(amount_entry.get())
                note = note_entry.get()
                self.model.add_transaction(self.current_user, amount, note)
                self.view.show_message("Giao dịch đã được thêm!")
                self.show_user_menu()
            except ValueError:
                self.view.show_message("Số tiền không hợp lệ!")

        tk.Button(self.view.root, text="Thêm", command=add).pack(pady=5)
        tk.Button(self.view.root, text="Quay lại", command=self.show_user_menu).pack(pady=5)

    def show_transactions(self):
        self.view.clear_window()
        tk.Label(self.view.root, text="Lịch sử giao dịch", font=("Arial", 14)).pack(pady=10)
        transactions = self.model.get_transactions(self.current_user)
        for t in transactions:
            tk.Label(self.view.root, text=f"{t['amount']}: {t['note']}").pack()
        tk.Button(self.view.root, text="Quay lại", command=self.show_user_menu).pack(pady=5)

    def logout(self):
        self.current_user = None
        self.show_main_menu()