import pandas as pd
from Order import Client, Instrument, Order

clients = pd.read_csv("../DataSets/example-set/input_clients.csv")
instruments = pd.read_csv("../DataSets/example-set/input_instruments.csv")
orders = pd.read_csv("../DataSets/example-set/input_orders.csv")

def client(clients):
    client_dict = {}
    for i in range(len(clients)):
        row = clients.iloc[i]
        clientId = row["ClientID"]
        currencies = row["Currencies"]
        curr_list = currencies.split(",")
        positionCheck = row["PositionCheck"]
        rating = row["Rating"]

        client_dict[clientId] = Client(client_id=clientId,currencies= curr_list, position_check=positionCheck, rating=rating)

    return (client_dict) 

def instrument(instruments):
    instrument_dict = {}

    for i in range(len(instruments)):
        row = instruments.iloc[i]
        instrumentId = row["InstrumentID"]
        currency = row["Currency"]
        lotSize = row["LotSize"]

        instrument_dict[instrumentId] = Instrument(instrument_id=instrumentId, currency=currency, lot_size=lotSize)

    return(instrument_dict) 

def order(orders):
    order_dict = {}

    for i in range(len(orders)):
        row = orders.iloc[i]
        time = row["Time"]
        client = row["Client"]
        instrument = row["Instrument"]
        side = row["Side"]
        price = row["Price"]
        quantity = row["Quantity"]
        orderId = row["OrderID"]

        order_dict[orderId] = Order(time=time, client_id=client, instrument_id=instrument, side=side, price=price, quantity=quantity, order_id=orderId)

    return(order_dict) 


print(client(clients))
print(instrument(instruments))
print(order(orders))

instrument_dict = instrument(instruments)
client_dict = client(clients)
order_dict = order(orders)


