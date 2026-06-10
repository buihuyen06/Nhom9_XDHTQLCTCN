import pandas as pd
import numpy as np
import os


class Thu_Model:
    def __init__(self):
        self.file_path = 'database/khoan_thu.csv'
        self.ensure_file_exists()

    def ensure_file_exists(self):
        """Tự động tạo thư mục và file csv bằng Pandas"""
        if not os.path.exists('database'):
            os.makedirs('database')
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
        try:
            so_tien = float(so_tien)
        except:
            so_tien = 0.0
        if len(records) == 0:
            new_id = 1
        else:
            array_ids = np.array([int(row[0]) for row in records])
            new_id = int(np.max(array_ids)) + 1

        new_row = pd.DataFrame([[new_id, ngay, nguon_thu, so_tien, phuong_thuc, ghi_chu]],
                               columns=['ID', 'Ngay', 'NguonThu', 'SoTien', 'PhuongThuc', 'GhiChu'])
        new_row.to_csv(self.file_path, mode='a', header=False, index=False, encoding='utf-8')
        return new_id

    def update(self, income_id, ngay, nguon_thu, so_tien, phuong_thuc, ghi_chu):
        if not os.path.exists(self.file_path): return

        df = pd.read_csv(self.file_path)

        # --- BỘ LỌC DỮ LIỆU ĐỂ TRÁNH LỖI KIỂU ---
        # 1. Ép toàn bộ cột SoTien về kiểu số, nếu lỗi thì biến thành 0
        df['SoTien'] = pd.to_numeric(df['SoTien'], errors='coerce').fillna(0)

        # 2. Ép ID về int để so sánh đúng
        df['ID'] = pd.to_numeric(df['ID'], errors='coerce').fillna(0).astype(int)

        # 3. Thực hiện cập nhật
        target_id = int(float(income_id))
        df.loc[df['ID'] == target_id, ['Ngay', 'NguonChi', 'SoTien', 'PhuongThuc', 'GhiChu']] = \
            [ngay, nguon_thu, float(so_tien), phuong_thuc, ghi_chu]

        df.to_csv(self.file_path, index=False, encoding='utf-8-sig')


    def delete(self, thu_id):
        """Xóa dòng dữ liệu bằng Pandas"""
        if not os.path.exists(self.file_path):
            return
        df = pd.read_csv(self.file_path)
        df = df[df['ID'] != int(thu_id)]
        df.to_csv(self.file_path, index=False, encoding='utf-8')