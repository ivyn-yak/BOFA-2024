import pandas as pd

clients = pd.read_csv("./DataSets/example-set/input_clients.csv")
instruments = pd.read_csv("./DataSets/example-set/input_instruments.csv")
orders = pd.read_csv("./DataSets/example-set/input_orders.csv")

print(orders.head())
print(clients.head())
print(instruments.head())

def processChecks(Order, Client, Instrument):
    # check 1 - invalid instrument
    instrument = Order.instrument
    instruments = Instrument.getAllInstruments

    if instrument not in instruments:
        return "Instrument Not Found"
    
    #check 2 - mismatch currency
    currencies = Client.currencies
    curr = Instrument.currency

    if curr not in currencies:
        return "Mismatch Currency"
    
    #check 3 - invalid lot size 
    lotSize = Instrument.lotSize
    qty = Order.quantity

    if qty % lotSize != 0:
        return "Invalid Lot Size"
    
    #check 4 - position size failed
    side = Order.side
    positionCheck = Client.positionCheck

    if side == "Sell" and positionCheck == "Y":
        position = Client.getPosition
        quantity = Order.quantity
        if quantity > position:
            return "Position Check Failed"

    return "Success"
