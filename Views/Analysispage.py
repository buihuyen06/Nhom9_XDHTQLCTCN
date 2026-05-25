import os
import sys
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

# --- SỬA LỖI ĐƯỜNG DẪN HỆ THỐNG ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)


class AnalysisPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#FFFFFF")
        self.ctrl = controller

        # Đường dẫn 2 file CSV
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.csv_path_thu = os.path.join(base_dir, "main", "giaodichthu.csv")
        self.csv_path_chi = os.path.join(base_dir, "main", "giaodichchi.csv")

        # --- 1. TIÊU ĐỀ TRANG ---
        tk.Label(
            self, text="📊 TỔNG KẾT THU CHI", font=("Arial", 18, "bold"), fg="#1E88E5", bg="#FFFFFF"
        ).pack(pady=15)

        # --- 2. BA KHUNG HIỂN THỊ TỔNG TIỀN ---
        summary_frame = tk.Frame(self, bg="#FFFFFF")
        summary_frame.pack(pady=10)

        # Cột Thu Nhập
        frame_thu = tk.Frame(summary_frame, bg="#E8F5E9", padx=20, pady=10)
        frame_thu.grid(row=0, column=0, padx=10)
        tk.Label(frame_thu, text="Tổng Thu (VNĐ)", bg="#E8F5E9", fg="#2E7D32").pack()
        self.lbl_thu = tk.Label(frame_thu, text="0", font=("Arial", 14, "bold"), bg="#E8F5E9", fg="#1B5E20")
        self.lbl_thu.pack()

        # Cột Chi Tiêu
        frame_chi = tk.Frame(summary_frame, bg="#FFEBEE", padx=20, pady=10)
        frame_chi.grid(row=0, column=1, padx=10)
        tk.Label(frame_chi, text="Tổng Chi (VNĐ)", bg="#FFEBEE", fg="#C62828").pack()
        self.lbl_chi = tk.Label(frame_chi, text="0", font=("Arial", 14, "bold"), bg="#FFEBEE", fg="#B71C1C")
        self.lbl_chi.pack()

        # Cột Số Dư
        frame_sodu = tk.Frame(summary_frame, bg="#E3F2FD", padx=20, pady=10)
        frame_sodu.grid(row=0, column=2, padx=10)
        tk.Label(frame_sodu, text="Số Dư (VNĐ)", bg="#E3F2FD", fg="#1565C0").pack()
        self.lbl_sodu = tk.Label(frame_sodu, text="0", font=("Arial", 14, "bold"), bg="#E3F2FD", fg="#0D47A1")
        self.lbl_sodu.pack()

        # --- 3. BẢNG THỐNG KÊ CHI TIẾT ---
        tk.Label(self, text="CHI TIẾT CÁC MỤC ĐÃ TIÊU TIỀN", font=("Arial", 12, "bold"), bg="#FFFFFF",
                 fg="#333333").pack(pady=10)

        columns = ("danhmuc", "tongtien")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=8)
        self.tree.heading("danhmuc", text="Tên Danh Mục")
        self.tree.heading("tongtien", text="Tổng Tiền (VNĐ)")

        self.tree.column("danhmuc", width=250, anchor="w")
        self.tree.column("tongtien", width=200, anchor="e")
        self.tree.pack(pady=5)

        # --- 4. CÁC NÚT BẤM ---
        btn_frame = tk.Frame(self, bg="#FFFFFF")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="🔄 TẢI LẠI DỮ LIỆU", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), width=20,
                  command=self.load_data).pack(side="left", padx=10)
        tk.Button(btn_frame, text="🏠 VỀ TRANG CHỦ", bg="#2196F3", fg="white", font=("Arial", 10, "bold"), width=20,
                  command=lambda: self.ctrl.show("HomePage")).pack(side="left", padx=10)

        # Tự động nạp dữ liệu khi mở trang
        self.load_data()

    def load_data(self):
        """Hàm đọc file và tính toán con số hiển thị"""
        tong_thu = 0
        tong_chi = 0
        df_chi = pd.DataFrame()

        # 1. Đọc và cộng tổng file Thu
        if os.path.exists(self.csv_path_thu):
            try:
                df_thu = pd.read_csv(self.csv_path_thu)
                tong_thu = df_thu["sotien"].sum()
            except:
                pass

        # 2. Đọc và cộng tổng file Chi
        if os.path.exists(self.csv_path_chi):
            try:
                df_chi = pd.read_csv(self.csv_path_chi)
                tong_chi = df_chi["sotien"].sum()
            except:
                pass

        # 3. Tính số dư và Cập nhật Text
        so_du = tong_thu - tong_chi
        self.lbl_thu.config(text=f"{int(tong_thu):,}")
        self.lbl_chi.config(text=f"{int(tong_chi):,}")
        self.lbl_sodu.config(text=f"{int(so_du):,}")
        self.lbl_sodu.config(fg="red" if so_du < 0 else "blue")  # Báo đỏ nếu âm tiền

        # 4. Gom nhóm dữ liệu đưa lên bảng (Chỉ tập trung phân tích Chi Tiêu cho đơn giản)
        for row in self.tree.get_children():
            self.tree.delete(row)

        if not df_chi.empty and "danhmucchi" in df_chi.columns:
            # Lệnh groupby: Gộp các danh mục giống nhau và cộng dồn số tiền
            df_gop = df_chi.groupby("danhmucchi")["sotien"].sum().reset_index()

            # Đẩy từng dòng dữ liệu đã gộp lên bảng
            for _, row in df_gop.iterrows():
                self.tree.insert("", "end", values=(
                    row["danhmucchi"],
                    f"{int(row['sotien']):,}"
                ))