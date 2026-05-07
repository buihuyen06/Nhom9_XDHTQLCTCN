import pandas as pd
class SpendingModel:
    def __init__(self):
        # Hệ thống đăng nhập
        self.users = {"admin": "123"}

        # Dữ liệu Chi tiêu
        self.transactions = [
            {"name": "Ăn trưa", "price": 35000, "type": "Chi"},
            {"name": "Lương tháng", "price": 1000000, "type": "Thu"}
        ]

        # QUẢN LÝ TÀI KHOẢN BẰNG PANDAS
        data = {
            "ID": [1, 2],
            "Tên": ["Tiền mặt", "Thẻ ATM"],
            "Số dư": [500000.0, 5465000.0]
        }
        self.df_accounts = pd.DataFrame(data)

    def add_account(self, name, balance):
        new_id = self.df_accounts["ID"].max() + 1 if not self.df_accounts.empty else 1
        new_row = pd.DataFrame([{"ID": new_id, "Tên": name, "Số dư": float(balance)}])
        self.df_accounts = pd.concat([self.df_accounts, new_row], ignore_index=True)

    def update_account(self, acc_id, name, balance):
        idx = self.df_accounts.index[self.df_accounts["ID"] == int(acc_id)]
        if not idx.empty:
            self.df_accounts.loc[idx, ["Tên", "Số dư"]] = [name, float(balance)]

    def delete_account(self, acc_id):
        self.df_accounts = self.df_accounts[self.df_accounts["ID"] != int(acc_id)]