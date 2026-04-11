import tkinter as tk
from Common.constants import PRIMARY_COLOR, TEXT_COLOR


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Tiêu đề
        tk.Label(self, text="TỔNG QUAN", font=("Arial", 18, "bold"), fg=PRIMARY_COLOR).pack(pady=10)

        # Hiển thị số dư hiện tại
        self.balance_label = tk.Label(self, text="", font=("Arial", 14))
        self.balance_label.pack(pady=5)

        # Tổng thu
        self.total_thu_label = tk.Label(self, text="", font=("Arial", 14))
        self.total_thu_label.pack(pady=5)

        # Tổng chi
        self.total_chi_label = tk.Label(self, text="", font=("Arial", 14))
        self.total_chi_label.pack(pady=5)

        # Lịch sử chi tiêu
        tk.Label(self, text="LỊCH SỬ CHI TIÊU", font=("Arial", 16, "bold"), fg=PRIMARY_COLOR).pack(pady=10)

        # Bảng hiển thị (Dùng Listbox cho đơn giản)
        self.listbox = tk.Listbox(self, width=50, height=10)
        self.listbox.pack(pady=10)

        # Nút làm mới
        tk.Button(self, text="Làm Mới", command=self.load_data, bg="#4CAF50", fg=TEXT_COLOR).pack(pady=5)
        self.load_data()  # Load dữ liệu ban đầu

    def load_data(self):
        data = self.controller.get_list()
        total_chi = sum(item['price'] for item in data if item['type'] == "Chi")
        total_thu = sum(item['price'] for item in data if item['type'] == "Thu")
        balance = self.controller.model.user['balance'] + total_thu - total_chi

        self.balance_label.config(text=f"Số dư hiện tại: {balance}đ")
        self.total_thu_label.config(text=f"Tổng thu: {total_thu}đ")
        self.total_chi_label.config(text=f"Tổng chi: {total_chi}đ")

        self.listbox.delete(0, tk.END)  # Xóa dữ liệu cũ
        for item in data:
            display_text = f" {item['type']} | {item['name']} | {item['price']}đ"
            color = "red" if item['type'] == "Chi" else "green"
            self.listbox.insert(tk.END, display_text)
            self.listbox.itemconfig(tk.END, {'fg': color})