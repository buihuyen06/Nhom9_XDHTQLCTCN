import os
import sys
import tkinter as tk
from tkinter import ttk
from Models.HistoryModel import HistoryModel
# --- SỬA LỖI ĐƯỜNG DẪN (MODULE NOT FOUND) ---
# Đoạn code này tự động tìm và nạp thư mục gốc vào hệ thống để Python luôn thấy thư mục 'Models'
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import class HistoryModel từ package Models vừa được sửa đường dẫn

class HistoryPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#E3F2FD")
        self.ctrl = controller

        # --- 1. TIÊU ĐỀ TRANG ---
        tk.Label(
            self,
            text="📋 LỊCH SỬ GIAO DỊCH",
            font=("Arial", 18, "bold"),
            fg="#1E88E5",
            bg="#E3F2FD"
        ).pack(pady=15)

        # --- 2. BẢNG HIỂN THỊ DỮ LIỆU (TREEVIEW) ---
        # Khung chứa bảng và thanh cuộn
        table_frame = tk.Frame(self)
        table_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Khởi tạo bảng với 5 cột tương ứng với cấu trúc dữ liệu
        columns = ("ngay", "phanloai", "hangmuc", "sotien", "ghichu")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

        # Định nghĩa tiêu đề hiển thị dạng tiếng Việt trên giao diện
        self.tree.heading("ngay", text="Ngày")
        self.tree.heading("phanloai", text="Phân Loại")
        self.tree.heading("hangmuc", text="Hạng Mục")
        self.tree.heading("sotien", text="Số Tiền")
        self.tree.heading("ghichu", text="Ghi Chú")

        # Cấu hình độ rộng và căn lề chữ cho các cột
        self.tree.column("ngay", width=90, anchor="center")
        self.tree.column("phanloai", width=90, anchor="center")
        self.tree.column("hangmuc", width=110, anchor="w")  # w = west (căn trái)
        self.tree.column("sotien", width=90, anchor="e")    # e = east (căn phải cho tiền tệ)
        self.tree.column("ghichu", width=150, anchor="w")

        # Tạo thanh cuộn dọc (Scrollbar) kết nối trực tiếp với bảng
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Sắp xếp hiển thị bảng bên trái, thanh cuộn bên phải
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- 3. NÚT ĐIỀU HƯỚNG QUAY LẠI ---
        tk.Button(
            self,
            text="🏠 QUAY LẠI TRANG CHỦ",
            font=("Arial", 11, "bold"),
            bg="#2196F3",
            fg="white",
            padx=15,
            pady=7,
            command=lambda: self.ctrl.show("HomePage")
        ).pack(pady=15)

    def load_data_to_table(self, text_records):
        """
        Hàm nạp dữ liệu: Nhận danh sách giao dịch (List of Dictionaries từ Model)
        và đổ dữ liệu động lên bảng Treeview.
        """
        # Bước 1: Xóa sạch toàn bộ các dòng cũ đang có trên bảng để làm mới dữ liệu
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Bước 2: Duyệt qua danh sách và chèn từng dòng mới vào cuối bảng
        for record in text_records:
            self.tree.insert("", "end", values=(
                record.get("ngay", ""),
                record.get("phanloai", ""),
                record.get("hangmuc", ""),
                record.get("sotien", ""),
                record.get("ghichu", "")
            ))