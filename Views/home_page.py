import tkinter as tk


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#FFF9C4")
        self.ctrl = controller  # MainApp
        self.render_ui()

        self.banner = tk.Label(
        self,
        text="💰 Tiền vào có kế hoạch, tiền ra có kiểm soát 💰\n✨ Một xu tiết kiệm là một xu kiếm được ✨",
        font=("Arial", 14, "bold"),
        fg="#2E7D32",
        bg="#FFF9C4",
        justify="center"
    )
        self.banner.pack(pady=15)

        self.colors = ["#E91E63", "#F06292", "#EC407A", "#AD1457"]
        self.i = 0

        self.animate_banner()  # gọi chạy animation


    def animate_banner(self):
        self.banner.config(fg=self.colors[self.i])
        self.i = (self.i + 1) % len(self.colors)
        self.after(500, self.animate_banner)
    def render_ui(self):
        tk.Label(self, text="TỔNG QUAN TÀI CHÍNH", font=("Comic Sans MS", 18, "bold"), fg="black", bg="#FFF9C4").pack(pady=10)

        # Khung Số dư
        self.f_sd = tk.Frame(self, bg="white", highlightthickness=1)
        self.f_sd.pack(fill="x", padx=20, pady=5)
        tk.Label(self.f_sd, text="💰 SỐ DƯ HIỆN TẠI", fg="#F48FB1", bg="white").pack()
        self.lbl_sd = tk.Label(self.f_sd, text="0đ", font=("Arial", 14, "bold"), bg="white")
        self.lbl_sd.pack()

        # Thu/Chi
        f_s = tk.Frame(self, bg="#FFF9C4")
        f_s.pack(fill="x", padx=20)
        for t, c, lbl in [("💸 TỔNG THU", "green", "lbl_thu"), ("📉 TỔNG CHI", "red", "lbl_chi")]:
            f = tk.Frame(f_s, bg="white", highlightthickness=1)
            f.pack(side="left", expand=True, fill="both", padx=2)
            tk.Label(f, text=t, fg=c, bg="white").pack()
            setattr(self, lbl, tk.Label(f, text="0đ", fg=c, bg="white", font=("Arial", 12, "bold")))
            getattr(self, lbl).pack()

        # --- PHẦN SỬA LỖI NÚT BẤM ---
        tk.Button(self,
                  text="➕ NHẬP LIỆU",
                  bg="#F8BBD0",
                  command=lambda: self.ctrl.show("InputPage")
                  ).pack(fill="x", padx=40, pady=10)
        tk.Button(self,
                  text="📋 LỊCH SỬ",
                  bg="#81D4FA",
                  command=lambda: self.ctrl.show("HistoryPage")
                  ).pack(fill="x", padx=40, pady=10)
        tk.Button(self,
                  text="📊 PHÂN TÍCH",
                  bg="#CE93D8",
                  command=lambda: self.ctrl.show("AnalysisPage")
                  ).pack(fill="x", padx=40, pady=10)
        buttons = [
            ("🔄 LÀM MỚI", "#A5D6A7", None)
        ]

        for txt, clr, target in buttons:
            if txt == "🔄 LÀM MỚI":
                cmd = self.refresh
            else:
                cmd = lambda t=target: self.ctrl.show(t)
            tk.Button(self, text=txt, bg=clr, command=cmd).pack(fill="x", padx=40, pady=5)

    def refresh(self):
        # Lấy SpendingController từ MainApp
        thu, chi, so_du = self.ctrl.controller.get_summary()

        # Cập nhật các label với dữ liệu mới
        self.lbl_sd.config(text=f"{so_du}đ")
        self.lbl_thu.config(text=f"{thu}đ")
        self.lbl_chi.config(text=f"{chi}đ")
