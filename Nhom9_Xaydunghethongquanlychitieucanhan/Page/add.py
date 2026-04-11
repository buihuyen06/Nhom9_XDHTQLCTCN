import tkinter as tk
from tkinter import messagebox
from Common.constants import PRIMARY_COLOR, TEXT_COLOR


class AddPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="THÊM MỚI GIAO DỊCH", font=("Arial", 18, "bold"), fg=PRIMARY_COLOR).pack(pady=15)

        tk.Label(self, text="Nội dung:").pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        tk.Label(self, text="Số tiền:").pack()
        self.price_entry = tk.Entry(self)
        self.price_entry.pack()

        tk.Label(self, text="Loại:").pack()
        self.type_var = tk.StringVar(value="Chi")
        tk.Radiobutton(self, text="Chi", variable=self.type_var, value="Chi").pack()
        tk.Radiobutton(self, text="Thu", variable=self.type_var, value="Thu").pack()

        tk.Button(self, text="Lưu", command=self.save, bg=PRIMARY_COLOR, fg=TEXT_COLOR).pack(pady=20)

    def save(self):
        name = self.name_entry.get()
        price = self.price_entry.get()
        t_type = self.type_var.get()

        if self.controller.add_new(name, int(price), t_type):
            messagebox.showinfo("Thành công", "Đã thêm giao dịch!")
        else:
            messagebox.showerror("Lỗi", "Số tiền phải > 0")