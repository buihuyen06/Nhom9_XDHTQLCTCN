import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from Models.chi import Chi_Model
from Models.ngansach import NganSach_Model  # Gọi model ngân sách để lấy số liệu tính toán thực tế


class Chi_Controller:
    def __init__(self, root):
        self.root = root
        self.model = Chi_Model()
        self.view = None

    def set_view(self, view):
        self.view = view
        self.load_data()

    # =========================================================
    # HÀM TỰ ĐỘNG KIỂM TRA HẠN MỨC ĐỂ HIỆN MESSAGEBOX
    # =========================================================
    def kiem_tra_va_canh_bao_ngan_sach(self, nguon_can_kiem_tra):
        """Kiểm tra số tiền còn lại của danh mục, nếu âm thì báo vượt hạn mức"""
        try:
            ns_model = NganSach_Model()
            # Lấy toàn bộ dữ liệu ngân sách kèm số tiền đã chi tiêu thực tế
            records = ns_model.get_all_with_spending()

            for row in records:
                # row[0] là Tên nguồn chi, row[3] là Số tiền còn lại
                if str(row[0]).strip().lower() == str(nguon_can_kiem_tra).strip().lower():
                    con_lai = float(row[3])
                    # Nếu số tiền còn lại bị nhỏ hơn 0 (bị âm) -> Báo vượt hạn mức liền
                    if con_lai < 0:
                        messagebox.showwarning(
                            "🚨 CẢNH BÁO VƯỢT HẠN MỨC",
                            f"Bạn đã vượt quá hạn mức chi tiêu cho phần '{row[0]}'!"
                        )
                    break
        except Exception:
            pass

    # =========================================================
    # HÀM LOAD DỮ LIỆU & TÍNH TỔNG TIỀN (KHỚP TÊN BIẾN VỚI VIEW)
    # =========================================================
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

        # Cập nhật nhãn hiển thị chính xác theo file khoanchi.py của bồ
        if hasattr(self.view, 'lbl_total'):
            self.view.lbl_total.config(text=f"TỔNG CHI: {tong_chi:,.0f} VND")
        if hasattr(self.view, 'lbl_bank'):
            self.view.lbl_bank.config(text=f"🏦 Ngân hàng: {tong_nh:,.0f} đ")
        if hasattr(self.view, 'lbl_cash'):
            self.view.lbl_cash.config(text=f"💵 Tiền mặt: {tong_tm:,.0f} đ")

    # =========================================================
    # CHỨC NĂNG: LỌC THEO THÁNG / NĂM
    # =========================================================
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
        """Lấy danh sách danh mục nạp vào Combobox"""
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

    # ==========================================
    # 1. CHỨC NĂNG: THÊM KHOẢN CHI MỚI
    # ==========================================
    def show_add_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Thêm Khoản Chi Mới")
        dialog.geometry("380x400")
        dialog.resizable(False, False)
        dialog.grab_set()

        tk.Label(dialog, text="THÊM KHOẢN CHI MỚI", font=("Arial", 12, "bold"), fg="#2ecc71").pack(pady=15)
        form = tk.Frame(dialog)
        form.pack(padx=20, fill="both", expand=True)

        tk.Label(form, text="Ngày (DD/MM/YYYY):").grid(row=0, column=0, sticky="w", pady=5)
        entry_ngay = tk.Entry(form, width=22)
        entry_ngay.insert(0, datetime.now().strftime("%d/%m/%Y"))
        entry_ngay.grid(row=0, column=1, pady=5)

        tk.Label(form, text="Nguồn chi:").grid(row=1, column=0, sticky="w", pady=5)
        danh_sach_nguon = self.get_danh_sach_nguon_chi()
        combo_nguon = ttk.Combobox(form, values=danh_sach_nguon, width=19, state="readonly")
        if danh_sach_nguon: combo_nguon.current(0)
        combo_nguon.grid(row=1, column=1, pady=5)

        tk.Label(form, text="Số tiền (VND):").grid(row=2, column=0, sticky="w", pady=5)
        entry_tien = tk.Entry(form, width=22)
        entry_tien.grid(row=2, column=1, pady=5)

        tk.Label(form, text="Phương thức:").grid(row=3, column=0, sticky="w", pady=5)
        combo_pt = ttk.Combobox(form, values=["Ngân hàng", "Tiền mặt"], width=19, state="readonly")
        combo_pt.current(0)
        combo_pt.grid(row=3, column=1, pady=5)

        tk.Label(form, text="Ghi chú:").grid(row=4, column=0, sticky="w", pady=5)
        entry_gc = tk.Entry(form, width=22)
        entry_gc.grid(row=4, column=1, pady=5)

        def save():
            ngay = entry_ngay.get().strip()
            nguon = combo_nguon.get()
            tien_str = entry_tien.get().strip()
            pt = combo_pt.get()
            gc = entry_gc.get().strip()

            if not tien_str:
                messagebox.showerror("Lỗi", "Vui lòng nhập số tiền!", parent=dialog)
                return
            try:
                if float(tien_str) < 0: raise ValueError
            except ValueError:
                messagebox.showerror("Lỗi", "Số tiền phải là số dương!", parent=dialog)
                return

            if hasattr(self.model, 'add'):
                self.model.add(ngay, nguon, tien_str, pt, gc)

            self.load_data()
            dialog.destroy()

            # 👇 ẤN LƯU XONG LÀ QUÉT KIỂM TRA VÀ HIỆN MESSAGE CẢNH BÁO LUÔN
            self.kiem_tra_va_canh_bao_ngan_sach(nguon)

        tk.Button(form, text="Lưu Lại", bg="#2ecc71", fg="white", font=("Arial", 10, "bold"),
                  command=save, width=15).grid(row=5, column=0, columnspan=2, pady=15)

    # ==========================================
    # 2. CHỨC NĂNG: CHỈNH SỬA KHOẢN CHI
    # ==========================================
    def show_edit_dialog(self):
        selected_item = self.view.tree.selection()
        if not selected_item:
            messagebox.showwarning("Nhắc nhở", "Vui lòng chọn một dòng để chỉnh sửa!")
            return

        item_data = self.view.tree.item(selected_item[0])['values']
        id_cu = str(item_data[0])

        dialog = tk.Toplevel(self.root)
        dialog.title("Chỉnh Sửa Khoản Chi")
        dialog.geometry("380x400")
        dialog.grab_set()

        tk.Label(dialog, text="CHỈNH SỬA KHOẢN CHI", font=("Arial", 12, "bold"), fg="#3498db").pack(pady=15)
        form = tk.Frame(dialog)
        form.pack(padx=20, fill="both", expand=True)

        tk.Label(form, text="Ngày (DD/MM/YYYY):").grid(row=0, column=0, sticky="w", pady=5)
        entry_ngay = tk.Entry(form, width=22)
        entry_ngay.insert(0, item_data[1])
        entry_ngay.grid(row=0, column=1, pady=5)

        tk.Label(form, text="Nguồn chi:").grid(row=1, column=0, sticky="w", pady=5)
        danh_sach_nguon = self.get_danh_sach_nguon_chi()
        combo_nguon = ttk.Combobox(form, values=danh_sach_nguon, width=19, state="readonly")
        combo_nguon.grid(row=1, column=1, pady=5)
        nguon_cu = str(item_data[2]).strip()
        if nguon_cu in danh_sach_nguon:
            combo_nguon.set(nguon_cu)
        else:
            combo_nguon['values'] = danh_sach_nguon + [nguon_cu]
            combo_nguon.set(nguon_cu)

        tk.Label(form, text="Số tiền (VND):").grid(row=2, column=0, sticky="w", pady=5)
        entry_tien = tk.Entry(form, width=22)
        entry_tien.insert(0, str(item_data[3]).replace(",", ""))
        entry_tien.grid(row=2, column=1, pady=5)

        tk.Label(form, text="Phương thức:").grid(row=3, column=0, sticky="w", pady=5)
        combo_pt = ttk.Combobox(form, values=["Ngân hàng", "Tiền mặt"], width=19, state="readonly")
        combo_pt.grid(row=3, column=1, pady=5)
        combo_pt.set(str(item_data[4]).strip())

        tk.Label(form, text="Ghi chú:").grid(row=4, column=0, sticky="w", pady=5)
        entry_gc = tk.Entry(form, width=22)
        entry_gc.insert(0, item_data[5] if str(item_data[5]) != 'None' else "")
        entry_gc.grid(row=4, column=1, pady=5)

        def save_edit():
            ngay = entry_ngay.get().strip()
            nguon = combo_nguon.get()
            tien_str = entry_tien.get().strip()
            pt = combo_pt.get()
            gc = entry_gc.get().strip()

            if not tien_str: return
            try:
                float(tien_str)
            except ValueError:
                return

            if hasattr(self.model, 'update'):
                self.model.update(id_cu, ngay, nguon, tien_str, pt, gc)

            self.load_data()
            dialog.destroy()

            # 👇 ẤN CẬP NHẬT XONG LÀ QUÉT KIỂM TRA VÀ HIỆN MESSAGE CẢNH BÁO LUÔN
            self.kiem_tra_va_canh_bao_ngan_sach(nguon)

        tk.Button(form, text="Cập Nhật", bg="#3498db", fg="white", font=("Arial", 10, "bold"),
                  command=save_edit, width=15).grid(row=5, column=0, columnspan=2, pady=15)

    # ==========================================
    # XÓA BẢN GHI & TÌM KIẾM POP-UP
    # ==========================================
    def delete_record(self):
        selected_item = self.view.tree.selection()
        if not selected_item:
            messagebox.showwarning("Nhắc nhở", "Vui lòng chọn dòng cần xóa!")
            return
        item_data = self.view.tree.item(selected_item[0])['values']
        id_xoa = str(item_data[0])
        if messagebox.askyesno("Xác nhận", "Bồ có chắc muốn xóa khoản chi này không?"):
            if hasattr(self.model, 'delete'): self.model.delete(id_xoa)
            self.load_data()

    def show_search_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Tìm Kiếm Khoản Chi")
        dialog.geometry("360x180")
        dialog.grab_set()
        form = tk.Frame(dialog, pady=15, padx=15)
        form.pack(fill="both", expand=True)
        tk.Label(form, text="Từ khóa:").grid(row=0, column=0, sticky="w")
        entry_keyword = tk.Entry(form, width=20)
        entry_keyword.grid(row=0, column=1, pady=5)

        def do_search():
            kw = entry_keyword.get().strip().lower()
            if hasattr(self.model, 'get_all'):
                filtered = [r for r in self.model.get_all() if kw in str(r[2]).lower() or kw in str(r[5]).lower()]
                self.load_data(filtered)
            dialog.destroy()

        tk.Button(form, text="Tìm Kiếm", bg="#e67e22", fg="white", command=do_search, width=12).grid(row=1, column=0,
                                                                                                     columnspan=2,
                                                                                                     pady=15)