
import pandas as pd
import numpy as np



clients_df = pd.read_csv(r'/Users/default/Pycharm1/pythonProject/DataSets/example-set/input_clients.csv')
transactions_df = pd.read_csv(r'/Users/default/Pycharm1/pythonProject/DataSets/example-set/input_orders.csv')
'''new order iput'''
# order_data=
# new_order_df = pd.DataFrame([order_data])
# new_order_df= pd.merge(new_order_df, clients_df, left_on='Client', right_on='ClientID')
merged_df = pd.merge(transactions_df, clients_df, left_on='Client', right_on='ClientID')
print(merged_df)

merged_df['sort_price'] = np.where(
        (merged_df['Price'] == 'Market') & (merged_df['Side'] == 'Buy'), float('inf'),
        np.where(
            (merged_df['Price'] == 'Market') & (merged_df['Side'] == 'Sell'), float('-inf'),
            pd.to_numeric(merged_df['Price'], errors='coerce')
        )
    )


buys = merged_df[merged_df['Side'] == 'Buy'].sort_values(by=['sort_price', 'Rating', 'Time'],
                                                             ascending=[False, False, False])
sells = merged_df[merged_df['Side'] == 'Sell'].sort_values(by=['sort_price', 'Rating', 'Time'],
                                                               ascending=[True, False, False])
sorted_df = pd.concat([buys, sells])

print(sorted_df[['Time', 'OrderID', 'Instrument', 'Quantity', 'Client', 'Price', 'Side', 'Rating']])

# def process_single_order(order_data, clients_df, order_book_df):
'''matching part'''
data = pd.concat([buys, sells])
df = pd.DataFrame(data)

# divide buy and sell
df['sort_price'] = pd.to_numeric(df['Price'], errors='coerce').fillna(
    df['Side'].map({'Buy': float('inf'), 'Sell': float('-inf')}))

buy_orders = df[df['Side'] == 'Buy'].sort_values(by=['sort_price', 'Rating', 'Time'], ascending=[False, True, True])
sell_orders = df[df['Side'] == 'Sell'].sort_values(by=['sort_price', 'Rating', 'Time'], ascending=[True, True, True])

matched_orders = []
while not buy_orders.empty and not sell_orders.empty:
    buy_order = buy_orders.iloc[0]
    sell_order = sell_orders.iloc[0]


    if buy_order['sort_price'] >= sell_order['sort_price']:

        quantity = min(buy_order['Quantity'], sell_order['Quantity'])
        matched_orders.append((buy_order['OrderID'], sell_order['OrderID'], quantity, sell_order['sort_price']))

        if buy_order['Quantity'] > quantity:
            buy_orders.at[buy_orders.index[0], 'Quantity'] -= quantity
        else:
            buy_orders = buy_orders.iloc[1:]

        if sell_order['Quantity'] > quantity:
            sell_orders.at[sell_orders.index[0], 'Quantity'] -= quantity
        else:
            sell_orders = sell_orders.iloc[1:]
    else:
        break

print(matched_orders)


