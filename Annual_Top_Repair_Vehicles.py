import pandas as pd
import matplotlib.pyplot as plt
from Connect_database import db_connection
from Best_sale_by_year import fetch_best_sale_by_year
import sqlite3

# python Annual_Top_Repair_Vehicles.py
def Annual_Top_Repair_Vehicles(datafram):
    original_list = list(datafram['Vehicle Type'])
    unique_list = list(dict.fromkeys(original_list)) # fromkeys(): put each element in the original list into a dictionary as a key, then give them a "None" value.
    return unique_list

def exacute_Annual_Top_Repair_Vehicles():
    conn = db_connection()
    if conn is not None:
        grouped_data_df = fetch_best_sale_by_year(conn, 2018)
        conn.close()
        unique_list = Annual_Top_Repair_Vehicles(grouped_data_df)
        return unique_list
    else:
        print("Connection to database failed.")
        

def main():
    result = exacute_Annual_Top_Repair_Vehicles()
    if result is not None:
        print(result)
    else:
        print("No data to display.")

if __name__ == "__main__":
    main()