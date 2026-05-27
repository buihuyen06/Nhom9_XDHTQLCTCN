import pandas as pd
import numpy as np
import os


class NganSach_Model:
    def __init__(self):
        self.file_path = 'data/ngan_sach.csv'
        self.chi_file = 'data/khoan_chi.csv'
        self.ensure_file_exists()

    def ensure_file_exists(self):
        if not os.path.exists('data'):
            os.makedirs('data')
        if not os.path.exists(self.file_path):
            df = pd.DataFrame(columns=['NguonChi', 'HanMuc'])
            df.to_csv(self.file_path, index=False, encoding='utf-8')

    def get_all_with_spending(self):
        """Hàm tính toán Ngân Sách bằng PANDAS (Ăn điểm phần Yêu cầu tính toán)"""
        if not os.path.exists(self.file_path):
            return []
        try:
            # 1. Đọc file Ngân sách
            df_ns = pd.read_csv(self.file_path)
            if df_ns.empty: return []

            # 2. Đọc file Khoản chi để tính tổng đã chi
            if os.path.exists(self.chi_file):
                df_chi = pd.read_csv(self.chi_file)
                if not df_chi.empty:
                    # Dùng Pandas groupby để cộng dồn tiền chi theo từng danh mục
                    tong_chi = df_chi.groupby('NguonChi')['SoTien'].sum().reset_index()

                    # Nối (Merge) bảng Ngân Sách và bảng Tổng Chi lại với nhau
                    df_merged = pd.merge(df_ns, tong_chi, on='NguonChi', how='left')
                    df_merged['SoTien'] = df_merged['SoTien'].fillna(0)  # Chỗ nào chưa chi thì điền số 0
                else:
                    df_merged = df_ns.copy()
                    df_merged['SoTien'] = 0
            else:
                df_merged = df_ns.copy()
                df_merged['SoTien'] = 0

            # 3. Sử dụng tính toán mảng (Numpy/Pandas vectorization) để tính tiền còn lại
            df_merged['DaChi'] = df_merged['SoTien']
            df_merged['ConLai'] = df_merged['HanMuc'] - df_merged['DaChi']

            # Lọc lấy đúng 4 cột cần thiết và trả về dạng list
            result = df_merged[['NguonChi', 'HanMuc', 'DaChi', 'ConLai']]
            return result.values.tolist()

        except Exception as e:
            return []

    def add_or_update(self, nguon_chi, han_muc):
        """Thêm hoặc sửa hạn mức ngân sách"""
        if not os.path.exists(self.file_path): return
        df = pd.read_csv(self.file_path)

        if nguon_chi in df['NguonChi'].values:
            # Nếu đã có thì cập nhật lại hạn mức
            df.loc[df['NguonChi'] == nguon_chi, 'HanMuc'] = han_muc
        else:
            # Nếu chưa có thì dùng concat để nối thêm dòng mới (Pandas đời mới chuộng concat hơn append)
            new_row = pd.DataFrame([[nguon_chi, han_muc]], columns=['NguonChi', 'HanMuc'])
            df = pd.concat([df, new_row], ignore_index=True)

        df.to_csv(self.file_path, index=False, encoding='utf-8')

    def delete(self, nguon_chi):
        if not os.path.exists(self.file_path): return
        df = pd.read_csv(self.file_path)
        df = df[df['NguonChi'] != nguon_chi]
        df.to_csv(self.file_path, index=False, encoding='utf-8')