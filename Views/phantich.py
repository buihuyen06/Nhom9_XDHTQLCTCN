import tkinter as tk
from tkinter import ttk
from datetime import datetime

class PhanTich_Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f2f5")
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        # 1. TIÊU ĐỀ
        tk.Label(self, text="📊 PHÂN TÍCH TÀI CHÍNH", font=("Arial", 18, "bold"),
                 fg="#2c3e50", bg="#f0f2f5").pack(pady=15)

        # 1.5. THANH BỘ LỌC THEO THÁNG / NĂM (MỚI THÊM)
        filter_frame = tk.Frame(self, bg="#f0f2f5")
        filter_frame.pack(pady=10)

        # Ô chọn Tháng
        tk.Label(filter_frame, text="Tháng:", font=("Arial", 11), bg="#f0f2f5").pack(side="left", padx=5)
        months = ["Tất cả"] + [f"{i:02d}" for i in range(1, 13)]
        self.combo_month = ttk.Combobox(filter_frame, values=months, width=10, state="readonly")
        self.combo_month.set("Tất cả")  # Mặc định ban đầu xem tất cả các tháng
        self.combo_month.pack(side="left", padx=5)

        # Ô chọn Năm
        tk.Label(filter_frame, text="Năm:", font=("Arial", 11), bg="#f0f2f5").pack(side="left", padx=5)
        current_year = datetime.now().year
        years = ["Tất cả"] + [str(y) for y in range(current_year - 2, current_year + 3)]
        self.combo_year = ttk.Combobox(filter_frame, values=years, width=10, state="readonly")
        self.combo_year.set("Tất cả")  # Mặc định ban đầu xem tất cả các năm
        self.combo_year.pack(side="left", padx=5)

        # Nút bấm áp dụng bộ lọc
        btn_filter = tk.Button(filter_frame, text="🔍 Lọc Số Liệu", bg="#3498db", fg="white",
                               font=("Arial", 10, "bold"), padx=10, bd=0, cursor="hand2",
                               command=self.controller.load_data_and_draw_chart)
        btn_filter.pack(side="left", padx=15)

        # 2. KHUNG TỔNG QUAN HIỂN THỊ SỐ DƯ
        self.summary_frame = tk.Frame(self, bg="#f0f2f5")
        self.summary_frame.pack(pady=10)

        self.lbl_thu = tk.Label(self.summary_frame, text="Tổng Thu: 0", font=("Arial", 14, "bold"), fg="#27ae60", bg="#f0f2f5")
        self.lbl_thu.pack(side="left", padx=30)

        self.lbl_chi = tk.Label(self.summary_frame, text="Tổng Chi: 0", font=("Arial", 14, "bold"), fg="#e74c3c", bg="#f0f2f5")
        self.lbl_chi.pack(side="left", padx=30)

        self.lbl_du = tk.Label(self.summary_frame, text="Số Dư: 0", font=("Arial", 14, "bold"), fg="#2980b9", bg="#f0f2f5")
        self.lbl_du.pack(side="left", padx=30)

        # 3. KHUNG CHỨA BIỂU ĐỒ MATPLOTLIB
        self.chart_frame = tk.Frame(self, bg="white", bd=2, relief="groove")
        self.chart_frame.pack(pady=20, fill="both", expand=True, padx=50)