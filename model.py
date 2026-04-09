import json
import os

class AccountModel:
    def __init__(self, filename='accounts.json'):
        self.filename = filename
        self.accounts = self.load_accounts()

    def load_accounts(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                return json.load(f)
        return {}

    def save_accounts(self):
        with open(self.filename, 'w') as f:
            json.dump(self.accounts, f, indent=4)

    def create_account(self, username, password):
        if username in self.accounts:
            return False
        self.accounts[username] = {'password': password, 'balance': 0.0, 'transactions': []}
        self.save_accounts()
        return True

    def authenticate(self, username, password):
        return username in self.accounts and self.accounts[username]['password'] == password

    def add_transaction(self, username, amount, note):
        self.accounts[username]['balance'] += amount
        self.accounts[username]['transactions'].append({'amount': amount, 'note': note})
        self.save_accounts()

    def get_balance(self, username):
        return self.accounts[username]['balance']

    def get_transactions(self, username):
        return self.accounts[username]['transactions']