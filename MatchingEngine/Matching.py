from Order import Order, Client, Instrument
from check import processChecks

class MatchingEngine:
    def __init__(self):
        self.order_book = {'Buy': [], 'Sell': []}
        self.close_price = None
        self.open_price = None

    def add_order(self, order):
        if order.side == 'Buy':
            self.order_book['Buy'].append(order)
        else:
            self.order_book['Sell'].append(order)
    def set_open_price(self):
        self.open_price = self.find_max_price_()
        return self.open_price
    def set_close_price(self):
        self.close_price = self.find_max_price_()
        return self.close_price

    def find_max_price_(self, filteredList):
        unique_price = []
        buy_dict = {}
        sell_dict = {}

        for obj in filteredList:
            price = obj.price 
            if price == "Market" and obj.side == "Buy":
                price = float("inf")
            
            if price == "Market" and obj.side == "Sell":
                price = float("-inf")

            if price not in unique_price:
                unique_price.append(price)

            if obj.side == "Buy":
                if price in buy_dict.keys():
                    buy_dict[price] += [(obj.order_id, obj.quantity)]
                else:
                    buy_dict[price] = [(obj.order_id, obj.quantity)]

            if obj.side == "Sell":
                if price in sell_dict.keys():
                    sell_dict[price] += [(obj.order_id, obj.quantity)]
                else:
                    sell_dict[price] = [(obj.order_id, obj.quantity)]

        

        # buy_orders = sorted(self.order_book['Buy'], key=lambda x: x.price, reverse=True)
        # sell_orders = sorted(self.order_book['Sell'], key=lambda x: x.price)
        # buy_cumulative = {}
        # sell_cumulative = {}
        # cumulative_quantity = 0
        # for order in buy_orders:
        #     cumulative_quantity += order.quantity
        #     buy_cumulative[order.price] = cumulative_quantity
        #     if order.price not in unique_price:
        #         unique_price.append(order.price)

        # cumulative_quantity = 0
        # for order in sell_orders:
        #     cumulative_quantity += order.quantity
        #     sell_cumulative[order.price] = cumulative_quantity
        #     if order.price not in unique_price:
        #         unique_price.append(order.price)
######
        max_volume = 0
        best_price = None

        unique_price = sorted(unique_price)

        # print(buy_dict, sell_dict, unique_price)

        # # print("here2", buy_cumulative, sell_cumulative)

        buy_mkt = []
        sell_mkt=[]

        for price in unique_price:            

            if price == float("inf"):
                buy_mkt = buy_dict[price]

            if price == float("-inf"):
                sell_mkt = sell_dict[price]
                
        print(buy_mkt)

        buy_order = []
        sell_order = []

        if buy_mkt: # there is buy market -> 
            for key in sell_dict.keys():
                sell_order += sell_dict[key]

        if sell_mkt: 
            for key in buy_dict.keys():
                buy_order += buy_dict[key]

        for price in unique_price:
            print("prce", price)
            # if (price in buy_dict.keys() and price in sell_dict.keys()):
            
            if not buy_mkt: # there is buy market -> 
                if price in sell_dict.keys():
                    sell_order += sell_dict[price]
                    print("HERE!!!!", sell_dict[price])


            if not sell_mkt: 
                if price in buy_dict.keys():
                    buy_order += buy_dict[price]
                    print("HERE!!!!", buy_dict[price])

            print(buy_order, sell_order, "HERE")

            buy_qty = 0
            for order in buy_order:
                print(order)
                qty = order[1]
                buy_qty += qty

            sell_qty = 0
            for order in sell_order:
                qty = order[1]
                sell_qty += qty

            matched = min(buy_qty, sell_qty)
            print(matched)
        
            if matched > max_volume and price != float("inf"):
                max_volume = matched
                best_price = price


        return ("result", best_price)
    
    def setup(self):
        
        filtered = []

        # for obj in filtered:
        #     self.add_order(obj)

        return self.order_book



engine = MatchingEngine()
engine.add_order(Order('09:00:01','B1','ANYID','SIA','Sell',32.1,4500))
engine.add_order(Order('09:00:01','E1','ANYID','SIA','Sell',32.0,1000))
engine.add_order(Order('09:00:01','A1','ANYID','SIA','Buy',"Market",1500))
engine.add_order(Order('09:00:01','C1','ANYID','SIA','Buy',32.0,100))
engine.add_order(Order('09:00:01','A2','ANYID','SIA','Buy',31.9,800))
# engine.set_close_price()
# print(engine.close_price)

print(engine.setup())

fil = [Order('09:00:01','B1','ANYID','SIA','Sell',32.1,4500),
       Order('09:00:01','E1','ANYID','SIA','Sell',32.0,1000),
       Order('09:00:01','A1','ANYID','SIA','Buy',"Market",1500),
       Order('09:00:01','C1','ANYID','SIA','Buy',32.0,100),
       Order('09:00:01','A2','ANYID','SIA','Buy',31.9,800)]
print(engine.find_max_price_(fil))


