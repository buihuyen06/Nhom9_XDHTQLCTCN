import tkinter as tk
from tkinter import ttk


class NganSach_Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f2f5")
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self, text="🎯 QUẢN LÝ NGÂN SÁCH CHI TIÊU", font=("Arial", 24, "bold"),
                 fg="#2c3e50", bg="#f0f2f5").pack(pady=20)

        # THANH CÔNG CỤ
        toolbar = tk.Frame(self, bg="#f0f2f5")
        toolbar.pack(pady=10, fill="x", padx=20)

        tk.Button(toolbar, text="➕ THÊM MỚI", bg="#2ecc71", fg="white", font=("Arial", 11, "bold"), width=15,
                  command=self.controller.show_add_dialog).pack(side="left", padx=6)

        tk.Button(toolbar, text="🔧 CHỈNH SỬA", bg="#3498db", fg="white", font=("Arial", 11, "bold"), width=15,
                  command=self.controller.show_edit_dialog).pack(side="left", padx=6)

        tk.Button(toolbar, text="🗑️ XÓA MỤC", bg="#e74c3c", fg="white", font=("Arial", 11, "bold"), width=15,
                  command=self.controller.delete_budget).pack(side="left", padx=6)

        # Khu vực tìm kiếm
        search_frame = tk.Frame(toolbar, bg="#f0f2f5")
        search_frame.pack(side="right", padx=5)

        tk.Label(search_frame, text="🔍 Tìm nguồn chi:", font=("Arial", 12), bg="#f0f2f5").pack(side="left", padx=4)
        self.entry_search = tk.Entry(search_frame, width=25, font=("Arial", 12)) # Font 10 -> 12, width 20 -> 25
        self.entry_search.pack(side="left", padx=4)
        self.entry_search.bind("<KeyRelease>", self.controller.search_budget)

        # BẢNG DỮ LIỆU TREEVIEW
        table_frame = tk.Frame(self)
        table_frame.pack(pady=10, fill="both", expand=True, padx=20)

        columns = ("nguonchi", "hanmuc", "dachi", "conlai")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        self.tree.heading("nguonchi", text="Nguồn Chi")
        self.tree.heading("hanmuc", text="Hạn Mức Quy Định (VND)")
        self.tree.heading("dachi", text="Số Tiền Đã Chi (VND)")
        self.tree.heading("conlai", text="Ngân Sách Còn Lại (VND)")

        self.tree.column("nguonchi", width=350, anchor=tk.W)
        self.tree.column("hanmuc", width=220, anchor=tk.E)
        self.tree.column("dachi", width=220, anchor=tk.E)
        self.tree.column("conlai", width=220, anchor=tk.E)

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")