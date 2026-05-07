import tkinter as tk


class AnalysisPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F3E5F5")
        self.ctrl = controller
        tk.Label(self, text="📊 PHÂN TÍCH CHI TIÊU", font=("Arial", 18, "bold"), bg="#F3E5F5").pack(pady=20)

        # Sau này bạn sẽ thêm biểu đồ hình quạt (Pie Chart) ở đây
        tk.Label(self, text="Biểu đồ phân tích sẽ hiện ở đây...", bg="#F3E5F5").pack()

        tk.Button(self, text="🏠 QUAY LẠI", command=lambda: self.ctrl.show("HomePage")).pack(pady=20)