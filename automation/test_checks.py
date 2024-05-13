from Classes import Order, Client, Instrument
import unittest

def processChecks(instrument_dict, client_dict, order_dict):
    rejected_orders = []
    order_book = []

    for order in order_dict.values():

        clientId = order.client_id
        instrument = order.instrument_id

        clientObj = client_dict[clientId]

        # check 1 - invalid instrument
        if instrument not in instrument_dict.keys():
            rejected_orders.append([str(order.order_id), "REJECTED - INSTRUMENT NOT FOUND"])
            break

        instrumentObj = instrument_dict[instrument]

        #check 2 - mismatch currency
        currencies = clientObj.currencies
        curr = instrumentObj.currency

        if curr not in currencies:
            rejected_orders.append(
                [str(order.order_id), "REJECTED - MISMATCH CURRENCY"]
            )
            break
        
        #check 3 - invalid lot size 
        lotSize = instrumentObj.lot_size
        qty = order.quantity

        if qty % lotSize != 0:
            rejected_orders.append(
                [str(order.order_id), "REJECTED - INVALID LOT SIZE"]
                )
            break
        
        #check 4 - position size failed
        side = order.side
        positionCheck = clientObj.position_check

        if side == "Sell" and positionCheck == "Y":
            position_dict = clientObj.net_position

            if instrument not in position_dict.keys():
                rejected_orders.append(
                [str(order.order_id), "REJECTED - POSITION CHECK FAILED"]
                )
                
            else:
                curr_position = position_dict[instrument]
                quantity = order.quantity
                if quantity > curr_position:
                    rejected_orders.append([str(order.order_id), "REJECTED - POSITION CHECK FAILED"])
                    
            break

        order_book.append(order)

    return {
        "rejected": rejected_orders,
        "filtered": order_book
    }

class CheckTest(unittest.TestCase):

    def test_check1(self):
        instrument_dict = {
            "SIA": Instrument(instrument_id="SGD", currency="SGD", lot_size=100)
        }

        client_dict = {
            "D": Client(client_id="D",currencies= ["USD"], position_check="Y", rating=4, net_position={})
        }

        order_dict = {
            "D1": Order(time="09:10:00", client_id="D", instrument_id="SIA", side="Sell", price="Market", quantity=300, order_id="D1")
        }

        result = processChecks(instrument_dict, client_dict, order_dict)["rejected"]
        order_id = result[0][0]
        reason = result[0][1]

        self.assertEqual(order_id, "D1")
        self.assertEqual(reason, "REJECTED - MISMATCH CURRENCY")


    def test_check2(self):
        instrument_dict = {
            "SIA": Instrument(instrument_id="SIA", currency="SGD", lot_size=100)
        }

        client_dict = {
            "B": Client(client_id="B",currencies= ["USD", "SGD", "JPY"], position_check="N", rating=2, net_position={})
        }

        order_dict = {
            "B1": Order(time="09:29:01", client_id="B", instrument_id="SIA", side="Sell", price=32.1, quantity=5, order_id="B2")
        }

        result = processChecks(instrument_dict, client_dict, order_dict)["rejected"]
        order_id = result[0][0]
        reason = result[0][1]
        
        self.assertEqual(order_id, "B2")
        self.assertEqual(reason, "REJECTED - INVALID LOT SIZE")

    def test_check3(self):
        instrument_dict = {
            "SIA": Instrument(instrument_id="SIA", currency="SGD", lot_size=100)
        }

        client_dict = {
            "B": Client(client_id="B",currencies= ["SGD"], position_check="N", rating=2, net_position={})
        }

        order_dict = {
            "B1": Order(time="09:29:01", client_id="B", instrument_id="XXX", side="Sell", price=32.1, quantity=5, order_id="B2")
        }

        result = processChecks(instrument_dict, client_dict, order_dict)["rejected"]
        order_id = result[0][0]
        reason = result[0][1]
        
        self.assertEqual(order_id, "B2")
        self.assertEqual(reason, "REJECTED - INSTRUMENT NOT FOUND")

    def test_check4(self):
        instrument_dict = {
            "SIA": Instrument(instrument_id="SIA", currency="SGD", lot_size=100)
        }

        client_dict = {
            "B": Client(client_id="B",currencies= ["SGD"], position_check="Y", rating=2, net_position={})
        }

        order_dict = {
            "B1": Order(time="09:29:01", client_id="B", instrument_id="SIA", side="Sell", price=32.1, quantity=1000, order_id="B2")
        }

        result = processChecks(instrument_dict, client_dict, order_dict)["rejected"]
        order_id = result[0][0]
        reason = result[0][1]
        
        self.assertEqual(order_id, "B2")
        self.assertEqual(reason, "REJECTED - POSITION CHECK FAILED")

    def test_check5(self):
        instrument_dict = {
            "SIA": Instrument(instrument_id="SIA", currency="SGD", lot_size=100)
        }

        client_dict = {
            "B": Client(client_id="B",currencies= ["SGD"], position_check="N", rating=2, net_position={})
        }

        order_dict = {
            "B1": Order(time="09:29:01", client_id="B", instrument_id="SIA", side="Sell", price=32.1, quantity=1000, order_id="B2")
        }

        result = processChecks(instrument_dict, client_dict, order_dict)["filtered"]
        
        client_id = result[0].client_id
        time = result[0].time
        instrument_id = result[0].instrument_id
        side = result[0].side
        price = result[0].price
        quantity = result[0].quantity
        order_id = result[0].order_id

        # print(result, expected)
        self.assertEqual(client_id, "B")
        self.assertEqual(time, "09:29:01")
        self.assertEqual(instrument_id, "SIA")
        self.assertEqual(side, "Sell")
        self.assertEqual(price, 32.1)
        self.assertEqual(quantity, 1000)
        self.assertEqual(order_id, "B2")
    

if __name__ == "__main__":
    unittest.main()
        
