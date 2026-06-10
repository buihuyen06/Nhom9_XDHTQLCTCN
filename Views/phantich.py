import tkinter as tk
from tkinter import ttk
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class PhanTich_Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f2f5")
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        # TIÊU ĐỀ
        tk.Label(
            self,
            text="📊 PHÂN TÍCH TÀI CHÍNH",
            font=("Arial", 24, "bold"),
            fg="#2c3e50",
            bg="#f0f2f5"
        ).pack(pady=20)

        # BỘ LỌC
        filter_frame = tk.Frame(self, bg="#f0f2f5")
        filter_frame.pack(pady=15)

        tk.Label(
            filter_frame,
            text="Tháng:",
            font=("Arial", 12),
            bg="#f0f2f5"
        ).pack(side="left", padx=5)

        months = ["Tất cả"] + [f"{i:02d}" for i in range(1, 13)]
        self.combo_month = ttk.Combobox(
            filter_frame,
            values=months,
            width=12,
            state="readonly"
        )
        self.combo_month.set("Tất cả")
        self.combo_month.pack(side="left", padx=6)

        tk.Label(
            filter_frame,
            text="Năm:",
            font=("Arial", 12),
            bg="#f0f2f5"
        ).pack(side="left", padx=5)

        current_year = datetime.now().year
        years = ["Tất cả"] + [str(y) for y in range(current_year - 2, current_year + 3)]

        self.combo_year = ttk.Combobox(
            filter_frame,
            values=years,
            width=12,
            state="readonly"
        )
        self.combo_year.set("Tất cả")
        self.combo_year.pack(side="left", padx=6)

        btn_filter = tk.Button(
            filter_frame,
            text="🔍 Lọc Số Liệu",
            bg="#3498db",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=3,
            bd=0,
            cursor="hand2",
            command=self.controller.load_data_and_draw_chart
        )
        btn_filter.pack(side="left", padx=20)

        # KHUNG TỔNG QUAN
        self.summary_frame = tk.Frame(self, bg="#f0f2f5")
        self.summary_frame.pack(pady=15)

        self.lbl_thu = tk.Label(
            self.summary_frame,
            text="Tổng Thu: 0",
            font=("Arial", 18, "bold"),
            fg="#27ae60",
            bg="#f0f2f5"
        )
        self.lbl_thu.pack(side="left", padx=40)

        self.lbl_chi = tk.Label(
            self.summary_frame,
            text="Tổng Chi: 0",
            font=("Arial", 18, "bold"),
            fg="#e74c3c",
            bg="#f0f2f5"
        )
        self.lbl_chi.pack(side="left", padx=40)

        self.lbl_du = tk.Label(
            self.summary_frame,
            text="Số Dư: 0",
            font=("Arial", 18, "bold"),
            fg="#2980b9",
            bg="#f0f2f5"
        )
        self.lbl_du.pack(side="left", padx=40)

        # KHUNG BIỂU ĐỒ
        self.chart_frame = tk.Frame(
            self,
            bg="white",
            bd=2,
            relief="groove"
        )
        self.chart_frame.pack(
            pady=15,
            fill="both",
            expand=True,
            padx=50
        )

    def update_dashboard(self, tong_thu, tong_chi, so_du, month, year):

        self.lbl_thu.config(text=f"Tổng Thu: {tong_thu:,.0f} đ")
        self.lbl_chi.config(text=f"Tổng Chi: {tong_chi:,.0f} đ")
        self.lbl_du.config(text=f"Số Dư: {so_du:,.0f} đ")

        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)

        if tong_thu == 0 and tong_chi == 0:
            ax.text(
                0.5,
                0.5,
                f"Không có dữ liệu giao dịch\n(Tháng {month} / {year})",
                ha="center",
                va="center",
                fontsize=11,
                color="gray"
            )
            ax.axis("off")

        else:
            labels = ["Tổng Thu", "Tổng Chi"]
            sizes = [tong_thu, tong_chi]
            colors = ["#2ecc71", "#e74c3c"]
            explode = (0.05, 0)

            ax.pie(
                sizes,
                labels=labels,
                colors=colors,
                explode=explode,
                autopct="%1.1f%%",
                startangle=90,
                textprops={
                    "fontsize": 10,
                    "weight": "bold"
                }
            )

            ax.axis("equal")

            title = "TỶ LỆ THU - CHI"

            if month != "Tất cả" or year != "Tất cả":
                title += f"\n(Tháng {month} / Năm {year})"

            ax.set_title(
                title,
                fontsize=12,
                fontweight="bold",
                pad=15
            )

        canvas = FigureCanvasTkAgg(
            fig,
            master=self.chart_frame
        )

        canvas.draw()
        canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )