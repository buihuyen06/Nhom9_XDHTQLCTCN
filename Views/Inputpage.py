import tkinter as tk

class InputPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#FCE4EC")  # Màu nền khác để phân biệt
        self.ctrl = controller

        # Tiêu đề trang mới
        tk.Label(self, text="TRANG NHẬP DỮ LIỆU", font=("Arial", 18, "bold"), bg="#FCE4EC").pack(pady=20)

        # Ví dụ một ô nhập liệu
        tk.Label(self, text="Nhập số tiền:", bg="#FCE4EC").pack()
        self.entry_price = tk.Entry(self)
        self.entry_price.pack(pady=5)

        # Nút để quay về Trang Chủ
        tk.Button(self, text="⬅ QUAY LẠI", command=lambda: self.ctrl.show_frame("HomePage")).pack(pady=20)