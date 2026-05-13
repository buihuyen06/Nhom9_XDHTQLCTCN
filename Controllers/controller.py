import os
from Models.query import Query


class SpendingController:
    def __init__(self):
        # Lấy thư mục hiện tại của file này
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        users_path = os.path.join(base_dir, "main", "tkdn.csv")

        self.query = Query(
            file_path=users_path,
            title=["tendn", "mk"]
        )

    def get_summary(self):
        # Sửa lỗi: query_tx và query_acc chưa được định nghĩa
        # Tạm thời return 0 để không báo lỗi
        return 0, 0, 0

    def check_login(self, u, p):
        # tìm username
        result = self.query.search("tendn", u)

        # kiểm tra có user và password đúng không
        if not result.empty:
            user = result.iloc[0]
            return str(user["mk"]) == str(p)

        return False

    def register(self, u, p):
        # kiểm tra user đã tồn tại chưa
        result = self.query.search("tendn", u)

        if result.empty:
            # thêm user mới
            self.query.create({
                "tendn": u,
                "mk": p
            })
            return True

        return False
