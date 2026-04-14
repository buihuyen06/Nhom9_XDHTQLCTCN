import tkinter as tk
from tkinter import ttk, messagebox


class AccountManagerPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.ctrl = controller

        tk.Label(self, text="QUẢN LÝ TÀI KHOẢN ", font=("Arial", 14, "bold")).pack(pady=10)

        # Tìm kiếm
        s_f = tk.Frame(self);
        s_f.pack(fill="x", padx=10)
        self.s_ent = tk.Entry(s_f);
        self.s_ent.pack(side="left", expand=True, fill="x", padx=5)
        tk.Button(s_f, text="Tìm", command=self.refresh).pack(side="left")

        # Bảng
        self.tree = ttk.Treeview(self, columns=("ID", "Tên", "Số dư"), show="headings")
        for c in ("ID", "Tên", "Số dư"): self.tree.heading(c, text=c)
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Form
        f = tk.Frame(self);
        f.pack(pady=5)
        self.n_ent = tk.Entry(f);
        self.n_ent.pack(side="left", padx=2)
        self.b_ent = tk.Entry(f);
        self.b_ent.pack(side="left", padx=2)

        # Nút
        btn_f = tk.Frame(self);
        btn_f.pack(pady=10)
        tk.Button(btn_f, text="Thêm", bg="green", fg="white", command=self.add).pack(side="left", padx=5)
        tk.Button(btn_f, text="Sửa", bg="orange", command=self.edit).pack(side="left", padx=5)
        tk.Button(btn_f, text="Xóa", bg="red", fg="white", command=self.delete).pack(side="left", padx=5)

    def refresh(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        df = self.ctrl.model.df_accounts
        q = self.s_ent.get().lower()
        if q: df = df[df["Tên"].str.contains(q, case=False, na=False)]
        for _, r in df.iterrows():
            self.tree.insert("", "end", values=(int(r["ID"]), r["Tên"], f"{r['Số dư']:,}đ"))

    def add(self):
        self.ctrl.model.add_account(self.n_ent.get(), self.b_ent.get())
        self.refresh()

    def on_select(self, e):
        s = self.tree.focus()
        if s:
            v = self.tree.item(s)['values']
            self.n_ent.delete(0, 'end');
            self.n_ent.insert(0, v[1])
            self.b_ent.delete(0, 'end');
            self.b_ent.insert(0, str(v[2]).replace(',', '').replace('đ', ''))

    def edit(self):
        s = self.tree.focus()
        if s:
            self.ctrl.model.update_account(self.tree.item(s)['values'][0], self.n_ent.get(), self.b_ent.get())
            self.refresh()

    def delete(self):
        s = self.tree.focus()
        if s:
            self.ctrl.model.delete_account(self.tree.item(s)['values'][0]);
            self.refresh()