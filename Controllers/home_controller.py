import tkinter as tk
from Models.thu import Thu_Model
from Models.chi import Chi_Model
from datetime import datetime

class HomeController:
    def __init__(self, root):
        self.root = root
        self.thu_model = Thu_Model()
        self.chi_model = Chi_Model()
        self.view = None  # Sẽ được gán và hiển thị thông qua bộ quản lý file chính MainApp

    def set_view(self, view):
        """Nhận diện view được phân phối từ MainApp để tương tác dữ liệu"""
        self.view = view
        self.load_data()

    def load_data(self):
        if not self.view or not hasattr(self.view, 'tree'):
            return

        # Xóa dữ liệu cũ trên bảng Treeview để tránh trùng lặp khi load lại
        for row in self.view.tree.get_children():
            self.view.tree.delete(row)

        # 1. Đọc dữ liệu từ file Khoản Thu và Khoản Chi thông qua Model tương ứng
        list_thu = self.thu_model.get_all()
        list_chi = self.chi_model.get_all()

        combined_records = []
        tong_thu = 0.0
        tong_chi = 0.0

        # 2. Chuẩn hóa dữ liệu Khoản Thu để đưa vào danh sách tổng hợp
        for row in list_thu:
            # Cấu trúc row từ thu.py: [ID, Ngay, NguonThu, SoTien, PhuongThuc, GhiChu]
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

        # 3. Chuẩn hóa dữ liệu Khoản Chi để đưa vào danh sách tổng hợp
        for row in list_chi:
            # Cấu trúc row từ chi.py: [ID, Ngay, NguonChi, SoTien, PhuongThuc, GhiChu]
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

        # 4. Sắp xếp danh sách đã gộp theo thứ tự Ngày mới nhất lên trên đầu
        def get_date(item):
            try:
                return datetime.strptime(item["ngay"], "%d/%m/%Y")
            except ValueError:
                return datetime(1900, 1, 1)

        combined_records.sort(key=get_date, reverse=True)

        # 5. Đổ dữ liệu gộp sau khi sắp xếp lên Treeview của HomePage
        for item in combined_records:
            formatted_money = "{:,.0f} VND".format(item["sotien"])
            self.view.tree.insert("", tk.END, values=(
                item["id"],
                item["ngay"],
                item["noidung"],
                item["loai"],
                formatted_money
            ))

        # 6. Cập nhật các thông số tính toán thực tế lên bộ thẻ hiển thị (Cards) phía trên
        if hasattr(self.view, 'card_labels') and len(self.view.card_labels) >= 4:
            so_du = tong_thu - tong_chi
            self.view.card_labels[1].config(text=f"🟩 TỔNG THU NHẬP\n\n{tong_thu:,.0f} VND")
            self.view.card_labels[2].config(text=f"🟥 TỔNG CHI TIÊU\n\n{tong_chi:,.0f} VND")
            self.view.card_labels[3].config(text=f"🟨 SỐ DƯ HIỆN TẠI\n\n{so_du:,.0f} VND")
        if hasattr(self.view, 'display_random_tip'):
            self.view.display_random_tip()