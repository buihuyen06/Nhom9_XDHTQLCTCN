import tkinter as tk
from Models.thu import Thu_Model
from Models.chi import Chi_Model
from datetime import datetime

class HomeController:
    def __init__(self, root):
        self.root = root
        self.thu_model = Thu_Model()
        self.chi_model = Chi_Model()
        self.view = None

    def set_view(self, view):
        self.view = view
        self.load_data()

    def load_data(self):
        if not self.view or not hasattr(self.view, 'tree'):
            return

        for row in self.view.tree.get_children():
            self.view.tree.delete(row)

        list_thu = self.thu_model.get_all()
        list_chi = self.chi_model.get_all()

        combined_records = []
        tong_thu = 0.0
        tong_chi = 0.0

        for row in list_thu:
            try:
                sotien_val = float(row[3])
            except (ValueError, IndexError):
                sotien_val = 0.0
            tong_thu += sotien_val

            combined_records.append({
                "id": f"THU-{row[0]}",
                "ngay": row[1],
                "noidung": row[2],
                "loai": "Khoản Thu",
                "sotien": sotien_val
            })

        for row in list_chi:
            try:
                sotien_val = float(row[3])
            except (ValueError, IndexError):
                sotien_val = 0.0
            tong_chi += sotien_val

            combined_records.append({
                "id": f"CHI-{row[0]}",
                "ngay": row[1],
                "noidung": row[2],
                "loai": "Khoản Chi",
                "sotien": sotien_val
            })

        def get_date(item):
            try:
                return datetime.strptime(item["ngay"], "%d/%m/%Y")
            except ValueError:
                return datetime(1900, 1, 1)

        combined_records.sort(key=get_date, reverse=True)

        for item in combined_records:
            formatted_money = "{:,.0f} VND".format(item["sotien"])
            self.view.tree.insert("", tk.END, values=(
                item["id"],
                item["ngay"],
                item["noidung"],
                item["loai"],
                formatted_money
            ))

        if hasattr(self.view, 'card_labels') and len(self.view.card_labels) >= 4:
            so_du = tong_thu - tong_chi
            self.view.card_labels[1].config(text=f"🟩 TỔNG THU NHẬP\n\n{tong_thu:,.0f} VND")
            self.view.card_labels[2].config(text=f"🟥 TỔNG CHI TIÊU\n\n{tong_chi:,.0f} VND")
            self.view.card_labels[3].config(text=f"🟨 SỐ DƯ HIỆN TẠI\n\n{so_du:,.0f} VND")
        if hasattr(self.view, 'display_random_tip'):
            self.view.display_random_tip()