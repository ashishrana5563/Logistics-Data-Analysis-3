"""
generate_logistics_dataset.py
-------------------------------
Week 3 Internship Task: Advanced Data Analysis and Visualization in Logistics
Generates a realistic hypothetical logistics dataset for analytical demonstration.

DISCLAIMER:
This dataset is entirely hypothetical and simulated for internship exercise purposes only.
It does not represent any real company, real shipments, or real logistics operations.
All values are generated programmatically using controlled random processes.

Author: Internship Analytics Project
Date: September 2026
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random
import os

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# FIXED RANDOM SEED â€” ensures full reproducibility
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)

N_RECORDS = 3500  # Number of simulated shipment records

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# REFERENCE LISTS
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
WAREHOUSES = ["WH-North", "WH-South", "WH-East", "WH-West", "WH-Central"]

REGIONS = ["North", "South", "East", "West", "Central", "Northeast", "Northwest", "Southeast"]

CITY_MAP = {
    "North":     ["Delhi", "Chandigarh", "Amritsar", "Ludhiana"],
    "South":     ["Chennai", "Bangalore", "Hyderabad", "Kochi"],
    "East":      ["Kolkata", "Bhubaneswar", "Guwahati", "Patna"],
    "West":      ["Mumbai", "Ahmedabad", "Pune", "Surat"],
    "Central":   ["Nagpur", "Bhopal", "Indore", "Raipur"],
    "Northeast": ["Guwahati", "Shillong", "Agartala", "Imphal"],
    "Northwest": ["Jaipur", "Jodhpur", "Bikaner", "Udaipur"],
    "Southeast": ["Visakhapatnam", "Vijayawada", "Coimbatore", "Madurai"],
}

CARRIERS = ["FastFreight Co.", "QuickShip Logistics", "National Cargo Ltd.", "SwiftMove Inc.", "GlobalTrans Corp."]

SHIPPING_MODES = ["Road", "Air", "Rail", "Sea", "Express"]

TRAFFIC_LEVELS = ["Low", "Moderate", "High", "Severe"]
WEATHER_CONDITIONS = ["Clear", "Cloudy", "Rain", "Fog", "Storm"]

# Region-specific distance ranges (km)
REGION_DISTANCE = {
    "North":     (200, 900),
    "South":     (600, 2000),
    "East":      (500, 1800),
    "West":      (400, 1500),
    "Central":   (300, 1200),
    "Northeast": (800, 2500),
    "Northwest": (300, 1100),
    "Southeast": (700, 2200),
}

# Warehouse-specific processing time parameters (mean, std) in hours
WH_PROCESSING_PARAMS = {
    "WH-North":   (6.5, 2.0),
    "WH-South":   (5.0, 1.5),
    "WH-East":    (7.5, 2.5),
    "WH-West":    (4.5, 1.2),
    "WH-Central": (8.0, 3.0),
}

# Shipping-mode speed factors (km/h effective delivery speed)
MODE_SPEED = {
    "Air":     550,
    "Express": 120,
    "Road":    60,
    "Rail":    80,
    "Sea":     25,
}

# Shipping-mode cost per km per kg (base rates)
MODE_COST_RATE = {
    "Air":     0.045,
    "Express": 0.025,
    "Road":    0.008,
    "Rail":    0.006,
    "Sea":     0.003,
}

# Carrier cost multipliers
CARRIER_MULTIPLIER = {
    "FastFreight Co.":      1.10,
    "QuickShip Logistics":  1.05,
    "National Cargo Ltd.":  0.95,
    "SwiftMove Inc.":       1.00,
    "GlobalTrans Corp.":    0.90,
}

# Traffic delay factor (additional hours per 100 km)
TRAFFIC_DELAY = {
    "Low":      0.0,
    "Moderate": 0.8,
    "High":     2.0,
    "Severe":   4.5,
}

# Weather delay factor (additional hours)
WEATHER_DELAY = {
    "Clear":  0.0,
    "Cloudy": 0.5,
    "Rain":   2.0,
    "Fog":    3.5,
    "Storm":  7.0,
}


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# HELPER FUNCTIONS
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def generate_order_dates(n, start="2025-01-01", end="2025-12-31"):
    """Generate random order dates within a calendar year with seasonal variation."""
    start_dt = datetime(2025, 1, 1)
    end_dt   = datetime(2025, 12, 31)
    date_range = (end_dt - start_dt).days

    # Seasonal weights â€” higher volume in Q4 (Octâ€“Dec) and Q2 (Aprâ€“Jun)
    weights = []
    for i in range(date_range + 1):
        d = start_dt + timedelta(days=i)
        month = d.month
        if month in [10, 11, 12]:
            w = 1.6
        elif month in [4, 5, 6]:
            w = 1.3
        elif month in [7, 8]:
            w = 0.8
        else:
            w = 1.0
        weights.append(w)

    weights = np.array(weights)
    weights /= weights.sum()

    day_offsets = np.random.choice(date_range + 1, size=n, p=weights)
    return [start_dt + timedelta(days=int(d)) for d in day_offsets]


def compute_delivery_time(distance_km, mode, warehouse_processing_h, traffic, weather):
    """Compute realistic delivery time in hours."""
    speed = MODE_SPEED[mode]
    transit_hours = distance_km / speed

    traffic_add   = TRAFFIC_DELAY[traffic] * (distance_km / 100)
    weather_add   = WEATHER_DELAY[weather]

    # Random operational noise Â±10%
    noise = np.random.uniform(0.90, 1.10)

    total_hours = (transit_hours + traffic_add + weather_add + warehouse_processing_h) * noise
    return round(max(total_hours, 1.0), 2)


def compute_cost(distance_km, weight_kg, mode, carrier, fuel_price_factor):
    """Compute realistic transportation cost in USD."""
    rate       = MODE_COST_RATE[mode]
    multiplier = CARRIER_MULTIPLIER[carrier]

    base_cost  = distance_km * weight_kg * rate * multiplier
    fuel_cost  = distance_km * 0.0012 * fuel_price_factor * weight_kg
    handling   = weight_kg * np.random.uniform(0.4, 1.2)

    noise = np.random.uniform(0.92, 1.10)
    transport_cost = (base_cost + fuel_cost + handling) * noise

    return round(transport_cost, 2), round(fuel_cost, 2), round(handling, 2)


def compute_promised_hours(distance_km, mode, is_express, warehouse_processing_h):
    """
    Compute promised delivery hours based on mode SLA.
    Includes warehouse processing time + transit time + a generous SLA buffer,
    producing a realistic on-time delivery rate of ~65-75%.
    """
    speed         = MODE_SPEED[mode]
    transit_hours = distance_km / speed
    # SLA buffer: transit × 1.40 (generous) + warehouse processing × 1.20
    sla_buffer    = 1.40
    promised      = transit_hours * sla_buffer + warehouse_processing_h * 1.20
    if is_express:
        promised *= 0.80  # Express SLA is tighter
    return round(max(promised, 2.0), 2)


def compute_customer_rating(delay_hours, weather, traffic):
    """Compute a 1â€“5 customer rating influenced by delay and conditions."""
    base_rating = 4.5
    # Each hour of delay reduces rating
    rating = base_rating - 0.05 * max(delay_hours, 0)
    # Severe weather/traffic reduce satisfaction slightly
    if weather == "Storm":
        rating -= 0.3
    elif weather == "Fog":
        rating -= 0.15
    if traffic == "Severe":
        rating -= 0.2
    # Clip between 1.0 and 5.0 and add small noise
    rating = np.clip(rating + np.random.uniform(-0.3, 0.3), 1.0, 5.0)
    return round(rating, 1)


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# MAIN DATASET GENERATION
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def generate_dataset(n=N_RECORDS):
    """
    Generate a realistic hypothetical logistics shipment dataset.

    Returns
    -------
    pd.DataFrame
    """
    print("=" * 60)
    print("  HYPOTHETICAL LOGISTICS DATASET GENERATION")
    print("  Week 3 Internship Task â€” Simulated Data Only")
    print("=" * 60)

    records = []
    order_dates = generate_order_dates(n)

    for i in range(n):
        shipment_id = f"SHP-{2025000 + i + 1}"

        # --- Dates ---
        order_date = order_dates[i]
        # Warehouse processing hours
        warehouse = random.choice(WAREHOUSES)
        wh_mean, wh_std = WH_PROCESSING_PARAMS[warehouse]
        wh_processing_h = round(max(np.random.normal(wh_mean, wh_std), 1.0), 2)

        ship_date = order_date + timedelta(hours=wh_processing_h)

        # --- Route ---
        region = random.choice(REGIONS)
        city_list = CITY_MAP[region]
        dest_city = random.choice(city_list)

        d_min, d_max = REGION_DISTANCE[region]
        distance_km = round(np.random.uniform(d_min, d_max), 1)

        # --- Shipment attributes ---
        mode    = random.choice(SHIPPING_MODES)
        carrier = random.choice(CARRIERS)

        is_express  = (mode == "Express") or (np.random.random() < 0.10)
        is_fragile  = np.random.random() < 0.15

        weight_kg        = round(np.random.lognormal(3.0, 0.8), 2)  # ~20 kg median, realistic spread
        weight_kg        = max(min(weight_kg, 2000), 0.5)
        shipment_volume  = round(np.random.lognormal(1.8, 0.7), 2)  # cubic meters

        # --- Conditions ---
        traffic_probs  = [0.30, 0.40, 0.20, 0.10]
        weather_probs  = [0.45, 0.25, 0.15, 0.10, 0.05]
        traffic  = np.random.choice(TRAFFIC_LEVELS, p=traffic_probs)
        weather  = np.random.choice(WEATHER_CONDITIONS, p=weather_probs)

        # --- Delivery time ---
        fuel_price_factor = np.random.uniform(0.85, 1.30)
        delivery_time_h   = compute_delivery_time(distance_km, mode, wh_processing_h, traffic, weather)
        promised_h        = compute_promised_hours(distance_km, mode, is_express, wh_processing_h)

        delivery_date = ship_date + timedelta(hours=delivery_time_h)

        # --- Cost ---
        transport_cost, fuel_cost, handling_cost = compute_cost(
            distance_km, weight_kg, mode, carrier, fuel_price_factor
        )

        # --- Status & Delay ---
        delay_hours = round(max(delivery_time_h - promised_h, 0), 2)
        if delivery_time_h <= promised_h:
            delivery_status = "On Time"
        elif delay_hours <= 6:
            delivery_status = "Slightly Delayed"
        elif delay_hours <= 24:
            delivery_status = "Delayed"
        else:
            delivery_status = "Severely Delayed"

        # --- Customer Rating ---
        rating = compute_customer_rating(delay_hours, weather, traffic)

        records.append({
            "Shipment_ID":               shipment_id,
            "Order_Date":                order_date.strftime("%Y-%m-%d"),
            "Ship_Date":                 ship_date.strftime("%Y-%m-%d"),
            "Delivery_Date":             delivery_date.strftime("%Y-%m-%d"),
            "Origin_Warehouse":          warehouse,
            "Destination_Region":        region,
            "Destination_City":          dest_city,
            "Carrier":                   carrier,
            "Shipping_Mode":             mode,
            "Shipment_Volume":           shipment_volume,
            "Weight_kg":                 weight_kg,
            "Distance_km":               distance_km,
            "Transportation_Cost_USD":   transport_cost,
            "Delivery_Time_Hours":       delivery_time_h,
            "Promised_Delivery_Hours":   promised_h,
            "Delivery_Status":           delivery_status,
            "Delay_Hours":               delay_hours,
            "Customer_Rating":           rating,
            "Fuel_Cost_USD":             fuel_cost,
            "Handling_Cost_USD":         handling_cost,
            "Warehouse_Processing_Hours": wh_processing_h,
            "Traffic_Level":             traffic,
            "Weather_Condition":         weather,
            "Is_Express":                int(is_express),
            "Is_Fragile":                int(is_fragile),
        })

    df = pd.DataFrame(records)
    return df


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# SAVE & REPORT
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def main():
    df = generate_dataset(N_RECORDS)

    output_path = "hypothetical_logistics_dataset.csv"
    df.to_csv(output_path, index=False)
    print(f"\nâœ“ Dataset saved â†’ {output_path}")

    # Summary report
    print("\n" + "â”€" * 50)
    print("DATASET SUMMARY")
    print("â”€" * 50)
    print(f"  Rows (shipment records) : {df.shape[0]}")
    print(f"  Columns (variables)     : {df.shape[1]}")

    print("\n  DATA TYPES:")
    for col, dtype in df.dtypes.items():
        print(f"    {col:<35} {dtype}")

    print("\n  NUMERIC SUMMARY:")
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    print(df[numeric_cols].describe().round(2).to_string())

    print("\n  MISSING VALUES:")
    missing = df.isnull().sum()
    if missing.sum() == 0:
        print("    No missing values â€” clean dataset.")
    else:
        print(missing[missing > 0].to_string())

    print("\n  DELIVERY STATUS DISTRIBUTION:")
    print(df["Delivery_Status"].value_counts().to_string())

    print("\n  SHIPPING MODE DISTRIBUTION:")
    print(df["Shipping_Mode"].value_counts().to_string())

    print("\n" + "=" * 60)
    print("  Dataset generation complete. Fully reproducible.")
    print("  DISCLAIMER: This dataset is HYPOTHETICAL and SIMULATED.")
    print("  It does not represent any real company or real data.")
    print("=" * 60)


if __name__ == "__main__":
    main()

