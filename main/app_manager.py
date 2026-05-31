import os
import shutil
import subprocess
from tkinter import messagebox, filedialog
import tkinter as tk
from tkinter import ttk
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
        self.geometry("1800x800")

        # --- CẤU HÌNH STYLE TOÀN CỤC CHO TRÌNH CHIẾU ---
        style = ttk.Style()
        style.theme_use("clam")
        # Cấu hình bảng hiển thị (Treeview) chữ to, hàng cao ráo
        style.configure("Treeview", font=("Arial", 12), rowheight=35, background="#FFFFFF", fieldbackground="#FFFFFF")
        style.configure("Treeview.Heading", font=("Arial", 13, "bold"), background="#E1EBF5", foreground="black")
        style.map("Treeview", background=[("selected", "#3498db")], foreground=[("selected", "white")])

        # Cấu hình ô chọn (Combobox) chữ to dễ bấm
        self.option_add("*TCombobox*Listbox.font", ("Arial", 12))
        style.configure("TCombobox", font=("Arial", 12))

        # 1. KHỞI TẠO SẴN KHUNG SIDEBAR TOÀN CỤC (Rộng 260px để chứa chữ to công cộng)
        self.sidebar = tk.Frame(self, bg="#A3C9E8", width=260)

        # 2. KHỞI TẠO CONTAINER CHỨA NỘI DUNG CÁC TRANG CON
        self.container = tk.Frame(self)
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
        for widget in self.sidebar.winfo_children():
            widget.destroy()

        self.container.pack_forget()

        # Đẩy Sidebar cố định sang sát mép trái, rộng 260px cho thoáng
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.container.pack(side="right", fill="both", expand=True)

        # --- THIẾT KẾ CÁC NÚT ĐIỀU HƯỚNG TRÊN SIDEBAR CHUNG (PHÓNG TO FONT) ---
        tk.Label(self.sidebar, text="\n QUẢN LÝ \n TÀI CHÍNH \n CÁ NHÂN \n", font=("Comic Sans MS", 16, "bold"), fg="#245C8F",
                 bg="#A3C9E8").pack(pady=20)

        tk.Button(self.sidebar, text="🏠 TRANG CHỦ", bg="#8AB8DD", fg="black", font=("Arial", 13, "bold"), height=2,
                  bd=0, cursor="hand2",
                  command=lambda: self.show("HomePage")).pack(fill="x", padx=15, pady=6)

        tk.Button(self.sidebar, text="💰 KHOẢN THU", bg="#8AB8DD", fg="black", font=("Arial", 13, "bold"), height=2,
                  bd=0, cursor="hand2",
                  command=lambda: self.show("Thu_Page")).pack(fill="x", padx=15, pady=6)

        tk.Button(self.sidebar, text="💸 KHOẢN CHI", bg="#8AB8DD", fg="black", font=("Arial", 13, "bold"), height=2,
                  bd=0, cursor="hand2",
                  command=lambda: self.show("Chi_Page")).pack(fill="x", padx=15, pady=6)

        tk.Button(self.sidebar, text="🎯 NGÂN SÁCH", bg="#8AB8DD", fg="black", font=("Arial", 13, "bold"), height=2,
                  bd=0, cursor="hand2",
                  command=lambda: [self.show("NganSach_Page"),
                                   self.ngansach_controller.load_data()]).pack(fill="x", padx=15, pady=6)

        tk.Button(self.sidebar, text="📊 PHÂN TÍCH", bg="#8AB8DD", fg="black", font=("Arial", 13, "bold"), height=2,
                  bd=0, cursor="hand2",
                  command=lambda: [self.show("PhanTich_Page"),
                                   self.phantich_controller.load_data_and_draw_chart()]).pack(fill="x", padx=15, pady=6)

        # --- KHU VỰC NÚT HỆ THỐNG ---
        frame_he_thong = tk.Frame(self.sidebar, bg="#A3C9E8")
        frame_he_thong.pack(side="bottom", fill="x", padx=15, pady=(10, 0))

        line = tk.Frame(frame_he_thong, bg="black", height=1)
        line.pack(fill="x", pady=(0, 8))

        tk.Button(frame_he_thong, text="📥 Import CSV", bg="#1abc9c", fg="white",
                  font=("Arial", 11, "bold"), bd=0, height=1, cursor="hand2",
                  command=self.import_csv).pack(fill="x", pady=3)

        tk.Button(frame_he_thong, text="📤 Export CSV", bg="#9b59b6", fg="white",
                  font=("Arial", 11, "bold"), bd=0, height=1, cursor="hand2",
                  command=self.export_csv).pack(fill="x", pady=3)

        tk.Button(frame_he_thong, text="📄 Hướng Dẫn (PDF)", bg="#34495e", fg="white",
                  font=("Arial", 11, "bold"), bd=0, height=1, cursor="hand2",
                  command=self.open_pdf_guide).pack(fill="x", pady=3)

        tk.Button(frame_he_thong, text="ℹ️ Về Phần Mềm", bg="#d35400", fg="white",
                  font=("Arial", 11, "bold"), bd=0, height=1, cursor="hand2",
                  command=self.show_about_dialog).pack(fill="x", pady=3)

        tk.Button(self.sidebar, text="🔒 ĐĂNG XUẤT", bg="#e74c3c", fg="white", font=("Arial", 13, "bold"), height=2,
                  bd=0, cursor="hand2",
                  command=self.logout).pack(fill="x", padx=15, side="bottom", pady=10)

        self.show("HomePage")

    def logout(self):
        self.sidebar.pack_forget()
        self.container.pack_forget()
        self.container.pack(side="top", fill="both", expand=True)
        self.show("LoginPage")

    def show(self, page_name):
        frame = self.pages[page_name]
        frame.tkraise()
        if hasattr(frame, 'refresh'):
            frame.refresh()

    def import_csv(self):
        file_path = filedialog.askopenfilename(
            title="Chọn file dữ liệu CSV để Import",
            filetypes=[("CSV Files", "*.csv")]
        )
        if file_path:
            try:
                if not os.path.exists('data'):
                    os.makedirs('data')
                shutil.copy(file_path, 'data/khoan_chi.csv')
                if "Chi_Page" in self.pages:
                    self.chi_controller.load_data()
                if "NganSach_Page" in self.pages:
                    self.ngansach_controller.load_data()
                messagebox.showinfo("Thành công",
                                    "Đã import dữ liệu thành công! Hệ thống đã tự động cập nhật lại các bảng dữ liệu.")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể import file: {str(e)}")

    def export_csv(self):
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
        pdf_path = "huong_dan.pdf"
        if os.path.exists(pdf_path):
            try:
                os.startfile(pdf_path)
            except Exception:
                try:
                    subprocess.run(["open", pdf_path] if os.name != 'nt' else ["start", pdf_path], shell=True)
                except Exception as e:
                    messagebox.showerror("Lỗi", f"Không thể mở file PDF: {str(e)}")
        else:
            messagebox.showerror("Lỗi", "Không tìm thấy file 'huong_dan.pdf' trong thư mục gốc của project!")

    def show_about_dialog(self):
        messagebox.showinfo(
            "ℹ️ Về Ứng Dụng",
            "Ứng dụng: Phần Mềm Quản Lý Chi Tiêu Cá Nhân (MVC)\n"
            "Phiên bản: Python 3.14\n"
            "Tác giả: \n Bùi Thị Huyền\n"
            "Nguyễn Thúy Vy \n"
            "Nguyễn Hoàng Minh \n"
            "Lớp: DH10TT02D - Trường Đại học Hạ Long\n"
            "Ngày phát hành: 27/05/2026\n\n"
            "Công nghệ sử dụng:\n"
            "- Giao diện: Python Tkinter\n"
            "- Mô hình tính toán: Pandas & Numpy\n"
            "- Đồ thị trực quan: Matplotlib"
        )