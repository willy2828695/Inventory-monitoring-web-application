# Function to fetch and group data by 料號 (Part Number)
import pandas as pd
import matplotlib.pyplot as plt
from Connect_database import db_connection
import sqlite3

def fetch_grouped_data(conn):
    query = "SELECT id,vehicle_type, brand, inventory FROM inventory;"
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        grouped_data = cursor.fetchall()
        
        grouped_data_df = pd.DataFrame(grouped_data, columns=['id','vehicle_type','brand','inventory'])
        return grouped_data_df
        
    except sqlite3.Error as e:
        print(f"Error fetching data: {e}")
        return None
    
    
    

def threshold_alarm(dataframe):
    # Convert the 'id' column of grouped_data_df to a dictionary with 'id' as keys
    id_list = dataframe['id'].tolist()
    # create a threshold dictionary, defult threshold is 2
    thresholds = {id_value: 100 for id_value in id_list}

    thresholds["4D30 94D NOK1"]= 1000
    thresholds["4G8297 94 NOK1"]= 1000
    thresholds[".5T 94 CFW"]= 700
    thresholds["RRV16 94 NOK1"]= 500
    thresholds["6D22 94K NOK1"]= 500
    thresholds["4JJ-1 94 NOK1"]= 500
    thresholds["4BC2 94 NOK1"]= 500
    thresholds["1W 94D1 NOK1"]= 500
    thresholds[".5T 94 CFW Z"]= 500
    thresholds["1Z 94D NOK1"]= 400
    thresholds["4JG-2 94D1 NOK1"]= 300
    thresholds["ATOS 94D 5M"]= 300
    thresholds["TII16 94D1 NOK1"]= 250
    thresholds["15B16V 94 NOK1"]= 150
    thresholds["4JG2 21 X2 A"]= 200
    thresholds["4G8298 94 D"]= 200
    thresholds["NXOU 94D5"]= 200
    thresholds["15B16V XD46 X"]= 200
    thresholds["5K 94 NOK1"]= 200
    thresholds["R2 XC"]= 150
    thresholds["V2TUC1 94D D"]= 150
    thresholds["1Z X2"]= 150
    thresholds["ZXD20 2A X2 Z"]= 150
    thresholds["C240 XC"]= 150
    thresholds["4G8298 2A X2"]= 150
    thresholds["6D95 XD45"]= 150
    thresholds["4M40T 1229 X41 A"]= 150
    thresholds["4G18 X3"]= 150
    thresholds["4JG-2 X2"]= 100
    thresholds["4G64K X3"]= 100
    thresholds["ZXD20 12 NOK X3"]= 100
    thresholds["ZXD20 X1G11"]= 100
    thresholds["7K1 12 NOK X4"]= 100
    thresholds["DE20 93C A2"]= 100
    thresholds["4M40 X15D"]= 100
    thresholds["4M40 X15C X"]= 100
    thresholds["ZXD20 2A X2 Z1"]= 100
    thresholds["13B X15D"]= 150
    thresholds["CRV03- X3"]= 100
    thresholds["1Z XC"]= 100
    thresholds["4M40 21 X2 XZ"]= 100
    thresholds["4D31 XC"]= 100

    return thresholds


    

def check_inventory_shortage(dataframe, thresholds):
    shortage_alarms = []
    for index, row in dataframe.iterrows():
        part_id = row['id']
        quantity = row['inventory']
        vehicle_type = row['vehicle_type']
        brand = row['brand']

        if part_id in thresholds and quantity < thresholds[part_id]:
            
            shortage_alarms.append({'id': part_id,'vehicle_type':vehicle_type ,'brand':brand,'inventory': int(quantity)})
    return shortage_alarms
# return a list of items that are below the inventory threshold



def execute_shortage_alarm():
    conn = db_connection()
    if conn is not None:
        group_data = fetch_grouped_data(conn)
        threshold = threshold_alarm(group_data)
        grouped_data_df = check_inventory_shortage(group_data, threshold)
        conn.close()
        return grouped_data_df
    else:
        print("Connection to database failed.")


def add_inventory(item_id, additional_quantity):
    conn = db_connection()
    if conn:
        cursor = conn.cursor()
        update_query = "UPDATE inventory SET inventory = inventory + ? WHERE id = ?;"
        try:
            cursor.execute(update_query, (additional_quantity, item_id))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating inventory for {item_id}: {e}")
        finally:
            conn.close()

    
def main():
    result = execute_shortage_alarm()
    if result is not None:
        print(result)
    else:
        print("No data to display.")
        
if __name__ == "__main__":
    main()