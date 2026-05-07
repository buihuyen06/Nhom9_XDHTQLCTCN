import tkinter as tk
from tkinter import ttk, messagebox
from Controllers.query import Query


class AccountManagerPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.ctrl = controller
        self.query = Query("accounts.csv", ["id", "ho_va_ten", "email", "trang_thai"])
        self.selected_id = None

        tk.Label(self, text="QUẢN LÝ TÀI KHOẢN", font=("Arial", 14, "bold")).pack(pady=10)

        # Thanh tìm kiếm
        s_f = tk.Frame(self)
        s_f.pack(fill="x", padx=10, pady=5)
        tk.Label(s_f, text="Tìm kiếm:").pack(side="left", padx=5)
        self.s_ent = tk.Entry(s_f)
        self.s_ent.pack(side="left", expand=True, fill="x", padx=5)
        tk.Button(s_f, text="Tìm", command=self.search).pack(side="left", padx=5)
        tk.Button(s_f, text="Tải lại", command=self.refresh).pack(side="left", padx=5)

        # Bảng hiển thị
        self.tree = ttk.Treeview(self, columns=("ID", "Họ và tên", "Email", "Trạng thái"), show="headings", height=10)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Họ và tên", text="Họ và tên")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Trạng thái", text="Trạng thái")
        
        self.tree.column("ID", width=50)
        self.tree.column("Họ và tên", width=150)
        self.tree.column("Email", width=200)
        self.tree.column("Trạng thái", width=100)
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Form nhập liệu
        f = tk.Frame(self)
        f.pack(pady=10, padx=10, fill="x")
        
        tk.Label(f, text="Họ và tên:").pack(side="left", padx=5)
        self.name_ent = tk.Entry(f, width=20)
        self.name_ent.pack(side="left", padx=5)
        
        tk.Label(f, text="Email:").pack(side="left", padx=5)
        self.email_ent = tk.Entry(f, width=25)
        self.email_ent.pack(side="left", padx=5)
        
        tk.Label(f, text="Trạng thái:").pack(side="left", padx=5)
        self.status_var = tk.StringVar(value="Hoạt động")
        self.status_combo = ttk.Combobox(f, textvariable=self.status_var, 
                                         values=["Hoạt động", "Khóa"], width=15, state="readonly")
        self.status_combo.pack(side="left", padx=5)

        # Nút chức năng
        btn_f = tk.Frame(self)
        btn_f.pack(pady=10)
        tk.Button(btn_f, text="Thêm", bg="green", fg="white", command=self.add, width=10).pack(side="left", padx=5)
        tk.Button(btn_f, text="Sửa", bg="orange", command=self.edit, width=10).pack(side="left", padx=5)
        tk.Button(btn_f, text="Xóa", bg="red", fg="white", command=self.delete, width=10).pack(side="left", padx=5)

        self.refresh()

    def refresh(self):
        """Tải lại toàn bộ dữ liệu"""
        for i in self.tree.get_children():
            self.tree.delete(i)
        



    def search(self):
        """Tìm kiếm theo tên"""
        keyword = self.s_ent.get().strip()
        if not keyword:
            self.refresh()
            return
        
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        result = self.query.search("ho_va_ten", keyword)
        for _, row in result.iterrows():
            self.tree.insert("", "end", values=(int(row["id"]), row["ho_va_ten"], row["email"], row["trang_thai"]))

    def on_select(self, event):
        """Chọn dòng để sửa/xóa"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            self.selected_id = values[0]
            self.name_ent.delete(0, tk.END)
            self.name_ent.insert(0, values[1])
            self.email_ent.delete(0, tk.END)
            self.email_ent.insert(0, values[2])
            self.status_var.set(values[3])

    def clear_form(self):
        """Xóa form"""
        self.selected_id = None
        self.name_ent.delete(0, tk.END)
        self.email_ent.delete(0, tk.END)
        self.status_var.set("Hoạt động")

    def add(self):
        """Thêm tài khoản mới"""
        name = self.name_ent.get().strip()
        email = self.email_ent.get().strip()
        status = self.status_var.get()
        
        if not name or not email:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        max_id = int(self.query.max("id")) if self.query.max("id") > 0 else 0
        self.query.create([max_id + 1, name, email, status])
        messagebox.showinfo("Thành công", "Thêm tài khoản thành công!")
        self.refresh()
        self.s_ent.delete(0, tk.END)

    def edit(self):
        """Sửa tài khoản"""
        if self.selected_id is None:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn tài khoản để sửa!")
            return
        
        name = self.name_ent.get().strip()
        email = self.email_ent.get().strip()
        status = self.status_var.get()
        
        if not name or not email:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        self.query.update("id", str(self.selected_id), [self.selected_id, name, email, status])
        messagebox.showinfo("Thành công", "Cập nhật tài khoản thành công!")
        self.refresh()
        self.s_ent.delete(0, tk.END)

    def delete(self):
        """Xóa tài khoản"""
        if self.selected_id is None:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn tài khoản để xóa!")
            return
        
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa tài khoản này?"):
            self.query.delete("id", str(self.selected_id))
            messagebox.showinfo("Thành công", "Xóa tài khoản thành công!")
            self.refresh()
            self.s_ent.delete(0, tk.END)