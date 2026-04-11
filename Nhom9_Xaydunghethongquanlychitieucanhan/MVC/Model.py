class SpendingModel:
    def __init__(self):
        # Giả lập database bằng List
        self.data = [
            {"name": "Ăn trưa", "price": 35000, "type": "Chi"},
            {"name": "Bố mẹ cho", "price": 1000000, "type": "Thu"}
        ]
        self.user = {"username": "sinhvien_it", "balance": 5000000}

    def save(self, name, price, t_type):
        self.data.append({"name": name, "price": price, "type": t_type})