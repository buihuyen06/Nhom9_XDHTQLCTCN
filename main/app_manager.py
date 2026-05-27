import os
import shutil
import subprocess
from tkinter import messagebox, filedialog
import tkinter as tk
from Controllers.home_controller import HomeController
from Controllers.login_controller import LoginController
from Controllers.thu_controller import Thu_Controller
from Controllers.chi_controller import Chi_Controller
from Controllers.phantich_controller import PhanTich_Controller
from Controllers.ngansach_controller import NganSach_Controller
from Views.login import LoginPage
from Views.home_page import HomePage
from Views.khoanthu import Thu_Page
from Views.khoanchi import Chi_Page
from Views.phantich import PhanTich_Page
from Views.ngansach import NganSach_Page


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("QUẢN LÝ TÀI CHÍNH CÁ NHÂN")
        self.geometry("1000x680")

        # 1. KHỞI TẠO SẴN KHUNG SIDEBAR TOÀN CỤC (Ẩn lúc đầu, hiện sau khi đăng nhập)
        self.sidebar = tk.Frame(self, bg="#FFD1DC", width=220)

        # 2. KHỞI TẠO CONTAINER CHỨA NỘI DUNG CÁC TRANG CON
        self.container = tk.Frame(self)
        # Mặc định ban đầu: Trang Login chiếm trọn vẹn toàn bộ màn hình
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # KHỞI TẠO CÁC CONTROLLER
        self.login_controller = LoginController(self)
        self.home_controller = HomeController(self)
        self.thu_controller = Thu_Controller(self)
        self.chi_controller = Chi_Controller(self)
        self.phantich_controller = PhanTich_Controller(self)
        self.ngansach_controller = NganSach_Controller(self)
        self.pages = {}
        self._init_frames()
        self.show("LoginPage")

    def _init_frames(self):
        """Khởi tạo tất cả các View và đưa vào bộ nhớ grid của container"""
        self.pages["LoginPage"] = LoginPage(self.container, self.login_controller)

        self.pages["HomePage"] = HomePage(self.container, self.home_controller)
        self.home_controller.set_view(self.pages["HomePage"])

        self.pages["Thu_Page"] = Thu_Page(self.container, self.thu_controller)
        self.thu_controller.set_view(self.pages["Thu_Page"])
        self.pages["Chi_Page"] = Chi_Page(self.container, self.chi_controller)
        self.chi_controller.set_view(self.pages["Chi_Page"])
        self.pages["PhanTich_Page"] = PhanTich_Page(self.container, self.phantich_controller)
        self.phantich_controller.set_view(self.pages["PhanTich_Page"])
        self.pages["NganSach_Page"] = NganSach_Page(self.container, self.ngansach_controller)
        self.ngansach_controller.set_view(self.pages["NganSach_Page"])

        for f in self.pages.values():
            f.grid(row=0, column=0, sticky="nsew")

    def login_ok(self):
        """Xử lý giao diện sau khi đăng nhập thành công: Định vị Sidebar cố định bên trái"""
        # Xóa các thành phần cũ trong sidebar nếu có (tránh bị trùng lặp nút khi re-login)
        for widget in self.sidebar.winfo_children():
            widget.destroy()

        # Chia lại Layout cho toàn bộ ứng dụng
        self.container.pack_forget()  # Ẩn tạm thời container full màn hình ban đầu

        # Đẩy Sidebar cố định sang sát mép trái, giữ nguyên kích thước 220px
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Đẩy vùng container nội dung sang bên phải chiếm trọn phần diện tích còn lại
        self.container.pack(side="right", fill="both", expand=True)

        # --- THIẾT KẾ CÁC NÚT ĐIỀU HƯỚNG TRÊN SIDEBAR CHUNG ---
        tk.Label(self.sidebar, text="VÍ CÁ NHÂN 💳", font=("Arial", 14, "bold"), fg="white", bg="#FFD1DC").pack(pady=25)

        tk.Button(self.sidebar, text="🏠 TRANG CHỦ", bg="#34495e", fg="white", font=("Arial", 11, "bold"), height=2,
                  bd=0, cursor="hand2",
                  command=lambda: self.show("HomePage")).pack(fill="x", padx=15, pady=5)

        tk.Button(self.sidebar, text="💰 KHOẢN THU", bg="#34495e", fg="white", font=("Arial", 11, "bold"), height=2,
                  bd=0, cursor="hand2",
                  command=lambda: self.show("Thu_Page")).pack(fill="x", padx=15, pady=5)

        tk.Button(self.sidebar, text="💸 KHOẢN CHI", bg="#34495e", fg="white", font=("Arial", 11, "bold"), height=2,
                  bd=0, cursor="hand2",
                  command=lambda: self.show("Chi_Page")).pack(fill="x", padx=15, pady=5)

        tk.Button(self.sidebar, text="🎯 NGÂN SÁCH", bg="#34495e", fg="white", font=("Arial", 11, "bold"), height=2,
                  bd=0, cursor="hand2",
                  command=lambda: [self.show("NganSach_Page"),
                                   self.ngansach_controller.load_data()]).pack(fill="x", padx=15, pady=5)

        tk.Button(self.sidebar, text="📊 PHÂN TÍCH", bg="#34495e", fg="white", font=("Arial", 11, "bold"), height=2,
                  bd=0, cursor="hand2",
                  command=lambda: [self.show("PhanTich_Page"),
                                   self.phantich_controller.load_data_and_draw_chart()]).pack(fill="x", padx=15, pady=5)

        # --- KHU VỰC 4 NÚT HỆ THỐNG GỘP TRỰC TIẾP VÀO APP_MANAGER ---
        frame_he_thong = tk.Frame(self.sidebar, bg="#FFD1DC")
        frame_he_thong.pack(side="bottom", fill="x", padx=15, pady=(10, 0))

        # Đường kẻ phân cách giữa Menu và Nút hệ thống
        line = tk.Frame(frame_he_thong, bg="#7f8c8d", height=1)
        line.pack(fill="x", pady=(0, 8))

        # 4 Nút gọi trực tiếp các hàm hệ thống độc lập bên dưới
        tk.Button(frame_he_thong, text="📥 Import CSV", bg="#1abc9c", fg="white",
                  font=("Arial", 9, "bold"), bd=0, height=1, cursor="hand2",
                  command=self.import_csv).pack(fill="x", pady=2)

        tk.Button(frame_he_thong, text="📤 Export CSV", bg="#9b59b6", fg="white",
                  font=("Arial", 9, "bold"), bd=0, height=1, cursor="hand2",
                  command=self.export_csv).pack(fill="x", pady=2)

        tk.Button(frame_he_thong, text="📄 Hướng Dẫn (PDF)", bg="#34495e", fg="white",
                  font=("Arial", 9, "bold"), bd=0, height=1, cursor="hand2",
                  command=self.open_pdf_guide).pack(fill="x", pady=2)

        tk.Button(frame_he_thong, text="ℹ️ Về Phần Mềm", bg="#d35400", fg="white",
                  font=("Arial", 9, "bold"), bd=0, height=1, cursor="hand2",
                  command=self.show_about_dialog).pack(fill="x", pady=2)

        # Nút đăng xuất cố định ở đáy (Chỉ giữ lại duy nhất 1 nút)
        tk.Button(self.sidebar, text="🔒 ĐĂNG XUẤT", bg="#e74c3c", fg="white", font=("Arial", 11, "bold"), height=2,
                  bd=0, cursor="hand2",
                  command=self.logout).pack(fill="x", padx=15, side="bottom", pady=10)

        # Mở trang chủ sau khi đăng nhập
        self.show("HomePage")

    def logout(self):
        """Quy trình thu hồi bố cục và quay về màn hình Login ban đầu"""
        self.sidebar.pack_forget()  # Ẩn thanh menu đi
        self.container.pack_forget()  # Giải phóng layout chia đôi

        # Đưa container quay lại chế độ bao phủ toàn màn hình nền công cộng
        self.container.pack(side="top", fill="both", expand=True)
        self.show("LoginPage")

    def show(self, page_name):
        """Hàm chuyển trang bằng cách đưa frame lên trên cùng"""
        frame = self.pages[page_name]
        frame.tkraise()
        if hasattr(frame, 'refresh'):
            frame.refresh()

    # =========================================================================
    # 4 HÀM LOGIC HỆ THỐNG (ĐÃ ĐƯỢC ĐƯA RA NGOÀI CÙNG CẤP VỚI LOGIN_OK)
    # =========================================================================

    def import_csv(self):
        """Tính năng nạp file dữ liệu CSV từ máy tính vào ứng dụng"""
        file_path = filedialog.askopenfilename(
            title="Chọn file dữ liệu CSV để Import",
            filetypes=[("CSV Files", "*.csv")]
        )
        if file_path:
            try:
                if not os.path.exists('data'):
                    os.makedirs('data')

                # Copy đè file người dùng chọn vào file gốc của bồ
                shutil.copy(file_path, 'data/khoan_chi.csv')

                # Gọi làm mới dữ liệu thông qua các trang đã khởi tạo để cập nhật Treeview
                if "Chi_Page" in self.pages:
                    self.chi_controller.load_data()
                if "NganSach_Page" in self.pages:
                    self.ngansach_controller.load_data()

                messagebox.showinfo("Thành công",
                                    "Đã import dữ liệu thành công! Hệ thống đã tự động cập nhật lại các bảng dữ liệu.")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể import file: {str(e)}")

    def export_csv(self):
        """Tính năng xuất toàn bộ dữ liệu trong ứng dụng ra file ngoài máy tính"""
        source_file = 'data/khoan_chi.csv'
        if not os.path.exists(source_file):
            messagebox.showwarning("Cảnh báo", "Hiện tại ứng dụng chưa có dữ liệu khoản chi để xuất!")
            return

        save_path = filedialog.asksaveasfilename(
            title="Chọn nơi lưu file CSV được xuất",
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")]
        )
        if save_path:
            try:
                shutil.copy(source_file, save_path)
                messagebox.showinfo("Thành công", f"Đã xuất dữ liệu thành công tại:\n{save_path}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xuất file: {str(e)}")

    def open_pdf_guide(self):
        """Tính năng NÂNG CAO: Tự động mở file hướng dẫn PDF bằng ứng dụng của máy tính"""
        pdf_path = "huong_dan.pdf"

        if os.path.exists(pdf_path):
            try:
                os.startfile(pdf_path)  # Chạy mượt trên Windows
            except Exception:
                try:
                    subprocess.run(["open", pdf_path] if os.name != 'nt' else ["start", pdf_path], shell=True)
                except Exception as e:
                    messagebox.showerror("Lỗi", f"Không thể mở file PDF: {str(e)}")
        else:
            messagebox.showerror("Lỗi",
                                 "Không tìm thấy file 'huong_dan.pdf' trong thư mục gốc của project!\nBồ nhớ bỏ 1 file PDF bất kỳ tên này vào thư mục chứa code nha.")

    def show_about_dialog(self):
        """Tính năng hiển thị thông tin phiên bản, bản quyền tác giả"""
        messagebox.showinfo(
            "ℹ️ Về Ứng Dụng",
            "Ứng dụng: Phần Mềm Quản Lý Chi Tiêu Cá Nhân (MVC)\n"
            "Phiên bản: Python 3.14\n"
            "Tác giả: Bùi Thị Huyền\n"
                    "Nguyễn Thúy Vy \n"
                    "Nguyễn Hoàng Minh \n"
            "Lớp: DH10TT02D - Trường Đại học Hạ Long\n"
            "Ngày phát hành: 27/05/2026\n\n"
            "Công nghệ sử dụng:\n"
            "- Giao diện: Python Tkinter\n"
            "- Mô hình tính toán: Pandas & Numpy\n"
            "- Đồ thị trực quan: Matplotlib"
        )

