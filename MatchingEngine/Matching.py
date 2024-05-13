from MatchingEngine.Order import Order

class MatchingEngine:
    def __init__(self):
        self.order_book = {'buy': [], 'sell': []}
        self.close_price = None
        self.open_price = None
    def add_order(self, order):
        if order.side == 'buy':
            self.order_book['buy'].append(order)
        else:
            self.order_book['sell'].append(order)
    def set_open_price(self):
        self.open_price = self.find_max_price_()
        return self.open_price
    def set_close_price(self):
        self.close_price = self.find_max_price_()
        return self.close_price

    def find_max_price_(self):
        buy_orders = sorted(self.order_book['buy'], key=lambda x: x.price, reverse=True)
        sell_orders = sorted(self.order_book['sell'], key=lambda x: x.price)
        buy_cumulative = {}
        sell_cumulative = {}
        cumulative_quantity = 0
        for order in buy_orders:
            cumulative_quantity += order.quantity
            buy_cumulative[order.price] = cumulative_quantity
        cumulative_quantity = 0
        for order in sell_orders:
            cumulative_quantity += order.quantity
            sell_cumulative[order.price] = cumulative_quantity

        max_volume = 0
        best_price = None

        for price in range(min(sell_cumulative.keys(), default=0), max(buy_cumulative.keys(), default=0)):
            buy_volume = buy_cumulative.get(price, 0)
            sell_volume = sell_cumulative.get(price, 0)
            matched_volume = min(buy_volume, sell_volume)
            if matched_volume > max_volume:
                max_volume = matched_volume
                best_price = price
        return best_price


engine = MatchingEngine()
engine.add_order(Order('9:00:01','A1','ANYID','SIA','buy',32,4500))
engine.add_order(Order('9:00:01','A1','ANYID','SIA','sell',31,1000))
engine.add_order(Order('9:00:01','A1','ANYID','SIA','buy',32,1500))
engine.add_order(Order('9:00:01','A1','ANYID','SIA','buy',32,100))
engine.add_order(Order('9:00:01','A1','ANYID','SIA','buy',31.9,800))
engine.set_close_price()
print(engine.close_price)


