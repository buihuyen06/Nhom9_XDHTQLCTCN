import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Models.phantich import PhanTich_Model


class PhanTich_Controller:
    def __init__(self, root):
        self.root = root
        self.model = PhanTich_Model()
        self.view = None

    def set_view(self, view):
        self.view = view
        self.load_data_and_draw_chart()

    def load_data_and_draw_chart(self):
        if not self.view:
            return

        selected_month = self.view.combo_month.get()
        selected_year = self.view.combo_year.get()

        tong_thu, tong_chi = self.model.get_summary_data(selected_month, selected_year)
        so_du = tong_thu - tong_chi

        self.view.lbl_thu.config(text=f"Tổng Thu: {tong_thu:,.0f} đ")
        self.view.lbl_chi.config(text=f"Tổng Chi: {tong_chi:,.0f} đ")
        self.view.lbl_du.config(text=f"Số Dư: {so_du:,.0f} đ")

        for widget in self.view.chart_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)

        if tong_thu == 0 and tong_chi == 0:
            ax.text(0.5, 0.5, f"Không có dữ liệu giao dịch\n(Tháng {selected_month} / {selected_year})",
                    horizontalalignment='center', verticalalignment='center', fontsize=11, color="gray")
            ax.axis('off')
        else:
            labels = ['Tổng Thu', 'Tổng Chi']
            sizes = [tong_thu, tong_chi]
            colors = ['#2ecc71', '#e74c3c']
            explode = (0.05, 0)

            ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                   autopct='%1.1f%%', startangle=90, textprops={'fontsize': 10, 'weight': 'bold'})
            ax.axis('equal')

            title_text = "TỶ LỆ THU - CHI"
            if selected_month != "Tất cả" or selected_year != "Tất cả":
                title_text += f"\n(Tháng {selected_month} / Năm {selected_year})"
            plt.title(title_text, fontsize=12, fontweight='bold', pad=15)

        canvas = FigureCanvasTkAgg(fig, master=self.view.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)