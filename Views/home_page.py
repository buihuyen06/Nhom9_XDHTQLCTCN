import tkinter as tk
from tkinter import ttk
from datetime import datetime
import random


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#FDFBF7")
        self.controller = controller
        self.setup_ui()
        self.update_clock()

    def setup_ui(self):
        main_frame = tk.Frame(self, bg="#FDFBF7")
        main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 1. TOP CARDS (Phóng to kích thước ô và font chữ)
        frame_cards = tk.Frame(main_frame, bg="#FDFBF7")
        frame_cards.pack(fill=tk.X, padx=20, pady=25)

        colors = ["#CFE8FF", "#FCE1D4", "#FCD271", "#F2966D"]
        self.card_labels = []

        for i in range(4):
            card = tk.Frame(frame_cards, bg=colors[i], width=280, height=130)  # Tăng kích thước card
            card.pack_propagate(False)
            card.pack(side=tk.LEFT, padx=15, expand=True, fill=tk.BOTH)
            lbl = tk.Label(card, text="", bg=colors[i], fg="black", font=("Arial", 14, "bold"), justify="center") # Font 11 -> 14
            lbl.pack(expand=True, fill=tk.BOTH, pady=10, padx=5)
            self.card_labels.append(lbl)

        # 2. BẢNG DANH SÁCH LỊCH SỬ GIAO DỊCH
        frame_table = tk.Frame(main_frame)
        frame_table.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        lbl_title = tk.Label(frame_table, text="📜 TỔNG HỢP THU CHI",
                             font=("Arial", 18, "bold"), fg="black", bg="#FDFBF7") # Font 15 -> 18 bold
        lbl_title.pack(fill=tk.X, pady=(0, 15))

        scrollbar = ttk.Scrollbar(frame_table, orient="vertical")

        columns = ("id", "ngay", "noidung", "loai", "sotien")
        self.tree = ttk.Treeview(frame_table, columns=columns, show="headings", yscrollcommand=scrollbar.set)

        scrollbar.config(command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill=tk.BOTH, expand=True)

        self.tree.heading("id", text="ID")
        self.tree.heading("ngay", text="Ngày")
        self.tree.heading("noidung", text="Nội Dung")
        self.tree.heading("loai", text="Loại")
        self.tree.heading("sotien", text="Số Tiền")

        # Nới rộng kích thước các cột trên màn hình lớn
        self.tree.column("id", width=80, anchor=tk.CENTER)
        self.tree.column("ngay", width=140, anchor=tk.CENTER)
        self.tree.column("noidung", width=400, anchor=tk.W)
        self.tree.column("loai", width=140, anchor=tk.CENTER)
        self.tree.column("sotien", width=200, anchor=tk.E)

        # 3. KHUNG MẸO CHI TIÊU (Chữ to rõ ràng hơn)
        self.frame_tips = tk.Frame(main_frame, bg="#FDFBF7")
        self.frame_tips.pack(fill=tk.X, padx=20, pady=(15, 25))

        self.lbl_tip_title = tk.Label(self.frame_tips, text="💡 MẸO CHI TIÊU HÔM NAY:",
                                      font=("Arial", 13, "bold"), fg="black", bg="#FDFBF7") # Font 10 -> 13
        self.lbl_tip_title.pack(anchor="w", padx=10, pady=(5, 5))

        self.lbl_tip_content = tk.Label(self.frame_tips, text="", font=("Arial", 13, "italic"),
                                         fg="black", bg="#FDFBF7", wraplength=1200, justify="left") # wraplength 700 -> 1200, font 13
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