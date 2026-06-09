import csv
import os


class FinanceModel:
    def __init__(self):
        # Đường dẫn tới file csv trong thư mục data
        self.file_path = 'database/data.csv'
        self.ensure_file_exists()

    def ensure_file_exists(self):
        # Tạo thư mục data nếu chưa có
        if not os.path.exists('database'):
            os.makedirs('database')
        # Tạo file csv với tiêu đề nếu chưa có
        if not os.path.exists(self.file_path):
            with open(self.file_path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', 'Ngay', 'NoiDung', 'Loai', 'SoTien',])

    def get_all(self):
        records = []
        with open(self.file_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # Bỏ qua dòng tiêu đề
            for row in reader:
                if row:  # Tránh dòng trống
                    records.append(row)
        return records

    def add(self, ngay, noidung, loai, sotien):
        records = self.get_all()
        # Tự động tạo ID tăng dần
        new_id = 1 if not records else int(records[-1][0]) + 1

        with open(self.file_path, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([new_id, ngay, noidung, loai, sotien])

    def delete(self, trans_id):
        records = self.get_all()
        # Ghi lại toàn bộ file, bỏ qua dòng có ID trùng khớp
        with open(self.file_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Ngay', 'NoiDung', 'Loai', 'SoTien'])
            for r in records:
                if str(r[0]) != str(trans_id):
                    writer.writerow(r)