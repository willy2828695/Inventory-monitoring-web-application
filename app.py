import streamlit as st
from streamlit_extras.chart_annotations import get_annotations_chart
import pandas as pd
import matplotlib.pyplot as plt
from Connect_database import db_connection
from Shortage_alarm import fetch_grouped_data, check_inventory_shortage, execute_shortage_alarm, add_inventory
from Customer_proportion import fetch_best_saler, exacute_fetch_client_proportion, plot_client_proportions
from Best_sale_by_year import exacute_best_sale_by_year
from product_trend import exacute_fetch_product_trend, plot_product_trend
import sqlite3

# source inventory/bin/activate
# streamlit run app.py
# python Shortage_alarm.py


if 'page' not in st.session_state:
    st.session_state['page'] = 'home'


# Sidebar content
with st.sidebar:
    st.write("### Directary")
    # home page button
    if st.button('Home'):
        st.session_state['page'] = 'home'
    # Inventory Alarm
    if st.button('Inventory Alarm'):
        st.session_state['page'] = 'inventory_alarm'
    
    if st.button('Sales forecast'):
        st.session_state['page'] = 'Sales_forecast'

    if st.button('Client analysis'):
        st.session_state['page'] = 'Client_analysis'

    if st.button('Revenue analysis'):
        st.session_state['page'] = 'Rvenue_analysis'


if st.session_state['page'] == 'home':
    st.write("This is the home page. Use the sidebar to navigate to different sections of the app.")


# Inventory Alarm page
elif st.session_state['page'] == 'inventory_alarm':

    st.title("Inventory Monitoring and Update System")

    # Execute the alarm function to get current shortages
    shortage_data = execute_shortage_alarm()

    if shortage_data:
        st.subheader("Current Inventory Shortages")

        

        header_cols = st.columns(6)
        header_titles = ['Product ID', 'Vehicle Type', 'Brand', 'Inventory', 'Add Inventory','Update']
        for col, title in zip(header_cols, header_titles):
            col.write(title)


        for index, item in enumerate(shortage_data):
            col1, col2, col3,col4,col5,col6 = st.columns(6)
            unique_key = f"{item['id']}_{index}"


            with col1:
                st.write(item['id'])
            with col2:
                st.write(item['vehicle_type'])
            with col3:
                st.write(item['brand'])

            with col4:
                st.write(item['inventory'])

            with col5:
                add_qty = st.number_input("", min_value=0, step=10, key=f"add_qty_{unique_key}",label_visibility="collapsed")
            
            


            with col6:
                if st.button(f"Update", key=f"update_{unique_key}"):
                    add_inventory(item['id'], add_qty)

                    
                
                    st.session_state['refresh_data'] = True
                    
                    st.experimental_rerun()  # Rerun the script to refresh data

    else:
        st.write("No inventory shortages detected.")

elif st.session_state['page'] == 'Client_analysis':
    st.write("Woring on it")


elif st.session_state['page'] == 'Sales_forecast':
    st.title("Product Sales Analysis")
    st.write("Select a Product ID to view the client sales proportions:")
    
    # create a select boe in sidebar that allows user to select the year
    
    selected_year = st.selectbox('Select Year for Forecast', list(range(2017,2025)), index=7)  # Default to 2024

    best_sellers_df = exacute_best_sale_by_year(selected_year)

    if best_sellers_df is not None and not best_sellers_df.empty:
        product_ids = best_sellers_df['id'].tolist()
        # store the id user selected
        selected_id = st.selectbox('Product ID', product_ids)
        if st.button('Show Client Sales Proportions'):
            client_data_df = exacute_fetch_client_proportion(selected_id)
            if client_data_df is not None and not client_data_df.empty:
                col1, col2 = st.columns(2)
                with col1:
                    plot_client_proportions(client_data_df)
                with col2:
                    st.dataframe(client_data_df,hide_index=True)

                top_three_clients = client_data_df.head(3)    
                product_trend_data = exacute_fetch_product_trend(selected_year,top_three_clients, selected_id)
                if product_trend_data is not None and not product_trend_data.empty:
                    plot_product_trend(product_trend_data)
                else:
                    st.write("Product trend figure failed: No sales data available for the selected product ID.")
            else:
                st.write("No sales data available for the selected product ID.")
            
        
    else:
        st.write("No best seller data available.")
        



elif st.session_state['page'] == 'Rvenue_analysis':
    st.write("Woring on it")




