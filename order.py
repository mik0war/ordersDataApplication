class Order:

    def __init__(self, id, user_fio, date_time, description, products):
        self.id = id
        self.user_fio = user_fio
        self.date_time = date_time
        self.description = description
        self.products = products


class Product:

    def __init__(self, name, cost, count):
        self.name = name
        self.cost = cost
        self.count = count