"""
week3_logistics_analysis.py
-------------------------------
Week 3 Internship Task: Advanced Data Analysis and Visualization in Logistics

Performs thorough Exploratory Data Analysis (EDA) on the hypothetical logistics dataset,
calculates logistics KPIs, generates professional visualizations, and saves summary CSVs.

DISCLAIMER: Dataset is hypothetical and simulated for educational/internship purposes only.

Author: Internship Analytics Project
Date: September 2026
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")   # Non-interactive backend for saving files
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from scipy import stats
import warnings
import os

warnings.filterwarnings("ignore")

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# GLOBAL STYLE CONFIGURATION
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
PALETTE_MAIN   = "viridis"
PALETTE_CAT    = "Set2"
BG_COLOR       = "#F8F9FA"
ACCENT         = "#2E4057"
HIGHLIGHT      = "#E63946"
GRID_COLOR     = "#DDDDDD"
FIG_DPI        = 150

plt.rcParams.update({
    "figure.facecolor":    BG_COLOR,
    "axes.facecolor":      "white",
    "axes.edgecolor":      "#CCCCCC",
    "axes.labelcolor":     ACCENT,
    "axes.titlepad":       12,
    "axes.titlesize":      13,
    "axes.titleweight":    "bold",
    "axes.labelsize":      11,
    "xtick.color":         "#555555",
    "ytick.color":         "#555555",
    "xtick.labelsize":     9,
    "ytick.labelsize":     9,
    "grid.color":          GRID_COLOR,
    "grid.linestyle":      "--",
    "grid.alpha":          0.7,
    "legend.fontsize":     9,
    "figure.titlesize":    15,
    "figure.titleweight":  "bold",
    "font.family":         "DejaVu Sans",
})

sns.set_style("whitegrid")


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# SECTION 1: LOAD DATA
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def load_data(path="hypothetical_logistics_dataset.csv"):
    """Load dataset and parse date columns."""
    df = pd.read_csv(path)
    date_cols = ["Order_Date", "Ship_Date", "Delivery_Date"]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col])
    df["Order_Month"]  = df["Order_Date"].dt.to_period("M")
    df["Order_Week"]   = df["Order_Date"].dt.isocalendar().week.astype(int)
    df["Order_DayOfWeek"] = df["Order_Date"].dt.day_name()
    print(f"  âœ“ Dataset loaded: {df.shape[0]} rows Ã— {df.shape[1]} columns")
    return df


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# SECTION 2: DATASET OVERVIEW
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def dataset_overview(df):
    """Print a structured overview of the dataset."""
    print("\n" + "=" * 60)
    print("  SECTION A â€” DATASET OVERVIEW")
    print("=" * 60)
    print(f"\n  Rows     : {df.shape[0]}")
    print(f"  Columns  : {df.shape[1]}")

    numeric_cols  = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols      = df.select_dtypes(include=["object"]).columns.tolist()
    date_cols     = df.select_dtypes(include=["datetime64"]).columns.tolist()

    print(f"\n  Numeric variables  ({len(numeric_cols)}): {numeric_cols}")
    print(f"\n  Categorical variables ({len(cat_cols)}): {cat_cols}")
    print(f"\n  Date variables    ({len(date_cols)}): {date_cols}")

    print("\n  MISSING VALUES:")
    missing = df.isnull().sum()
    if missing.sum() == 0:
        print("    None â€” dataset is complete.")
    else:
        print(missing[missing > 0])

    return numeric_cols, cat_cols, date_cols


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# SECTION 3: DESCRIPTIVE STATISTICS
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

KEY_NUMERIC = [
    "Delivery_Time_Hours", "Promised_Delivery_Hours", "Delay_Hours",
    "Weight_kg", "Distance_km", "Transportation_Cost_USD",
    "Fuel_Cost_USD", "Handling_Cost_USD",
    "Warehouse_Processing_Hours", "Shipment_Volume", "Customer_Rating",
]


def descriptive_statistics(df):
    """Calculate and print comprehensive descriptive statistics."""
    print("\n" + "=" * 60)
    print("  SECTION B â€” DESCRIPTIVE STATISTICS")
    print("=" * 60)

    stats_rows = []
    for col in KEY_NUMERIC:
        s = df[col]
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        row = {
            "Variable":  col,
            "Mean":      round(s.mean(), 3),
            "Median":    round(s.median(), 3),
            "Std_Dev":   round(s.std(), 3),
            "Min":       round(s.min(), 3),
            "Q1":        round(q1, 3),
            "Q3":        round(q3, 3),
            "Max":       round(s.max(), 3),
            "IQR":       round(q3 - q1, 3),
            "Skewness":  round(s.skew(), 3),
        }
        stats_rows.append(row)

    stats_df = pd.DataFrame(stats_rows)
    print("\n" + stats_df.to_string(index=False))
    return stats_df


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# SECTION 4: CATEGORICAL ANALYSIS
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def categorical_analysis(df):
    """Calculate counts and proportions for categorical variables."""
    print("\n" + "=" * 60)
    print("  SECTION C â€” CATEGORICAL ANALYSIS")
    print("=" * 60)

    cat_targets = [
        "Carrier", "Shipping_Mode", "Destination_Region",
        "Delivery_Status", "Traffic_Level", "Weather_Condition",
        "Origin_Warehouse",
    ]

    for col in cat_targets:
        counts = df[col].value_counts()
        pct    = (counts / len(df) * 100).round(2)
        result = pd.DataFrame({"Count": counts, "Percentage(%)": pct})
        print(f"\n  {col}:\n{result.to_string()}")


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# SECTION 5: KPI CALCULATIONS
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def calculate_kpis(df):
    """Calculate and print key logistics KPIs."""
    print("\n" + "=" * 60)
    print("  SECTION D â€” LOGISTICS KPI ANALYSIS")
    print("=" * 60)

    total_shipments     = len(df)
    on_time_count       = (df["Delivery_Status"] == "On Time").sum()
    on_time_rate        = on_time_count / total_shipments * 100
    avg_delivery_time   = df["Delivery_Time_Hours"].mean()
    avg_delay           = df["Delay_Hours"].mean()
    avg_transport_cost  = df["Transportation_Cost_USD"].mean()
    cost_per_km         = (df["Transportation_Cost_USD"] / df["Distance_km"]).mean()
    avg_customer_rating = df["Customer_Rating"].mean()
    total_volume        = df["Shipment_Volume"].sum()
    avg_wh_processing   = df["Warehouse_Processing_Hours"].mean()
    avg_weight          = df["Weight_kg"].mean()
    total_fuel_cost     = df["Fuel_Cost_USD"].sum()

    kpis = {
        "Total Shipments":              total_shipments,
        "On-Time Delivery Rate (%)":    round(on_time_rate, 2),
        "Avg Delivery Time (Hours)":    round(avg_delivery_time, 2),
        "Avg Delay Hours":              round(avg_delay, 2),
        "Avg Transportation Cost (USD)":round(avg_transport_cost, 2),
        "Cost per Kilometer (USD/km)":  round(cost_per_km, 4),
        "Cost per Shipment (USD)":      round(avg_transport_cost, 2),
        "Avg Customer Rating (1-5)":    round(avg_customer_rating, 2),
        "Total Shipment Volume (mÂ³)":   round(total_volume, 2),
        "Avg Warehouse Processing (h)": round(avg_wh_processing, 2),
        "Avg Weight (kg)":              round(avg_weight, 2),
        "Total Fuel Cost (USD)":        round(total_fuel_cost, 2),
    }

    print("\n  FORMULA DEFINITIONS:")
    print("    On-Time Delivery Rate = (On-Time Shipments / Total Shipments) Ã— 100")
    print("    Cost per Kilometer    = Avg(Transportation_Cost_USD / Distance_km)")
    print("    Avg Delay Hours       = Mean(Delay_Hours) for all shipments (0 if on time)")

    print("\n  CALCULATED KPIs:")
    for k, v in kpis.items():
        print(f"    {k:<40} : {v:>12,.4f}")

    kpi_df = pd.DataFrame(list(kpis.items()), columns=["KPI", "Value"])
    kpi_df.to_csv("kpi_summary.csv", index=False)
    print("\n  âœ“ kpi_summary.csv saved.")
    return kpis


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# SECTION 6: CORRELATION ANALYSIS
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def correlation_analysis(df):
    """Compute and save Pearson correlation matrix for key numeric variables."""
    print("\n" + "=" * 60)
    print("  SECTION E â€” CORRELATION ANALYSIS (Pearson)")
    print("=" * 60)

    corr_cols = [
        "Distance_km", "Weight_kg", "Delivery_Time_Hours",
        "Transportation_Cost_USD", "Fuel_Cost_USD", "Handling_Cost_USD",
        "Warehouse_Processing_Hours", "Delay_Hours",
        "Customer_Rating", "Shipment_Volume",
    ]
    corr_matrix = df[corr_cols].corr()
    corr_matrix.to_csv("correlation_matrix.csv")

    print("\n  Key correlations with Transportation_Cost_USD:")
    cost_corr = corr_matrix["Transportation_Cost_USD"].drop("Transportation_Cost_USD")
    for var, r in cost_corr.sort_values(key=abs, ascending=False).items():
        strength = "Strong" if abs(r) > 0.6 else ("Moderate" if abs(r) > 0.3 else "Weak")
        print(f"    {var:<35} r = {r:+.3f}  ({strength})")

    print("\n  Key correlations with Delivery_Time_Hours:")
    time_corr = corr_matrix["Delivery_Time_Hours"].drop("Delivery_Time_Hours")
    for var, r in time_corr.sort_values(key=abs, ascending=False).items():
        strength = "Strong" if abs(r) > 0.6 else ("Moderate" if abs(r) > 0.3 else "Weak")
        print(f"    {var:<35} r = {r:+.3f}  ({strength})")

    print("\n  NOTE: Correlation does not imply causation.")
    print("  âœ“ correlation_matrix.csv saved.")
    return corr_matrix


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# SECTION 7: SUMMARY CSV OUTPUTS
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def generate_summary_csvs(df):
    """Generate and save carrier, region, shipping-mode, and monthly summary CSVs."""

    # Carrier performance
    carrier_perf = df.groupby("Carrier").agg(
        Total_Shipments      = ("Shipment_ID", "count"),
        Avg_Delivery_Time    = ("Delivery_Time_Hours", "mean"),
        Avg_Delay_Hours      = ("Delay_Hours", "mean"),
        Avg_Cost_USD         = ("Transportation_Cost_USD", "mean"),
        Avg_Customer_Rating  = ("Customer_Rating", "mean"),
        OnTime_Rate_Pct      = ("Delivery_Status",
                                lambda x: (x == "On Time").mean() * 100),
    ).round(2).reset_index()
    carrier_perf.to_csv("carrier_performance.csv", index=False)

    # Region performance
    region_perf = df.groupby("Destination_Region").agg(
        Total_Shipments      = ("Shipment_ID", "count"),
        Avg_Delivery_Time    = ("Delivery_Time_Hours", "mean"),
        Avg_Delay_Hours      = ("Delay_Hours", "mean"),
        Avg_Cost_USD         = ("Transportation_Cost_USD", "mean"),
        Avg_Distance_km      = ("Distance_km", "mean"),
        OnTime_Rate_Pct      = ("Delivery_Status",
                                lambda x: (x == "On Time").mean() * 100),
    ).round(2).reset_index()
    region_perf.to_csv("region_performance.csv", index=False)

    # Shipping mode analysis
    mode_analysis = df.groupby("Shipping_Mode").agg(
        Total_Shipments      = ("Shipment_ID", "count"),
        Avg_Delivery_Time    = ("Delivery_Time_Hours", "mean"),
        Median_Delivery_Time = ("Delivery_Time_Hours", "median"),
        Avg_Cost_USD         = ("Transportation_Cost_USD", "mean"),
        Avg_Distance_km      = ("Distance_km", "mean"),
        OnTime_Rate_Pct      = ("Delivery_Status",
                                lambda x: (x == "On Time").mean() * 100),
        Avg_Customer_Rating  = ("Customer_Rating", "mean"),
    ).round(2).reset_index()
    mode_analysis.to_csv("shipping_mode_analysis.csv", index=False)

    # Monthly trends
    df["Month_Str"] = df["Order_Date"].dt.strftime("%Y-%m")
    monthly = df.groupby("Month_Str").agg(
        Total_Shipments      = ("Shipment_ID", "count"),
        Avg_Delivery_Time    = ("Delivery_Time_Hours", "mean"),
        Avg_Cost_USD         = ("Transportation_Cost_USD", "mean"),
        Avg_Delay_Hours      = ("Delay_Hours", "mean"),
        Total_Volume_m3      = ("Shipment_Volume", "sum"),
        OnTime_Rate_Pct      = ("Delivery_Status",
                                lambda x: (x == "On Time").mean() * 100),
    ).round(2).reset_index()
    monthly.to_csv("monthly_trends.csv", index=False)

    print("\n  âœ“ carrier_performance.csv saved.")
    print("  âœ“ region_performance.csv saved.")
    print("  âœ“ shipping_mode_analysis.csv saved.")
    print("  âœ“ monthly_trends.csv saved.")

    return carrier_perf, region_perf, mode_analysis, monthly


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# SECTION 8: VISUALIZATIONS
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def savefig(name, fig=None):
    """Save current or specified figure with tight layout."""
    if fig:
        fig.tight_layout()
        fig.savefig(name, dpi=FIG_DPI, bbox_inches="tight", facecolor=BG_COLOR)
        plt.close(fig)
    else:
        plt.tight_layout()
        plt.savefig(name, dpi=FIG_DPI, bbox_inches="tight", facecolor=BG_COLOR)
        plt.close()
    print(f"  âœ“ Saved: {name}")


# --- Chart 1: Shipment Volume Over Time ---
def plot_shipment_volume_trend(df):
    """Line chart of daily/weekly shipment volume over time."""
    daily = df.groupby("Order_Date").size().reset_index(name="Shipments")
    # 7-day rolling average for smoothness
    daily["Rolling7"] = daily["Shipments"].rolling(7, min_periods=1).mean()

    fig, ax = plt.subplots(figsize=(13, 5))
    ax.bar(daily["Order_Date"], daily["Shipments"], color="#A8DADC", alpha=0.5,
           label="Daily Shipments")
    ax.plot(daily["Order_Date"], daily["Rolling7"], color=HIGHLIGHT, lw=2.2,
            label="7-Day Rolling Avg")
    ax.set_title("Shipment Volume Over Time (Daily + 7-Day Rolling Avg)\n"
                 "Hypothetical Dataset â€” 2025", fontsize=14)
    ax.set_xlabel("Order Date")
    ax.set_ylabel("Number of Shipments")
    ax.legend()
    ax.grid(True, alpha=0.5)
    fig.text(0.01, -0.03, "Chart 1 | Justification: Bar+line combo shows both daily granularity "
             "and smoothed trend, revealing seasonal demand peaks.", fontsize=8, color="#555555")
    savefig("shipment_volume_trend.png", fig)


# --- Chart 2: Delivery Time Distribution ---
def plot_delivery_time_distribution(df):
    """Histogram + KDE of delivery time hours."""
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(df["Delivery_Time_Hours"], bins=60, kde=True, ax=ax,
                 color="#457B9D", edgecolor="white", alpha=0.8)
    mean_v   = df["Delivery_Time_Hours"].mean()
    median_v = df["Delivery_Time_Hours"].median()
    ax.axvline(mean_v,   color=HIGHLIGHT,  ls="--", lw=1.8, label=f"Mean  = {mean_v:.1f} h")
    ax.axvline(median_v, color="#2A9D8F", ls=":",  lw=1.8, label=f"Median = {median_v:.1f} h")
    ax.set_title("Delivery Time Distribution (Hours)\nAll Shipments â€” Hypothetical Dataset", fontsize=14)
    ax.set_xlabel("Delivery Time (Hours)")
    ax.set_ylabel("Frequency")
    ax.legend()
    fig.text(0.01, -0.03, "Chart 2 | Justification: Histogram+KDE reveals central tendency, "
             "spread, and skewness of delivery durations.", fontsize=8, color="#555555")
    savefig("delivery_time_distribution.png", fig)


# --- Chart 3: Transportation Cost Distribution ---
def plot_cost_distribution(df):
    """Histogram of transportation cost."""
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(df["Transportation_Cost_USD"], bins=60, kde=True, ax=ax,
                 color="#E9C46A", edgecolor="white", alpha=0.8)
    mean_c = df["Transportation_Cost_USD"].mean()
    ax.axvline(mean_c, color=HIGHLIGHT, ls="--", lw=1.8, label=f"Mean = ${mean_c:,.0f}")
    ax.set_title("Transportation Cost Distribution (USD)\nAll Shipments â€” Hypothetical Dataset", fontsize=14)
    ax.set_xlabel("Transportation Cost (USD)")
    ax.set_ylabel("Frequency")
    ax.legend()
    fig.text(0.01, -0.03, "Chart 3 | Justification: Histogram shows cost variability "
             "and identifies whether costs are skewed by a few expensive shipments.", fontsize=8, color="#555555")
    savefig("transportation_cost_distribution.png", fig)


# --- Chart 4: Delivery Time by Shipping Mode ---
def plot_delivery_time_by_mode(df):
    """Boxplot of delivery time across shipping modes."""
    order = df.groupby("Shipping_Mode")["Delivery_Time_Hours"].median().sort_values().index
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=df, x="Shipping_Mode", y="Delivery_Time_Hours",
                order=order, palette=PALETTE_CAT, ax=ax,
                flierprops=dict(marker="o", markersize=3, alpha=0.5))
    ax.set_title("Delivery Time by Shipping Mode\nBoxplot â€” Median, IQR, and Outliers", fontsize=14)
    ax.set_xlabel("Shipping Mode")
    ax.set_ylabel("Delivery Time (Hours)")
    fig.text(0.01, -0.03, "Chart 4 | Justification: Boxplots show median, spread, and outliers "
             "per mode â€” more informative than averages alone.", fontsize=8, color="#555555")
    savefig("delivery_time_by_shipping_mode.png", fig)


# --- Chart 5: Transportation Cost by Shipping Mode ---
def plot_cost_by_mode(df):
    """Boxplot of transportation cost by shipping mode."""
    order = df.groupby("Shipping_Mode")["Transportation_Cost_USD"].median().sort_values().index
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=df, x="Shipping_Mode", y="Transportation_Cost_USD",
                order=order, palette="Set3", ax=ax,
                flierprops=dict(marker="o", markersize=3, alpha=0.5))
    ax.set_title("Transportation Cost by Shipping Mode (USD)\nBoxplot Comparison", fontsize=14)
    ax.set_xlabel("Shipping Mode")
    ax.set_ylabel("Transportation Cost (USD)")
    fig.text(0.01, -0.03, "Chart 5 | Justification: Comparing cost distributions across modes "
             "reveals which modes are cost-efficient vs. premium.", fontsize=8, color="#555555")
    savefig("cost_by_shipping_mode.png", fig)


# --- Chart 6: Average Delivery Time by Region ---
def plot_delivery_time_by_region(df):
    """Horizontal bar chart of average delivery time per destination region."""
    region_avg = df.groupby("Destination_Region")["Delivery_Time_Hours"].mean().sort_values()
    colors = [HIGHLIGHT if v == region_avg.max() else "#457B9D" for v in region_avg]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(region_avg.index, region_avg.values, color=colors, edgecolor="white", height=0.6)
    for bar, v in zip(bars, region_avg.values):
        ax.text(v + 0.5, bar.get_y() + bar.get_height() / 2,
                f"{v:.1f} h", va="center", ha="left", fontsize=9)
    ax.set_title("Average Delivery Time by Destination Region (Hours)\nHypothetical Dataset", fontsize=14)
    ax.set_xlabel("Avg Delivery Time (Hours)")
    ax.set_ylabel("Destination Region")
    fig.text(0.01, -0.03, "Chart 6 | Justification: Horizontal bar chart with data labels "
             "clearly ranks regions, highlighting bottleneck areas.", fontsize=8, color="#555555")
    savefig("delivery_time_by_region.png", fig)


# --- Chart 7: Average Transportation Cost by Carrier ---
def plot_cost_by_carrier(df):
    """Bar chart of average transportation cost per carrier."""
    carrier_avg = df.groupby("Carrier")["Transportation_Cost_USD"].mean().sort_values(ascending=False)
    colors = ["#E63946" if v == carrier_avg.max() else "#2A9D8F" for v in carrier_avg]

    fig, ax = plt.subplots(figsize=(11, 6))
    bars = ax.bar(carrier_avg.index, carrier_avg.values, color=colors, edgecolor="white", width=0.55)
    for bar, v in zip(bars, carrier_avg.values):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 20,
                f"${v:,.0f}", ha="center", va="bottom", fontsize=9)
    ax.set_title("Average Transportation Cost by Carrier (USD)\nHypothetical Dataset", fontsize=14)
    ax.set_xlabel("Carrier")
    ax.set_ylabel("Avg Transportation Cost (USD)")
    ax.tick_params(axis="x", rotation=15)
    fig.text(0.01, -0.03, "Chart 7 | Justification: Bar chart with data labels enables "
             "direct carrier cost comparison for procurement decisions.", fontsize=8, color="#555555")
    savefig("cost_by_carrier.png", fig)


# --- Chart 8: Distance vs. Transportation Cost ---
def plot_distance_vs_cost(df):
    """Scatter plot with regression line: Distance vs Transportation Cost."""
    sample = df.sample(min(1500, len(df)), random_state=42)
    slope, intercept, r_val, p_val, _ = stats.linregress(
        sample["Distance_km"], sample["Transportation_Cost_USD"]
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(sample["Distance_km"], sample["Transportation_Cost_USD"],
               alpha=0.25, s=20, color="#457B9D", label="Shipments")
    x_line = np.linspace(sample["Distance_km"].min(), sample["Distance_km"].max(), 200)
    ax.plot(x_line, slope * x_line + intercept, color=HIGHLIGHT, lw=2,
            label=f"Regression (r = {r_val:.3f})")
    ax.set_title("Distance vs. Transportation Cost\nScatter Plot with Regression Line", fontsize=14)
    ax.set_xlabel("Distance (km)")
    ax.set_ylabel("Transportation Cost (USD)")
    ax.legend()
    fig.text(0.01, -0.03, f"Chart 8 | Justification: Scatter + regression quantifies "
             f"distance-cost relationship (r={r_val:.3f}). "
             "Correlation â‰  causation.", fontsize=8, color="#555555")
    savefig("distance_vs_cost.png", fig)


# --- Chart 9: Distance vs. Delivery Time ---
def plot_distance_vs_delivery_time(df):
    """Scatter plot: Distance vs Delivery Time, coloured by Shipping Mode."""
    sample = df.sample(min(1500, len(df)), random_state=42)
    modes  = sample["Shipping_Mode"].unique()
    palette = dict(zip(modes, sns.color_palette(PALETTE_CAT, len(modes))))

    fig, ax = plt.subplots(figsize=(10, 6))
    for mode in modes:
        sub = sample[sample["Shipping_Mode"] == mode]
        ax.scatter(sub["Distance_km"], sub["Delivery_Time_Hours"],
                   alpha=0.3, s=18, label=mode, color=palette[mode])
    ax.set_title("Distance vs. Delivery Time â€” Coloured by Shipping Mode", fontsize=14)
    ax.set_xlabel("Distance (km)")
    ax.set_ylabel("Delivery Time (Hours)")
    ax.legend(title="Shipping Mode", markerscale=1.5)
    fig.text(0.01, -0.03, "Chart 9 | Justification: Colour-coded scatter shows how different "
             "modes produce different delivery durations for similar distances.", fontsize=8, color="#555555")
    savefig("distance_vs_delivery_time.png", fig)


# --- Chart 10: Correlation Heatmap ---
def plot_correlation_heatmap(df):
    """Heatmap of Pearson correlations among key numeric variables."""
    corr_cols = [
        "Distance_km", "Weight_kg", "Delivery_Time_Hours",
        "Transportation_Cost_USD", "Fuel_Cost_USD", "Handling_Cost_USD",
        "Warehouse_Processing_Hours", "Delay_Hours",
        "Customer_Rating", "Shipment_Volume",
    ]
    corr = df[corr_cols].corr()

    fig, ax = plt.subplots(figsize=(12, 9))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="coolwarm",
                center=0, vmin=-1, vmax=1, linewidths=0.5, ax=ax,
                annot_kws={"size": 8}, cbar_kws={"shrink": 0.8})
    ax.set_title("Pearson Correlation Heatmap â€” Key Numeric Variables\nHypothetical Dataset",
                 fontsize=14)
    plt.xticks(rotation=35, ha="right")
    fig.text(0.01, -0.02, "Chart 10 | Justification: Heatmap gives a comprehensive view of "
             "all pairwise correlations, highlighting multicollinearity and key drivers.", fontsize=8, color="#555555")
    savefig("correlation_heatmap.png", fig)


# --- Chart 11: Delay Rate by Traffic Level ---
def plot_delay_by_traffic(df):
    """Bar chart of delay rate (%) by traffic level."""
    df["Is_Delayed"] = (df["Delivery_Status"] != "On Time").astype(int)
    traffic_delay = df.groupby("Traffic_Level")["Is_Delayed"].mean().mul(100)
    order = ["Low", "Moderate", "High", "Severe"]
    traffic_delay = traffic_delay.reindex([o for o in order if o in traffic_delay.index])

    fig, ax = plt.subplots(figsize=(9, 5))
    colors = sns.color_palette("YlOrRd", len(traffic_delay))
    bars = ax.bar(traffic_delay.index, traffic_delay.values, color=colors, edgecolor="white")
    for bar, v in zip(bars, traffic_delay.values):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 0.5,
                f"{v:.1f}%", ha="center", va="bottom", fontsize=10)
    ax.set_title("Shipment Delay Rate by Traffic Level (%)\nHypothetical Dataset", fontsize=14)
    ax.set_xlabel("Traffic Level")
    ax.set_ylabel("Delay Rate (%)")
    ax.set_ylim(0, max(traffic_delay.values) * 1.25)
    fig.text(0.01, -0.03, "Chart 11 | Justification: Bar chart shows how traffic severity "
             "correlates with delay rate â€” useful for contingency planning.", fontsize=8, color="#555555")
    savefig("delay_by_traffic.png", fig)


# --- Chart 12: Delay Rate by Weather Condition ---
def plot_delay_by_weather(df):
    """Bar chart of delay rate (%) by weather condition."""
    if "Is_Delayed" not in df.columns:
        df["Is_Delayed"] = (df["Delivery_Status"] != "On Time").astype(int)
    weather_delay = df.groupby("Weather_Condition")["Is_Delayed"].mean().mul(100)
    order = ["Clear", "Cloudy", "Rain", "Fog", "Storm"]
    weather_delay = weather_delay.reindex([o for o in order if o in weather_delay.index])

    fig, ax = plt.subplots(figsize=(10, 5))
    colors = sns.color_palette("Blues", len(weather_delay))
    bars = ax.bar(weather_delay.index, weather_delay.values, color=colors, edgecolor="white")
    for bar, v in zip(bars, weather_delay.values):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 0.5,
                f"{v:.1f}%", ha="center", va="bottom", fontsize=10)
    ax.set_title("Shipment Delay Rate by Weather Condition (%)\nHypothetical Dataset", fontsize=14)
    ax.set_xlabel("Weather Condition")
    ax.set_ylabel("Delay Rate (%)")
    ax.set_ylim(0, max(weather_delay.values) * 1.25)
    fig.text(0.01, -0.03, "Chart 12 | Justification: Weather-based delay analysis identifies "
             "risk conditions that demand proactive routing or scheduling adjustments.", fontsize=8, color="#555555")
    savefig("delay_by_weather.png", fig)


# --- Chart 13: Customer Rating vs. Delay Hours ---
def plot_customer_rating_vs_delay(df):
    """Scatter + regression: Customer Rating vs Delay Hours."""
    delayed = df[df["Delay_Hours"] > 0].copy()
    sample  = delayed.sample(min(1200, len(delayed)), random_state=42)

    slope, intercept, r_val, p_val, _ = stats.linregress(
        sample["Delay_Hours"], sample["Customer_Rating"]
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    sc = ax.scatter(sample["Delay_Hours"], sample["Customer_Rating"],
                    alpha=0.25, s=20, c=sample["Customer_Rating"],
                    cmap="RdYlGn", vmin=1, vmax=5)
    x_line = np.linspace(0, sample["Delay_Hours"].max(), 200)
    ax.plot(x_line, slope * x_line + intercept, color=HIGHLIGHT, lw=2,
            label=f"Trend (r = {r_val:.3f})")
    plt.colorbar(sc, ax=ax, label="Customer Rating")
    ax.set_title("Customer Rating vs. Delay Hours\n(Delayed Shipments Only)", fontsize=14)
    ax.set_xlabel("Delay Hours")
    ax.set_ylabel("Customer Rating (1â€“5)")
    ax.legend()
    fig.text(0.01, -0.03, f"Chart 13 | Justification: Scatter + regression reveals how delivery "
             f"delays influence satisfaction scores (r={r_val:.3f}). Colour encoding enhances readability.",
             fontsize=8, color="#555555")
    savefig("customer_rating_vs_delay.png", fig)


# --- Chart 14: Monthly Cost Trend ---
def plot_monthly_cost_trend(df):
    """Line + bar chart of monthly average transportation cost."""
    df["Month_Str"] = df["Order_Date"].dt.strftime("%Y-%m")
    monthly = df.groupby("Month_Str").agg(
        Avg_Cost=("Transportation_Cost_USD", "mean"),
        Total_Shipments=("Shipment_ID", "count"),
    ).reset_index()

    fig, ax1 = plt.subplots(figsize=(13, 5))
    ax2 = ax1.twinx()

    ax1.bar(monthly["Month_Str"], monthly["Total_Shipments"],
            color="#A8DADC", alpha=0.5, label="Shipment Count")
    ax2.plot(monthly["Month_Str"], monthly["Avg_Cost"],
             color=HIGHLIGHT, marker="o", lw=2.2, label="Avg Cost (USD)")

    ax1.set_xlabel("Month")
    ax1.set_ylabel("Shipment Count", color="#457B9D")
    ax2.set_ylabel("Avg Transportation Cost (USD)", color=HIGHLIGHT)
    ax1.tick_params(axis="x", rotation=45)
    ax1.set_title("Monthly Transportation Cost Trend vs. Shipment Volume\nHypothetical Dataset 2025",
                  fontsize=14)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

    fig.text(0.01, -0.04, "Chart 14 | Justification: Dual-axis chart compares volume and cost "
             "simultaneously, revealing whether cost changes with demand.", fontsize=8, color="#555555")
    savefig("monthly_cost_trend.png", fig)


# --- Chart 15: Warehouse Processing Time by Warehouse ---
def plot_warehouse_processing(df):
    """Violin + boxplot: Warehouse processing time per warehouse."""
    order = df.groupby("Origin_Warehouse")["Warehouse_Processing_Hours"].median().sort_values().index
    fig, ax = plt.subplots(figsize=(11, 6))
    sns.violinplot(data=df, x="Origin_Warehouse", y="Warehouse_Processing_Hours",
                   order=order, palette="Pastel1", inner="quartile", ax=ax)
    ax.set_title("Warehouse Processing Time Distribution by Warehouse (Hours)\nHypothetical Dataset",
                 fontsize=14)
    ax.set_xlabel("Origin Warehouse")
    ax.set_ylabel("Processing Time (Hours)")
    fig.text(0.01, -0.03, "Chart 15 | Justification: Violin plots show full distribution "
             "of processing times per warehouse, revealing bottleneck facilities.", fontsize=8, color="#555555")
    savefig("warehouse_processing_time.png", fig)


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# SECTION 9: KPI DASHBOARD
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def plot_kpi_dashboard(df, kpis):
    """Create a professional KPI dashboard summarizing key metrics."""
    fig = plt.figure(figsize=(18, 13), facecolor="#1A1A2E")
    fig.suptitle("LOGISTICS OPERATIONS KPI DASHBOARD\nHypothetical Dataset â€” 2025 Full Year",
                 fontsize=18, fontweight="bold", color="white", y=0.98)

    gs = gridspec.GridSpec(4, 4, figure=fig, hspace=0.55, wspace=0.45)

    kpi_metrics = [
        ("Total\nShipments",          f"{kpis['Total Shipments']:,}",              "#06D6A0"),
        ("On-Time\nDelivery Rate",     f"{kpis['On-Time Delivery Rate (%)']:.1f}%", "#118AB2"),
        ("Avg Delivery\nTime",         f"{kpis['Avg Delivery Time (Hours)']:.1f} h","#FFD166"),
        ("Avg Delay",                  f"{kpis['Avg Delay Hours']:.1f} h",          "#EF476F"),
        ("Avg Transport\nCost",        f"${kpis['Avg Transportation Cost (USD)']:,.0f}", "#A8DADC"),
        ("Avg Customer\nRating",       f"{kpis['Avg Customer Rating (1-5)']:.2f}/5", "#95D5B2"),
    ]

    for idx, (label, value, color) in enumerate(kpi_metrics):
        row = idx // 4
        col = idx % 4
        ax_kpi = fig.add_subplot(gs[row, col])
        ax_kpi.set_facecolor("#16213E")
        ax_kpi.set_xlim(0, 1)
        ax_kpi.set_ylim(0, 1)
        ax_kpi.axis("off")
        ax_kpi.text(0.5, 0.70, value, ha="center", va="center",
                    fontsize=17, fontweight="bold", color=color, transform=ax_kpi.transAxes)
        ax_kpi.text(0.5, 0.25, label, ha="center", va="center",
                    fontsize=9, color="white", transform=ax_kpi.transAxes)
        for spine in ["top", "bottom", "left", "right"]:
            ax_kpi.spines[spine].set_visible(True)
            ax_kpi.spines[spine].set_color(color)
            ax_kpi.spines[spine].set_linewidth(2)

    # Supporting chart A: Delivery Status Donut
    ax_donut = fig.add_subplot(gs[2:4, 0:2])
    ax_donut.set_facecolor("#16213E")
    status_counts = df["Delivery_Status"].value_counts()
    colors_donut  = ["#06D6A0", "#FFD166", "#EF476F", "#9E0059"][:len(status_counts)]
    wedges, texts, autotexts = ax_donut.pie(
        status_counts.values, labels=status_counts.index,
        autopct="%1.1f%%", colors=colors_donut[:len(status_counts)],
        startangle=90, pctdistance=0.80,
        wedgeprops=dict(width=0.55, edgecolor="#1A1A2E", linewidth=2),
    )
    for t in texts:
        t.set_color("white"); t.set_fontsize(9)
    for at in autotexts:
        at.set_color("white"); at.set_fontsize(8)
    ax_donut.set_title("Delivery Status Distribution", color="white", fontsize=11, pad=10)

    # Supporting chart B: Monthly Shipment Volume Trend
    ax_trend = fig.add_subplot(gs[2:4, 2:4])
    ax_trend.set_facecolor("#16213E")
    df["Month_Str"] = df["Order_Date"].dt.strftime("%Y-%m")
    monthly_vol = df.groupby("Month_Str").size()
    ax_trend.fill_between(range(len(monthly_vol)), monthly_vol.values,
                          color="#118AB2", alpha=0.6)
    ax_trend.plot(range(len(monthly_vol)), monthly_vol.values,
                  color="#06D6A0", lw=2.5, marker="o", markersize=5)
    ax_trend.set_xticks(range(len(monthly_vol)))
    ax_trend.set_xticklabels(monthly_vol.index, rotation=45, ha="right", fontsize=7.5, color="white")
    ax_trend.set_ylabel("Shipments", color="white")
    ax_trend.set_title("Monthly Shipment Volume Trend", color="white", fontsize=11, pad=10)
    ax_trend.tick_params(colors="white")
    ax_trend.spines["bottom"].set_color("#FFFFFF40")
    ax_trend.spines["left"].set_color("#FFFFFF40")
    ax_trend.spines["top"].set_visible(False)
    ax_trend.spines["right"].set_visible(False)

    fig.text(0.01, 0.01,
             "DISCLAIMER: All data shown is HYPOTHETICAL and SIMULATED for internship analytics purposes only. "
             "This does not represent any real company or operational data.",
             fontsize=7.5, color="#AAAAAA")

    fig.savefig("logistics_kpi_dashboard.png", dpi=FIG_DPI,
                bbox_inches="tight", facecolor="#1A1A2E")
    plt.close(fig)
    print("  âœ“ Saved: logistics_kpi_dashboard.png")


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# MAIN ORCHESTRATION
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def main():
    print("\n" + "=" * 60)
    print("  WEEK 3 LOGISTICS ANALYSIS â€” STARTING")
    print("=" * 60)

    # Load
    df = load_data("hypothetical_logistics_dataset.csv")

    # EDA Sections
    numeric_cols, cat_cols, date_cols = dataset_overview(df)
    stats_df    = descriptive_statistics(df)
    categorical_analysis(df)
    kpis        = calculate_kpis(df)
    corr_matrix = correlation_analysis(df)

    # Summary CSVs
    print("\n" + "=" * 60)
    print("  GENERATING SUMMARY CSVs")
    print("=" * 60)
    carrier_perf, region_perf, mode_analysis, monthly = generate_summary_csvs(df)

    # Visualizations
    print("\n" + "=" * 60)
    print("  GENERATING VISUALIZATIONS (14 charts + dashboard)")
    print("=" * 60)
    plot_shipment_volume_trend(df)
    plot_delivery_time_distribution(df)
    plot_cost_distribution(df)
    plot_delivery_time_by_mode(df)
    plot_cost_by_mode(df)
    plot_delivery_time_by_region(df)
    plot_cost_by_carrier(df)
    plot_distance_vs_cost(df)
    plot_distance_vs_delivery_time(df)
    plot_correlation_heatmap(df)
    plot_delay_by_traffic(df)
    plot_delay_by_weather(df)
    plot_customer_rating_vs_delay(df)
    plot_monthly_cost_trend(df)
    plot_warehouse_processing(df)
    plot_kpi_dashboard(df, kpis)

    print("\n" + "=" * 60)
    print("  ALL ANALYSIS COMPLETE")
    print("=" * 60)
    print(f"  Total visualizations saved : 16 (14 charts + KPI dashboard + warehouse)")
    print(f"  Total CSV summaries saved  : 6")
    print("  Ready for report generation.")

    return df, kpis, corr_matrix, stats_df, carrier_perf, region_perf, mode_analysis, monthly


if __name__ == "__main__":
    main()

