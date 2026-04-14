import tkinter as tk


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#FFF9C4")
        self.ctrl = controller
        self.render_ui()

    def render_ui(self):
        tk.Label(self, text="TỔNG QUAN TÀI CHÍNH", font=("Arial", 18, "bold"), fg="#F48FB1", bg="#FFF9C4").pack(pady=10)

        # Khung Số dư
        self.f_sd = tk.Frame(self, bg="white", highlightthickness=1);
        self.f_sd.pack(fill="x", padx=20, pady=5)
        tk.Label(self.f_sd, text="💰 SỐ DƯ HIỆN TẠI", fg="#F48FB1", bg="white").pack()
        self.lbl_sd = tk.Label(self.f_sd, text="0đ", font=("Arial", 14, "bold"), bg="white");
        self.lbl_sd.pack()

        # Thu/Chi
        f_s = tk.Frame(self, bg="#FFF9C4");
        f_s.pack(fill="x", padx=20)
        for t, c, lbl in [("💸 TỔNG THU", "green", "lbl_thu"), ("📉 TỔNG CHI", "red", "lbl_chi")]:
            f = tk.Frame(f_s, bg="white", highlightthickness=1);
            f.pack(side="left", expand=True, fill="both", padx=2)
            tk.Label(f, text=t, fg=c, bg="white").pack()
            setattr(self, lbl, tk.Label(f, text="0đ", fg=c, bg="white", font=("Arial", 12, "bold")))
            getattr(self, lbl).pack()

        # Nút chức năng
        for txt, clr in [("➕ NHẬP LIỆU", "#F8BBD0"), ("📋 LỊCH SỬ", "#81D4FA"), ("📊 PHÂN TÍCH", "#CE93D8"),
                         ("🔄 LÀM MỚI", "#A5D6A7")]:
            tk.Button(self, text=txt, bg=clr, relief="flat", height=2, command=self.refresh).pack(fill="x", padx=20,
                                                                                                  pady=2)

    def refresh(self):
        thu = sum(t['price'] for t in self.ctrl.model.transactions if t['type'] == 'Thu')
        chi = sum(t['price'] for t in self.ctrl.model.transactions if t['type'] == 'Chi')
        bal = self.ctrl.model.df_accounts["Số dư"].sum()
        self.lbl_sd.config(text=f"{thu - chi + bal:,.0f}đ")
        self.lbl_thu.config(text=f"{thu:,.0f}đ")
        self.lbl_chi.config(text=f"{chi:,.0f}đ")