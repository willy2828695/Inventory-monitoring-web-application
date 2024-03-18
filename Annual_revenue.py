import pandas as pd
import matplotlib.pyplot as plt
from Connect_database import db_connection
import sqlite3

def annual_revenue_by_year(conn,year):
    query = "SELECT client,profit_amount FROM sales_record WHERE date LIKE'{}%'"
    cursor = conn.cursor()
    try:
        cursor.execute(query.format(year))
        grouped_data = cursor.fetchall()
        #print("Data fetched successfully!")
        
        grouped_data_df = pd.DataFrame(grouped_data, columns=['Client','Profit'])
        return grouped_data_df
        
    except sqlite3.Error as e:
        return f"Error fetching data: {e}"


def collect_annual_revenue():
    # create revenue chart by year
    annual_revenue_data=[]
    year = 2017
    # connect to database
    conn = db_connection()

    while year <=2024:
        revenue_data = annual_revenue_by_year(conn,year)
        annual_profit_from_ZYL = sum(revenue_data['Profit'])
        annual_revenue_data.append({"Year":int(year), "Revenue":annual_profit_from_ZYL})
        year+=1
    annual_revenue_data_df = pd.DataFrame(annual_revenue_data)
    conn.close()
    return annual_revenue_data_df



def plotting_total_revenue(darafram):
    x = pd.to_datetime(darafram['Year'], format='%Y').dt.year.to_numpy()

    # Convert 'Revenue' to float and then to a numpy array
    y = darafram['Revenue'].astype(float).to_numpy()



    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, marker='.', linestyle='-', color='blue', label='Annual Revenue')

    for i, txt in enumerate(y):
        plt.text(x[i], y[i], f"{txt:,.2f}", fontsize=8)
        
    plt.title("Annual revenue Over Time")
    plt.xlabel('Year')
    plt.ylabel('Revenue ($)')
    plt.grid(True)
    plt.legend()
    plt.show()

def exacute_annual_revenue():

    list_of_revenue = collect_annual_revenue()
    return plotting_total_revenue(list_of_revenue)
    


def main():
    result = exacute_annual_revenue()
    if result is not None:
        print(result)
    else:
        print("No data to display.")

if __name__ == "__main__":
    main()