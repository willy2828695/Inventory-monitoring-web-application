import pandas as pd
import matplotlib.pyplot as plt
from Connect_database import db_connection
import sqlite3
import streamlit as st

# python Customer_proportion.py
# Function to fetch and group data by 料號 (Part Number)
def fetch_best_saler(conn):
    query = "SELECT id, vehicle_type, COUNT(*) as frequency FROM sales_record GROUP BY id ORDER BY frequency DESC LIMIT 20;"
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        grouped_data = cursor.fetchall()
        #print("Data fetched successfully!")
        
        grouped_data_df = pd.DataFrame(grouped_data, columns=['id', 'Vehicle Type','Frequency'])
        return grouped_data_df
        
    except sqlite3.Error as e:
        print(f"Error fetching data: {e}")
        return None

# select the top_selling_id in Streamlit select box which generated by fetch_best_saler
def fetch_client_proportion(conn,product_id):
    
    client_sales_query = "SELECT client, sum(quantity) as totalQuantity FROM sales_record WHERE id = '{}' GROUP BY client;"
    cursor = conn.cursor()
    cursor.execute(client_sales_query.format(product_id))
    client_proportion_data = cursor.fetchall()
    client_sales_df = pd.DataFrame(client_proportion_data, columns=['Client', 'Total Quantity'])
    return client_sales_df
            

# get client and total quantity dataframe
def exacute_fetch_client_proportion(product_id):
    conn = db_connection() 
    if conn is not None:
        # grouped_data_df = fetch_best_saler(conn)
        client_data_df = fetch_client_proportion(conn,product_id)
        conn.close()
        client_data_df_sort = client_data_df.sort_values(by='Total Quantity', ascending=False)
        return client_data_df_sort.head(5)
    else:
        print("Connection to database failed.")

def exacute_fetch_client_proportion_for_product_trend(product_id):
    conn = db_connection() 
    if conn is not None:
        # grouped_data_df = fetch_best_saler(conn)
        client_data_df = fetch_client_proportion(conn,product_id)
        conn.close()
        client_data_df_sort = client_data_df.sort_values(by='Total Quantity', ascending=False)
        return client_data_df_sort.head(3)
    else:
        print("Connection to database failed.")

def plot_client_proportions(dataframe):
    if dataframe.empty:
        st.write("The DataFrame is empty.")
        return

    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(
    dataframe['Total Quantity'],
    autopct='%1.1f%%',
    startangle=140,
    )
    plt.setp(autotexts, size=10, weight="bold", color="white")
    ax.set_title('Client Proportion for Top-Selling Product')
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig)

       
    
    

def main():
    dataframe = exacute_fetch_client_proportion('4AFE 44 B2')
    result = plot_client_proportions(dataframe)
    if result is not None:
        print(result)
    else:
        print("No data to display.")

if __name__ == "__main__":
    main()