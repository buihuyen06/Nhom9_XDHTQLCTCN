import tkinter as tk
from tkinter import messagebox


class AddNganSachDialog(tk.Toplevel):
    def __init__(self, parent, existing_names, save_callback):
        super().__init__(parent)
        self.existing_names = existing_names  # Danh sách tên nguồn chi đã có để kiểm tra trùng
        self.save_callback = save_callback

        self.title("➕ Thêm Ngân Sách Mới")
        self.geometry("320x200")
        self.resizable(False, False)
        self.grab_set()

        form = tk.Frame(self, padx=15, pady=15)
        form.pack(fill="both", expand=True)

        tk.Label(form, text="Nguồn chi:").grid(row=0, column=0, sticky="w", pady=8)
        self.entry_nguonchi = tk.Entry(form, width=20)
        self.entry_nguonchi.grid(row=0, column=1, pady=8)
        self.entry_nguonchi.focus()

        tk.Label(form, text="Hạn Mức (VND):").grid(row=1, column=0, sticky="w", pady=8)
        self.entry_limit = tk.Entry(form, width=20)
        self.entry_limit.grid(row=1, column=1, pady=8)

        tk.Button(form, text="➕ THÊM MỚI", bg="#2ecc71", fg="white", font=("Arial", 10, "bold"),
                  command=self.validate_and_save, width=12).grid(row=2, column=0, columnspan=2, pady=15)

    def validate_and_save(self):
        nguonchi = self.entry_nguonchi.get().strip()
        limit_str = self.entry_limit.get().strip()

        # Kiểm tra rỗng
        if not nguonchi or not limit_str:
            messagebox.showerror("Lỗi", "Vui lòng không bỏ trống thông tin!", parent=self)
            return

        # Kiểm tra số tiền hợp lệ
        try:
            limit = float(limit_str)
            if limit < 0: raise ValueError
        except ValueError:
            messagebox.showerror("Lỗi", "Hạn mức phải là số dương hợp lệ!", parent=self)
            return

        # Kiểm tra trùng lặp nguồn chi
        if nguonchi.lower() in self.existing_names:
            messagebox.showerror("Lỗi", f"Nguồn chi '{nguonchi}' đã tồn tại ngân sách!", parent=self)
            return

        # Trả dữ liệu sạch về Controller
        self.save_callback(nguonchi, limit)
        self.destroy()


class EditNganSachDialog(tk.Toplevel):
    def __init__(self, parent, nguonchi_cu, hanmuc_cu, update_callback):
        super().__init__(parent)
        self.nguonchi_cu = nguonchi_cu
        self.update_callback = update_callback

        self.title("🔧 Chỉnh Sửa Hạn Mức")
        self.geometry("320x200")
        self.resizable(False, False)
        self.grab_set()

        form = tk.Frame(self, padx=15, pady=15)
        form.pack(fill="both", expand=True)

        tk.Label(form, text="Nguồn chi:").grid(row=0, column=0, sticky="w", pady=8)
        lbl_nguonchi = tk.Label(form, text=nguonchi_cu, font=("Arial", 10, "bold"), fg="#2c3e50")
        lbl_nguonchi.grid(row=0, column=1, sticky="w", pady=8)

        tk.Label(form, text="Hạn Mức Mới:").grid(row=1, column=0, sticky="w", pady=8)
        self.entry_limit = tk.Entry(form, width=20)
        self.entry_limit.insert(0, hanmuc_cu)
        self.entry_limit.grid(row=1, column=1, pady=8)
        self.entry_limit.focus()

        tk.Button(form, text="💾 CẬP NHẬT", bg="#3498db", fg="white", font=("Arial", 10, "bold"),
                  command=self.validate_and_update, width=12).grid(row=2, column=0, columnspan=2, pady=15)

    def validate_and_update(self):
        limit_str = self.entry_limit.get().strip()

        try:
            limit = float(limit_str)
            if limit < 0: raise ValueError
        except ValueError:
            messagebox.showerror("Lỗi", "Hạn mức phải là số dương hợp lệ!", parent=self)
            return

        self.update_callback(self.nguonchi_cu, limit)
        self.destroy()