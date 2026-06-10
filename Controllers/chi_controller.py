from tkinter import ttk, messagebox
from Models.chi import Chi_Model
from Models.ngansach import NganSach_Model
from Views.chi_dialogs import AddChiDialog, EditChiDialog, SearchDialog

class Chi_Controller:
    def __init__(self, root):
        self.root = root
        self.model = Chi_Model()
        self.view = None

    def set_view(self, view):
        self.view = view
        self.load_data()

    def show_add_dialog(self):
        AddChiDialog(self.root, self.get_danh_sach_nguon_chi(), self.process_add)
    def show_edit_dialog(self):
        selected = self.view.tree.selection()
        if not selected:
            messagebox.showwarning("Nhắc nhở", "Vui lòng chọn một dòng để chỉnh sửa!")
            return
        item_data = self.view.tree.item(selected[0])['values']
        EditChiDialog(self.root, item_data, self.get_danh_sach_nguon_chi(), self.process_update)

    def show_search_dialog(self):
        SearchDialog(self.root, self.process_search)

    def process_add(self, ngay, nguon, tien_str, pt, gc):
        if hasattr(self.model, 'add'):
            self.model.add(ngay, nguon, tien_str, pt, gc)
        self.load_data()
        self.kiem_tra_va_canh_bao_ngan_sach(nguon)

    def process_update(self, id_cu, ngay, nguon, tien_str, pt, gc):
        if hasattr(self.model, 'update'):
            self.model.update(id_cu, ngay, nguon, tien_str, pt, gc)
        self.load_data()
        self.kiem_tra_va_canh_bao_ngan_sach(nguon)

    def process_search(self, keyword):
        kw = keyword.strip().lower()
        if hasattr(self.model, 'get_all'):
            filtered = [r for r in self.model.get_all() if kw in str(r[2]).lower() or kw in str(r[5]).lower()]
            self.load_data(filtered)

    def delete_record(self):
        selected_item = self.view.tree.selection()
        if not selected_item:
            messagebox.showwarning("Nhắc nhở", "Vui lòng chọn dòng cần xóa!")
            return
        item_data = self.view.tree.item(selected_item[0])['values']
        id_xoa = str(item_data[0])
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa khoản chi này không?"):
            if hasattr(self.model, 'delete'):
                self.model.delete(id_xoa)
            self.load_data()

    def load_data(self, records=None):
        if not self.view or not hasattr(self.view, 'tree'):
            return

        for row in self.view.tree.get_children():
            self.view.tree.delete(row)

        if records is None:
            records = self.model.get_all() if hasattr(self.model, 'get_all') else []

        tong_chi = 0
        tong_nh = 0
        tong_tm = 0

        for row in records:
            try:
                val = float(str(row[3]).replace(",", ""))
                tong_chi += val
                if "Ngân hàng" in str(row[4]):
                    tong_nh += val
                elif "Tiền mặt" in str(row[4]):
                    tong_tm += val
                tien_str = f"{val:,.0f}"
            except (ValueError, IndexError):
                tien_str = row[3] if len(row) > 3 else "0"

            self.view.tree.insert("", "end", values=(row[0], row[1], row[2], tien_str, row[4], row[5]))

        if hasattr(self.view, 'lbl_total'):
            self.view.lbl_total.config(text=f"TỔNG CHI: {tong_chi:,.0f} VND")
        if hasattr(self.view, 'lbl_bank'):
            self.view.lbl_bank.config(text=f"🏦 Ngân hàng: {tong_nh:,.0f} đ")
        if hasattr(self.view, 'lbl_cash'):
            self.view.lbl_cash.config(text=f"💵 Tiền mặt: {tong_tm:,.0f} đ")

    def filter_by_month(self, month, year):
        if hasattr(self.model, 'get_all'):
            all_records = self.model.get_all()
            filtered_records = []
            for row in all_records:
                try:
                    ngay_chi_str = row[1]
                    parts = ngay_chi_str.split('/')
                    if len(parts) == 3 and int(parts[1]) == int(month) and int(parts[2]) == int(year):
                        filtered_records.append(row)
                except Exception:
                    pass
            self.load_data(filtered_records)

    def get_danh_sach_nguon_chi(self):
        nguon_chi_list = []
        try:
            ns_model = NganSach_Model()
            records = ns_model.get_all_with_spending()
            for row in records:
                nguon_chi_list.append(row[0])
        except Exception:
            pass
        if not nguon_chi_list:
            nguon_chi_list = ["Ăn uống", "Đi lại", "Mua sắm", "Khác"]
        return nguon_chi_list

    def kiem_tra_va_canh_bao_ngan_sach(self, nguon_can_kiem_tra):
        try:
            ns_model = NganSach_Model()
            records = ns_model.get_all_with_spending()

            for row in records:
                if str(row[0]).strip().lower() == str(nguon_can_kiem_tra).strip().lower():
                    con_lai = float(row[3])
                    if con_lai < 0:
                        messagebox.showwarning(
                            "🚨 CẢNH BÁO VƯỢT HẠN MỨC",
                            f"Bạn đã vượt quá hạn mức chi tiêu cho phần '{row[0]}'!"
                        )
                    break
        except Exception:
            pass