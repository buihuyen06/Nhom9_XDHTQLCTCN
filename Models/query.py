import os
import pandas as pd


class CSVQuery:
    def __init__(self, file_path):
        """Khởi tạo cấu trúc file dữ liệu tài khoản."""
        self.file_path = file_path

        # Nếu file tkdn.csv chưa tồn tại, tự động tạo mới với các tiêu đề cột mặc định
        if not os.path.exists(self.file_path):
            # Cập nhật: Thêm cột 'vaitro' để hỗ trợ phân quyền Admin/User
            df = pd.DataFrame(columns=["tendn", "mk", "vaitro"])

            # Đảm bảo thư mục cha (ví dụ thư mục "main") đã được tạo
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

            # Lưu file với mã hóa utf-8 để tránh lỗi font tiếng Việt
            df.to_csv(self.file_path, index=False, encoding="utf-8")

    def _read_file(self):
        """Hỗ trợ đọc file CSV nội bộ, trả về một DataFrame."""
        try:
            return pd.read_csv(self.file_path, encoding="utf-8")
        except Exception:
            # Nếu có lỗi đọc file, trả về DataFrame trống đúng cấu trúc
            return pd.DataFrame(columns=["tendn", "mk", "vaitro"])

    def search(self, field, value):
        """Tìm kiếm dữ liệu dựa trên tên cột (field) và giá trị cần tìm (value)."""
        df = self._read_file()
        # Chuyển đổi toàn bộ cột về dạng chuỗi (str) để so sánh chính xác tuyệt đối
        result = df[df[field].astype(str) == str(value)]
        return result

    def create(self, data_dict):
        """Thêm một dòng tài khoản mới vào file CSV."""
        df = self._read_file()
        # Tạo một DataFrame mới từ dữ liệu người dùng truyền vào
        new_row = pd.DataFrame([data_dict])

        # Nối dòng mới vào DataFrame cũ (dùng pd.concat thay cho append để tránh cảnh báo)
        df = pd.concat([df, new_row], ignore_index=True)

        # Ghi đè lại vào file CSV
        df.to_csv(self.file_path, index=False, encoding="utf-8")