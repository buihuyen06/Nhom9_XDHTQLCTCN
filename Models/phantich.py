from Models.thu import Thu_Model
from Models.chi import Chi_Model
from datetime import datetime


class PhanTich_Model:
    def __init__(self):
        self.thu_model = Thu_Model()
        self.chi_model = Chi_Model()

    def get_summary_data(self, selected_month="Tất cả", selected_year="Tất cả"):
        """Lấy tổng thu và tổng chi từ 2 bảng, có hỗ trợ lọc dữ liệu"""
        thu_records = self.thu_model.get_all()
        chi_records = self.chi_model.get_all()

        # 1. Tính tổng các khoản Thu có chọn lọc
        tong_thu = 0
        for r in thu_records:
            try:
                # r[1] là cột Ngày nhận (Định dạng DD/MM/YYYY)
                date_obj = datetime.strptime(r[1], "%d/%m/%Y")

                # Kiểm tra bộ lọc tháng
                if selected_month != "Tất cả" and int(date_obj.month) != int(selected_month):
                    continue
                # Kiểm tra bộ lọc năm
                if selected_year != "Tất cả" and int(date_obj.year) != int(selected_year):
                    continue

                tong_thu += float(r[3])
            except:
                pass

        # 2. Tính tổng các khoản Chi có chọn lọc
        tong_chi = 0
        for r in chi_records:
            try:
                date_obj = datetime.strptime(r[1], "%d/%m/%Y")

                if selected_month != "Tất cả" and int(date_obj.month) != int(selected_month):
                    continue
                if selected_year != "Tất cả" and int(date_obj.year) != int(selected_year):
                    continue

                tong_chi += float(r[3])
            except:
                pass

        return tong_thu, tong_chi