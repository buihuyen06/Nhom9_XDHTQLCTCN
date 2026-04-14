class SpendingController:
    def __init__(self, model):
        self.model = model

    def check_login(self, u, p):
        return u in self.model.users and self.model.users[u] == p

    def register(self, u, p):
        if u not in self.model.users:
            self.model.users[u] = p
            return True
        return False