import tkinter as tk
from tkinter import messagebox
from Models.thu import Thu_Model
from datetime import datetime
from Views.thu_dialogs import AddThuDialog, EditThuDialog, SearchThuDialog

class Thu_Controller:
    def __init__(self, root):
        self.root = root
        self.model = Thu_Model()
        self.view = None

    def set_view(self, view):
        self.view = view
        self.load_data()

    def load_data(self, records=None):
        if not self.view or not hasattr(self.view, 'tree'):
            return

        for row in self.view.tree.get_children():
            self.view.tree.delete(row)

        if records is None:
            records = self.model.get_all()

        def safe_date(row):
            try: return datetime.strptime(row[1], "%d/%m/%Y")
            except ValueError: return datetime(1900, 1, 1)

        records.sort(key=safe_date, reverse=True)

        total, total_bank, total_cash = 0, 0, 0

        for row in records:
            try:
                tien = float(row[3])
                total += tien
                phuong_thuc = row[4] if len(row) > 4 else "Tiền mặt"
                ghi_chu = row[5] if len(row) > 5 else (row[4] if len(row) > 4 else "")

                if "Ngân hàng" in phuong_thuc: total_bank += tien
                else: total_cash += tien

                formatted_money = "{:,.0f}".format(tien)
            except Exception:
                formatted_money = row[3]
                phuong_thuc = row[4] if len(row) > 4 else ""
                ghi_chu = row[5] if len(row) > 5 else ""

            self.view.tree.insert("", tk.END, values=(row[0], row[1], row[2], formatted_money, phuong_thuc, ghi_chu))

        if hasattr(self.view, 'lbl_total'): self.view.lbl_total.config(text=f"TỔNG THU: {total:,.0f} VND")
        if hasattr(self.view, 'lbl_bank'): self.view.lbl_bank.config(text=f"🏦 Ngân hàng: {total_bank:,.0f} đ")
        if hasattr(self.view, 'lbl_cash'): self.view.lbl_cash.config(text=f"💵 Tiền mặt: {total_cash:,.0f} đ")

    def filter_by_month(self, month, year):
        all_records = self.model.get_all()
        filtered = []
        for r in all_records:
            try:
                d = datetime.strptime(r[1], "%d/%m/%Y")
                if d.month == int(month) and d.year == int(year):
                    filtered.append(r)
            except ValueError:
                continue
        self.load_data(filtered)

    def show_add_dialog(self):
        AddThuDialog(self.root, self.process_add)

    def process_add(self, ngay, nguon, tien, pt, gc):
        self.model.add(ngay, nguon, tien, pt, gc)
        self.load_data()
        messagebox.showinfo("Thành công", "Đã thêm khoản thu mới thành công!")

    def show_edit_dialog(self):
        selected = self.view.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn 1 dòng khoản thu trên bảng để sửa!")
            return
        item_data = self.view.tree.item(selected[0])['values']
        EditThuDialog(self.root, item_data, self.process_update)

    def process_update(self, income_id, ngay, nguon, tien, pt, gc):
        self.model.update(income_id, ngay, nguon, tien, pt, gc)
        self.load_data()
        messagebox.showinfo("Thành công", "Đã cập nhật khoản thu thành công!")

    def show_search_dialog(self):
        SearchThuDialog(self.root, self.process_search)

    def process_search(self, keyword):
        all_records = self.model.get_all()
        filtered = []
        for r in all_records:
            nguon = str(r[2]).lower() if len(r) > 2 else ""
            ghichu = str(r[5]).lower() if len(r) > 5 else ""
            if keyword in nguon or keyword in ghichu:
                filtered.append(r)
        self.load_data(filtered)

    def delete_record(self):
        selected = self.view.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn bản ghi cần xóa trên bảng!")
            return
        item_data = self.view.tree.item(selected[0])['values']
        income_id = item_data[0]

        if messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc chắn muốn xóa khoản thu nhập '{item_data[2]}' không?"):
            self.model.delete(income_id)
            self.load_data()
            messagebox.showinfo("Xóa thành công", "Đã gỡ bỏ bản ghi khỏi tệp data!")