import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class AddChiDialog(tk.Toplevel):
    def __init__(self, parent, danh_sach_nguon, save_callback):
        super().__init__(parent)
        self.save_callback = save_callback
        self.title("Thêm Khoản Chi Mới")
        self.geometry("380x400")
        self.resizable(False, False)
        self.grab_set()

        tk.Label(self, text="THÊM KHOẢN CHI MỚI", font=("Arial", 12, "bold"), fg="#2ecc71").pack(pady=15)
        form = tk.Frame(self)
        form.pack(padx=20, fill="both", expand=True)

        tk.Label(form, text="Ngày (DD/MM/YYYY):").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_ngay = tk.Entry(form, width=22)
        self.entry_ngay.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.entry_ngay.grid(row=0, column=1, pady=5)

        tk.Label(form, text="Nguồn chi:").grid(row=1, column=0, sticky="w", pady=5)
        self.combo_nguon = ttk.Combobox(form, values=danh_sach_nguon, width=19, state="readonly")
        if danh_sach_nguon: self.combo_nguon.current(0)
        self.combo_nguon.grid(row=1, column=1, pady=5)

        tk.Label(form, text="Số tiền (VND):").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_tien = tk.Entry(form, width=22)
        self.entry_tien.grid(row=2, column=1, pady=5)

        tk.Label(form, text="Phương thức:").grid(row=3, column=0, sticky="w", pady=5)
        self.combo_pt = ttk.Combobox(form, values=["Ngân hàng", "Tiền mặt"], width=19, state="readonly")
        self.combo_pt.current(0)
        self.combo_pt.grid(row=3, column=1, pady=5)

        tk.Label(form, text="Ghi chú:").grid(row=4, column=0, sticky="w", pady=5)
        self.entry_gc = tk.Entry(form, width=22)
        self.entry_gc.grid(row=4, column=1, pady=5)

        tk.Button(form, text="Lưu Lại", bg="#2ecc71", fg="white", font=("Arial", 10, "bold"),
                  command=self.validate_and_save, width=15).grid(row=5, column=0, columnspan=2, pady=15)

    def validate_and_save(self):
        ngay, nguon, tien_str = self.entry_ngay.get().strip(), self.combo_nguon.get(), self.entry_tien.get().strip()
        pt, gc = self.combo_pt.get(), self.entry_gc.get().strip()

        if not tien_str:
            messagebox.showerror("Lỗi", "Vui lòng nhập số tiền!", parent=self)
            return
        try:
            if float(tien_str) < 0: raise ValueError
        except ValueError:
            messagebox.showerror("Lỗi", "Số tiền phải là số dương!", parent=self)
            return

        self.save_callback(ngay, nguon, tien_str, pt, gc)
        self.destroy()

class EditChiDialog(tk.Toplevel):
    def __init__(self, parent, item_data, danh_sach_nguon, update_callback):
        super().__init__(parent)
        self.update_callback = update_callback
        self.id_cu = str(item_data[0])
        self.title("Chỉnh Sửa Khoản Chi")
        self.geometry("380x400")
        self.grab_set()

        tk.Label(self, text="CHỈNH SỬA KHOẢN CHI", font=("Arial", 12, "bold"), fg="#3498db").pack(pady=15)
        form = tk.Frame(self)
        form.pack(padx=20, fill="both", expand=True)

        tk.Label(form, text="Ngày:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_ngay = tk.Entry(form, width=22)
        self.entry_ngay.insert(0, item_data[1])
        self.entry_ngay.grid(row=0, column=1, pady=5)

        tk.Label(form, text="Nguồn chi:").grid(row=1, column=0, sticky="w", pady=5)
        nguon_cu = str(item_data[2]).strip()
        self.combo_nguon = ttk.Combobox(form, values=danh_sach_nguon if nguon_cu in danh_sach_nguon else danh_sach_nguon + [nguon_cu], width=19, state="readonly")
        self.combo_nguon.set(nguon_cu)
        self.combo_nguon.grid(row=1, column=1, pady=5)

        tk.Label(form, text="Số tiền:").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_tien = tk.Entry(form, width=22)
        self.entry_tien.insert(0, str(item_data[3]).replace(",", ""))
        self.entry_tien.grid(row=2, column=1, pady=5)

        tk.Label(form, text="Phương thức:").grid(row=3, column=0, sticky="w", pady=5)
        self.combo_pt = ttk.Combobox(form, values=["Ngân hàng", "Tiền mặt"], width=19, state="readonly")
        self.combo_pt.set(str(item_data[4]).strip())
        self.combo_pt.grid(row=3, column=1, pady=5)

        tk.Label(form, text="Ghi chú:").grid(row=4, column=0, sticky="w", pady=5)
        self.entry_gc = tk.Entry(form, width=22)
        self.entry_gc.insert(0, item_data[5] if str(item_data[5]) != 'None' else "")
        self.entry_gc.grid(row=4, column=1, pady=5)

        tk.Button(form, text="Cập Nhật", bg="#3498db", fg="white", font=("Arial", 10, "bold"),
                  command=self.validate_and_update, width=15).grid(row=5, column=0, columnspan=2, pady=15)

    def validate_and_update(self):
        ngay, nguon, tien_str = self.entry_ngay.get().strip(), self.combo_nguon.get(), self.entry_tien.get().strip()
        pt, gc = self.combo_pt.get(), self.entry_gc.get().strip()

        if not tien_str: return
        try: float(tien_str)
        except ValueError: return

        self.update_callback(self.id_cu, ngay, nguon, tien_str, pt, gc)
        self.destroy()

class SearchDialog(tk.Toplevel):
    def __init__(self, parent, search_callback):
        super().__init__(parent)
        self.search_callback = search_callback
        self.title("Tìm Kiếm")
        self.geometry("360x180")
        self.grab_set()

        form = tk.Frame(self, pady=15, padx=15)
        form.pack(fill="both", expand=True)
        tk.Label(form, text="Từ khóa:").grid(row=0, column=0, sticky="w")
        self.entry_keyword = tk.Entry(form, width=20)
        self.entry_keyword.grid(row=0, column=1, pady=5)

        tk.Button(form, text="Tìm Kiếm", bg="#e67e22", fg="white", command=self.run_search, width=12).grid(row=1, column=0, columnspan=2, pady=15)

    def run_search(self):
        self.search_callback(self.entry_keyword.get())
        self.destroy()