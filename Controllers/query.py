import pandas as pd
import os

class Query:
    def __init__(self, file_path, title=[]):
        self.file_path = file_path
        self.title = title
        # Tạo file nếu chưa tồn tại
        if not os.path.exists(file_path):
            pd.DataFrame(columns=title).to_csv(file_path, index=False)

    def list(self, page, page_size):
        """Lấy danh sách dữ liệu phân trang"""
        data = pd.read_csv(self.file_path)
        if self.title:
            data = data[self.title]
        start = (page - 1) * page_size
        end = start + page_size

        page_info = {
            "page": page,
            "page_size": page_size,
            "total_records": len(data),
            "total_pages": (len(data) + page_size - 1) // page_size,
            "data": data[start:end]
        }
        return page_info

    def search(self, title_keyword, keyword):
        """Tìm kiếm theo từ khóa"""
        data = pd.read_csv(self.file_path)
        if self.title:
            data = data[self.title]
        result = data[data[title_keyword].astype(str).str.contains(str(keyword), case=False, na=False)]
        return result

    def delete(self, title_keyword, keyword):
        """Xóa dữ liệu"""
        data = pd.read_csv(self.file_path)
        if self.title:
            data = data[self.title]
        result = data[~data[title_keyword].astype(str).str.contains(str(keyword))]
        result.to_csv(self.file_path, index=False)
        return True

    def update(self, title_keyword, keyword, new_data):
        """Cập nhật dữ liệu"""
        data = pd.read_csv(self.file_path)
        if self.title:
            data = data[self.title]
        mask = data[title_keyword].astype(str).str.contains(str(keyword), case=False, na=False)
        for idx, val in enumerate(new_data):
            data.loc[mask, self.title[idx]] = val
        data.to_csv(self.file_path, index=False)
        return True

    def create(self, new_data):
        """Thêm bản ghi mới"""
        data = pd.read_csv(self.file_path)
        if self.title:
            data = data[self.title]
        new_row = pd.DataFrame([new_data], columns=self.title)
        data = pd.concat([data, new_row], ignore_index=True)
        data.to_csv(self.file_path, index=False)
        return True

    def max(self, title_keyword):
        """Lấy giá trị max của cột"""
        data = pd.read_csv(self.file_path)
        if self.title:
            data = data[self.title]
        max_value = data[title_keyword].max()
        return max_value if pd.notna(max_value) else 0

    def get_all(self):
        """Lấy toàn bộ dữ liệu"""
        data = pd.read_csv(self.file_path)
        if self.title:
            data = data[self.title]
        return data
