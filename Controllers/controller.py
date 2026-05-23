import os
# Import class CSVQuery từ file csv_query.py (Đảm bảo 2 file ở cùng thư mục hoặc import đúng đường dẫn)
from Models.query import CSVQuery


class SpendingController:
    def __init__(self):
        """Cấu hình đường dẫn và khởi tạo CSVQuery."""
        # Lấy đường dẫn tuyệt đối của thư mục chứa dự án
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Đường dẫn dẫn thẳng tới file: đường_dẫn_gốc/main/tkdn.csv
        users_path = os.path.join(base_dir, "main", "tkdn.csv")

        # Khởi tạo đối tượng query
        self.query = CSVQuery(users_path)

    def get_summary(self):
        """Hàm thống kê chi tiêu (tạm thời trả về các giá trị mặc định)."""
        return 0, 0, 0

    def check_login(self, u, p, role):
        """Kiểm tra tên đăng nhập, mật khẩu VÀ loại tài khoản."""
        result = self.query.search("tendn", u)

        if not result.empty:
            user = result.iloc[0]

            # Kiểm tra xem mật khẩu có khớp không
            is_pass_match = str(user["mk"]) == str(p)

            # Lấy vai trò từ file CSV (Dùng get để tránh lỗi nếu file CSV cũ chưa có cột vaitro)
            db_role = str(user.get("vaitro", "Người dùng"))
            is_role_match = (db_role == role)

            return is_pass_match and is_role_match

        return False

    def register(self, u, p, role="Người dùng"):
        """Đăng ký tài khoản mới, mặc định là 'Người dùng'."""
        result = self.query.search("tendn", u)

        if result.empty:
            # Lưu thêm thông tin cột 'vaitro'
            self.query.create({"tendn": u, "mk": p, "vaitro": role})
            return True

        return False