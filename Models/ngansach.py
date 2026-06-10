import pandas as pd
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
        if not os.path.exists(self.file_path):
            return []
        try:
            df_ns = pd.read_csv(self.file_path)
            if df_ns.empty:
                df_ns = pd.DataFrame(columns=['NguonChi', 'HanMuc'])

            if os.path.exists(self.chi_file):
                df_chi = pd.read_csv(self.chi_file)
                if not df_chi.empty:
                    tong_chi = df_chi.groupby('NguonChi')['SoTien'].sum().reset_index()
                    tong_chi.columns = ['NguonChi', 'DaChi']
                    df_merged = pd.merge(df_ns, tong_chi, on='NguonChi', how='outer')
                else:
                    df_merged = df_ns.copy()
                    df_merged['DaChi'] = 0

            df_merged['HanMuc'] = df_merged['HanMuc'].fillna(0)
            df_merged['DaChi'] = df_merged['DaChi'].fillna(0)

            df_merged['ConLai'] = df_merged['HanMuc'] - df_merged['DaChi']

            result = df_merged[['NguonChi', 'HanMuc', 'DaChi', 'ConLai']]
            return result.values.tolist()

        except Exception as e:
            return []

    def add_or_update(self, nguon_chi, han_muc):
        if not os.path.exists(self.file_path): return
        df = pd.read_csv(self.file_path)

        df['NguonChi'] = df['NguonChi'].astype(str)

        if nguon_chi in df['NguonChi'].values:
            df.loc[df['NguonChi'] == nguon_chi, 'HanMuc'] = han_muc
        else:
            new_row = pd.DataFrame([[nguon_chi, han_muc]], columns=['NguonChi', 'HanMuc'])
            df = pd.concat([df, new_row], ignore_index=True)

        df.to_csv(self.file_path, index=False, encoding='utf-8')

    def delete(self, nguon_chi):
        if not os.path.exists(self.file_path): return
        df = pd.read_csv(self.file_path)
        df['NguonChi'] = df['NguonChi'].astype(str)
        df = df[df['NguonChi'] != nguon_chi]
        df.to_csv(self.file_path, index=False, encoding='utf-8')