import View.HistoryPage as HistoryPage


class LichSuChiTieu:
    def __init__(self, file_path, title=None):
        self.file_path = file_path

        if title is None:
            title = ["ngay", "phanloai", "hangmuc", "sotien", "ghichu"]

        self.title = title

    # Đọc file CSV
    def read_csv(self):
        return HistoryPage.read_csv(self.file_path)

    # Hiển thị danh sách có phân trang
    def list(self, page=1, page_size=10):
        data = self.read_csv()

        if self.title:
            data = data[self.title]

        start = (page - 1) * page_size
        end = start + page_size

        page_data = [
            data.iloc[i].to_dict()
            for i in range(start, min(end, len(data)))
        ]

        result = {
            "page": page,
            "page_size": page_size,
            "total_records": len(data),
            "total_pages": (len(data) + page_size - 1) // page_size,
            "data": page_data
        }

        return result

    # Tìm kiếm
    def search(self, title_keyword, keyword):
        data = self.read_csv()

        if self.title:
            data = data[self.title]

        result = data[
            data[title_keyword]
            .astype(str)
            .str.contains(keyword, case=False, na=False)
        ]

        return [result.iloc[i].to_dict() for i in range(len(result))]

    # Xóa dữ liệu
    def delete(self, title_keyword, keyword):
        data = self.read_csv()

        result = data[
            ~data[title_keyword]
            .astype(str)
            .str.contains(keyword, case=False, na=False)
        ]

        result.to_csv(self.file_path, index=False)

        return True

    # Cập nhật dữ liệu
    def update(self, title_keyword, keyword, title_edit, new_data):
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

    # Thêm dữ liệu mới
    def create(self, new_data):
        data = self.read_csv()

        new_row =  HistoryPage.DataFrame([new_data], columns=self.title)

        data =  HistoryPage.concat([data, new_row], ignore_index=True)

        data.to_csv(self.file_path, index=False)

        return True