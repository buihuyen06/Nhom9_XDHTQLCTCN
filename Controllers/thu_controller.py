import tkinter as tk
from tkinter import ttk, messagebox
from Models.thu import Thu_Model
from datetime import datetime


class Thu_Controller:
    def __init__(self, root):
        self.root = root
        self.model = Thu_Model()
        self.view = None

    def set_view(self, view):
        self.view = view
        self.load_data()

    def load_data(self, records=None):
        """Tải dữ liệu lên bảng: Mới nhất trên cùng + Tính tổng Ngân hàng/Tiền mặt"""
        if not self.view or not hasattr(self.view, 'tree'):
            return

        for row in self.view.tree.get_children():
            self.view.tree.delete(row)

        if records is None:
            records = self.model.get_all()

        # --- Sắp xếp an toàn theo ngày mới nhất lên đầu ---
        def safe_date(row):
            try:
                return datetime.strptime(row[1], "%d/%m/%Y")
            except ValueError:
                return datetime(1900, 1, 1)

        records.sort(key=safe_date, reverse=True)

        total = 0
        total_bank = 0
        total_cash = 0

        for row in records:
            try:
                tien = float(row[3])
                total += tien

                # Tính toán theo Phương thức (Cột index 4)
                # Đảm bảo row có đủ cột (tránh lỗi nếu file cũ chưa có cột phương thức)
                phuong_thuc = row[4] if len(row) > 4 else "Tiền mặt"
                ghi_chu = row[5] if len(row) > 5 else (row[4] if len(row) > 4 else "")

                if "Ngân hàng" in phuong_thuc:
                    total_bank += tien
                else:
                    total_cash += tien

                formatted_money = "{:,.0f}".format(tien)
            except Exception:
                formatted_money = row[3]
                phuong_thuc = row[4] if len(row) > 4 else ""
                ghi_chu = row[5] if len(row) > 5 else ""

            # Hiển thị 6 cột: ID, Ngày, Nguồn, Số tiền, Phương thức, Ghi chú
            self.view.tree.insert("", tk.END, values=(row[0], row[1], row[2], formatted_money, phuong_thuc, ghi_chu))

        # Cập nhật nhãn tổng
        if hasattr(self.view, 'lbl_total'):
            self.view.lbl_total.config(text=f"TỔNG THU: {total:,.0f} VND")
        if hasattr(self.view, 'lbl_bank'):
            self.view.lbl_bank.config(text=f"🏦 Ngân hàng: {total_bank:,.0f} đ")
        if hasattr(self.view, 'lbl_cash'):
            self.view.lbl_cash.config(text=f"💵 Tiền mặt: {total_cash:,.0f} đ")

    def filter_by_month(self, month, year):
        """Lọc theo tháng/năm và cập nhật lại tổng thu"""
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
        """Bảng điền thông tin khi THÊM mới"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Thêm Khoản Thu")
        dialog.geometry("380x350")
        dialog.grab_set()

        tk.Label(dialog, text="THÊM KHOẢN THU MỚI", font=("Arial", 12, "bold"), fg="#2ecc71").pack(pady=15)

        form = tk.Frame(dialog)
        form.pack(padx=20, fill="both", expand=True)

        tk.Label(form, text="Ngày (DD/MM/YYYY):").grid(row=0, column=0, sticky="w", pady=5)
        entry_ngay = tk.Entry(form, width=22)
        entry_ngay.insert(0, datetime.now().strftime("%d/%m/%Y"))
        entry_ngay.grid(row=0, column=1, pady=5)

        tk.Label(form, text="Nguồn thu nhập:").grid(row=1, column=0, sticky="w", pady=5)
        entry_nguon = tk.Entry(form, width=22)
        entry_nguon.grid(row=1, column=1, pady=5)

        tk.Label(form, text="Số tiền (VND):").grid(row=2, column=0, sticky="w", pady=5)
        entry_tien = tk.Entry(form, width=22)
        entry_tien.grid(row=2, column=1, pady=5)

        # Thêm Combobox Phương thức
        tk.Label(form, text="Phương thức:").grid(row=3, column=0, sticky="w", pady=5)
        combo_pt = ttk.Combobox(form, values=["Ngân hàng", "Tiền mặt"], width=19, state="readonly")
        combo_pt.current(0)  # Mặc định là Ngân hàng
        combo_pt.grid(row=3, column=1, pady=5)

        tk.Label(form, text="Ghi chú:").grid(row=4, column=0, sticky="w", pady=5)
        entry_gc = tk.Entry(form, width=22)
        entry_gc.grid(row=4, column=1, pady=5)

        def save():
            ngay = entry_ngay.get().strip()
            nguon = entry_nguon.get().strip()
            tien_str = entry_tien.get().strip()
            pt = combo_pt.get()
            gc = entry_gc.get().strip()

            if not nguon or not tien_str:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ nguồn thu và số tiền!", parent=dialog)
                return
            try:
                tien = float(tien_str)
            except ValueError:
                messagebox.showerror("Lỗi", "Số tiền phải là số hợp lệ!", parent=dialog)
                return

            self.model.add(ngay, nguon, tien, pt, gc)
            self.load_data()
            dialog.destroy()
            messagebox.showinfo("Thành công", "Đã thêm khoản thu mới thành công!")

        tk.Button(dialog, text="LƯU LẠI", bg="#2ecc71", fg="white", font=("Arial", 10, "bold"), width=15,
                  command=save).pack(pady=15)

    def show_edit_dialog(self):
        """Bảng chọn và sửa thông tin dòng dữ liệu hiện tại"""
        selected = self.view.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn 1 dòng khoản thu trên bảng để sửa!")
            return

        item_data = self.view.tree.item(selected)['values']
        income_id = item_data[0]

        dialog = tk.Toplevel(self.root)
        dialog.title("Sửa Khoản Thu")
        dialog.geometry("380x350")
        dialog.grab_set()

        tk.Label(dialog, text="CHỈNH SỬA KHOẢN THU", font=("Arial", 12, "bold"), fg="#3498db").pack(pady=15)

        form = tk.Frame(dialog)
        form.pack(padx=20, fill="both", expand=True)

        tk.Label(form, text="Ngày:").grid(row=0, column=0, sticky="w", pady=5)
        entry_ngay = tk.Entry(form, width=22)
        entry_ngay.insert(0, item_data[1])
        entry_ngay.grid(row=0, column=1, pady=5)

        tk.Label(form, text="Nguồn thu nhập:").grid(row=1, column=0, sticky="w", pady=5)
        entry_nguon = tk.Entry(form, width=22)
        entry_nguon.insert(0, item_data[2])
        entry_nguon.grid(row=1, column=1, pady=5)

        tk.Label(form, text="Số tiền (VND):").grid(row=2, column=0, sticky="w", pady=5)
        entry_tien = tk.Entry(form, width=22)
        entry_tien.insert(0, str(item_data[3]).replace(",", ""))
        entry_tien.grid(row=2, column=1, pady=5)

        # Thêm Combobox Phương thức
        tk.Label(form, text="Phương thức:").grid(row=3, column=0, sticky="w", pady=5)
        combo_pt = ttk.Combobox(form, values=["Ngân hàng", "Tiền mặt"], width=19, state="readonly")

        # Gán giá trị phương thức từ bảng vào Combobox (nếu có)
        pt_value = item_data[4] if len(item_data) > 4 else "Tiền mặt"
        combo_pt.set(pt_value)
        combo_pt.grid(row=3, column=1, pady=5)

        tk.Label(form, text="Ghi chú:").grid(row=4, column=0, sticky="w", pady=5)
        entry_gc = tk.Entry(form, width=22)
        gc_value = item_data[5] if len(item_data) > 5 else ""
        entry_gc.insert(0, gc_value)
        entry_gc.grid(row=4, column=1, pady=5)

        def update():
            ngay = entry_ngay.get().strip()
            nguon = entry_nguon.get().strip()
            tien_str = entry_tien.get().strip()
            pt = combo_pt.get()
            gc = entry_gc.get().strip()

            if not nguon or not tien_str:
                messagebox.showerror("Lỗi", "Không được bỏ trống dữ liệu!", parent=dialog)
                return
            try:
                tien = float(tien_str)
            except ValueError:
                messagebox.showerror("Lỗi", "Số tiền phải hợp lệ!", parent=dialog)
                return

            self.model.update(income_id, ngay, nguon, tien, pt, gc)
            self.load_data()
            dialog.destroy()
            messagebox.showinfo("Thành công", "Đã cập nhật khoản thu thành công!")

        tk.Button(dialog, text="CẬP NHẬT", bg="#3498db", fg="white", font=("Arial", 10, "bold"), width=15,
                  command=update).pack(pady=15)

    def delete_record(self):
        """Xử lý nút xóa dữ liệu trực tiếp"""
        selected = self.view.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn bản ghi cần xóa trên bảng!")
            return

        item_data = self.view.tree.item(selected)['values']
        income_id = item_data[0]

        confirm = messagebox.askyesno("Xác nhận xóa",
                                      f"Bồ có chắc chắn muốn xóa khoản thu nhập '{item_data[2]}' không?")
        if confirm:
            self.model.delete(income_id)
            self.load_data()
            messagebox.showinfo("Xóa thành công", "Đã gỡ bỏ bản ghi khỏi tệp data!")

    def show_search_dialog(self):
        """Bảng tìm kiếm thông tin nhanh"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Tìm Kiếm")
        dialog.geometry("350x180")
        dialog.grab_set()

        tk.Label(dialog, text="TÌM KIẾM KHOẢN THU", font=("Arial", 12, "bold"), fg="#f1c40f").pack(pady=15)

        frame = tk.Frame(dialog)
        frame.pack(padx=20, fill="x")

        tk.Label(frame, text="Nhập từ khóa cần tìm (Nguồn / Ghi chú):").pack(anchor="w", pady=2)
        entry_key = tk.Entry(frame, width=35)
        entry_key.pack(pady=5)

        def run_search():
            key = entry_key.get().strip().lower()
            all_records = self.model.get_all()
            # Cập nhật vị trí cột tìm kiếm cho khớp cấu trúc mới (Nguồn = index 2, Ghi chú = index 5)
            filtered = []
            for r in all_records:
                nguon = str(r[2]).lower() if len(r) > 2 else ""
                ghichu = str(r[5]).lower() if len(r) > 5 else ""
                if key in nguon or key in ghichu:
                    filtered.append(r)

            self.load_data(filtered)
            dialog.destroy()

        tk.Button(dialog, text="TÌM KIẾM", bg="#f1c40f", fg="black", font=("Arial", 10, "bold"), width=12,
                  command=run_search).pack(pady=10)