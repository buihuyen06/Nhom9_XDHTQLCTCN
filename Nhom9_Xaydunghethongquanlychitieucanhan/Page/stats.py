import tkinter as tk
from Common.constants import PRIMARY_COLOR


class StatsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="PHÂN TÍCH THU CHI", font=("Arial", 18, "bold"), fg=PRIMARY_COLOR).pack(pady=15)

        data = self.controller.get_list()
        total_chi = sum(item['price'] for item in data if item['type'] == "Chi")

        tk.Label(self, text=f"Tổng chi tiêu: {total_chi}đ", font=("Arial", 12)).pack(pady=10)

        # Mô phỏng biểu đồ
        canvas = tk.Canvas(self, width=200, height=100, bg="#E0E0E0")
        canvas.pack()
        # Hình tròn
        canvas.create_oval(50, 10, 150, 90, fill="#FF5722")