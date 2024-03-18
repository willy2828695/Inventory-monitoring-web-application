import pandas as pd
import matplotlib.pyplot as plt
from Connect_database import db_connection
import sqlite3

# python Best_sale_by_year.py
# Function to fetch and group data by 料號 (Part Number)
def fetch_best_sale_by_year(conn,year):
    query = "SELECT id, vehicle_type, COUNT(*) as frequency FROM sales_record WHERE date LIKE'{}%'GROUP BY id ORDER BY frequency DESC LIMIT 20;"
    cursor = conn.cursor()
    try:
        cursor.execute(query.format(year))
        grouped_data = cursor.fetchall()
        #print("Data fetched successfully!")
        
        grouped_data_df = pd.DataFrame(grouped_data, columns=['id', 'Vehicle Type','Frequency'])
        return grouped_data_df
        
    except sqlite3.Error as e:
        print(f"Error fetching data: {e}")
        return None


def exacute_best_sale_by_year(year):
    conn = db_connection()
    if conn is not None:
        grouped_data_df = fetch_best_sale_by_year(conn, year)
        conn.close()
        return grouped_data_df
    else:
        print("Connection to database failed.")

def main():
    result = exacute_best_sale_by_year(2017)
    if result is not None:
        result1 = result['id'].tolist()
        print(result1)
    else:
        print("No data to display.")

if __name__ == "__main__":
    main()