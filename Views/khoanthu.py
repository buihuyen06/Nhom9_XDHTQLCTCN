import tkinter as tk
from tkinter import ttk
from datetime import datetime


class Thu_Page(tk.Frame):
    def __init__(self, parent, controller):
        # Thiết lập nền chính của toàn trang
        super().__init__(parent, bg="#FDEFF2")
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        bg_pastel = "#FDEFF2"
        fg_dark = "#5A2B36"

        # 1. TIÊU ĐỀ TRANG
        tk.Label(self, text="💰 QUẢN LÝ CÁC KHOẢN THU NHẬP", font=("Arial", 24, "bold"),
                 fg=fg_dark, bg=bg_pastel).pack(pady=20)

        # 2. THANH CÔNG CỤ (Các nút chức năng)
        toolbar = tk.Frame(self, bg=bg_pastel)
        toolbar.pack(pady=10, fill="x", padx=20)

        tk.Button(toolbar, text="➕ THÊM MỚI", bg="#2ecc71", fg="white", font=("Arial", 11, "bold"), width=15,
                  command=self.controller.show_add_dialog).pack(side="left", padx=6)
        tk.Button(toolbar, text="🔧 CHỈNH SỬA", bg="#3498db", fg="white", font=("Arial", 11, "bold"), width=15,
                  command=self.controller.show_edit_dialog).pack(side="left", padx=6)
        tk.Button(toolbar, text="❌ XÓA BẢN GHI", bg="#e74c3c", fg="white", font=("Arial", 11, "bold"), width=15,
                  command=self.controller.delete_record).pack(side="left", padx=6)
        tk.Button(toolbar, text="🔍 TÌM KIẾM", bg="#f1c40f", fg="black", font=("Arial", 11, "bold"), width=15,
                  command=self.controller.show_search_dialog).pack(side="left", padx=6)
        tk.Button(toolbar, text="🔄 TẢI LẠI", bg="#95a5a6", fg="white", font=("Arial", 11, "bold"), width=15,
                  command=self.controller.load_data).pack(side="left", padx=6)

        # 3. THANH BỘ LỌC THÁNG/NĂM
        filter_frame = tk.Frame(self, bg=bg_pastel)
        filter_frame.pack(pady=15, fill="x", padx=20)

        tk.Label(filter_frame, text="Chọn Tháng:", font=("Arial", 12), fg=fg_dark, bg=bg_pastel).pack(side="left")
        self.combo_m = ttk.Combobox(filter_frame, values=list(range(1, 13)), width=6)
        self.combo_m.set(datetime.now().month)
        self.combo_m.pack(side="left", padx=8)

        tk.Label(filter_frame, text="Năm:", font=("Arial", 12), fg=fg_dark, bg=bg_pastel).pack(side="left")
        self.combo_y = ttk.Combobox(filter_frame, values=[2025, 2026, 2027], width=8)
        self.combo_y.set(2026)
        self.combo_y.pack(side="left", padx=8)

        tk.Button(filter_frame, text="LỌC THÁNG", font=("Arial", 11, "bold"), bg="#FFF0F2", fg=fg_dark, bd=1,
                  command=lambda: self.controller.filter_by_month(self.combo_m.get(), self.combo_y.get())).pack(
            side="left", padx=15)

        # 4. KHU VỰC HIỂN THỊ TỔNG TIỀN THU NHẬP
        totals_frame = tk.Frame(filter_frame, bg=bg_pastel)
        totals_frame.pack(side="right", padx=20)

        self.lbl_total = tk.Label(totals_frame, text="TỔNG THU: 0 VND", font=("Arial", 16, "bold"),
                                  fg=fg_dark, bg=bg_pastel)
        self.lbl_total.pack(side="top", anchor="e", pady=2)

        self.lbl_bank = tk.Label(totals_frame, text="🏦 Ngân hàng: 0 đ", font=("Arial", 13, "bold"),
                                 fg="#1A5276", bg=bg_pastel) # Màu xanh sẫm đọc rõ trên nền hồng
        self.lbl_bank.pack(side="top", anchor="e", pady=2)

        self.lbl_cash = tk.Label(totals_frame, text="💵 Tiền mặt: 0 đ", font=("Arial", 13, "bold"),
                                 fg="#196F3D", bg=bg_pastel) # Màu xanh lá sẫm
        self.lbl_cash.pack(side="top", anchor="e", pady=2)

        # 5. BẢNG DỮ LIỆU TỔNG HỢP (Kế thừa kích thước chữ lớn từ app_manager)
        table_frame = tk.Frame(self)
        table_frame.pack(pady=10, fill="both", expand=True, padx=20)

        columns = ("id", "ngay", "nguonthu", "sotien", "phuongthuc", "ghichu")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        self.tree.heading("id", text="ID")
        self.tree.heading("ngay", text="Ngày Nhận")
        self.tree.heading("nguonthu", text="Nguồn Tiền Nhận")
        self.tree.heading("sotien", text="Số Tiền (VND)")
        self.tree.heading("phuongthuc", text="Phương Thức")
        self.tree.heading("ghichu", text="Ghi Chú")

        # Độ rộng cột thoải mái cho màn hình 1800x800
        self.tree.column("id", width=50, anchor=tk.CENTER)
        self.tree.column("ngay", width=140, anchor=tk.CENTER)
        self.tree.column("nguonthu", width=300, anchor=tk.W)
        self.tree.column("sotien", width=180, anchor=tk.E)
        self.tree.column("phuongthuc", width=140, anchor=tk.CENTER)
        self.tree.column("ghichu", width=300, anchor=tk.W)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def refresh(self):
        self.controller.load_data()