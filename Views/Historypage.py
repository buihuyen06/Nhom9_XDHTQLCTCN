import tkinter as tk


class HistoryPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#E3F2FD")
        self.ctrl = controller
        tk.Label(self, text="📋 LỊCH SỬ GIAO DỊCH", font=("Arial", 18, "bold"), bg="#E3F2FD").pack(pady=20)

        # Sau này bạn sẽ thêm Table hoặc Listbox ở đây
        tk.Label(self, text="Danh sách các giao dịch sẽ hiện ở đây...", bg="#E3F2FD").pack()

        tk.Button(self, text="🏠 QUAY LẠI", command=lambda: self.ctrl.show("HomePage")).pack(pady=20)