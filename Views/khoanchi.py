import tkinter as tk
from tkinter import ttk
from datetime import datetime


class Chi_Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f2f5")
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        # 1. TIÊU ĐỀ
        tk.Label(self, text="💰 QUẢN LÝ CÁC KHOẢN CHI", font=("Arial", 18, "bold"),
                 fg="#2c3e50", bg="#f0f2f5").pack(pady=15)

        # 2. THANH CÔNG CỤ (Nút chức năng)
        toolbar = tk.Frame(self, bg="#f0f2f5")
        toolbar.pack(pady=5, fill="x", padx=20)

        tk.Button(toolbar, text="➕ THÊM MỚI", bg="#2ecc71", fg="white", font=("Arial", 9, "bold"), width=12,
                  command=self.controller.show_add_dialog).pack(side="left", padx=4)
        tk.Button(toolbar, text="🔧 CHỈNH SỬA", bg="#3498db", fg="white", font=("Arial", 9, "bold"), width=12,
                  command=self.controller.show_edit_dialog).pack(side="left", padx=4)
        tk.Button(toolbar, text="❌ XÓA BẢN GHI", bg="#e74c3c", fg="white", font=("Arial", 9, "bold"), width=12,
                  command=self.controller.delete_record).pack(side="left", padx=4)
        tk.Button(toolbar, text="🔍 TÌM KIẾM", bg="#f1c40f", fg="black", font=("Arial", 9, "bold"), width=12,
                  command=self.controller.show_search_dialog).pack(side="left", padx=4)
        tk.Button(toolbar, text="🔄 TẢI LẠI", bg="#95a5a6", fg="white", font=("Arial", 9, "bold"), width=12,
                  command=self.controller.load_data).pack(side="left", padx=4)

        # 3. THANH LỌC THÁNG/NĂM
        filter_frame = tk.Frame(self, bg="#f0f2f5")
        filter_frame.pack(pady=10, fill="x", padx=20)

        tk.Label(filter_frame, text="Chọn Tháng:", bg="#f0f2f5").pack(side="left")
        self.combo_m = ttk.Combobox(filter_frame, values=list(range(1, 13)), width=5)
        self.combo_m.set(datetime.now().month)
        self.combo_m.pack(side="left", padx=5)

        tk.Label(filter_frame, text="Năm:", bg="#f0f2f5").pack(side="left")
        self.combo_y = ttk.Combobox(filter_frame, values=[2025, 2026, 2027], width=6)
        self.combo_y.set(2026)
        self.combo_y.pack(side="left", padx=5)

        tk.Button(filter_frame, text="LỌC THÁNG",
                  command=lambda: self.controller.filter_by_month(self.combo_m.get(), self.combo_y.get())).pack(
            side="left", padx=10)

        # 4. NHÃN HIỂN THỊ TỔNG TIỀN (Quan trọng để Controller cập nhật)
        # --- TẠO MỘT KHUNG NHỎ CHỨA CÁC ĐÒNG TỔNG TIỀN NẰM BÊN PHẢI ---
        totals_frame = tk.Frame(filter_frame, bg="#f0f2f5")
        totals_frame.pack(side="right", padx=20)

        # 1. Chữ TỔNG CHI nằm trên cùng
        self.lbl_total = tk.Label(totals_frame, text="TỔNG CHI: 0 VND", font=("Arial", 12, "bold"),
                                  fg="#2c3e50", bg="#f0f2f5")
        self.lbl_total.pack(side="top", anchor="e", pady=2)  # side="top" để xếp dọc, anchor="e" để căn thẳng lề phải

        # 2. Tổng Ngân hàng nằm ngay phía dưới
        self.lbl_bank = tk.Label(totals_frame, text="🏦 Ngân hàng: 0 đ", font=("Arial", 10, "bold"),
                                 fg="#2980b9", bg="#f0f2f5")
        self.lbl_bank.pack(side="top", anchor="e", pady=2)

        # 3. Tổng Tiền mặt nằm dưới cùng
        self.lbl_cash = tk.Label(totals_frame, text="💵 Tiền mặt: 0 đ", font=("Arial", 10, "bold"),
                                 fg="#27ae60", bg="#f0f2f5")
        self.lbl_cash.pack(side="top", anchor="e", pady=2)
        # 5. BẢNG DỮ LIỆU (Treeview)
        table_frame = tk.Frame(self)
        table_frame.pack(pady=10, fill="both", expand=True, padx=20)

        columns = ("id", "ngay", "nguonchi", "sotien","phuongthuc", "ghichu")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        self.tree.heading("id", text="ID")
        self.tree.heading("ngay", text="Ngày Chi")
        self.tree.heading("nguonchi", text="Nguồn Tiền Chi")
        self.tree.heading("sotien", text="Số Tiền (VND)")
        self.tree.heading("phuongthuc", text="Phương Thức")
        self.tree.heading("ghichu", text="Ghi Chú")

        self.tree.column("id", width=35, anchor=tk.CENTER)
        self.tree.column("ngay", width=110, anchor=tk.CENTER)
        self.tree.column("nguonchi", width=220, anchor=tk.W)
        self.tree.column("sotien", width=150, anchor=tk.E)
        self.tree.column("phuongthuc", width=100, anchor=tk.CENTER)
        self.tree.column("ghichu", width=220, anchor=tk.W)

        # Thanh cuộn dọc
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def refresh(self):
        """Hàm tự động gọi lại khi bồ chuyển tab qua trang này"""
        self.controller.load_data()