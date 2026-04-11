from MVC.Model import SpendingModel

class SpendingController:
    def __init__(self):
        self.model = SpendingModel()

    def get_list(self):
        return self.model.data

    def add_new(self, name, price, t_type):
        if price > 0:
            self.model.save(name, price, t_type)
            return True
        return False