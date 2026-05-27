import pandas as pd
import numpy as np
import os


class Thu_Model:
    def __init__(self):
        self.file_path = 'data/khoan_thu.csv'
        self.ensure_file_exists()

    def ensure_file_exists(self):
        """Tự động tạo thư mục và file csv bằng Pandas"""
        if not os.path.exists('data'):
            os.makedirs('data')
        if not os.path.exists(self.file_path):
            df = pd.DataFrame(columns=['ID', 'Ngay', 'NguonThu', 'SoTien', 'PhuongThuc', 'GhiChu'])
            df.to_csv(self.file_path, index=False, encoding='utf-8')

    def get_all(self):
        """Đọc toàn bộ dữ liệu Khoản Thu bằng Pandas"""
        if not os.path.exists(self.file_path):
            return []
        try:
            df = pd.read_csv(self.file_path)
            df = df.fillna("")
            return df.values.tolist()
        except Exception:
            return []

    def add(self, ngay, nguon_thu, so_tien, phuong_thuc, ghi_chu):
        """Thêm bản ghi mới, dùng Numpy tìm ID lớn nhất"""
        records = self.get_all()
        if len(records) == 0:
            new_id = 1
        else:
            array_ids = np.array([int(row[0]) for row in records])
            new_id = int(np.max(array_ids)) + 1

        new_row = pd.DataFrame([[new_id, ngay, nguon_thu, so_tien, phuong_thuc, ghi_chu]],
                               columns=['ID', 'Ngay', 'NguonThu', 'SoTien', 'PhuongThuc', 'GhiChu'])
        new_row.to_csv(self.file_path, mode='a', header=False, index=False, encoding='utf-8')
        return new_id

    def update(self, thu_id, ngay, nguon_thu, so_tien, phuong_thuc, ghi_chu):
        """Cập nhật dữ liệu bằng Pandas"""
        if not os.path.exists(self.file_path):
            return
        df = pd.read_csv(self.file_path)
        df.loc[df['ID'] == int(thu_id), ['Ngay', 'NguonThu', 'SoTien', 'PhuongThuc', 'GhiChu']] = [ngay, nguon_thu,
                                                                                                   so_tien, phuong_thuc,
                                                                                                   ghi_chu]
        df.to_csv(self.file_path, index=False, encoding='utf-8')

    def delete(self, thu_id):
        """Xóa dòng dữ liệu bằng Pandas"""
        if not os.path.exists(self.file_path):
            return
        df = pd.read_csv(self.file_path)
        df = df[df['ID'] != int(thu_id)]
        df.to_csv(self.file_path, index=False, encoding='utf-8')