import os
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd


class AdminPage(tk.Frame):
    def __init__(self, parent, controller, go_login):
        super().__init__(parent, bg="#ECEFF1")
        self.ctrl = controller
        self.go_login = go_login

        # Đường dẫn file dữ liệu (áp dụng cấu trúc thư mục của dự án)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.csv_path = os.path.join(base_dir, "main", "tkdn.csv")

        # --- TIÊU ĐỀ ---
        tk.Label(self, text="⚙️ QUẢN TRỊ HỆ THỐNG", font=("Arial", 22, "bold"), fg="#37474F", bg="#ECEFF1").pack(
            pady=10)

        # --- KHUNG TÌM KIẾM ---
        search_frame = tk.Frame(self, bg="#ECEFF1")
        search_frame.pack(pady=5)

        tk.Label(search_frame, text="Tìm tên đăng nhập:", bg="#ECEFF1", font=("Arial", 10)).grid(row=0, column=0,
                                                                                                 padx=5)
        self.search_ent = tk.Entry(search_frame, width=25)
        self.search_ent.grid(row=0, column=1, padx=5)

        tk.Button(search_frame, text="🔍 Tìm", bg="#4CAF50", fg="white", command=self.search_user).grid(row=0, column=2,
                                                                                                       padx=5)
        tk.Button(search_frame, text="🔄 Tải lại", bg="#9E9E9E", fg="white", command=lambda: self.load_users()).grid(
            row=0, column=3, padx=5)

        # --- BẢNG HIỂN THỊ TÀI KHOẢN ---
        table_frame = tk.Frame(self)
        table_frame.pack(pady=5, padx=20, fill="both", expand=True)

        columns = ("tendn", "mk", "vaitro")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

        self.tree.heading("tendn", text="Tên đăng nhập")
        self.tree.heading("mk", text="Mật khẩu")
        self.tree.heading("vaitro", text="Vai trò")

        self.tree.column("tendn", width=150, anchor="center")
        self.tree.column("mk", width=150, anchor="center")
        self.tree.column("vaitro", width=150, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.pack(side=tk.RIGHT, fill="y")

        # --- NÚT BẤM CHỨC NĂNG ---
        btn_frame = tk.Frame(self, bg="#ECEFF1")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="➕ Thêm", bg="#2196F3", fg="white", width=10, font=("Arial", 10, "bold"),
                  command=self.add_user).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="✏️ Sửa", bg="#FFC107", fg="black", width=10, font=("Arial", 10, "bold"),
                  command=self.edit_user).grid(row=0, column=1, padx=10)
        tk.Button(btn_frame, text="❌ Xóa", bg="#FF9800", fg="white", width=10, font=("Arial", 10, "bold"),
                  command=self.delete_user).grid(row=0, column=2, padx=10)
        tk.Button(btn_frame, text="🚪 Đăng xuất", bg="#F44336", fg="white", width=10, font=("Arial", 10, "bold"),
                  command=self.handle_logout).grid(row=0, column=3, padx=10)

        # Tải danh sách lần đầu
        self.load_users()

    # ================= CÁC HÀM XỬ LÝ (CRUD) =================

    def _get_df(self):
        """Hàm phụ: Đọc file CSV lên thành DataFrame"""
        try:
            return pd.read_csv(self.csv_path, dtype=str)
        except Exception:
            return pd.DataFrame(columns=["tendn", "mk", "vaitro"])

    def load_users(self, filter_name=""):
        """Đọc và hiển thị danh sách (có hỗ trợ lọc tìm kiếm)"""
        # Xóa trắng bảng
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            df = self._get_df()
            # Nếu có từ khóa tìm kiếm, tiến hành lọc dữ liệu
            if filter_name:
                df = df[df['tendn'].astype(str).str.contains(filter_name, case=False, na=False)]

            # Ghi dữ liệu vào bảng
            for _, row in df.iterrows():
                self.tree.insert("", tk.END,
                                 values=(row.get("tendn", ""), row.get("mk", ""), row.get("vaitro", "Người dùng")))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách!\n{e}")

    def search_user(self):
        """Lấy từ khóa và gọi hàm load_users để lọc"""
        tu_khoa = self.search_ent.get().strip()
        self.load_users(tu_khoa)

    def delete_user(self):
        """Xóa tài khoản được chọn"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một tài khoản trên bảng để xóa!")
            return

        vals = self.tree.item(selected[0], "values")
        tendn_can_xoa, vaitro = vals[0], vals[2]

        if vaitro == "Quản trị hệ thống":
            messagebox.showerror("Từ chối", "Không thể xóa tài khoản Quản trị hệ thống!")
            return

        if messagebox.askyesno("Xác nhận", f"Xóa vĩnh viễn tài khoản '{tendn_can_xoa}'?"):
            df = self._get_df()
            df = df[df['tendn'] != tendn_can_xoa]
            df.to_csv(self.csv_path, index=False)
            messagebox.showinfo("Thành công", "Đã xóa tài khoản!")
            self.load_users()

    def add_user(self):
        """Mở cửa sổ Thêm mới"""
        self.open_form(mode="add")

    def edit_user(self):
        """Mở cửa sổ Sửa dựa trên dòng đang chọn"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một tài khoản trên bảng để sửa!")
            return

        vals = self.tree.item(selected[0], "values")
        self.open_form(mode="edit", tendn=vals[0], mk=vals[1], vaitro=vals[2])

    def open_form(self, mode, tendn="", mk="", vaitro="Người dùng"):
        """Tạo một cửa sổ Popup (Toplevel) dùng chung cho cả Thêm và Sửa"""
        win = tk.Toplevel(self)
        win.title("Thêm tài khoản" if mode == "add" else "Sửa tài khoản")
        win.geometry("300x250")
        win.grab_set()  # Khóa tương tác với cửa sổ chính khi popup đang mở

        tk.Label(win, text="Tên đăng nhập:").pack(pady=(10, 0))
        u_ent = tk.Entry(win, width=30)
        u_ent.insert(0, tendn)
        if mode == "edit":
            u_ent.config(state="readonly")  # Sửa thì không cho đổi Tên đăng nhập
        u_ent.pack(pady=5)

        tk.Label(win, text="Mật khẩu:").pack()
        p_ent = tk.Entry(win, width=30)
        p_ent.insert(0, mk)
        p_ent.pack(pady=5)

        tk.Label(win, text="Vai trò:").pack()
        role_cb = ttk.Combobox(win, width=27, values=("Người dùng", "Quản trị hệ thống"), state="readonly")
        role_cb.set(vaitro)
        role_cb.pack(pady=5)

        def save_data():
            nu = u_ent.get().strip()
            np = p_ent.get().strip()
            nr = role_cb.get()

            if not nu or not np:
                messagebox.showwarning("Lỗi", "Vui lòng nhập đủ tên đăng nhập và mật khẩu!", parent=win)
                return

            df = self._get_df()

            if mode == "add":
                # Kiểm tra trùng lặp
                if nu in df['tendn'].values:
                    messagebox.showerror("Lỗi", "Tên đăng nhập này đã tồn tại!", parent=win)
                    return
                # Thêm mới
                new_row = pd.DataFrame([{"tendn": nu, "mk": np, "vaitro": nr}])
                df = pd.concat([df, new_row], ignore_index=True)
            else:
                # Cập nhật dòng hiện tại
                df.loc[df['tendn'] == nu, ['mk', 'vaitro']] = [np, nr]

            # Lưu file và làm mới bảng
            df.to_csv(self.csv_path, index=False)
            self.load_users()
            win.destroy()
            messagebox.showinfo("Thành công", "Lưu dữ liệu thành công!")

        tk.Button(win, text="💾 LƯU LẠI", bg="#4CAF50", fg="white", width=15, command=save_data).pack(pady=15)

    def handle_logout(self):
        if messagebox.askyesno("Đăng xuất", "Bạn có chắc chắn muốn đăng xuất khỏi quyền Quản trị?"):
            self.go_login()

