import tkinter as tk
from tkinter import messagebox
from Models.ngansach import NganSach_Model


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
        dialog = tk.Toplevel(self.root)
        dialog.title("➕ Thêm Ngân Sách Mới")
        dialog.geometry("320x200")
        dialog.resizable(False, False)
        dialog.grab_set()

        form = tk.Frame(dialog, padx=15, pady=15)
        form.pack(fill="both", expand=True)

        tk.Label(form, text="Nguồn chi:").grid(row=0, column=0, sticky="w", pady=8)
        entry_nguonchi = tk.Entry(form, width=20)
        entry_nguonchi.grid(row=0, column=1, pady=8)
        entry_nguonchi.focus()

        tk.Label(form, text="Hạn Mức (VND):").grid(row=1, column=0, sticky="w", pady=8)
        entry_limit = tk.Entry(form, width=20)
        entry_limit.grid(row=1, column=1, pady=8)

        def save_new():
            nguonchi = entry_nguonchi.get().strip()
            limit_str = entry_limit.get().strip()

            if not nguonchi or not limit_str:
                messagebox.showerror("Lỗi", "Vui lòng không bỏ trống thông tin!", parent=dialog)
                return

            try:
                limit = float(limit_str)
                if limit < 0: raise ValueError
            except ValueError:
                messagebox.showerror("Lỗi", "Hạn mức phải là số dương hợp lệ!", parent=dialog)
                return

            existing_budgets = self.model.get_all_with_spending()
            if any(b[0].lower() == nguonchi.lower() for b in existing_budgets):
                messagebox.showerror("Lỗi", f"Nguồn chi '{nguonchi}' đã tồn tại ngân sách!", parent=dialog)
                return

            self.model.add_or_update(nguonchi, limit)
            self.load_data()
            dialog.destroy()
            messagebox.showinfo("Thành công", f"Đã thêm ngân sách cho nguồn '{nguonchi}'!")

        tk.Button(form, text="➕ THÊM MỚI", bg="#2ecc71", fg="white", font=("Arial", 10, "bold"),
                  command=save_new, width=12).grid(row=2, column=0, columnspan=2, pady=15)

    def show_edit_dialog(self):
        selected_item = self.view.tree.selection()
        if not selected_item:
            messagebox.showwarning("Nhắc nhở", "Vui lòng click chọn một dòng trong bảng để chỉnh sửa!")
            return

        item_data = self.view.tree.item(selected_item[0])['values']
        nguonchi_cu = item_data[0]
        hanmuc_cu = str(item_data[1]).replace(",", "")

        dialog = tk.Toplevel(self.root)
        dialog.title("🔧 Chỉnh Sửa Hạn Mức")
        dialog.geometry("320x200")
        dialog.resizable(False, False)
        dialog.grab_set()

        form = tk.Frame(dialog, padx=15, pady=15)
        form.pack(fill="both", expand=True)

        tk.Label(form, text="Nguồn chi:").grid(row=0, column=0, sticky="w", pady=8)
        lbl_nguonchi = tk.Label(form, text=nguonchi_cu, font=("Arial", 10, "bold"), fg="#2c3e50")
        lbl_nguonchi.grid(row=0, column=1, sticky="w", pady=8)

        tk.Label(form, text="Hạn Mức Mới:").grid(row=1, column=0, sticky="w", pady=8)
        entry_limit = tk.Entry(form, width=20)
        entry_limit.insert(0, hanmuc_cu)
        entry_limit.grid(row=1, column=1, pady=8)
        entry_limit.focus()

        def save_edit():
            limit_str = entry_limit.get().strip()
            try:
                limit = float(limit_str)
                if limit < 0: raise ValueError
            except ValueError:
                messagebox.showerror("Lỗi", "Hạn mức phải là số dương hợp lệ!", parent=dialog)
                return

            self.model.add_or_update(nguonchi_cu, limit)
            self.load_data()
            dialog.destroy()
            messagebox.showinfo("Thành công", f"Đã cập nhật lại hạn mức nguồn '{nguonchi_cu}'!")

        tk.Button(form, text="💾 CẬP NHẬT", bg="#3498db", fg="white", font=("Arial", 10, "bold"),
                  command=save_edit, width=12).grid(row=2, column=0, columnspan=2, pady=15)

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
        keyword = self.view.entry_search.get().strip().lower()
        all_records = self.model.get_all_with_spending()

        filtered_records = [r for r in all_records if keyword in r[0].lower()]
        self.load_data(filtered_records)