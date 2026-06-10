from Models.phantich import PhanTich_Model

class PhanTich_Controller:
    def __init__(self, root):
        self.root = root
        self.view = None
        self.model = PhanTich_Model()   # THÊM DÒNG NÀY

    def set_view(self, view):
        self.view = view
        self.load_data_and_draw_chart()

    def load_data_and_draw_chart(self):
        if not self.view:
            return

        selected_month = self.view.combo_month.get()
        selected_year = self.view.combo_year.get()

        tong_thu, tong_chi = self.model.get_summary_data(
            selected_month,
            selected_year
        )

        so_du = tong_thu - tong_chi

        self.view.update_dashboard(
            tong_thu,
            tong_chi,
            so_du,
            selected_month,
            selected_year
        )