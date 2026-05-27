import tkinter as tk
from tkinter import ttk
from datetime import datetime
import random


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f2f5")
        self.controller = controller
        self.setup_ui()
        self.update_clock()

    def setup_ui(self):
        # ================= MAIN CONTENT (BÊN PHẢI) =================
        main_frame = tk.Frame(self, bg="#f0f2f5")
        main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 1. TOP CARDS (4 ô hiển thị dashboard phía trên)
        frame_cards = tk.Frame(main_frame, bg="#f0f2f5")
        frame_cards.pack(fill=tk.X, padx=20, pady=20)

        colors = ["#34495e", "#2ecc71", "#e74c3c", "#f39c12"]
        self.card_labels = []

        for i in range(4):
            card = tk.Frame(frame_cards, bg=colors[i], width=200, height=100)
            card.pack_propagate(False)
            card.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.BOTH)
            lbl = tk.Label(card, text="", bg=colors[i], fg="white", font=("Arial", 11, "bold"), justify="center")
            lbl.pack(expand=True, fill=tk.BOTH, pady=10, padx=5)
            self.card_labels.append(lbl)

        # 2. BẢNG DANH SÁCH LỊCH SỬ GIAO DỊCH (Có thanh trượt)
        frame_table = tk.Frame(main_frame)
        frame_table.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        lbl_title = tk.Label(frame_table, text="📜 LỊCH SỬ GIAO DỊCH GẦN ĐÂY (TỔNG HỢP THU & CHI)",
                             font=("Arial", 12, "bold"), fg="#2c3e50", bg="#f0f2f5")
        lbl_title.pack(pady=(0, 10))

        # Khởi tạo thanh trượt
        scrollbar = ttk.Scrollbar(frame_table, orient="vertical")

        # Cấu trúc bảng
        columns = ("id", "ngay", "noidung", "loai", "sotien")
        self.tree = ttk.Treeview(frame_table, columns=columns, show="headings", yscrollcommand=scrollbar.set)

        # Gắn kết thanh trượt
        scrollbar.config(command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill=tk.BOTH, expand=True)

        # Định nghĩa tiêu đề và cột
        self.tree.heading("id", text="ID")
        self.tree.heading("ngay", text="Ngày")
        self.tree.heading("noidung", text="Nội Dung")
        self.tree.heading("loai", text="Loại")
        self.tree.heading("sotien", text="Số Tiền")

        self.tree.column("id", width=60, anchor=tk.CENTER)
        self.tree.column("ngay", width=100, anchor=tk.CENTER)
        self.tree.column("noidung", width=250, anchor=tk.W)
        self.tree.column("loai", width=100, anchor=tk.CENTER)
        self.tree.column("sotien", width=150, anchor=tk.E)

        # 3. KHUNG MẸO CHI TIÊU
        self.frame_tips = tk.Frame(main_frame, bg="#ecf0f1", highlightbackground="#bdc3c7", highlightthickness=1)
        self.frame_tips.pack(fill=tk.X, padx=20, pady=(10, 20))

        self.lbl_tip_title = tk.Label(self.frame_tips, text="💡 MẸO CHI TIÊU HÔM NAY:",
                                      font=("Arial", 10, "bold"), bg="#ecf0f1", fg="#2c3e50")
        self.lbl_tip_title.pack(anchor="w", padx=10, pady=(5, 0))

        self.lbl_tip_content = tk.Label(self.frame_tips, text="", font=("Arial", 10, "italic"),
                                        bg="#ecf0f1", fg="#34495e", wraplength=700, justify="left")
        self.lbl_tip_content.pack(anchor="w", padx=10, pady=(0, 5))

        self.display_random_tip()

    def refresh(self):
        if self.controller:
            self.controller.load_data()

    def update_clock(self):
        now = datetime.now()
        time_str = now.strftime("%d/%m/%Y\n%H:%M:%S")
        if hasattr(self, 'card_labels') and len(self.card_labels) > 0:
            self.card_labels[0].config(text=f"⏱️ NGÀY & GIỜ\n\n{time_str}")
        self.after(1000, self.update_clock)

    def display_random_tip(self):
        tips_list = [
            "Mua sắm có kế hoạch: Luôn lập danh sách đồ cần mua.",
            "Quy tắc 30 ngày: Đợi 30 ngày trước khi mua món đồ không thiết yếu.",
            "Nấu ăn tại nhà giúp bạn tiết kiệm đến 50% chi phí.",
            "Tiết kiệm trước, chi tiêu sau.",
            "Kiểm soát các khoản phí nhỏ mỗi ngày."
        ]
        tip = random.choice(tips_list)
        self.lbl_tip_content.config(text=tip)