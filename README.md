# 📦 Logistics Data Analysis — Week 3

## Advanced Data Analysis and Visualization in Logistics
**Week 3 Internship Task | Python Analytics Project**

> ⚠️ **DISCLAIMER**: The dataset used in this project is **entirely hypothetical and simulated** for internship exercise purposes only. It does not represent any real company, real shipments, or real logistics operations. All numerical results are computed programmatically from the generated data.

---

## 🎯 Project Overview

This project demonstrates advanced exploratory data analysis (EDA), KPI calculation, and professional data visualization applied to a realistic hypothetical logistics scenario. The analysis focuses on a simulated organization managing shipments between 5 origin warehouses and 8 destination regions using 5 carriers and 5 shipping modes.

---

## 📋 Objective

Deepen analytical skills through:
- Building a realistic synthetic logistics dataset
- Performing thorough Exploratory Data Analysis (EDA)
- Calculating logistics KPIs programmatically
- Producing 16 professional visualizations
- Interpreting findings and formulating recommendations
- Generating a professional DOCX report

---

## 🏭 Logistics Scenario

| Element            | Details                                                    |
|--------------------|------------------------------------------------------------|
| Analysis Period    | January 2025 – December 2025 (simulated)                  |
| Origin Warehouses  | WH-North, WH-South, WH-East, WH-West, WH-Central          |
| Destination Regions| North, South, East, West, Central, Northeast, Northwest, Southeast |
| Carriers           | FastFreight Co., QuickShip Logistics, National Cargo Ltd., SwiftMove Inc., GlobalTrans Corp. |
| Shipping Modes     | Road, Air, Rail, Sea, Express                              |
| Records            | 3,500 simulated shipment records                           |
| Random Seed        | 42 (fully reproducible)                                    |

---

## 📊 Dataset Description

The dataset (`hypothetical_logistics_dataset.csv`) contains **3,500 rows × 25 columns**.

### Key Variables

| Variable                  | Type        | Description                                      |
|---------------------------|-------------|--------------------------------------------------|
| Shipment_ID               | String      | Unique identifier per shipment                   |
| Order_Date / Ship_Date / Delivery_Date | Date | Shipment lifecycle timestamps          |
| Origin_Warehouse          | Categorical | Source facility (5 warehouses)                   |
| Destination_Region / City | Categorical | Delivery location                                |
| Carrier                   | Categorical | Logistics carrier (5 options)                    |
| Shipping_Mode             | Categorical | Transport mode: Road/Air/Rail/Sea/Express         |
| Weight_kg                 | Numeric     | Shipment weight (log-normal distribution)         |
| Distance_km               | Numeric     | Route distance in kilometres                      |
| Transportation_Cost_USD   | Numeric     | Total transport cost (USD)                        |
| Delivery_Time_Hours       | Numeric     | Actual delivery duration (hours)                 |
| Promised_Delivery_Hours   | Numeric     | SLA delivery window (hours)                      |
| Delivery_Status           | Categorical | On Time / Slightly Delayed / Delayed / Severely Delayed |
| Delay_Hours               | Numeric     | Hours beyond promised time (0 = on time)         |
| Customer_Rating           | Numeric     | Satisfaction score 1.0–5.0                       |
| Fuel_Cost_USD             | Numeric     | Fuel cost component (USD)                        |
| Handling_Cost_USD         | Numeric     | Warehouse handling cost (USD)                    |
| Warehouse_Processing_Hours| Numeric     | Time in warehouse before dispatch                 |
| Traffic_Level             | Categorical | Low / Moderate / High / Severe                   |
| Weather_Condition         | Categorical | Clear / Cloudy / Rain / Fog / Storm              |
| Is_Express                | Binary      | Express shipment flag (0/1)                      |
| Is_Fragile                | Binary      | Fragile cargo flag (0/1)                         |

---

## 🔄 Analytical Workflow

```
1. generate_logistics_dataset.py  →  hypothetical_logistics_dataset.csv
2. week3_logistics_analysis.py    →  Charts (PNG) + Summary CSVs
3. generate_docx_report.py        →  Week_3_...docx (professional report)
```

---

## 📈 Key Performance Indicators (KPIs)

All KPIs are calculated programmatically — no hardcoded values.

| KPI                          | Formula                                              |
|------------------------------|------------------------------------------------------|
| On-Time Delivery Rate        | On-Time Shipments / Total Shipments × 100            |
| Average Delivery Time        | Mean(Delivery_Time_Hours)                            |
| Average Delay Hours          | Mean(Delay_Hours) — all shipments                   |
| Average Transportation Cost  | Mean(Transportation_Cost_USD)                        |
| Cost per Kilometer           | Mean(Transportation_Cost_USD / Distance_km)          |
| Average Customer Rating      | Mean(Customer_Rating)                                |
| Avg Warehouse Processing     | Mean(Warehouse_Processing_Hours)                     |

---

## 📉 Visualizations (16 total)

| # | File                              | Chart Type         | Insight Area              |
|---|-----------------------------------|--------------------|---------------------------|
| 1 | shipment_volume_trend.png         | Line + Bar         | Demand trends             |
| 2 | delivery_time_distribution.png    | Histogram + KDE    | Delivery performance      |
| 3 | transportation_cost_distribution.png | Histogram       | Cost variability          |
| 4 | delivery_time_by_shipping_mode.png| Boxplot            | Mode performance          |
| 5 | cost_by_shipping_mode.png         | Boxplot            | Mode costs                |
| 6 | delivery_time_by_region.png       | Horizontal Bar     | Regional bottlenecks      |
| 7 | cost_by_carrier.png               | Bar Chart          | Carrier cost comparison   |
| 8 | distance_vs_cost.png              | Scatter + Regression | Cost drivers             |
| 9 | distance_vs_delivery_time.png     | Scatter (coloured) | Distance-time relationship|
| 10| correlation_heatmap.png           | Heatmap            | Variable relationships    |
| 11| delay_by_traffic.png              | Bar Chart          | Traffic impact            |
| 12| delay_by_weather.png              | Bar Chart          | Weather impact            |
| 13| customer_rating_vs_delay.png      | Scatter + Regression | Customer satisfaction    |
| 14| monthly_cost_trend.png            | Dual-axis Line+Bar | Cost & volume trends      |
| 15| warehouse_processing_time.png     | Violin Plot        | Warehouse bottlenecks     |
| 16| logistics_kpi_dashboard.png       | Dashboard          | Executive summary         |

---

## 🔍 Key Findings

- **On-Time Delivery**: 36.63% of shipments delivered within the promised time window
- **Cost Driver #1 (r = +0.738)**: Fuel Cost has the strongest positive correlation with Transportation Cost. Because Fuel Cost is a component of Transportation Cost in the simulated dataset, the strong relationship is expected and does not imply independent causation.
- **Cost Driver #2 (r = +0.605)**: Weight is the next strongest correlate with Transportation Cost
- **Cost Driver #3 (r = +0.257)**: Distance shows a weaker positive correlation with Transportation Cost
- **Bottleneck**: WH-Central has the highest warehouse processing time
- **Fastest Mode**: Air (23.29 h avg delivery time, highest avg cost)
- **Cheapest Mode**: Sea ($156.67 avg cost, longest delivery time)
- **Delay Drivers**: Severe traffic and Storm weather produce highest delay rates
- **Customer Impact**: Delay hours strongly negatively correlate with customer ratings (r = −0.960)
- **Seasonal Peak**: Q4 (October–December) shows highest shipment volume

---

## 🛠️ Technologies

| Library        | Purpose                                    |
|----------------|--------------------------------------------|
| Python 3.8+    | Core programming language                  |
| pandas         | Data manipulation and aggregation          |
| numpy          | Numerical computation, random generation   |
| matplotlib     | Core visualization engine                  |
| seaborn        | Statistical visualizations                 |
| scipy          | Pearson correlation, regression            |
| python-docx    | DOCX report generation                     |
| openpyxl       | Excel compatibility (optional)             |

---

## 📁 Project Structure

```
Logistics-Data-Analysis-3/
│
├── generate_logistics_dataset.py         # Step 1: Generate dataset
├── week3_logistics_analysis.py           # Step 2: EDA + visualizations
├── generate_docx_report.py               # Step 3: Professional report
├── requirements.txt                      # Python dependencies
├── README.md                             # This file
├── .gitignore                            # Git exclusions
│
├── hypothetical_logistics_dataset.csv    # Generated dataset (3,500 records)
├── kpi_summary.csv                       # KPI results table
├── carrier_performance.csv               # Per-carrier metrics
├── region_performance.csv                # Per-region metrics
├── shipping_mode_analysis.csv            # Per-mode metrics
├── monthly_trends.csv                    # Monthly aggregates
├── correlation_matrix.csv                # Full correlation matrix
│
├── shipment_volume_trend.png
├── delivery_time_distribution.png
├── transportation_cost_distribution.png
├── delivery_time_by_shipping_mode.png
├── cost_by_shipping_mode.png
├── delivery_time_by_region.png
├── cost_by_carrier.png
├── distance_vs_cost.png
├── distance_vs_delivery_time.png
├── correlation_heatmap.png
├── delay_by_traffic.png
├── delay_by_weather.png
├── customer_rating_vs_delay.png
├── monthly_cost_trend.png
├── warehouse_processing_time.png
├── logistics_kpi_dashboard.png
│
└── Week_3_Advanced_Data_Analysis_and_Visualization_in_Logistics.docx
```

---

## ⚙️ Installation

```bash
# Clone or download the project folder
cd Logistics-Data-Analysis-3

# Install dependencies
pip install -r requirements.txt
```

---

## ▶️ How to Run

Run the three scripts in order:

```bash
# Step 1: Generate the hypothetical dataset
python generate_logistics_dataset.py

# Step 2: Run full EDA, KPI calculations, and generate all visualizations
python week3_logistics_analysis.py

# Step 3: Generate the professional DOCX report
python generate_docx_report.py
```

All outputs are saved to the same project directory.
**Fixed random seed = 42** ensures identical results on every run.

---

## 📤 Output Files

| File                          | Description                              |
|-------------------------------|------------------------------------------|
| hypothetical_logistics_dataset.csv | Primary dataset (3,500 records)    |
| kpi_summary.csv               | Calculated logistics KPIs                |
| carrier_performance.csv       | Per-carrier performance metrics          |
| region_performance.csv        | Per-region delivery & cost metrics       |
| shipping_mode_analysis.csv    | Per-shipping-mode analysis               |
| monthly_trends.csv            | Monthly aggregated trends                |
| correlation_matrix.csv        | Full Pearson correlation matrix          |
| *.png (16 files)              | Professional visualization charts        |
| Week_3_...docx                | Complete internship submission report    |

---

## ⚠️ Limitations

- Dataset is **entirely hypothetical** — does not represent any real company
- Statistical relationships reflect generation parameters, not real operations
- Correlation observed ≠ causation
- Real-world deployment requires actual operational data and expert validation
- Simplified cost/time models are used for analytical demonstration only

---

## 📝 License

This project is created for internship educational purposes. The hypothetical dataset is freely reproducible under the fixed random seed provided.
