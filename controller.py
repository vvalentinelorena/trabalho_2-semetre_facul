from model import Model
from view import View

class Controller:
    def __init__(self):
        self.model = Model("bd_cdf.db")
        self.view = View(self)
        self.refresh_data_table()

    def insert_data(self, nome, valor, datadgasto, quant):
        print("controler",nome)
        self.model.insert_data(nome, valor, datadgasto, quant)
        self.refresh_data_table()

    def update_data(self, id, nome, valor, datadgasto, quant):
        self.model.update_data(id, nome, valor, datadgasto, quant)
        self.refresh_data_table()

    def delete_data(self, id):
        self.model.delete_data(id)
        self.refresh_data_table()

    def refresh_data_table(self):
        data = self.model.get_data()

    



