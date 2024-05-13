
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



def process_single_order(order_data, clients_df, order_book_df):





