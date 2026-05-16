import random
import tkinter as tk
from datetime import datetime


class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#FFF9C4")
        self.ctrl = controller  # MainApp

        # Khai báo các thuộc tính phục vụ cho hiệu ứng nhấp nháy chữ banner
        self.colors = ["#E91E63", "#F06292", "#EC407A", "#AD1457"]
        self.i = 0

        # Gọi hàm vẽ giao diện
        self.render_ui()

        # Gọi chạy hiệu ứng nhấp nháy cho banner
        self.animate_banner()

    def lay_loi_chao(self):
        """Tự động đưa ra lời chào theo thời gian thực của máy tính"""
        gio_hien_tai = datetime.now().hour
        if gio_hien_tai < 12:
            return "🌤️ Chúc bạn một buổi sáng tốt lành!"
        elif gio_hien_tai < 18:
            return "🌤️ Chiều rồi, kiểm tra chi tiêu hôm nay chưa?"
        else:
            return "🌙 Tối rồi, đừng quên ghi lại chi tiêu nhé!"

    def lay_meo_ngau_nhien(self):
        """Trả về một mẹo tiết kiệm tiền ngẫu nhiên từ danh sách"""
        cac_meo = [
            "Hãy ghi lại mọi khoản chi dù là nhỏ nhất.",
            "Hạn chế mang quá nhiều tiền mặt khi đi mua sắm.",
            "Tập thói quen tích lũy ít nhất 10% thu nhập trước khi tiêu.",
            "Trước khi mua một món đồ, hãy nghĩ xem nó là 'Cần' hay 'Muốn'.",
            "Nấu ăn tại nhà giúp bạn tiết kiệm được một khoản kha khá đấy!",
            "Tắt các thiết bị điện khi không sử dụng để tiết kiệm hóa đơn.",
            "Hạn chế sa đà vào các chương trình giảm giá không cần thiết.",
        ]
        return "💡 Mẹo hôm nay: " + random.choice(cac_meo)

    def lam_moi_giao_dien(self):
        """Hàm xử lý khi bấm nút 'LÀM MỚI'"""
        self.lbl_loi_chao.config(text=self.lay_loi_chao())
        self.lbl_meo.config(text=self.lay_meo_ngau_nhien())

    def animate_banner(self):
        """Hiệu ứng chữ đổi màu động cho banner"""
        self.banner.config(fg=self.colors[self.i])
        self.i = (self.i + 1) % len(self.colors)
        self.after(500, self.animate_banner)

    def render_ui(self):
        # Tiêu đề trang
        tk.Label(
            self,
            text="TỔNG QUAN TÀI CHÍNH",
            font=("Comic Sans MS", 18, "bold"),
            fg="black",
            bg="#FFF9C4",
        ).pack(pady=10)

        # =========================================================================
        #  (Khung chứa ngày tháng, lời chào và mẹo ngẫu nhiên)
        # =========================================================================
        frame_thay_the = tk.Frame(
            self, bg="#FFFFFF", highlightbackground="#CCCCCC", highlightthickness=1
        )
        frame_thay_the.pack(fill="x", padx=40, pady=10)

        # 1. Hiển thị ngày tháng hiện tại
        ngay_hien_tai = (
            datetime.now()
            .strftime("Hôm nay: Thứ %u, Ngày %d/%m/%Y")
            .replace("Thứ 7", "Thứ Bảy")
            .replace("Thứ 8", "Chủ Nhật")
        )
        lbl_ngay = tk.Label(
            frame_thay_the,
            text=ngay_hien_tai,
            font=("Arial", 10, "italic"),
            bg="#FFFFFF",
            fg="#666666",
        )
        lbl_ngay.pack(pady=(8, 0))

        # 2. Hiển thị lời chào động (Dùng self. để hàm lam_moi_giao_dien gọi tới được)
        self.lbl_loi_chao = tk.Label(
            frame_thay_the,
            text=self.lay_loi_chao(),
            font=("Arial", 11, "bold"),
            bg="#FFFFFF",
            fg="#2E7D32",
        )
        self.lbl_loi_chao.pack(pady=5)

        # 3. Hiển thị mẹo ngẫu nhiên
        self.lbl_meo = tk.Label(
            frame_thay_the,
            text=self.lay_meo_ngau_nhien(),
            font=("Arial", 10),
            bg="#FFFFFF",
            fg="#333333",
            wraplength=280,
            justify="center",
        )
        self.lbl_meo.pack(pady=(0, 8), padx=10)
        # =========================================================================

        # --- ĐOẠN ĐƯỢC THIẾT KẾ LẠI CHO CÁC NÚT BẤM CHUYỂN TRANG ---
        tk.Button(
            self,
            text="➕ NHẬP LIỆU",
            font=("Arial", 11, "bold"),
            bg="#F8BBD0",
            command=lambda: self.ctrl.show("InputPage"),
        ).pack(fill="x", padx=40, pady=8)

        tk.Button(
            self,
            text="📋 LỊCH SỬ",
            font=("Arial", 11, "bold"),
            bg="#81D4FA",
            command=lambda: self.ctrl.show("HistoryPage"),
        ).pack(fill="x", padx=40, pady=8)

        tk.Button(
            self,
            text="📊 PHÂN TÍCH",
            font=("Arial", 11, "bold"),
            bg="#CE93D8",
            command=lambda: self.ctrl.show("AnalysisPage"),
        ).pack(fill="x", padx=40, pady=8)

        # Nút LÀM MỚI (Kết nối trực tiếp đến hàm làm mới dữ liệu mẹo vặt)
        tk.Button(
            self,
            text="🔄 LÀM MỚI",
            font=("Arial", 11, "bold"),
            bg="#A5D6A7",
            command=self.lam_moi_giao_dien,
        ).pack(fill="x", padx=40, pady=8)

        # Banner Slogan chuyển xuống dưới cùng của trang cho cân đối
        self.banner = tk.Label(
            self,
            text="💰 Tiền vào có kế hoạch, tiền ra có kiểm soát 💰\n✨ Một xu tiết kiệm là một xu kiếm được ✨",
            font=("Arial", 11, "bold"),
            fg="#2E7D32",
            bg="#FFF9C4",
            justify="center",
        )
        self.banner.pack(side="bottom", pady=20)