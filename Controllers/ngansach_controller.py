from tkinter import messagebox
from Models.ngansach import NganSach_Model
from Views.ngansach_dialog import AddNganSachDialog, EditNganSachDialog


class NganSach_Controller:
    def __init__(self, root):
        self.root = root
        self.model = NganSach_Model()
        self.view = None

    def set_view(self, view):
        self.view = view
        self.load_data()

    def load_data(self, records=None):
        if not self.view or not hasattr(self.view, 'tree'):
            return

        self.view.tree.tag_configure('am_tien', foreground='red', font=("Arial", 10, "bold"))

        for row in self.view.tree.get_children():
            self.view.tree.delete(row)

        if records is None:
            records = self.model.get_all_with_spending()

        for row in records:
            han_muc_str = f"{row[1]:,.0f}"
            da_chi_str = f"{row[2]:,.0f}"
            con_lai_str = f"{row[3]:,.0f}"

            is_negative = False
            try:
                if float(row[3]) < 0:
                    is_negative = True
            except (ValueError, TypeError):
                pass

            if is_negative:
                self.view.tree.insert("", "end", values=(row[0], han_muc_str, da_chi_str, con_lai_str),
                                      tags=('am_tien',))
            else:
                self.view.tree.insert("", "end", values=(row[0], han_muc_str, da_chi_str, con_lai_str))

    def show_add_dialog(self):
        # Lấy danh sách tên nguồn chi hiện có để truyền vào View kiểm tra trùng lặp
        existing_budgets = self.model.get_all_with_spending()
        existing_names = [b[0].lower() for b in existing_budgets]

        AddNganSachDialog(self.root, existing_names, self.process_add)

    def process_add(self, nguonchi, limit):
        self.model.add_or_update(nguonchi, limit)
        self.load_data()
        messagebox.showinfo("Thành công", f"Đã thêm ngân sách cho nguồn '{nguonchi}'!")

    def show_edit_dialog(self):
        selected_item = self.view.tree.selection()
        if not selected_item:
            messagebox.showwarning("Nhắc nhở", "Vui lòng click chọn một dòng trong bảng để chỉnh sửa!")
            return

        item_data = self.view.tree.item(selected_item[0])['values']
        nguonchi_cu = item_data[0]
        hanmuc_cu = str(item_data[1]).replace(",", "")

        EditNganSachDialog(self.root, nguonchi_cu, hanmuc_cu, self.process_update)

    def process_update(self, nguonchi_cu, limit):
        self.model.add_or_update(nguonchi_cu, limit)
        self.load_data()
        messagebox.showinfo("Thành công", f"Đã cập nhật lại hạn mức nguồn '{nguonchi_cu}'!")

    def delete_budget(self):
        """Chức năng Xóa mục"""
        selected_item = self.view.tree.selection()
        if not selected_item:
            messagebox.showwarning("Nhắc nhở", "Vui lòng chọn dòng ngân sách cần xóa!")
            return

        item_data = self.view.tree.item(selected_item[0])['values']
        nguonchi = item_data[0]

        confirm = messagebox.askyesno("Xác nhận", f"Bồ có chắc muốn dừng theo dõi ngân sách cho nguồn '{nguonchi}'?")
        if confirm:
            self.model.delete(nguonchi)
            self.load_data()
            messagebox.showinfo("Thông báo", f"Đã xóa theo dõi nguồn '{nguonchi}'!")

    def search_budget(self, event=None):
        """Tìm kiếm trực tiếp từ thanh tìm kiếm trên màn hình (không dùng Popup)"""
        keyword = self.view.entry_search.get().strip().lower()
        all_records = self.model.get_all_with_spending()

        filtered_records = [r for r in all_records if keyword in r[0].lower()]
        self.load_data(filtered_records)