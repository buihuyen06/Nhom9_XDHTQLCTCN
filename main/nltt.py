import tkinter as tk
from tkinter import messagebox
from LichSuChiTieu import LichSuChiTieu

# Khởi tạo đối tượng quản lý chi tiêu
lich_su = LichSuChiTieu("chi_tieu.csv")

def submit_data():
    ngay = entry_ngay.get()
    phanloai = entry_phanloai.get()
    hangmuc = entry_hangmuc.get()
    sotien = entry_sotien.get()
    ghichu = entry_ghichu.get()

    if not ngay or not phanloai or not hangmuc or not sotien:
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin bắt buộc!")
        return

    try:
        sotien = float(sotien)
    except ValueError:
        messagebox.showerror("Lỗi dữ liệu", "Số tiền phải là số!")
        return

    new_data = [ngay, phanloai, hangmuc, sotien, ghichu]
    lich_su.create(new_data)
    messagebox.showinfo("Thành công", "Đã thêm chi tiêu mới!")
    clear_form()

def clear_form():
    entry_ngay.delete(0, tk.END)
    entry_phanloai.delete(0, tk.END)
    entry_hangmuc.delete(0, tk.END)
    entry_sotien.delete(0, tk.END)
    entry_ghichu.delete(0, tk.END)

# Tạo giao diện nhập liệu
root = tk.Tk()
root.title("Nhập liệu chi tiêu cá nhân")

tk.Label(root, text="Ngày (YYYY-MM-DD):").grid(row=0, column=0, sticky="w")
entry_ngay = tk.Entry(root)
entry_ngay.grid(row=0, column=1)

tk.Label(root, text="Phân loại:").grid(row=1, column=0, sticky="w")
entry_phanloai = tk.Entry(root)
entry_phanloai.grid(row=1, column=1)

tk.Label(root, text="Hạng mục:").grid(row=2, column=0, sticky="w")
entry_hangmuc = tk.Entry(root)
entry_hangmuc.grid(row=2, column=1)

tk.Label(root, text="Số tiền:").grid(row=3, column=0, sticky="w")
entry_sotien = tk.Entry(root)
entry_sotien.grid(row=3, column=1)

tk.Label(root, text="Ghi chú:").grid(row=4, column=0, sticky="w")
entry_ghichu = tk.Entry(root)
entry_ghichu.grid(row=4, column=1)

tk.Button(root, text="Thêm chi tiêu", command=submit_data).grid(row=5, column=0, pady=10)
tk.Button(root, text="Xóa form", command=clear_form).grid(row=5, column=1, pady=10)

root.mainloop()
