import pandas as pd
import numpy as np
import os


class Chi_Model:
    def __init__(self):
        self.file_path = 'data/khoan_chi.csv'
        self.ensure_file_exists()

    def ensure_file_exists(self):
        """Tự động tạo thư mục data và file csv bằng Pandas nếu chưa có"""
        if not os.path.exists('data'):
            os.makedirs('data')
        if not os.path.exists(self.file_path):
            # Dùng pandas tạo cấu trúc file mẫu
            df = pd.DataFrame(columns=['ID', 'Ngay', 'NguonChi', 'SoTien', 'PhuongThuc', 'GhiChu'])
            df.to_csv(self.file_path, index=False, encoding='utf-8')

    def get_all(self):
        """Đọc toàn bộ danh sách bằng Pandas"""
        if not os.path.exists(self.file_path):
            return []
        try:
            df = pd.read_csv(self.file_path)
            df = df.fillna("")  # Xử lý các ô trống tránh lỗi hiển thị
            return df.values.tolist()  # Trả về dạng list cho Treeview hiển thị
        except Exception:
            return []

    def add(self, ngay, nguon_chi, so_tien, phuong_thuc, ghi_chu):
        """Thêm một khoản chi mới với ID tự tăng tính toán bằng Numpy"""
        records = self.get_all()

        # SỬ DỤNG NUMPY: Gom toàn bộ ID lại thành mảng Numpy để tìm ID lớn nhất cực nhanh
        if len(records) == 0:
            new_id = 1
        else:
            array_ids = np.array([int(row[0]) for row in records])
            new_id = int(np.max(array_ids)) + 1

        # Dùng Pandas để append dòng mới vào file
        new_row = pd.DataFrame([[new_id, ngay, nguon_chi, so_tien, phuong_thuc, ghi_chu]],
                               columns=['ID', 'Ngay', 'NguonChi', 'SoTien', 'PhuongThuc', 'GhiChu'])
        new_row.to_csv(self.file_path, mode='a', header=False, index=False, encoding='utf-8')
        return new_id

    def update(self, income_id, ngay, nguon_chi, so_tien, phuong_thuc, ghi_chu):
        """Cập nhật bản ghi theo ID bằng Pandas"""
        if not os.path.exists(self.file_path):
            return
        df = pd.read_csv(self.file_path)
        # Tìm dòng có ID trùng khớp và cập nhật dữ liệu
        df.loc[df['ID'] == int(income_id), ['Ngay', 'NguonChi', 'SoTien', 'PhuongThuc', 'GhiChu']] = [ngay, nguon_chi,
                                                                                                      so_tien,
                                                                                                      phuong_thuc,
                                                                                                      ghi_chu]
        df.to_csv(self.file_path, index=False, encoding='utf-8')

    def delete(self, income_id):
        """Xóa bản ghi khỏi dữ liệu bằng Pandas"""
        if not os.path.exists(self.file_path):
            return
        df = pd.read_csv(self.file_path)
        # Lọc bỏ dòng có ID được chọn
        df = df[df['ID'] != int(income_id)]
        df.to_csv(self.file_path, index=False, encoding='utf-8')