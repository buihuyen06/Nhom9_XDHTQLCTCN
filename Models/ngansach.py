import pandas as pd
import numpy as np
import os


class NganSach_Model:
    def __init__(self):
        self.file_path = 'database/ngan_sach.csv'
        self.chi_file = 'database/khoan_chi.csv'
        self.ensure_file_exists()

    def ensure_file_exists(self):
        if not os.path.exists('database'):
            os.makedirs('database')
        if not os.path.exists(self.file_path):
            df = pd.DataFrame(columns=['NguonChi', 'HanMuc'])
            df.to_csv(self.file_path, index=False, encoding='utf-8')

    def get_all_with_spending(self):
        """Hàm tính toán Ngân Sách bằng PANDAS (Tự động cập nhật danh mục từ file Import)"""
        if not os.path.exists(self.file_path):
            return []
        try:
            # 1. Đọc file Ngân sách (Nếu file trống thì tạo DataFrame rỗng cấu trúc để Merge không lỗi)
            df_ns = pd.read_csv(self.file_path)
            if df_ns.empty:
                df_ns = pd.DataFrame(columns=['NguonChi', 'HanMuc'])

            # 2. Đọc file Khoản chi để tính tổng đã chi
            if os.path.exists(self.chi_file):
                df_chi = pd.read_csv(self.chi_file)
                if not df_chi.empty:
                    # Dùng Pandas groupby để cộng dồn tiền chi theo từng danh mục
                    tong_chi = df_chi.groupby('NguonChi')['SoTien'].sum().reset_index()
                    tong_chi.columns = ['NguonChi', 'DaChi']  # Đổi tên cột cho rõ nghĩa

                    # 🔥 ĐỔI THÀNH 'outer' để lấy TẤT CẢ các danh mục xuất hiện ở cả 2 file
                    df_merged = pd.merge(df_ns, tong_chi, on='NguonChi', how='outer')
                else:
                    df_merged = df_ns.copy()
                    df_merged['DaChi'] = 0
            else:
                df_merged = df_ns.copy()
                df_merged['DaChi'] = 0

            # 3. Điền số 0 vào các ô trống (NaN) sinh ra do phép nối Outer Join
            # - Danh mục mới từ file CSV chưa được cài hạn mức -> HanMuc = 0
            # - Danh mục đã cài hạn mức nhưng tháng này chưa tiêu gì -> DaChi = 0
            df_merged['HanMuc'] = df_merged['HanMuc'].fillna(0)
            df_merged['DaChi'] = df_merged['DaChi'].fillna(0)

            # 4. Sử dụng tính toán mảng (Numpy/Pandas vectorization) để tính tiền còn lại
            df_merged['ConLai'] = df_merged['HanMuc'] - df_merged['DaChi']

            # Lọc lấy đúng 4 cột cần thiết và trả về dạng danh sách list của list
            result = df_merged[['NguonChi', 'HanMuc', 'DaChi', 'ConLai']]
            return result.values.tolist()

        except Exception as e:
            return []

    def add_or_update(self, nguon_chi, han_muc):
        """Thêm hoặc sửa hạn mức ngân sách"""
        if not os.path.exists(self.file_path): return
        df = pd.read_csv(self.file_path)

        # Đảm bảo ép kiểu danh mục về string để so sánh chính xác
        df['NguonChi'] = df['NguonChi'].astype(str)

        if nguon_chi in df['NguonChi'].values:
            # Nếu đã có thì cập nhật lại hạn mức
            df.loc[df['NguonChi'] == nguon_chi, 'HanMuc'] = han_muc
        else:
            # Nếu chưa có thì dùng concat để nối thêm dòng mới
            new_row = pd.DataFrame([[nguon_chi, han_muc]], columns=['NguonChi', 'HanMuc'])
            df = pd.concat([df, new_row], ignore_index=True)

        df.to_csv(self.file_path, index=False, encoding='utf-8')

    def delete(self, nguon_chi):
        """Xóa mục khỏi cấu hình ngân sách"""
        if not os.path.exists(self.file_path): return
        df = pd.read_csv(self.file_path)
        df['NguonChi'] = df['NguonChi'].astype(str)
        df = df[df['NguonChi'] != nguon_chi]
        df.to_csv(self.file_path, index=False, encoding='utf-8')