import pandas as pd
from csvToDict import order, instrument, client

clients = pd.read_csv("../DataSets/example-set/input_clients.csv")
instruments = pd.read_csv("../DataSets/example-set/input_instruments.csv")
orders = pd.read_csv("../DataSets/example-set/input_orders.csv")

instrument_dict = instrument(instruments)
client_dict = client(clients)
order_dict = order(orders)

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


processChecks(instrument_dict, client_dict, order_dict)
