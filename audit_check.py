import pandas as pd
import numpy as np
import os

df = pd.read_csv('hypothetical_logistics_dataset.csv', parse_dates=['Order_Date'])
kpi = pd.read_csv('kpi_summary.csv')
corr = pd.read_csv('correlation_matrix.csv', index_col=0)
carrier = pd.read_csv('carrier_performance.csv')
region = pd.read_csv('region_performance.csv')
mode = pd.read_csv('shipping_mode_analysis.csv')
monthly = pd.read_csv('monthly_trends.csv')

print('=== AUDIT DATA ===')
print(f'Dataset: {df.shape[0]} rows x {df.shape[1]} cols')
on_time_rate = (df['Delivery_Status']=='On Time').mean()*100
print(f'On-Time Rate: {on_time_rate:.2f}%')
print(f'Avg Delivery Time: {df["Delivery_Time_Hours"].mean():.2f} h')
print(f'Avg Cost: ${df["Transportation_Cost_USD"].mean():.2f}')
print(f'Avg Rating: {df["Customer_Rating"].mean():.2f}')
print(f'Corr Dist-Cost: {corr.loc["Distance_km","Transportation_Cost_USD"]:.3f}')
print(f'Corr Delay-Rating: {corr.loc["Delay_Hours","Customer_Rating"]:.3f}')
slowest_region = region.sort_values('Avg_Delivery_Time',ascending=False).iloc[0]['Destination_Region']
print(f'Slowest region: {slowest_region}')
wh_slowest = df.groupby('Origin_Warehouse')['Warehouse_Processing_Hours'].mean().idxmax()
print(f'Highest WH processing: {wh_slowest}')
cheapest_carrier = carrier.sort_values('Avg_Cost_USD').iloc[0]['Carrier']
expensive_carrier = carrier.sort_values('Avg_Cost_USD',ascending=False).iloc[0]['Carrier']
print(f'Cheapest carrier: {cheapest_carrier}')
print(f'Most expensive carrier: {expensive_carrier}')
print()
print('MODE ANALYSIS:')
print(mode[['Shipping_Mode','Avg_Delivery_Time','Avg_Cost_USD','OnTime_Rate_Pct']].to_string(index=False))
print()
print('REGION ANALYSIS:')
print(region[['Destination_Region','Avg_Delivery_Time','Avg_Cost_USD','OnTime_Rate_Pct']].sort_values('Avg_Delivery_Time', ascending=False).to_string(index=False))
print()
print('PNG FILES:')
pngs = [f for f in os.listdir('.') if f.endswith('.png')]
print(f'  Count: {len(pngs)}')
for p in sorted(pngs):
    print(f'  {p}')
print()
print('CSV FILES:')
csvs = [f for f in os.listdir('.') if f.endswith('.csv')]
print(f'  Count: {len(csvs)}')
for c in sorted(csvs):
    print(f'  {c}')
print()
docx_exists = os.path.exists('Week_3_Advanced_Data_Analysis_and_Visualization_in_Logistics.docx')
print(f'DOCX exists: {docx_exists}')
print(f'DOCX size: {os.path.getsize("Week_3_Advanced_Data_Analysis_and_Visualization_in_Logistics.docx")/1024:.1f} KB')
