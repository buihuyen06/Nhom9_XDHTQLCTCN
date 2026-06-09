import os
import shutil
import subprocess
import pandas as pd
from tkinter import messagebox, filedialog
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # 🔥 1. IMPORT THÊM THƯ VIỆN XỬ LÝ ẢNH

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
        self.title("Xây dựng hệ thống quản lý chi tiêu cá nhân - Nhóm 9")
        self.geometry("1800x800")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", font=("Arial", 12), rowheight=35, background="#FFFFFF", fieldbackground="#FFFFFF")
        style.configure("Treeview.Heading", font=("Arial", 13, "bold"), background="#E1EBF5", foreground="black")
        style.map("Treeview", background=[("selected", "#3498db")], foreground=[("selected", "white")])

        self.option_add("*TCombobox*Listbox.font", ("Arial", 12))
        style.configure("TCombobox", font=("Arial", 12))

        # 1. KHỞI TẠO SẴN KHUNG SIDEBAR TOÀN CỤC
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
        """Xử lý giao diện sau khi đăng nhập thành công"""
        for widget in self.sidebar.winfo_children():
            widget.destroy()

        self.container.pack_forget()
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        self.container.pack(side="right", fill="both", expand=True)

        logo_path = "database/anh.png"
        if os.path.exists(logo_path):
            try:
                img_open = Image.open(logo_path)
                # Tự động căn chỉnh kích thước ảnh vừa khít thanh sidebar (Rộng 200px, Cao tự căn chỉnh theo tỉ lệ)
                w_percent = (200 / float(img_open.size[0]))
                h_size = int((float(img_open.size[1]) * float(w_percent)))
                img_resized = img_open.resize((200, h_size), Image.Resampling.LANCZOS)

                # Ép kiểu ảnh sang định dạng Tkinter (Dùng self.logo_image để tránh lỗi Garbage Collector làm mất ảnh)
                self.logo_image = ImageTk.PhotoImage(img_resized)

                lbl_logo = tk.Label(self.sidebar, image=self.logo_image, bg="#A3C9E8")
                lbl_logo.pack(pady=25)
            except Exception:
                pass

        # --- CÁC NÚT ĐIỀU HƯỚNG ---
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
            title="Chọn file dữ liệu CSV để Import vào phần mềm",
            filetypes=[("CSV Files", "*.csv")]
        )
        if not file_path: return

        try:
            df_test = pd.read_csv(file_path)
            if 'NguonThu' in df_test.columns:
                target_file = 'database/khoan_thu.csv'
                loai_data = "Khoản Thu Nhập"
            elif 'NguonChi' in df_test.columns:
                target_file = 'database/khoan_chi.csv'
                loai_data = "Khoản Chi Tiêu"
            else:
                messagebox.showerror("Lỗi cấu trúc",
                                     "File CSV không đúng định dạng!\nFile phải có cột 'NguonThu' hoặc 'NguonChi'.")
                return

            if not os.path.exists('database'): os.makedirs('database')

            # Áp dụng giải pháp gộp dữ liệu động bằng Pandas đã tối ưu thay vì copy đè của bài trước bồ nhé
            if os.path.exists(target_file):
                df_old = pd.read_csv(target_file)
                df_combined = pd.concat([df_old, df_test], ignore_index=True).drop_duplicates()
                df_combined.to_csv(target_file, index=False, encoding='utf-8-sig')
            else:
                df_test.to_csv(target_file, index=False, encoding='utf-8-sig')

            if "Thu_Page" in self.pages and hasattr(self, 'thu_controller'): self.thu_controller.load_data()
            if "Chi_Page" in self.pages and hasattr(self, 'chi_controller'): self.chi_controller.load_data()
            if "NganSach_Page" in self.pages and hasattr(self,
                                                         'ngansach_controller'): self.ngansach_controller.load_data()
            if "HomePage" in self.pages and hasattr(self, 'home_controller'): self.home_controller.load_data()
            if "PhanTich_Page" in self.pages and hasattr(self,
                                                         'phantich_controller'): self.phantich_controller.load_data_and_draw_chart()

            messagebox.showinfo("Thành công", f"Đã import dữ liệu [{loai_data}] thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi hệ thống", f"Không thể import file: {str(e)}")

    def export_csv(self):
        export_window = tk.Toplevel(self)
        export_window.title("Xuất dữ liệu")
        export_window.geometry("380x150")
        export_window.resizable(False, False)
        export_window.grab_set()

        export_window.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (export_window.winfo_width() // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (export_window.winfo_height() // 2)
        export_window.geometry(f"+{x}+{y}")

        tk.Label(export_window, text="Bạn muốn xuất dữ liệu nào?", font=("Arial", 12, "bold")).pack(pady=15)
        button_frame = tk.Frame(export_window)
        button_frame.pack(pady=5)

        def thuc_hien_export(loai_chon):
            export_window.destroy()
            if loai_chon == "thu":
                source_file = "database/khoan_thu.csv"
                default_name = "baocao_khoanthu.csv"
                dialog_title = "Lưu file Khoản Thu Nhập ra máy tính"
            else:
                source_file = "database/khoan_chi.csv"
                default_name = "baocao_khoanchi.csv"
                dialog_title = "Lưu file Khoản Chi Tiêu ra máy tính"

            if not os.path.exists(source_file):
                messagebox.showwarning("Thông báo", "Chưa có dữ liệu nào để xuất!")
                return

            save_path = filedialog.asksaveasfilename(
                initialfile=default_name,
                defaultextension=".csv",
                filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
                title=dialog_title
            )

            if save_path:
                try:
                    shutil.copy(source_file, save_path)
                    messagebox.showinfo("Thành công", f"Đã xuất dữ liệu thành công tại:\n{save_path}")
                except Exception as e:
                    messagebox.showerror("Lỗi", f"Không thể xuất file: {str(e)}")

        tk.Button(button_frame, text="💰 Khoản Thu", bg="#2ecc71", fg="white", font=("Arial", 11, "bold"),
                  cursor="hand2", command=lambda: thuc_hien_export("thu")).pack(side="left", padx=10)
        tk.Button(button_frame, text="💸 Khoản Chi", bg="#e74c3c", fg="white", font=("Arial", 11, "bold"),
                  cursor="hand2", command=lambda: thuc_hien_export("chi")).pack(side="left", padx=10)

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
