class Client:
    def __init__(self, client_id, currencies, position_check, rating, net_position):
        self.client_id = client_id
        self.currencies = currencies
        self.position_check = position_check
        self.rating = rating
        self.net_position = net_position


class Instrument:
    def __init__(self, instrument_id, currency, lot_size):
        self.instrument_id = instrument_id
        self.currency = currency
        self.lot_size = lot_size

class Order:
    def __init__(self, time, order_id, client_id, instrument_id, side, price, quantity):
        self.time = time
        self.order_id = order_id
        self.client_id = client_id
        self.instrument_id = instrument_id
        self.side = side
        self.price = price
        self.quantity = quantity