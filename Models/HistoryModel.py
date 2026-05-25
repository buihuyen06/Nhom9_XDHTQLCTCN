import os
import pandas as pd

class HistoryModel:
    def __init__(self, file_path):
        self.file_path = file_path
        self.title = ["ngay", "phanloai", "hangmuc", "sotien", "ghichu"]

        # Tự động tạo file CSV mới kèm tiêu đề nếu file chưa tồn tại
        if not os.path.exists(self.file_path):
            df = pd.DataFrame(columns=self.title)
            df.to_csv(self.file_path, index=False)

    def read_csv(self):
        """Đọc toàn bộ dữ liệu từ file CSV lên thành DataFrame"""
        try:
            return pd.read_csv(self.file_path)
        except Exception:
            return pd.DataFrame(columns=self.title)

    def list(self, page=1, page_size=10):
        """Hiển thị danh sách giao dịch có phân trang (Pagination)"""
        data = self.read_csv()
        data = data[self.title]  # Lọc đúng các cột tiêu đề

        # Tính toán vị trí cắt dữ liệu theo trang
        start = (page - 1) * page_size
        end = start + page_size

        # Chuyển đổi dữ liệu từng dòng thành dạng danh sách các Dictionary
        page_data = [
            data.iloc[i].to_dict()
            for i in range(start, min(end, len(data)))
        ]

        # Trả về kết quả cấu trúc phân trang
        result = {
            "page": page,
            "page_size": page_size,
            "total_records": len(data),
            "total_pages": (len(data) + page_size - 1) // page_size,
            "data": page_data
        }
        return result

    def search(self, title_keyword, keyword):
        """Tìm kiếm giao dịch theo từ khóa (Không phân biệt hoa thường)"""
        data = self.read_csv()
        result = data[
            data[title_keyword]
            .astype(str)
            .str.contains(keyword, case=False, na=False)
        ]
        return [result.iloc[i].to_dict() for i in range(len(result))]

    def delete(self, title_keyword, keyword):
        """Xóa dữ liệu bằng cách giữ lại các dòng KHÔNG chứa từ khóa cần xóa"""
        data = self.read_csv()
        result = data[
            ~data[title_keyword]
            .astype(str)
            .str.contains(keyword, case=False, na=False)
        ]
        result.to_csv(self.file_path, index=False)
        return True

    def update(self, title_keyword, keyword, title_edit, new_data):
        """Cập nhật dữ liệu mới vào các hàng và cột được chỉ định"""
        data = self.read_csv()
        for i in range(len(title_edit)):
            data.loc[
                data[title_keyword]
                .astype(str)
                .str.contains(keyword, case=False, na=False),
                title_edit[i]
            ] = new_data[i]
        data.to_csv(self.file_path, index=False)
        return True

    def create(self, new_data):
        """Thêm một dòng giao dịch mới vào cuối file CSV"""
        data = self.read_csv()
        new_row = pd.DataFrame([new_data], columns=self.title)
        data = pd.concat([data, new_row], ignore_index=True)
        data.to_csv(self.file_path, index=False)
        return True