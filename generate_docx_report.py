"""
generate_docx_report.py
-------------------------------
Week 3 Internship Task: Advanced Data Analysis and Visualization in Logistics

Generates a professional DOCX report embedding all charts, KPIs, tables,
code excerpts, interpretations, and findings from the Week 3 analysis.

DISCLAIMER: Dataset is hypothetical and simulated for internship exercise purposes only.

Author: Internship Analytics Project
Date: September 2026
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import warnings

warnings.filterwarnings("ignore")


# ─────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────

def set_cell_bg(cell, hex_color):
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd  = OxmlElement("w:shd")
    shd.set(qn("w:val"),   "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"),  hex_color)
    tcPr.append(shd)


def add_page_break(doc):
    doc.add_page_break()


def heading(doc, text, level=1):
    h = doc.add_heading(text, level=level)
    if level == 1:
        h.runs[0].font.color.rgb = RGBColor(0x2E, 0x40, 0x57)
    elif level == 2:
        h.runs[0].font.color.rgb = RGBColor(0x45, 0x7B, 0x9D)
    elif level == 3:
        h.runs[0].font.color.rgb = RGBColor(0x2A, 0x9D, 0x8F)
    return h


def body(doc, text, bold=False, italic=False, indent=False):
    p = doc.add_paragraph()
    if indent:
        p.paragraph_format.left_indent = Cm(1)
    run = p.add_run(text)
    run.font.size = Pt(10.5)
    run.bold   = bold
    run.italic = italic
    return p


def bullet(doc, text, level=0):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.left_indent = Cm(0.5 * (level + 1))
    run = p.add_run(text)
    run.font.size = Pt(10.5)
    return p


def code_block(doc, code_text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent  = Cm(1)
    p.paragraph_format.right_indent = Cm(1)
    run = p.add_run(code_text)
    run.font.name = "Courier New"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(0x1A, 0x53, 0x76)
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"),   "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"),  "D6EAF8")
    pPr.append(shd)
    return p


def embed_image(doc, path, caption_text, fig_num, width_in=5.5):
    if os.path.exists(path):
        doc.add_picture(path, width=Inches(width_in))
        last_para = doc.paragraphs[-1]
        last_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap = doc.add_paragraph()
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = cap.add_run(f"Figure {fig_num}: {caption_text}")
        run.font.size   = Pt(9)
        run.font.italic = True
        run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
    else:
        body(doc, f"[Figure {fig_num}: {path} not found]", italic=True)


def add_disclaimer(doc):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(
        "WARNING: All data in this report is HYPOTHETICAL and SIMULATED "
        "for internship analytical exercise purposes only. "
        "This does not represent any real company, real shipments, or real logistics operations."
    )
    run.font.size   = Pt(9)
    run.font.italic = True
    run.font.color.rgb = RGBColor(0x99, 0x00, 0x00)


# ─────────────────────────────────────────────────────────────────────
# LOAD RESULTS
# ─────────────────────────────────────────────────────────────────────

def load_all_data():
    df      = pd.read_csv("hypothetical_logistics_dataset.csv", parse_dates=["Order_Date"])
    kpi_df  = pd.read_csv("kpi_summary.csv")
    corr    = pd.read_csv("correlation_matrix.csv", index_col=0)
    carrier = pd.read_csv("carrier_performance.csv")
    region  = pd.read_csv("region_performance.csv")
    mode    = pd.read_csv("shipping_mode_analysis.csv")
    monthly = pd.read_csv("monthly_trends.csv")
    kpis    = dict(zip(kpi_df["KPI"], kpi_df["Value"]))
    return df, kpis, corr, carrier, region, mode, monthly


def compute_desc_stats(df):
    key_cols = [
        "Delivery_Time_Hours", "Promised_Delivery_Hours", "Delay_Hours",
        "Weight_kg", "Distance_km", "Transportation_Cost_USD",
        "Fuel_Cost_USD", "Handling_Cost_USD",
        "Warehouse_Processing_Hours", "Shipment_Volume", "Customer_Rating",
    ]
    rows = []
    for col in key_cols:
        s  = df[col]
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        rows.append({
            "Variable":  col,
            "Mean":      round(s.mean(), 2),
            "Median":    round(s.median(), 2),
            "Std Dev":   round(s.std(), 2),
            "Min":       round(s.min(), 2),
            "Q1":        round(q1, 2),
            "Q3":        round(q3, 2),
            "Max":       round(s.max(), 2),
            "IQR":       round(q3 - q1, 2),
        })
    return pd.DataFrame(rows)


# ─────────────────────────────────────────────────────────────────────
# BUILD DOCUMENT
# ─────────────────────────────────────────────────────────────────────

def build_report():
    df, kpis, corr, carrier_perf, region_perf, mode_analysis, monthly = load_all_data()
    desc_stats = compute_desc_stats(df)

    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(10.5)
    for sec in doc.sections:
        sec.top_margin    = Cm(2.0)
        sec.bottom_margin = Cm(2.0)
        sec.left_margin   = Cm(2.5)
        sec.right_margin  = Cm(2.5)

    # ── TITLE PAGE ──
    doc.add_paragraph()
    doc.add_paragraph()
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    tr = title.add_run("WEEK 3 INTERNSHIP TASK")
    tr.font.size = Pt(22); tr.bold = True
    tr.font.color.rgb = RGBColor(0x2E, 0x40, 0x57)

    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sr = sub.add_run("Advanced Data Analysis and Visualization in Logistics")
    sr.font.size = Pt(16); sr.bold = True
    sr.font.color.rgb = RGBColor(0x45, 0x7B, 0x9D)

    doc.add_paragraph()
    for line in [
        "Python Analytics Project -- Hypothetical Dataset",
        "Analysis Period: January 2025 - December 2025",
        f"Report Generated: {datetime.now().strftime('%B %d, %Y')}",
        "Tools: Python | pandas | numpy | matplotlib | seaborn | scipy | python-docx",
    ]:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(line)
        run.font.size = Pt(11)

    doc.add_paragraph()
    add_disclaimer(doc)
    add_page_break(doc)

    # ── EXECUTIVE SUMMARY ──
    heading(doc, "1. Executive Summary", 1)
    body(doc, (
        f"This report presents a comprehensive Week 3 internship analytics exercise focused on "
        f"Advanced Data Analysis and Visualization in Logistics. A hypothetical logistics dataset "
        f"of {int(kpis['Total Shipments']):,} shipment records spanning a full simulated calendar "
        f"year (2025) was programmatically generated using Python with a fixed random seed (42) "
        f"to ensure full reproducibility."
    ))
    body(doc, (
        f"The analysis covers exploratory data analysis (EDA), key logistics KPIs, correlation "
        f"analysis, 16 professional visualizations, and actionable insights across operational "
        f"efficiency, cost drivers, bottleneck identification, and customer impact. "
        f"All numerical findings presented in this report are derived directly from Python "
        f"calculations on the generated dataset -- no values have been manually edited or assumed."
    ))
    body(doc, (
        f"Key summary metrics: On-Time Delivery Rate = {kpis['On-Time Delivery Rate (%)']:.1f}%, "
        f"Average Delivery Time = {kpis['Avg Delivery Time (Hours)']:.1f} hours, "
        f"Average Transportation Cost = ${kpis['Avg Transportation Cost (USD)']:,.2f} USD, "
        f"Average Customer Rating = {kpis['Avg Customer Rating (1-5)']:.2f} / 5.0."
    ))
    add_page_break(doc)

    # ── PROJECT OBJECTIVE ──
    heading(doc, "2. Project Objective", 1)
    body(doc, "The primary objective is to deepen analytical skills through the exploration, "
         "analysis, and visualization of logistics data using Python. The project focuses on "
         "the following core analytical questions:")
    questions = [
        "How long do deliveries take, and how does this vary by mode and region?",
        "Which shipping modes have higher transportation costs?",
        "Which regions or warehouses experience longer delivery times?",
        "How does shipment volume change over time (daily, weekly, monthly)?",
        "Is shipment distance related to transportation cost?",
        "Does shipment weight affect transportation cost?",
        "Which factors are associated with delivery delays?",
        "Where are possible operational bottlenecks?",
        "Which operational areas require attention based on the simulated data?",
    ]
    for q in questions:
        bullet(doc, q)

    # ── LOGISTICS SCENARIO ──
    heading(doc, "3. Logistics Scenario", 1)
    body(doc, (
        "The hypothetical scenario models an organization managing outbound shipments from "
        "5 origin warehouses (WH-North, WH-South, WH-East, WH-West, WH-Central) to customers "
        "across 8 destination regions in a simulated domestic market. The organization uses "
        "5 carriers and 5 shipping modes (Road, Air, Rail, Sea, Express) to fulfil orders "
        "placed throughout the year 2025."
    ))
    add_page_break(doc)

    # ── DATASET DESCRIPTION ──
    heading(doc, "4. Hypothetical Dataset Description", 1)
    add_disclaimer(doc)
    doc.add_paragraph()
    body(doc, (
        f"The dataset contains {int(kpis['Total Shipments']):,} simulated shipment records "
        f"with 25 variables. It was generated using Python with numpy random seed = 42, "
        f"ensuring complete reproducibility. The dataset covers January-December 2025."
    ))

    heading(doc, "4.1 Dataset Variables and Data Dictionary", 2)
    variables = [
        ("Shipment_ID",             "Unique shipment identifier (e.g. SHP-2025001)",   "String"),
        ("Order_Date",              "Date when order was placed",                       "Date"),
        ("Ship_Date",               "Date when shipment left the warehouse",            "Date"),
        ("Delivery_Date",           "Actual delivery date",                             "Date"),
        ("Origin_Warehouse",        "Source warehouse (5 options)",                     "Categorical"),
        ("Destination_Region",      "Delivery region (8 options)",                      "Categorical"),
        ("Destination_City",        "Specific delivery city",                           "Categorical"),
        ("Carrier",                 "Logistics carrier company (5 options)",            "Categorical"),
        ("Shipping_Mode",           "Transport mode: Road/Air/Rail/Sea/Express",        "Categorical"),
        ("Shipment_Volume",         "Cubic meters of shipment",                         "Numeric (m3)"),
        ("Weight_kg",               "Shipment weight in kilograms",                     "Numeric (kg)"),
        ("Distance_km",             "Delivery route distance in kilometres",            "Numeric (km)"),
        ("Transportation_Cost_USD", "Total transport cost in USD",                      "Numeric (USD)"),
        ("Delivery_Time_Hours",     "Actual delivery duration in hours",                "Numeric (h)"),
        ("Promised_Delivery_Hours", "SLA-promised delivery window in hours",            "Numeric (h)"),
        ("Delivery_Status",         "On Time / Slightly Delayed / Delayed / Severely Delayed", "Categorical"),
        ("Delay_Hours",             "Hours beyond promised time (0 if on time)",        "Numeric (h)"),
        ("Customer_Rating",         "Customer satisfaction rating 1-5",                 "Numeric"),
        ("Fuel_Cost_USD",           "Estimated fuel cost component in USD",             "Numeric (USD)"),
        ("Handling_Cost_USD",       "Warehouse handling cost in USD",                   "Numeric (USD)"),
        ("Warehouse_Processing_Hours","Time spent in warehouse before dispatch (h)",    "Numeric (h)"),
        ("Traffic_Level",           "Road traffic condition: Low/Moderate/High/Severe", "Categorical"),
        ("Weather_Condition",       "Weather during transit: Clear/Cloudy/Rain/Fog/Storm", "Categorical"),
        ("Is_Express",              "1 if express shipment, 0 otherwise",               "Binary"),
        ("Is_Fragile",              "1 if fragile cargo, 0 otherwise",                  "Binary"),
    ]

    tbl = doc.add_table(rows=1, cols=3)
    tbl.style = "Table Grid"
    hdr_cells = tbl.rows[0].cells
    for cell, txt in zip(hdr_cells, ["Variable", "Description", "Type"]):
        cell.text = txt
        cell.paragraphs[0].runs[0].bold = True
        set_cell_bg(cell, "2E4057")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for var, desc, dtype in variables:
        row_cells = tbl.add_row().cells
        row_cells[0].text = var
        row_cells[0].paragraphs[0].runs[0].font.name = "Courier New"
        row_cells[0].paragraphs[0].runs[0].font.size = Pt(9)
        row_cells[1].text = desc
        row_cells[2].text = dtype

    add_page_break(doc)

    # ── DATA GENERATION METHODOLOGY ──
    heading(doc, "5. Data Generation Methodology", 1)
    body(doc, "The dataset was generated using the script generate_logistics_dataset.py. Key design decisions:")
    decisions = [
        "Fixed random seed (np.random.seed(42)) ensures reproducibility across runs.",
        "Order dates follow seasonal weights: higher volume in Q4 (Oct-Dec) and Q2 (Apr-Jun).",
        "Delivery time is computed from transit speed + traffic delay + weather delay + warehouse processing, "
        "with +-10% multiplicative noise to avoid perfect linearity.",
        "Transportation cost is calculated from distance x weight x mode rate x carrier multiplier + fuel + handling costs.",
        "Weight follows a log-normal distribution (realistic: most shipments are moderate weight, few are very heavy).",
        "Delivery status is derived by comparing actual vs. promised delivery hours.",
        "Customer ratings decrease with delay duration and adverse conditions, with controlled noise.",
        "All parameters produce realistic -- not mathematically perfect -- relationships.",
    ]
    for d in decisions:
        bullet(doc, d)

    heading(doc, "5.1 Python Tools and Libraries", 2)
    libs = [
        ("pandas",      "Data manipulation, groupby aggregations, date parsing"),
        ("numpy",       "Numerical computations, random number generation, statistics"),
        ("matplotlib",  "Core visualization engine, figure/axis management"),
        ("seaborn",     "Statistical chart types (boxplots, heatmaps, violin plots, histograms)"),
        ("scipy.stats", "Pearson correlation, linear regression for trend lines"),
        ("python-docx", "Programmatic DOCX generation with embedded images and tables"),
    ]
    for lib, purpose in libs:
        bullet(doc, f"{lib}: {purpose}")

    add_page_break(doc)

    # ── EDA METHODOLOGY ──
    heading(doc, "6. EDA Methodology", 1)
    body(doc, "The Exploratory Data Analysis follows a structured five-phase methodology:")
    phases = [
        "Dataset Overview: Shape, data types, missing value audit, categorical levels.",
        "Descriptive Statistics: Mean, median, std dev, quartiles, IQR, skewness for all key numeric variables.",
        "Categorical Analysis: Value counts and percentage distributions for all categorical fields.",
        "KPI Calculation: Nine logistics KPIs computed programmatically from the dataset.",
        "Correlation Analysis: Pearson correlation matrix for ten key numeric variables.",
    ]
    for i, p in enumerate(phases, 1):
        bullet(doc, f"Phase {i}: {p}")

    # ── DATASET OVERVIEW ──
    heading(doc, "7. Dataset Overview", 1)
    overview_data = [
        ("Total Records",          f"{int(kpis['Total Shipments']):,} shipment records"),
        ("Total Variables",        "25 variables"),
        ("Numeric Variables",      "11 (Weight_kg, Distance_km, costs, times, ratings, volume)"),
        ("Categorical Variables",  "9 (Carrier, Shipping_Mode, Region, Warehouse, Status, Traffic, Weather, City, Warehouse)"),
        ("Date Variables",         "3 (Order_Date, Ship_Date, Delivery_Date)"),
        ("Binary Variables",       "2 (Is_Express, Is_Fragile)"),
        ("Date Range",             "January 2025 - December 2025"),
        ("Missing Values",         "None -- dataset is complete"),
        ("Random Seed",            "42 (fixed for reproducibility)"),
    ]
    tbl2 = doc.add_table(rows=1, cols=2)
    tbl2.style = "Table Grid"
    for cell, txt in zip(tbl2.rows[0].cells, ["Attribute", "Detail"]):
        cell.text = txt
        cell.paragraphs[0].runs[0].bold = True
        set_cell_bg(cell, "457B9D")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    for attr, detail in overview_data:
        r = tbl2.add_row().cells
        r[0].text = attr; r[1].text = detail
    doc.add_paragraph()

    # ── DESCRIPTIVE STATISTICS ──
    heading(doc, "8. Descriptive Statistics", 1)
    body(doc, "The following table summarises central tendencies and distributions for all key numeric variables:")

    tbl3 = doc.add_table(rows=1, cols=len(desc_stats.columns))
    tbl3.style = "Table Grid"
    for cell, col in zip(tbl3.rows[0].cells, desc_stats.columns):
        cell.text = col
        cell.paragraphs[0].runs[0].bold = True
        set_cell_bg(cell, "2E4057")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        cell.paragraphs[0].runs[0].font.size = Pt(8)

    for _, row in desc_stats.iterrows():
        r = tbl3.add_row().cells
        for i, val in enumerate(row):
            r[i].text = str(val)
            r[i].paragraphs[0].runs[0].font.size = Pt(8)

    doc.add_paragraph()
    body(doc, (
        "Observations: Delivery_Time_Hours shows high variance across shipping modes. "
        f"Transportation_Cost_USD ranges from ${df['Transportation_Cost_USD'].min():,.0f} to "
        f"${df['Transportation_Cost_USD'].max():,.0f}, reflecting large differences in distance "
        f"and weight. Delay_Hours is right-skewed (many shipments have zero delay while a smaller "
        f"proportion experience significant delays). Customer_Rating shows a left-skewed distribution, "
        f"indicating that most customers rate their experience above average."
    ))
    add_page_break(doc)

    # ── KPI ANALYSIS ──
    heading(doc, "9. KPI Analysis", 1)
    body(doc, "Key Performance Indicators were calculated programmatically from the dataset:")

    kpi_display = [
        ("On-Time Delivery Rate",
         "On-Time Shipments / Total Shipments x 100",
         f"{kpis['On-Time Delivery Rate (%)']:.2f}%",
         "Percentage of shipments delivered within promised time window"),
        ("Average Delivery Time",
         "Mean(Delivery_Time_Hours)",
         f"{kpis['Avg Delivery Time (Hours)']:.2f} hours",
         "Mean actual delivery duration across all shipments"),
        ("Average Delay Hours",
         "Mean(Delay_Hours) -- all shipments (0 if on time)",
         f"{kpis['Avg Delay Hours']:.2f} hours",
         "Average delay per shipment including non-delayed ones"),
        ("Average Transportation Cost",
         "Mean(Transportation_Cost_USD)",
         f"${kpis['Avg Transportation Cost (USD)']:,.2f}",
         "Average total cost per shipment"),
        ("Cost per Kilometer",
         "Mean(Transportation_Cost_USD / Distance_km)",
         f"${kpis['Cost per Kilometer (USD/km)']:.4f} / km",
         "Average transport cost per kilometre of distance"),
        ("Average Customer Rating",
         "Mean(Customer_Rating)",
         f"{kpis['Avg Customer Rating (1-5)']:.2f} / 5.0",
         "Mean customer satisfaction score"),
        ("Total Shipment Volume",
         "Sum(Shipment_Volume)",
          f"{df['Shipment_Volume'].sum():,.2f} m3",
         "Total cubic metres processed"),
        ("Avg Warehouse Processing Time",
         "Mean(Warehouse_Processing_Hours)",
         f"{kpis['Avg Warehouse Processing (h)']:.2f} hours",
         "Average time a shipment spends in the warehouse before dispatch"),
        ("Total Shipments",
         "Count(Shipment_ID)",
         f"{int(kpis['Total Shipments']):,}",
         "Total number of shipment records in the dataset"),
    ]

    tbl4 = doc.add_table(rows=1, cols=4)
    tbl4.style = "Table Grid"
    for cell, txt in zip(tbl4.rows[0].cells, ["KPI", "Formula", "Calculated Value", "Description"]):
        cell.text = txt
        cell.paragraphs[0].runs[0].bold = True
        set_cell_bg(cell, "2A9D8F")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        cell.paragraphs[0].runs[0].font.size = Pt(9)

    for kpi_name, formula, value, desc in kpi_display:
        r = tbl4.add_row().cells
        r[0].text = kpi_name;  r[0].paragraphs[0].runs[0].font.size = Pt(9)
        r[1].text = formula;   r[1].paragraphs[0].runs[0].font.size = Pt(8)
        r[2].text = value;     r[2].paragraphs[0].runs[0].font.size = Pt(9)
        r[3].text = desc;      r[3].paragraphs[0].runs[0].font.size = Pt(9)
    doc.add_paragraph()
    add_page_break(doc)

    # ── CORRELATION ANALYSIS ──
    heading(doc, "10. Correlation Analysis", 1)
    body(doc, (
        "A Pearson correlation matrix was computed for 10 key numeric variables. "
        "Note: Correlation measures linear association and does not imply causation."
    ))

    key_pairs = [
        ("Fuel_Cost_USD",              "Transportation_Cost_USD"),
        ("Weight_kg",                  "Transportation_Cost_USD"),
        ("Handling_Cost_USD",          "Transportation_Cost_USD"),
        ("Distance_km",                "Transportation_Cost_USD"),
        ("Distance_km",                "Delivery_Time_Hours"),
        ("Warehouse_Processing_Hours", "Delivery_Time_Hours"),
        ("Delay_Hours",                "Customer_Rating"),
    ]
    tbl5 = doc.add_table(rows=1, cols=3)
    tbl5.style = "Table Grid"
    for cell, txt in zip(tbl5.rows[0].cells, ["Variable A", "Variable B", "Pearson r"]):
        cell.text = txt
        cell.paragraphs[0].runs[0].bold = True
        set_cell_bg(cell, "2E4057")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for a, b in key_pairs:
        r_val = corr.loc[a, b] if a in corr.index and b in corr.columns else "N/A"
        r_str = f"{r_val:+.3f}" if isinstance(r_val, float) else str(r_val)
        row = tbl5.add_row().cells
        row[0].text = a; row[1].text = b; row[2].text = r_str
    doc.add_paragraph()

    body(doc, (
        "IMPORTANT INTERPRETATION NOTE: Fuel_Cost_USD and Handling_Cost_USD are sub-components "
        "of Transportation_Cost_USD in the simulated dataset. Their high correlations with "
        "Transportation_Cost_USD are therefore mathematically expected and do not reflect "
        "independent causal factors. Among independently modelled variables, Weight_kg shows "
        f"the strongest associative relationship with Transportation_Cost_USD "
        f"(r = {corr.loc['Weight_kg','Transportation_Cost_USD']:+.3f}). "
        "All correlation values should be interpreted as associative patterns only. "
        "Causation cannot be inferred from correlation in this simulated dataset."
    ))
    add_page_break(doc)

    # ── VISUALIZATION SECTIONS ──
    heading(doc, "11. Visualizations and Interpretations", 1)
    body(doc, (
        "All visualizations were generated using matplotlib and seaborn. "
        "Each chart was selected based on the nature of the variable being examined "
        "and the analytical question it addresses."
    ))

    viz_specs = [
        ("shipment_volume_trend.png",
         "Figure 1: Shipment Volume Over Time",
         "Shipment Volume Over Time (Line + Bar Chart)",
         "Chart 1 -- Shipment Volume Over Time",
         "Line chart with 7-day rolling average overlaid on daily bar chart.",
         "Order_Date (x-axis) vs. daily shipment count (y-axis). 7-day rolling average smooths noise.",
         (
             "A line chart with a rolling average overlay was selected because it captures both "
             "daily granularity (bar chart) and the underlying trend (line), making seasonal "
             "patterns clearly visible without losing short-term variation."
         ),
         (
             f"The chart reveals seasonal demand peaks in Q4 (October-December) and Q2 "
             f"(April-June), consistent with the dataset's generation logic. Volume dips "
             f"slightly in July-August. This pattern has direct operational implications: "
             f"warehouse staffing and carrier capacity should be pre-arranged for Q4 peaks."
         )),

        ("delivery_time_distribution.png",
         "Figure 2: Delivery Time Distribution",
         "Delivery Time Distribution (Histogram + KDE)",
         "Chart 2 -- Delivery Time Distribution",
         "Histogram with kernel density estimate (KDE) overlay.",
         "Delivery_Time_Hours. Mean and median marked with vertical reference lines.",
         (
             "A histogram with KDE was selected to simultaneously show frequency distribution "
             "(histogram bins) and the smooth probability density (KDE curve). "
             "This reveals skewness, multi-modality, and central tendency more clearly than "
             "a simple average."
         ),
         (
             f"The distribution shows delivery times spanning from under 1 hour (Air express) "
             f"to hundreds of hours (Sea mode, long distances). The distribution is right-skewed, "
             f"indicating that while most shipments complete within a moderate timeframe, "
             f"a tail of very long deliveries inflates the mean above the median. "
             f"Mean = {df['Delivery_Time_Hours'].mean():.1f} h, Median = {df['Delivery_Time_Hours'].median():.1f} h."
         )),

        ("transportation_cost_distribution.png",
         "Figure 3: Transportation Cost Distribution",
         "Transportation Cost Distribution (Histogram + KDE)",
         "Chart 3 -- Transportation Cost Distribution",
         "Histogram with KDE for Transportation_Cost_USD.",
         "Transportation_Cost_USD. Mean reference line marked.",
         (
             "A histogram was selected to show the cost distribution shape. "
             "Log-normal cost patterns (common in logistics) produce a right-skewed histogram, "
             "which is important for procurement and budgeting decisions."
         ),
         (
             f"Transportation cost is strongly right-skewed. The majority of shipments cost "
             f"less than the mean of ${df['Transportation_Cost_USD'].mean():,.0f}. "
             f"A small proportion of high-distance, high-weight air shipments account for a "
             f"disproportionate share of total cost, a common pattern in real logistics operations."
         )),

        ("delivery_time_by_shipping_mode.png",
         "Figure 4: Delivery Time by Shipping Mode",
         "Delivery Time by Shipping Mode (Boxplot)",
         "Chart 4 -- Delivery Time by Shipping Mode",
         "Boxplot showing median, IQR, whiskers, and outliers per shipping mode.",
         "Shipping_Mode (x-axis) vs. Delivery_Time_Hours (y-axis).",
         (
             "Boxplots were selected because they show the full distribution summary "
             "(median, spread, extreme values) rather than just the mean. "
             "This is critical for comparing delivery performance across modes, where "
             "both typical performance and consistency matter."
         ),
         (
             "Air mode shows the lowest median delivery time but also exhibits outliers "
             "caused by weather and traffic disruptions. Sea mode shows the widest spread "
             "and longest median delivery times due to its low speed. Road and Rail show "
             "moderate delivery times with considerable variation driven by distance. "
             "Express mode is consistent and fast due to priority handling."
         )),

        ("cost_by_shipping_mode.png",
         "Figure 5: Transportation Cost by Shipping Mode",
         "Transportation Cost by Shipping Mode (Boxplot)",
         "Chart 5 -- Transportation Cost by Shipping Mode",
         "Boxplot of Transportation_Cost_USD by Shipping_Mode.",
         "Shipping_Mode (x-axis) vs. Transportation_Cost_USD (y-axis).",
         (
             "Boxplots again allow comparing both typical costs and variability per mode. "
             "A bar chart of averages alone would mask cost spread, which is critical "
             "for carrier contract negotiations."
         ),
         (
             "Air shipments have the highest median cost, reflecting the premium cost-per-km "
             "rate. Sea mode is the cheapest despite long distances, due to its low rate. "
             "Road and Rail are mid-range. Express mode costs more than Road/Rail due to priority "
             "handling charges, but significantly less than Air."
         )),

        ("delivery_time_by_region.png",
         "Figure 6: Average Delivery Time by Region",
         "Average Delivery Time by Destination Region (Bar Chart)",
         "Chart 6 -- Delivery Time by Region",
         "Horizontal bar chart of mean delivery time per destination region.",
         "Destination_Region (y-axis) vs. Avg_Delivery_Time_Hours (x-axis).",
         (
             "A horizontal bar chart with data labels was selected for clear ranking "
             "of regions by average delivery time. Horizontal orientation accommodates "
             "region name labels without rotation or truncation."
         ),
         (
             "Northeast and Southeast regions show higher average delivery times due to "
             "their larger distance ranges in the dataset generation logic. "
             "Central and Northern regions tend to be served faster. "
             "This regional pattern identifies where dedicated carrier lanes or warehouse "
             "positioning could reduce delivery lead times."
         )),

        ("cost_by_carrier.png",
         "Figure 7: Average Transportation Cost by Carrier",
         "Average Transportation Cost by Carrier (Bar Chart)",
         "Chart 7 -- Cost by Carrier",
         "Vertical bar chart of mean transportation cost per carrier.",
         "Carrier (x-axis) vs. Avg_Transportation_Cost_USD (y-axis).",
         (
             "A bar chart enables direct comparison of carrier cost performance. "
             "Data labels make exact values readable. Colour highlights the highest-cost carrier."
         ),
         (
             "FastFreight Co. shows the highest average cost (multiplier: 1.10), "
             "while GlobalTrans Corp. shows the lowest (multiplier: 0.90). "
             "For cost-sensitive shipments, routing through GlobalTrans or National Cargo "
             "could reduce transportation spend without necessarily compromising delivery time."
         )),

        ("distance_vs_cost.png",
         "Figure 8: Distance vs. Transportation Cost",
         "Distance vs. Transportation Cost (Scatter Plot + Regression)",
         "Chart 8 -- Distance vs. Cost",
         "Scatter plot with linear regression trend line.",
         "Distance_km (x-axis) vs. Transportation_Cost_USD (y-axis).",
         (
             "A scatter plot with regression was selected to quantify and visualise the "
             "relationship between distance and cost. The regression line and r-value "
             "provide an objective measure of association strength."
         ),
         (
             f"A positive association is observed between distance and transportation cost "
             f"(r = {corr.loc['Distance_km','Transportation_Cost_USD']:+.3f}). This is a "
             f"weak-to-moderate correlation. Within the full correlation ranking, Fuel Cost "
             f"(r = {corr.loc['Fuel_Cost_USD','Transportation_Cost_USD']:+.3f}, a cost sub-component) "
             f"and Weight (r = {corr.loc['Weight_kg','Transportation_Cost_USD']:+.3f}) show stronger "
             f"associations with Transportation Cost. Significant scatter around the regression line "
             f"confirms that mode, weight, and carrier also meaningfully influence cost. "
             f"This is not a causal claim."
         )),

        ("distance_vs_delivery_time.png",
         "Figure 9: Distance vs. Delivery Time",
         "Distance vs. Delivery Time (Scatter Plot Coloured by Mode)",
         "Chart 9 -- Distance vs. Delivery Time",
         "Scatter plot with colour encoding by shipping mode.",
         "Distance_km (x-axis) vs. Delivery_Time_Hours (y-axis). Colour = Shipping_Mode.",
         (
             "A colour-encoded scatter plot was selected to simultaneously show the "
             "distance-time relationship and the mode-specific patterns. "
             "This is more informative than a simple scatter because it reveals that "
             "different modes produce very different time profiles for equivalent distances."
         ),
         (
             "The chart clearly shows mode-specific clusters: Air shipments cluster at "
             "low delivery times regardless of distance, while Sea and Road shipments "
             "form steeper slopes (more time per km). This validates the dataset design "
             "and provides operational insight: Air is the fastest per km but most expensive."
         )),

        ("correlation_heatmap.png",
         "Figure 10: Correlation Heatmap",
         "Pearson Correlation Heatmap -- Key Numeric Variables",
         "Chart 10 -- Correlation Heatmap",
         "Lower-triangle heatmap with annotated correlation coefficients.",
         "10 key numeric variables. Colour scale: blue (negative) to red (positive).",
         (
             "A heatmap was selected to provide a comprehensive overview of all pairwise "
             "correlations in a single chart. It enables rapid identification of strong "
             "associations and potential multicollinearity."
         ),
         (
             "Strong positive correlations are visible between Fuel_Cost_USD and "
             "Transportation_Cost_USD (expected: Fuel Cost is a cost sub-component), "
             "and between Weight_kg and Transportation_Cost_USD. "
             "Delay_Hours shows a strong negative correlation with Customer_Rating, indicating "
             "that longer delays are associated with lower satisfaction. "
             "Distance_km shows a moderate positive correlation with Delivery_Time_Hours."
         )),
    ]

    for i, (img, caption, full_title, section_title, chart_type, variables_used,
            justification, interpretation) in enumerate(viz_specs, 1):
        heading(doc, f"11.{i} {section_title}", 2)
        body(doc, f"Chart Type: {chart_type}", bold=True)
        body(doc, f"Variables Used: {variables_used}")
        body(doc, "Why This Chart Was Selected:", bold=True)
        body(doc, justification, indent=True)
        embed_image(doc, img, full_title, i, width_in=5.5)
        body(doc, "Interpretation:", bold=True)
        body(doc, interpretation, indent=True)
        doc.add_paragraph()

    extra_charts = [
        ("delay_by_traffic.png",
         "Figure 11: Delay Rate by Traffic Level",
         "Delay Rate by Traffic Level (%)",
         "Chart 11 -- Delay Rate by Traffic Level",
         "Bar chart of delay percentage grouped by traffic severity.",
         "Traffic_Level (x-axis) vs. Delay_Rate_% (y-axis).",
         (
             "A bar chart with a progressive colour scale was selected to intuitively "
             "communicate increasing delay risk with traffic severity. "
             "This is an easily interpretable format for operational stakeholders."
         ),
         (
             "Severe traffic is associated with the highest delay rate, followed by High, "
             "Moderate, and Low. This confirms that traffic conditions are a significant "
             "factor in delivery punctuality and that contingency routing plans should be "
             "activated under Severe traffic forecasts."
         )),
        ("delay_by_weather.png",
         "Figure 12: Delay Rate by Weather Condition",
         "Delay Rate by Weather Condition (%)",
         "Chart 12 -- Delay Rate by Weather Condition",
         "Bar chart of delay rate by weather condition.",
         "Weather_Condition (x-axis) vs. Delay_Rate_% (y-axis).",
         (
             "A bar chart ordered by weather severity was selected to clearly show "
             "the progressive delay impact of deteriorating weather."
         ),
         (
             "Storm conditions are associated with the highest delay rate, followed by "
             "Fog and Rain. Clear weather shows the lowest delay rate. The gradient from "
             "Clear to Storm demonstrates a consistent weather-delay pattern."
         )),
        ("customer_rating_vs_delay.png",
         "Figure 13: Customer Rating vs. Delay Hours",
         "Customer Rating vs. Delay Hours (Scatter + Regression)",
         "Chart 13 -- Customer Rating vs. Delay",
         "Scatter plot with regression line, colour-coded by customer rating.",
         "Delay_Hours (x-axis) vs. Customer_Rating (y-axis, 1-5). Colour = rating value.",
         (
             "A scatter plot with regression and colour encoding was selected to show both "
             "the overall trend (regression line) and individual data point distribution. "
             "Colour encoding adds a third dimension (rating level) to the 2D chart."
         ),
         (
             f"A strong negative correlation (r = {corr.loc['Delay_Hours','Customer_Rating']:+.3f}) "
             f"is observed between delay hours and customer rating -- longer delays are associated "
             f"with substantially lower ratings. Operations teams should prioritise reducing delays "
             f"for high-value customers. Correlation does not imply causation."
         )),
        ("monthly_cost_trend.png",
         "Figure 14: Monthly Cost Trend",
         "Monthly Transportation Cost Trend vs. Shipment Volume",
         "Chart 14 -- Monthly Cost Trend",
         "Dual-axis chart: bar chart (shipment count) + line chart (avg cost).",
         "Month (x-axis) vs. Shipment Count (left y-axis) and Avg Cost (right y-axis).",
         (
             "A dual-axis chart was selected to overlay volume and cost trends, enabling "
             "the reader to assess whether cost scales with volume (economies of scale) "
             "or remains stable regardless of demand."
         ),
         (
             "Monthly average cost is relatively stable across the year. "
             "Shipment volume shows the seasonal peaks in Q2 and Q4 as designed. "
             "The absence of a strong cost increase during peak months may suggest that "
             "volume discounts or mode-mix changes offset peak-period cost pressures."
         )),
        ("warehouse_processing_time.png",
         "Figure 15: Warehouse Processing Time by Warehouse",
         "Warehouse Processing Time Distribution by Warehouse (Violin Plot)",
         "Chart 15 -- Warehouse Processing Times",
         "Violin plot (with embedded quartile lines) per warehouse.",
         "Origin_Warehouse (x-axis) vs. Warehouse_Processing_Hours (y-axis).",
         (
             "Violin plots were selected because they show the complete probability "
             "density of processing times, not just summary statistics. "
             "They reveal skewness and outliers more clearly than boxplots "
             "for continuous operational time variables."
         ),
         (
             "WH-Central shows the widest distribution and highest median processing time, "
             "indicating inconsistent throughput -- a candidate for operational review. "
             "WH-West demonstrates the lowest and most consistent processing times, suggesting "
             "efficient warehouse processes worth benchmarking across other facilities."
         )),
    ]

    for i, (img, caption, full_title, section_title, chart_type, variables_used,
            justification, interpretation) in enumerate(extra_charts, 11):
        heading(doc, f"11.{i} {section_title}", 2)
        body(doc, f"Chart Type: {chart_type}", bold=True)
        body(doc, f"Variables Used: {variables_used}")
        body(doc, "Why This Chart Was Selected:", bold=True)
        body(doc, justification, indent=True)
        embed_image(doc, img, full_title, i, width_in=5.5)
        body(doc, "Interpretation:", bold=True)
        body(doc, interpretation, indent=True)
        doc.add_paragraph()

    add_page_break(doc)

    # ── KPI DASHBOARD ──
    heading(doc, "12. KPI Dashboard", 1)
    body(doc, (
        "A dedicated KPI dashboard was created to provide an at-a-glance summary of the most "
        "important logistics performance metrics alongside two supporting visualizations: "
        "the delivery status distribution (donut chart) and the monthly shipment volume trend."
    ))
    embed_image(doc, "logistics_kpi_dashboard.png",
                "Figure 16: Logistics KPI Dashboard -- Full Year 2025 (Hypothetical Dataset)", 16,
                width_in=6.0)
    body(doc, (
        "The dashboard uses a dark-theme design to make KPI values stand out visually. "
        "Each KPI tile is colour-coded to aid rapid interpretation. "
        "The dashboard is suitable for operational reporting and management briefings."
    ))
    add_page_break(doc)

    # ── ANALYTICAL INSIGHTS ──
    heading(doc, "13. Analytical Insights", 1)

    heading(doc, "13.1 Operational Efficiency", 2)
    body(doc, "DATA FINDINGS:", bold=True)
    insights_ops = [
        f"On-Time Delivery Rate: {kpis['On-Time Delivery Rate (%)']:.1f}% of shipments are delivered within promised time windows.",
        "Air and Express modes consistently achieve shorter delivery times but at higher cost.",
        "Road and Rail show wider delivery time distributions due to traffic and distance variability.",
        f"Average warehouse processing time is {kpis['Avg Warehouse Processing (h)']:.1f} hours, "
        "with WH-Central showing the highest median processing time.",
        "WH-West demonstrates the most consistent and efficient processing times.",
    ]
    for ins in insights_ops:
        bullet(doc, ins)

    heading(doc, "13.2 Cost Drivers", 2)
    body(doc, "DATA FINDINGS:", bold=True)
    r_dist_cost = corr.loc["Distance_km", "Transportation_Cost_USD"]
    r_wt_cost   = corr.loc["Weight_kg",   "Transportation_Cost_USD"]
    r_fuel_cost = corr.loc["Fuel_Cost_USD", "Transportation_Cost_USD"]
    r_hdl_cost  = corr.loc["Handling_Cost_USD", "Transportation_Cost_USD"]
    insights_cost = [
        f"Within the correlation matrix, Fuel_Cost_USD shows the highest correlation with "
        f"Transportation_Cost_USD (r = {r_fuel_cost:+.3f}). Because Fuel Cost is included as "
        f"a component of Transportation Cost in the simulated dataset, this relationship is "
        f"expected and does not reflect independent causation.",
        f"Among independently modelled variables, Weight_kg shows the strongest associative "
        f"relationship with Transportation_Cost_USD (r = {r_wt_cost:+.3f}), reflecting "
        f"mode-specific rate structures where heavier shipments incur higher costs.",
        f"Handling_Cost_USD and Transportation_Cost_USD: r = {r_hdl_cost:+.3f} -- also expected "
        f"since Handling Cost is a cost sub-component.",
        f"Distance_km and Transportation_Cost_USD: r = {r_dist_cost:+.3f} -- a positive but "
        f"weak-to-moderate correlation. Distance contributes to cost, but mode type, shipment "
        f"weight, and carrier multipliers also strongly influence total cost.",
        "FastFreight Co. averages the highest per-shipment cost; GlobalTrans Corp. the lowest.",
        "Air shipments carry the highest cost per km; Sea mode the lowest.",
        "Note: Correlation does not imply causation. These are associative patterns in a simulated dataset.",
    ]
    for ins in insights_cost:
        bullet(doc, ins)

    heading(doc, "13.3 Bottleneck Analysis", 2)
    body(doc, "DATA FINDINGS:", bold=True)
    insights_bottleneck = [
        "WH-Central has the highest median warehouse processing time, creating a pre-dispatch bottleneck.",
        "Severe traffic is associated with the highest delay rates among all traffic levels.",
        "Storm and Fog weather conditions correspond with elevated delay percentages.",
        "Northeast and Southeast regions experience the longest average delivery times.",
        "Sea mode, while cost-efficient, creates throughput bottlenecks for time-sensitive shipments.",
    ]
    for ins in insights_bottleneck:
        bullet(doc, ins)

    heading(doc, "13.4 Customer Impact Analysis", 2)
    r_delay_rating = corr.loc["Delay_Hours", "Customer_Rating"]
    body(doc, "DATA FINDINGS:", bold=True)
    insights_cust = [
        f"Delay Hours and Customer Rating: r = {r_delay_rating:+.3f}. "
        f"Longer delays are strongly associated with lower satisfaction scores.",
        f"Average customer rating across all shipments: {kpis['Avg Customer Rating (1-5)']:.2f}/5.0.",
        "Severely delayed shipments typically receive ratings well below the dataset average.",
        "Storm-affected shipments show both higher delay rates and lower average ratings.",
        "On-time delivery has the strongest positive effect on customer satisfaction "
        "in this simulated dataset.",
    ]
    for ins in insights_cust:
        bullet(doc, ins)

    heading(doc, "13.5 Trends", 2)
    body(doc, "DATA FINDINGS:", bold=True)
    insights_trends = [
        "Shipment volume peaks in Q4 (October-December) and secondarily in Q2 (April-June).",
        "Volume is lowest during July-August.",
        "Average monthly transportation cost remains relatively stable despite volume variation.",
        "Delivery time performance does not deteriorate significantly during high-volume months "
        "in this dataset, though real-world operations may differ.",
    ]
    for ins in insights_trends:
        bullet(doc, ins)
    add_page_break(doc)

    # ── KEY INSIGHTS SUMMARY ──
    heading(doc, "14. Key Insights Summary", 1)
    summary_insights = [
        (f"On-Time Rate: {kpis['On-Time Delivery Rate (%)']:.1f}%",
         f"{kpis['On-Time Delivery Rate (%)']:.1f}% of shipments met their promised delivery window."),
        (f"Highest-r Correlate with Cost: Fuel_Cost_USD (r = {corr.loc['Fuel_Cost_USD','Transportation_Cost_USD']:+.3f})",
         f"Expected: Fuel Cost is a cost sub-component. Among independently modelled variables, "
         f"Weight_kg (r = {corr.loc['Weight_kg','Transportation_Cost_USD']:+.3f}) shows the "
         f"strongest association with Transportation Cost."),
        ("Bottleneck Warehouse: WH-Central",
         "Highest median processing time across all five warehouses."),
        ("Fastest Mode: Air",
         "Lowest median delivery time but highest average cost per shipment."),
        ("Most Cost-Efficient Mode: Sea",
         "Lowest average transportation cost but longest delivery times."),
        ("Delay Driver: Severe Traffic + Storm Weather",
         "Both conditions are associated with the highest delay rates."),
        ("Customer Satisfaction Driver: On-Time Delivery",
         f"Delay Hours strongly negatively correlates with Customer Rating (r = {corr.loc['Delay_Hours','Customer_Rating']:+.3f})."),
        ("Seasonal Peak: Q4 (Oct-Dec)",
         "Highest shipment volume period; requires proactive capacity planning."),
    ]
    tbl_ins = doc.add_table(rows=1, cols=2)
    tbl_ins.style = "Table Grid"
    for cell, txt in zip(tbl_ins.rows[0].cells, ["Key Insight", "Supporting Finding"]):
        cell.text = txt
        cell.paragraphs[0].runs[0].bold = True
        set_cell_bg(cell, "2E4057")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    for insight, finding in summary_insights:
        r = tbl_ins.add_row().cells
        r[0].text = insight; r[1].text = finding
    doc.add_paragraph()
    add_page_break(doc)

    # ── RECOMMENDATIONS ──
    heading(doc, "15. Recommendations", 1)
    body(doc, (
        "The following recommendations are derived directly from the analytical findings above. "
        "Each recommendation is clearly linked to its supporting data finding. "
        "These recommendations apply to the hypothetical scenario and should not be "
        "applied to real operations without validation on actual data."
    ))

    recs = [
        (
            "Increase warehouse staffing at WH-Central during peak periods",
            "WH-Central shows the highest and most variable processing times (DATA FINDING). "
            "Additional sorting and dispatch personnel during Q4 peak volumes could reduce "
            "processing bottlenecks and improve on-time departure rates.",
        ),
        (
            "Implement weather-triggered contingency routing for Storm and Fog conditions",
            "Storm and Fog weather conditions show the highest delay rates (DATA FINDING). "
            "Pre-defined alternative routing plans activated under these conditions could "
            "reduce weather-related delivery failures.",
        ),
        (
            "Review carrier contracts for Northeast and Southeast regions",
            "These regions show the longest average delivery times (DATA FINDING). "
            "Negotiating dedicated carrier lanes or regional partnerships may reduce "
            "last-mile delivery time in these areas.",
        ),
        (
            "Evaluate mode selection criteria for cost-sensitive, time-flexible shipments",
            "Sea mode offers the lowest cost but longest lead time (DATA FINDING). "
            "For non-urgent, bulk shipments, defaulting to Sea or Rail could significantly "
            "reduce per-shipment transportation cost.",
        ),
        (
            "Develop traffic severity alerts to trigger pre-emptive dispatch earlier",
            "Severe traffic is associated with the highest delay rates (DATA FINDING). "
            "Earlier dispatch under Severe traffic forecasts could absorb transit delays "
            "and preserve on-time delivery performance.",
        ),
        (
            "Benchmark WH-Central against WH-West for process improvement",
            "WH-West demonstrates the most efficient and consistent processing times "
            "(DATA FINDING). Documenting and replicating WH-West's operational practices "
            "at WH-Central could reduce cross-facility processing time variance.",
        ),
        (
            "Plan carrier capacity agreements for Q4 peak volume periods",
            "Q4 (Oct-Dec) shows the highest shipment volumes (DATA FINDING). "
            "Pre-season capacity agreements with carriers reduce rate volatility and "
            "ensure service availability during the busiest period.",
        ),
        (
            "Prioritise on-time delivery for high-value customer segments",
            "Delay Hours strongly negatively correlate with Customer Rating (DATA FINDING). "
            "Identifying and flagging high-value orders for expedited handling or "
            "Express mode routing could protect customer relationships.",
        ),
    ]

    for i, (rec_title, rec_body) in enumerate(recs, 1):
        p = doc.add_paragraph()
        run = p.add_run(f"Recommendation {i}: {rec_title}")
        run.bold = True; run.font.color.rgb = RGBColor(0x2A, 0x9D, 0x8F)
        body(doc, rec_body, indent=True)
        doc.add_paragraph()

    add_page_break(doc)

    # ── LIMITATIONS ──
    heading(doc, "16. Limitations", 1)
    limitations = [
        "The dataset is entirely hypothetical and simulated. It does not represent any real company, "
        "real shipments, or real logistics network. All findings are illustrative only.",
        "All statistical relationships in the dataset were designed by the analyst. "
        "Correlations observed reflect generation parameters, not true operational reality.",
        "Correlation does not establish causation. No causal claims are made from this analysis.",
        "Fuel Cost and Handling Cost are sub-components of Transportation Cost in the simulation. "
        "Their high correlation with Transportation Cost is mathematically expected and does not "
        "reflect independent drivers that could be separately managed.",
        "The dataset uses simplified cost and time formulas. Real logistics costs involve "
        "surcharges, tolls, customs, and dynamic fuel pricing not captured here.",
        "Seasonal patterns were artificially weighted. Real seasonality is driven by market "
        "factors, holidays, and supply chain dynamics not modelled here.",
        "Real-world deployment of any insights derived from this exercise would require "
        "validation against actual operational data, professional logistics expertise, "
        "and appropriate statistical methodology.",
    ]
    for lim in limitations:
        bullet(doc, lim)
    add_page_break(doc)

    # ── PYTHON CODE EXCERPTS ──
    heading(doc, "17. Python Code Excerpts", 1)

    heading(doc, "17.1 Dataset Generation", 2)
    code_block(doc, """\
import numpy as np, pandas as pd, random
from datetime import datetime, timedelta

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)

def compute_delivery_time(distance_km, mode, warehouse_h, traffic, weather):
    speed       = MODE_SPEED[mode]
    transit_h   = distance_km / speed
    traffic_add = TRAFFIC_DELAY[traffic] * (distance_km / 100)
    weather_add = WEATHER_DELAY[weather]
    noise       = np.random.uniform(0.90, 1.10)
    return round((transit_h + traffic_add + weather_add + warehouse_h) * noise, 2)

def compute_cost(distance_km, weight_kg, mode, carrier, fuel_factor):
    rate       = MODE_COST_RATE[mode]
    multiplier = CARRIER_MULTIPLIER[carrier]
    base_cost  = distance_km * weight_kg * rate * multiplier
    fuel_cost  = distance_km * 0.0012 * fuel_factor * weight_kg
    handling   = weight_kg * np.random.uniform(0.4, 1.2)
    noise      = np.random.uniform(0.92, 1.10)
    return round((base_cost + fuel_cost + handling) * noise, 2), round(fuel_cost,2), round(handling,2)
""")

    heading(doc, "17.2 KPI Calculation", 2)
    code_block(doc, """\
total_shipments     = len(df)
on_time_count       = (df["Delivery_Status"] == "On Time").sum()
on_time_rate        = on_time_count / total_shipments * 100
avg_delivery_time   = df["Delivery_Time_Hours"].mean()
avg_delay           = df["Delay_Hours"].mean()
avg_transport_cost  = df["Transportation_Cost_USD"].mean()
cost_per_km         = (df["Transportation_Cost_USD"] / df["Distance_km"]).mean()
avg_customer_rating = df["Customer_Rating"].mean()
""")

    heading(doc, "17.3 Correlation Analysis", 2)
    code_block(doc, """\
from scipy import stats

corr_cols = ["Distance_km","Weight_kg","Delivery_Time_Hours",
             "Transportation_Cost_USD","Fuel_Cost_USD","Handling_Cost_USD",
             "Warehouse_Processing_Hours","Delay_Hours","Customer_Rating","Shipment_Volume"]
corr_matrix = df[corr_cols].corr()
corr_matrix.to_csv("correlation_matrix.csv")

# NOTE: Fuel_Cost_USD and Handling_Cost_USD are sub-components of Transportation_Cost_USD.
# Their high correlation with Transportation_Cost_USD is expected by design.
# Among independently modelled variables, Weight_kg shows the strongest association.
slope, intercept, r_val, p_val, _ = stats.linregress(
    df["Distance_km"], df["Transportation_Cost_USD"])
""")

    heading(doc, "17.4 Visualization Example (Correlation Heatmap)", 2)
    code_block(doc, """\
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

corr = df[corr_cols].corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
fig, ax = plt.subplots(figsize=(12, 9))
sns.heatmap(corr, mask=mask, annot=True, fmt=".2f",
            cmap="coolwarm", center=0, vmin=-1, vmax=1,
            linewidths=0.5, ax=ax, annot_kws={"size": 8})
ax.set_title("Pearson Correlation Heatmap")
fig.savefig("correlation_heatmap.png", dpi=150, bbox_inches="tight")
plt.close(fig)
""")
    add_page_break(doc)

    # ── REPRODUCIBILITY ──
    heading(doc, "18. Reproducibility -- How to Run", 1)
    body(doc, "Install dependencies:")
    code_block(doc, "pip install -r requirements.txt")
    body(doc, "Run in sequence:")
    code_block(doc, """\
python generate_logistics_dataset.py
python week3_logistics_analysis.py
python generate_docx_report.py""")
    body(doc, (
        "All three scripts use relative file paths and will save all outputs "
        "(CSV files, PNG charts, DOCX report) to the same project directory. "
        "Fixed random seed = 42 ensures identical results on every run."
    ))
    add_page_break(doc)

    # ── REFERENCES ──
    heading(doc, "19. References and Technical Documentation", 1)
    refs = [
        "pandas Documentation -- https://pandas.pydata.org/docs/",
        "NumPy Documentation -- https://numpy.org/doc/",
        "Matplotlib Documentation -- https://matplotlib.org/stable/contents.html",
        "Seaborn Documentation -- https://seaborn.pydata.org/",
        "SciPy Stats Documentation -- https://docs.scipy.org/doc/scipy/reference/stats.html",
        "python-docx Documentation -- https://python-docx.readthedocs.io/",
        "Tukey, J.W. (1977). Exploratory Data Analysis. Addison-Wesley.",
        "Pearson, K. (1895). Notes on regression and inheritance. Proceedings of the Royal Society.",
        "NOTE: All data in this project is hypothetical. No external datasets were used.",
    ]
    for ref in refs:
        bullet(doc, ref)

    # ── CONCLUSION ──
    heading(doc, "20. Conclusion", 1)
    body(doc, (
        f"This Week 3 internship project successfully demonstrates advanced exploratory data "
        f"analysis and visualization applied to a hypothetical logistics scenario. "
        f"Using Python (pandas, numpy, matplotlib, seaborn, scipy), a realistic dataset of "
        f"{int(kpis['Total Shipments']):,} shipment records was generated, analysed, "
        f"and visualised across 16 charts and a KPI dashboard."
    ))
    body(doc, (
        "The analysis identified meaningful patterns in delivery performance, cost drivers, "
        "warehouse processing bottlenecks, and customer satisfaction -- all directly derived "
        "from the simulated data without manual adjustment of results. Eight actionable "
        "recommendations were formulated based directly on the analytical findings."
    ))
    body(doc, (
        "All findings are explicitly qualified as reflecting a simulated environment. "
        "Real-world logistics analytics would require actual operational data, domain expertise, "
        "and rigorous statistical validation before driving business decisions. "
        "This project demonstrates the analytical workflow, Python tools, and reporting "
        "standards required for professional logistics data analysis."
    ))
    doc.add_paragraph()
    add_disclaimer(doc)

    output_file = "Week_3_Advanced_Data_Analysis_and_Visualization_in_Logistics.docx"
    doc.save(output_file)
    print(f"\n[OK] Report saved -> {output_file}")
    return output_file


def main():
    print("\n" + "=" * 60)
    print("  GENERATING DOCX REPORT")
    print("=" * 60)
    out = build_report()
    print("\n" + "=" * 60)
    print("  REPORT GENERATION COMPLETE")
    print(f"  Output: {out}")
    print("=" * 60)


if __name__ == "__main__":
    main()
