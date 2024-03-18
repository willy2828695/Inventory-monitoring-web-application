import pandas as pd
import matplotlib.pyplot as plt
from Connect_database import db_connection
import sqlite3

def fetch_product_cost(conn,product):
    query = "SELECT 日期,料號,數量,成本, round(成本  / 數量,2) AS UnitCost FROM LK_inventory WHERE 料號='{}';"
    cursor = conn.cursor()
    try:
        cursor.execute(query.format(product))
        grouped_data = cursor.fetchall()
        #print("Data fetched successfully!")
        
        grouped_data_df = pd.DataFrame(grouped_data, columns=['date','id', 'Quantity','Cost Amount','Unitcost'])

        return grouped_data_df
        
    except sqlite3.Error as e:
        print(f"Error fetching data: {e}")
        return None
    

# Plotting
def plotting(datafram):
    x = pd.to_datetime(datafram['date']).dt.date.to_numpy()

    y = datafram['Unitcost'].astype(float).to_numpy()
    average_open_price = y.mean()


    x = pd.to_datetime(datafram['date']).dt.date.to_numpy()
    y = datafram['Unitcost'].astype(float).to_numpy()
    average_open_price = y.mean()
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, marker='.', linestyle='-', color='blue', label=f'Open Price')
    plt.axhline(average_open_price, color='red', linestyle='--', label=f'Average: ${average_open_price:.2f}')
    product = datafram['id'].iloc[0]
    plt.title("{}'s Price Over Time".format(product))
    plt.xlabel('Date')
    plt.ylabel('Price ($)')
    # plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.show()

def exacute_product_cost_chart():
    conn = db_connection()
    if conn is not None:
        grouped_data_df = fetch_product_cost(conn, "MET1 121 D A")
        conn.close()
        result = plotting(grouped_data_df)
        return result
    else:
        print("Connection to database failed.")

def main():
    result = exacute_product_cost_chart()
    if result is not None:
        print(result)
    else:
        print("No data to display.")

if __name__ == "__main__":
    main()