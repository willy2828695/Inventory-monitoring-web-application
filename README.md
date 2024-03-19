# Inventory-monitoring-web-application

This was my first full-stack project completed during my software engineering internship. 

On the back-end side, I used Python and SQLite API to extract sales data and inventory records from the company's ERM system. Then, I built a well-structured database to store them, which could be manipulated by the inventory monitoring function I wrote in Python.

On the front-end side, I utilized the Streamlit framework to design my web application and to demonstrate back-end functions in terms of inventory alarms, sales analysis, and acquisition forecasting.

## Fuction features:
1. Inventory Alarm: 
   This function page displays products that are below the inventory threshold and provides a means for employees to increase quantities even when acquisitions are halted.
<img width="1436" alt="截圖 2024-03-19 下午5 28 54" src="https://github.com/willy2828695/Inventory-monitoring-web-application/assets/157180894/4b6121e1-dcb0-4536-8b82-592a20b38dd0">

2. Selecting function:
 I created two selection boxes: one for choosing a year and another for selecting from the top 20 products. These allow employees to specify different year and product pairs based on the analysis requirements.

<img width="1436" alt="截圖 2024-03-19 下午5 29 04" src="https://github.com/willy2828695/Inventory-monitoring-web-application/assets/157180894/5bdcccdf-92a9-4aa8-a394-01e8063599df">

3. Sales Analysis:
When specific year and product pairs are chosen, the system displays a pie chart and a line chart illustrating each client's proportion of purchases for a certain product. This visualization aids in revealing buying patterns, thereby facilitating the forecasting of future acquisitions.
<img width="1436" alt="截圖 2024-03-19 下午5 29 40" src="https://github.com/willy2828695/Inventory-monitoring-web-application/assets/157180894/5274dc8d-309b-42ed-b32b-1fef513fbcfa">
