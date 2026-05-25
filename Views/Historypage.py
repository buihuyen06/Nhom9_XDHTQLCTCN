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


class HistoryPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#E3F2FD")
        self.ctrl = controller

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.csv_path_thu = os.path.join(base_dir, "main", "giaodichthu.csv")
        self.csv_path_chi = os.path.join(base_dir, "main", "giaodichchi.csv")

        self.current_view = "Chi tiêu"

        # --- 1. TIÊU ĐỀ TRANG ---
        self.lbl_title = tk.Label(self, text="📋 LỊCH SỬ GIAO DỊCH (CHI TIÊU)", font=("Arial", 18, "bold"), fg="#1E88E5",
                                  bg="#E3F2FD")
        self.lbl_title.pack(pady=10)

        # --- 2. THANH CÔNG CỤ: CHUYỂN ĐỔI & TÌM KIẾM ---
        toolbar_frame = tk.Frame(self, bg="#E3F2FD")
        toolbar_frame.pack(pady=5, fill="x", padx=20)

        self.btn_view_chi = tk.Button(toolbar_frame, text="💸 XEM KHOẢN CHI", font=("Arial", 10, "bold"), bg="#F44336",
                                      fg="white", command=lambda: self.switch_view("Chi tiêu"))
        self.btn_view_chi.pack(side="left", padx=5)

        self.btn_view_thu = tk.Button(toolbar_frame, text="💰 XEM KHOẢN THU", font=("Arial", 10, "bold"), bg="#4CAF50",
                                      fg="white", command=lambda: self.switch_view("Thu nhập"))
        self.btn_view_thu.pack(side="left", padx=5)

        tk.Button(toolbar_frame, text="🔍 TÌM", bg="#FFC107", font=("Arial", 10, "bold"), command=self.search_data).pack(
            side="right", padx=5)
        self.ent_search = tk.Entry(toolbar_frame, width=25, font=("Arial", 11))
        self.ent_search.pack(side="right", padx=5)
        tk.Label(toolbar_frame, text="Tìm kiếm (Danh mục/Ghi chú):", bg="#E3F2FD").pack(side="right")

        # --- 3. BẢNG HIỂN THỊ DỮ LIỆU (TREEVIEW) ---
        table_frame = tk.Frame(self)
        table_frame.pack(padx=20, pady=5, fill="both", expand=True)

        columns = ("ngay", "pttt", "danhmuc", "sotien", "ghichu")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

        self.tree.heading("ngay", text="Ngày GD")
        self.tree.heading("pttt", text="Phương Thức TT")
        self.tree.heading("danhmuc", text="Danh Mục")
        self.tree.heading("sotien", text="Số Tiền")
        self.tree.heading("ghichu", text="Ghi Chú")

        self.tree.column("ngay", width=90, anchor="center")
        self.tree.column("pttt", width=130, anchor="center")
        self.tree.column("danhmuc", width=140, anchor="w")
        self.tree.column("sotien", width=110, anchor="e")
        self.tree.column("ghichu", width=150, anchor="w")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- 4. THANH CÔNG CỤ: THÊM / SỬA / XÓA ---
        action_frame = tk.Frame(self, bg="#E3F2FD")
        action_frame.pack(pady=10)

        tk.Button(action_frame, text="➕ THÊM MỚI", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), width=15,
                  command=lambda: self.ctrl.show("InputPage")).pack(side="left", padx=10)
        tk.Button(action_frame, text="✏️ SỬA DÒNG", bg="#FF9800", fg="white", font=("Arial", 10, "bold"), width=15,
                  command=self.edit_transaction).pack(side="left", padx=10)
        tk.Button(action_frame, text="🗑️ XÓA DÒNG", bg="#F44336", fg="white", font=("Arial", 10, "bold"), width=15,
                  command=self.delete_transaction).pack(side="left", padx=10)

        tk.Button(self, text="🏠 QUAY LẠI TRANG CHỦ", font=("Arial", 11, "bold"), bg="#2196F3", fg="white", padx=15,
                  pady=5, command=lambda: self.ctrl.show("HomePage")).pack(pady=5)

    def switch_view(self, view_type):
        """Đổi chế độ xem Thu hoặc Chi"""
        self.current_view = view_type
        if view_type == "Thu nhập":
            self.lbl_title.config(text="📋 LỊCH SỬ GIAO DỊCH (THU NHẬP)", fg="#2E7D32")
        else:
            self.lbl_title.config(text="📋 LỊCH SỬ GIAO DỊCH (CHI TIÊU)", fg="#1E88E5")
        self.load_data_from_csv()

    def search_data(self):
        keyword = self.ent_search.get().strip().lower()
        self.load_data_from_csv(search_keyword=keyword)

    def load_data_from_csv(self, search_keyword=""):
        """Đọc và nạp dữ liệu từ file CSV lên Treeview"""
        for row in self.tree.get_children():
            self.tree.delete(row)

        target_csv = self.csv_path_thu if self.current_view == "Thu nhập" else self.csv_path_chi

        if os.path.exists(target_csv):
            try:
                df = pd.read_csv(target_csv)
                df = df.fillna("")

                for idx, row in df.iterrows():
                    if search_keyword:
                        dm = str(row.get("danhmucchi", "")).lower()
                        gc = str(row.get("ghichu", "")).lower()
                        if search_keyword not in dm and search_keyword not in gc:
                            continue

                    try:
                        formatted_money = f"{int(float(row['sotien'])):,}"
                    except:
                        formatted_money = str(row['sotien'])

                    # Chèn iid bằng đúng số thứ tự dòng để Sửa/Xóa chính xác
                    self.tree.insert("", "end", iid=str(idx), values=(
                        row.get("ngagiaodich", ""),
                        row.get("pttt", ""),
                        row.get("danhmucchi", ""),
                        formatted_money,
                        row.get("ghichu", "")
                    ))
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể đọc file: {str(e)}")

    def delete_transaction(self):
        """Xóa dòng dữ liệu và lưu ngay vào CSV"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Chưa chọn", "Vui lòng click chọn một dòng trên bảng để xóa!")
            return

        # Lấy chính xác Index của dòng trong Pandas
        row_index = int(selected_item[0])

        if messagebox.askyesno("Xác nhận",
                               "Bạn có chắc chắn muốn xóa giao dịch này? Hành động này không thể hoàn tác."):
            target_csv = self.csv_path_thu if self.current_view == "Thu nhập" else self.csv_path_chi
            try:
                df = pd.read_csv(target_csv)
                df = df.drop(index=row_index)  # Xóa dòng
                df.to_csv(target_csv, index=False)  # Lưu đè file

                messagebox.showinfo("Thành công", "Đã xóa giao dịch khỏi cơ sở dữ liệu!")
                self.load_data_from_csv()  # Tải lại bảng để cập nhật UI
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa dữ liệu: {str(e)}")

    def edit_transaction(self):
        """Mở cửa sổ sửa và lưu đè trực tiếp vào CSV"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Chưa chọn", "Vui lòng click chọn một dòng trên bảng để sửa!")
            return

        row_index = int(selected_item[0])
        target_csv = self.csv_path_thu if self.current_view == "Thu nhập" else self.csv_path_chi

        try:
            df = pd.read_csv(target_csv)
            old_data = df.loc[row_index]  # Lấy dữ liệu cũ theo Index
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi đọc dữ liệu từ file CSV: {str(e)}")
            return

        # --- Tạo Cửa Sổ Nhập Liệu (Popup) ---
        popup = tk.Toplevel(self)
        popup.title("Sửa Giao Dịch")
        popup.geometry("350x320")
        popup.config(bg="#FFFFFF")
        popup.grab_set()

        tk.Label(popup, text="SỬA THÔNG TIN", font=("Arial", 12, "bold"), bg="#FFFFFF").grid(row=0, column=0,
                                                                                             columnspan=2, pady=10)

        labels = ["Ngày GD:", "Phương thức TT:", "Danh mục:", "Số tiền:", "Ghi chú:"]
        entries = []

        for i, lbl_text in enumerate(labels):
            tk.Label(popup, text=lbl_text, bg="#FFFFFF").grid(row=i + 1, column=0, sticky="w", padx=15, pady=5)
            ent = tk.Entry(popup, width=25)
            ent.grid(row=i + 1, column=1, padx=5, pady=5)
            entries.append(ent)

        # Đổ dữ liệu cũ vào form (ép kiểu về string để hiển thị an toàn)
        entries[0].insert(0, str(old_data.get("ngagiaodich", "")))
        entries[1].insert(0, str(old_data.get("pttt", "")))
        entries[2].insert(0, str(old_data.get("danhmucchi", "")))
        # Hiển thị số tiền thô (không có dấu phẩy) để người dùng dễ sửa
        entries[3].insert(0, str(int(float(old_data.get("sotien", 0)))))
        entries[4].insert(0, str(old_data.get("ghichu", "")))

        def save_edit():
            try:
                # 1. Thu thập dữ liệu mới
                ngay_moi = entries[0].get().strip()
                pttt_moi = entries[1].get().strip()
                dm_moi = entries[2].get().strip()

                # 2. Xử lý bảo mật số tiền: Loại bỏ toàn bộ dấu phẩy, khoảng trắng trước khi chuyển thành số
                tien_str = entries[3].get().strip().replace(",", "").replace(".", "")
                tien_moi = float(tien_str)

                gc_moi = entries[4].get().strip()

                # 3. Ghi đè vào DataFrame tại chính xác dòng (row_index) đó bằng hàm `.loc`
                df.loc[row_index, "ngagiaodich"] = ngay_moi
                df.loc[row_index, "pttt"] = pttt_moi
                df.loc[row_index, "danhmucchi"] = dm_moi
                df.loc[row_index, "sotien"] = tien_moi
                df.loc[row_index, "ghichu"] = gc_moi

                # 4. BẤM NÚT LƯU: Ghi đè file CSV
                df.to_csv(target_csv, index=False)

                messagebox.showinfo("Thành công", "Đã lưu bản cập nhật vào file CSV!", parent=popup)
                popup.destroy()  # Đóng cửa sổ popup

                # 5. Load lại Treeview để hiển thị dữ liệu mới
                self.load_data_from_csv()

            except ValueError:
                messagebox.showerror("Lỗi", "Số tiền không hợp lệ! Vui lòng chỉ nhập số.", parent=popup)
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu vào file CSV: {str(e)}", parent=popup)

        tk.Button(popup, text="💾 LƯU THAY ĐỔI", bg="#4CAF50", fg="white", width=15, command=save_edit).grid(row=6, column=0, columnspan=2, pady=15)