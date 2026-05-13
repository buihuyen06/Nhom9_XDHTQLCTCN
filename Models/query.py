
import pandas as pd
import os


class Query:
    def __init__(self, file_path, title=None):
        self.file_path = file_path
        self.title = title or []

        folder = os.path.dirname(file_path)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)

        if not os.path.exists(self.file_path):
            pd.DataFrame(columns=self.title).to_csv(self.file_path, index=False)

    def list(self, page=1, page_size=10):
        data = pd.read_csv(self.file_path)

        if self.title:
            data = data[self.title]

        start = (page - 1) * page_size
        end = start + page_size

        return {
            "page": page,
            "page_size": page_size,
            "total_records": len(data),
            "total_pages": (len(data) + page_size - 1) // page_size,
            "data": data.iloc[start:end]
        }

    def search(self, title_keyword, keyword):
        data = pd.read_csv(self.file_path)

        result = data[
            data[title_keyword].astype(str) == str(keyword)
        ]

        return result

    def delete(self, title_keyword, keyword):
        data = pd.read_csv(self.file_path)

        result = data[
            data[title_keyword].astype(str) != str(keyword)
        ]

        result.to_csv(self.file_path, index=False)

        return True

    def update(self, title_keyword, keyword, new_data):
        data = pd.read_csv(self.file_path)

        mask = data[title_keyword].astype(str) == str(keyword)

        for key, value in new_data.items():
            data.loc[mask, key] = value

        data.to_csv(self.file_path, index=False)

        return True

    def create(self, new_data):
        data = pd.read_csv(self.file_path)

        new_row = pd.DataFrame([new_data])

        data = pd.concat([data, new_row], ignore_index=True)

        data.to_csv(self.file_path, index=False)

        return True

    def max(self, title_keyword):
        data = pd.read_csv(self.file_path)

        if data.empty:
            return 0

        max_value = data[title_keyword].max()

        return max_value if pd.notna(max_value) else 0