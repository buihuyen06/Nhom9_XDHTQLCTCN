import os
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class InputPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#FFFFFF")
        self.ctrl = controller

        # --- ĐỊNH VỊ ĐƯỜNG DẪN VÀ KHỞI TẠO 2 FILE CSV TÁCH BIỆT ---
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Đường dẫn tới file Thu nhập và file Chi tiêu
        self.csv_path_thu = os.path.join(base_dir, "main", "giaodichthu.csv")
        self.csv_path_chi = os.path.join(base_dir, "main", "giaodichchi.csv")

        # Tiêu đề cột chuẩn cho cả 2 file
        self.title_columns = ["danhmucchi", "pttt", "sotien", "ngagiaodich", "ghichu"]

        # Tự động tạo thư mục main nếu chưa có
        os.makedirs(os.path.dirname(self.csv_path_thu), exist_ok=True)

        # Khởi tạo file Thu nhập nếu chưa tồn tại
        if not os.path.exists(self.csv_path_thu):
            df_init_thu = pd.DataFrame(columns=self.title_columns)
            df_init_thu.to_csv(self.csv_path_thu, index=False)

        # Khởi tạo file Chi tiêu nếu chưa tồn tại
        if not os.path.exists(self.csv_path_chi):
            df_init_chi = pd.DataFrame(columns=self.title_columns)
            df_init_chi.to_csv(self.csv_path_chi, index=False)

        # Kho dữ liệu danh mục để thay đổi động
        self.DATA_DANH_MUC = {
            "Chi tiêu": ["Ăn uống", "Đi lại / Xăng xe", "Mua sắm", "Học tập", "Tiền nhà / Điện nước", "Giải trí",
                         "Khác"],
            "Thu nhập": ["Nhận lương", "Tiền thưởng", "Được cho/Tặng", "Đầu tư / Tiết kiệm", "Kinh doanh phụ", "Khác"]
        }

        # --- 1. HEADER BANNER ---
        header_frame = tk.Frame(self, bg="#FCE4EC", height=100)
        header_frame.pack(fill="x", padx=15, pady=10)
        header_frame.pack_propagate(False)

        lbl_quote = tk.Label(
            header_frame,
            text="Mọi số tiền tiết kiệm\nlà một số tiền kiếm được 🐾",
            font=("Arial", 14, "italic", "bold"),
            fg="#D81B60",
            bg="#FCE4EC"
        )
        lbl_quote.pack(side="left", padx=30, pady=15)

        # --- 2. FORM NHẬP LIỆU GIAO DỊCH ---
        form_frame = tk.LabelFrame(
            self,
            text=" GHI CHÉP THU CHI ",
            font=("Arial", 11, "bold"),
            bg="#FFFFFF",
            fg="#333333",
            padx=20,
            pady=15
        )
        form_frame.pack(padx=15, pady=5, fill="x")

        # --- HÀNG 0: Phân loại (Thu hay Chi) ---
        tk.Label(form_frame, text="Phân loại:", bg="#FFFFFF", font=("Arial", 10)).grid(row=0, column=0, sticky="w",
                                                                                       pady=8)
        self.cb_phanloai = ttk.Combobox(
            form_frame,
            values=["Chi tiêu", "Thu nhập"],
            width=25,
            state="readonly"
        )
        self.cb_phanloai.current(0)  # Mặc định là Chi tiêu
        self.cb_phanloai.grid(row=0, column=1, padx=10, pady=8)
        # Lắng nghe sự kiện đổi phân loại để cập nhật danh mục động
        self.cb_phanloai.bind("<<ComboboxSelected>>", self.thay_doi_danh_muc)

        # --- HÀNG 1: Danh mục & Phương thức thanh toán ---
        tk.Label(form_frame, text="Danh mục:", bg="#FFFFFF", font=("Arial", 10)).grid(row=1, column=0, sticky="w",
                                                                                      pady=8)
        self.cb_danhmuc = ttk.Combobox(form_frame, width=25, state="readonly")
        self.cb_danhmuc.grid(row=1, column=1, padx=10, pady=8)

        # Gọi hàm nạp danh mục Chi tiêu lên trước
        self.thay_doi_danh_muc()

        tk.Label(form_frame, text="Phương thức TT:", bg="#FFFFFF", font=("Arial", 10)).grid(row=1, column=2, sticky="w",
                                                                                            pady=8, padx=(20, 0))
        self.cb_pttt = ttk.Combobox(
            form_frame,
            values=["Tiền mặt", "Chuyển khoản (Bank)", "Ví điện tử (Momo/ZaloPay)", "Thẻ tín dụng"],
            width=25,
            state="readonly"
        )
        self.cb_pttt.current(0)
        self.cb_pttt.grid(row=1, column=3, padx=10, pady=8)

        # --- HÀNG 2: Số tiền & Ngày giao dịch ---
        tk.Label(form_frame, text="Số tiền (VNĐ):", bg="#FFFFFF", font=("Arial", 10)).grid(row=2, column=0, sticky="w",
                                                                                           pady=8)
        self.ent_sotien = tk.Entry(form_frame, width=28, font=("Arial", 10))
        self.ent_sotien.grid(row=2, column=1, padx=10, pady=8)

        tk.Label(form_frame, text="Ngày giao dịch:", bg="#FFFFFF", font=("Arial", 10)).grid(row=2, column=2, sticky="w",
                                                                                            pady=8, padx=(20, 0))
        self.ent_ngay = tk.Entry(form_frame, width=28, font=("Arial", 10))
        self.ent_ngay.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.ent_ngay.grid(row=2, column=3, padx=10, pady=8)

        # --- HÀNG 3: Ghi chú ---
        tk.Label(form_frame, text="Ghi chú:", bg="#FFFFFF", font=("Arial", 10)).grid(row=3, column=0, sticky="w",
                                                                                     pady=8)
        self.ent_ghichu = tk.Entry(form_frame, width=71, font=("Arial", 10))
        self.ent_ghichu.grid(row=3, column=1, columnspan=3, padx=10, pady=8, sticky="w")

        # --- 3. KHUNG CHỨA CÁC NÚT BẤM ---
        btn_frame = tk.Frame(self, bg="#FFFFFF")
        btn_frame.pack(pady=20)

        btn_save = tk.Button(
            btn_frame,
            text="✅ LƯU GIAO DỊCH",
            bg="#4CAF50",
            fg="white",
            font=("Arial", 11, "bold"),
            width=18,
            height=2,
            command=self.save_data
        )
        btn_save.pack(side="left", padx=15)

        btn_back = tk.Button(
            btn_frame,
            text="🏠 VỀ TRANG CHỦ",
            bg="#2196F3",
            fg="white",
            font=("Arial", 11, "bold"),
            width=18,
            height=2,
            command=lambda: self.ctrl.show("HomePage")
        )
        btn_back.pack(side="left", padx=15)

    def thay_doi_danh_muc(self, event=None):
        """Hàm xử lý cập nhật danh mục động dựa trên việc chọn Thu nhập hay Chi tiêu"""
        loai_da_chon = self.cb_phanloai.get()
        danh_sach_moi = self.DATA_DANH_MUC[loai_da_chon]
        self.cb_danhmuc["values"] = danh_sach_moi
        self.cb_danhmuc.current(0)  # Tự chọn mục đầu tiên

    def save_data(self):
        """Hàm xử lý lưu dữ liệu động bằng Pandas vào 2 file CSV riêng biệt"""
        phanloai = self.cb_phanloai.get()
        danhmucchi = self.cb_danhmuc.get()
        pttt = self.cb_pttt.get()
        sotien = self.ent_sotien.get().strip()
        ngagiaodich = self.ent_ngay.get().strip()
        ghichu = self.ent_ghichu.get().strip()

        if not sotien:
            messagebox.showwarning("Nhập thiếu", "Vui lòng nhập số tiền!")
            return

        try:
            val_sotien = float(sotien)
        except ValueError:
            messagebox.showerror("Sai định dạng", "Số tiền nhập vào phải là số!")
            return

        # --- RẼ NHÁNH ĐƯỜNG DẪN FILE DỰA TRÊN PHÂN LOẠI ---
        if phanloai == "Thu nhập":
            target_csv = self.csv_path_thu
        else:
            target_csv = self.csv_path_chi

        try:
            # Bước 1: Đọc file CSV mục tiêu (Thu hoặc Chi) lên RAM
            if os.path.exists(target_csv):
                df_old = pd.read_csv(target_csv)
            else:
                df_old = pd.DataFrame(columns=self.title_columns)

            # Bước 2: Đóng gói dòng dữ liệu mới (Không cần thêm chuỗi [Thu]/[Chi] vì file đã tách biệt)
            new_row_data = {
                "danhmucchi": [danhmucchi],
                "pttt": [pttt],
                "sotien": [val_sotien],
                "ngagiaodich": [ngagiaodich],
                "ghichu": [ghichu]
            }
            df_new_row = pd.DataFrame(new_row_data)

            # Bước 3: Nối dòng mới và xuất ghi đè lại file tương ứng
            df_updated = pd.concat([df_old, df_new_row], ignore_index=True)
            df_updated.to_csv(target_csv, index=False)

            # --- THÔNG BÁO VÀ LÀM SẠCH GIAO DIỆN ---
            file_name_display = "giaodichthu.csv" if phanloai == "Thu nhập" else "giaodichchi.csv"
            messagebox.showinfo("Thành công", f"Đã ghi nhận khoản {phanloai} và lưu vào file '{file_name_display}'!")

            self.ent_sotien.delete(0, 'end')
            self.ent_ghichu.delete(0, 'end')

        except Exception as e:
            messagebox.showerror("Lỗi hệ thống", f"Không thể ghi dữ liệu!\nChi tiết: {str(e)}")