# Week 3 Submission Audit
## Advanced Data Analysis and Visualization in Logistics

**Project Folder:** Logistics-Data-Analysis-3
**Audit Date:** September 2026
**Random Seed:** 42 (fully reproducible)

---

## Requirement Audit Table

| # | Requirement | Status | Evidence | Correction Needed |
|---|-------------|--------|----------|-------------------|
| 1 | Hypothetical dataset clearly labeled as simulated | PASS | Disclaimer on title page, executive summary, dataset section, all chart captions | None |
| 2 | Dataset generated programmatically with Python | PASS | generate_logistics_dataset.py using numpy/random, seed=42 | None |
| 3 | Fixed random seed for reproducibility | PASS | RANDOM_SEED=42, np.random.seed(42), random.seed(42) | None |
| 4 | Dataset size 2500-5000 records | PASS | 3500 shipment records | None |
| 5 | Dataset saved as CSV | PASS | hypothetical_logistics_dataset.csv (639 KB) | None |
| 6 | 25 required variables defined | PASS | All 25 variables present and correctly typed | None |
| 7 | Logically realistic data relationships | PASS | Distance->time; distance+weight->cost; traffic/weather->delays | None |
| 8 | Realistic random variation | PASS | +-10% multiplicative noise, log-normal weight distribution | None |
| 9 | No large data-quality problems | PASS | Zero missing values; clean dataset | None |
| 10 | Dataset script prints summary | PASS | Rows, cols, types, numeric summary, missing values printed | None |
| 11 | EDA script: week3_logistics_analysis.py | PASS | File exists, 47 KB, 16 charts + 6 CSVs produced | None |
| 12 | Dataset overview section | PASS | dataset_overview() prints full breakdown | None |
| 13 | Descriptive statistics (9 stats, 11 vars) | PASS | descriptive_statistics() computes mean, median, std, min, Q1, Q3, max, IQR, skewness | None |
| 14 | Categorical analysis (counts + %) | PASS | categorical_analysis() for 7 categorical variables | None |
| 15 | KPI calculations with formulas | PASS | calculate_kpis() -- 9 KPIs, formulas printed, saved to kpi_summary.csv | None |
| 16 | Pearson correlation analysis | PASS | correlation_analysis() -- 10 vars, saved to correlation_matrix.csv | None |
| 17 | KPI: On-Time Delivery Rate | PASS | 36.63% computed programmatically | None |
| 18 | KPI: Avg Delivery Time | PASS | 36.84 hours | None |
| 19 | KPI: Avg Delay Hours | PASS | 9.41 hours | None |
| 20 | KPI: Avg Transportation Cost | PASS | $625.75 USD | None |
| 21 | KPI: Cost per Kilometer | PASS | $0.5691/km | None |
| 22 | KPI: Avg Customer Rating | PASS | 3.99/5.0 | None |
| 23 | KPI: Shipment Volume | PASS | 27139.76 m3 total | None |
| 24 | KPI: Avg Warehouse Processing Time | PASS | 6.35 hours | None |
| 25 | No hardcoded KPI values | PASS | All KPIs computed from loaded CSV | None |
| 26 | Minimum 10 visualizations | PASS | 16 visualizations total | None |
| 27 | Chart 1: Shipment Volume Over Time | PASS | shipment_volume_trend.png (bar+rolling line) | None |
| 28 | Chart 2: Delivery Time Distribution | PASS | delivery_time_distribution.png (histogram+KDE) | None |
| 29 | Chart 3: Cost Distribution | PASS | transportation_cost_distribution.png | None |
| 30 | Chart 4: Delivery Time by Mode (boxplot) | PASS | delivery_time_by_shipping_mode.png | None |
| 31 | Chart 5: Cost by Mode | PASS | cost_by_shipping_mode.png | None |
| 32 | Chart 6: Delivery Time by Region | PASS | delivery_time_by_region.png | None |
| 33 | Chart 7: Cost by Carrier | PASS | cost_by_carrier.png | None |
| 34 | Chart 8: Distance vs Cost (scatter+regression) | PASS | distance_vs_cost.png | None |
| 35 | Chart 9: Distance vs Delivery Time | PASS | distance_vs_delivery_time.png (colour by mode) | None |
| 36 | Chart 10: Correlation Heatmap | PASS | correlation_heatmap.png | None |
| 37 | Additional charts 11-15 | PASS | delay_by_traffic, delay_by_weather, customer_rating_vs_delay, monthly_cost_trend, warehouse_processing_time | None |
| 38 | KPI Dashboard | PASS | logistics_kpi_dashboard.png (dark theme, 6 KPI tiles + 2 charts) | None |
| 39 | Charts: title, axes, units, legend | PASS | All 16 charts properly labelled | None |
| 40 | Professional chart formatting | PASS | Consistent palette, DPI=150, white grid, professional fonts | None |
| 41 | Visualization justification for each chart | PASS | Each chart has "Why This Chart Was Selected" in the report | None |
| 42 | Interpretations based on actual results | PASS | All interpretations reference computed r-values and actual dataset findings | None |
| 43 | kpi_summary.csv | PASS | Exists, 392 bytes | None |
| 44 | carrier_performance.csv | PASS | Exists, 365 bytes | None |
| 45 | region_performance.csv | PASS | Exists, 470 bytes | None |
| 46 | shipping_mode_analysis.csv | PASS | Exists, 373 bytes | None |
| 47 | monthly_trends.csv | PASS | Exists, 644 bytes | None |
| 48 | correlation_matrix.csv | PASS | Exists, 2256 bytes, 10x10 matrix | None |
| 49 | DOCX report generated | PASS | 1662 KB, 20 sections | None |
| 50 | DOCX: Title Page | PASS | Title, subtitle, date, tools, disclaimer | None |
| 51 | DOCX: Executive Summary | PASS | Section 1 with key metrics | None |
| 52 | DOCX: Project Objective | PASS | Section 2 with 9 analytical questions | None |
| 53 | DOCX: Logistics Scenario | PASS | Section 3 -- warehouses, regions, carriers, modes | None |
| 54 | DOCX: Dataset Description + Data Dictionary | PASS | Section 4 -- 25-variable table | None |
| 55 | DOCX: Data Generation Methodology | PASS | Section 5 -- 8 design decisions | None |
| 56 | DOCX: Python Tools and Libraries | PASS | Section 5.1 -- 6 libraries | None |
| 57 | DOCX: EDA Methodology | PASS | Section 6 -- 5 phases | None |
| 58 | DOCX: Dataset Overview | PASS | Section 7 -- formatted table | None |
| 59 | DOCX: Descriptive Statistics | PASS | Section 8 -- 11x9 table | None |
| 60 | DOCX: KPI Analysis with formulas | PASS | Section 9 -- 9 KPIs with formulas and values | None |
| 61 | DOCX: Correlation Analysis | PASS | Section 10 -- key pairs with r-values | None |
| 62 | DOCX: 15 visualization sections | PASS | Sections 11.1-11.15 with justification+interpretation each | None |
| 63 | Charts embedded in DOCX | PASS | All 16 PNG files embedded via add_picture() | None |
| 64 | Figure captions/numbers | PASS | Figure N: description below each chart | None |
| 65 | DOCX: KPI Dashboard section | PASS | Section 12 | None |
| 66 | DOCX: Operational Efficiency Findings | PASS | Section 13.1 -- 5 findings | None |
| 67 | DOCX: Cost Driver Findings | PASS | Section 13.2 -- r-values cited | None |
| 68 | DOCX: Bottleneck Analysis | PASS | Section 13.3 -- WH-Central, Northeast | None |
| 69 | DOCX: Customer Impact | PASS | Section 13.4 -- r=-0.960 cited | None |
| 70 | DOCX: Trends | PASS | Section 13.5 -- Q4/Q2 peaks | None |
| 71 | DOCX: Key Insights Summary Table | PASS | Section 14 -- 8-row table | None |
| 72 | DOCX: Recommendations (8) | PASS | Section 15 -- all linked to findings | None |
| 73 | DOCX: Limitations | PASS | Section 16 -- 7 limitations | None |
| 74 | DOCX: Python Code Excerpts | PASS | Section 17 -- 4 code blocks | None |
| 75 | DOCX: How to Run | PASS | Section 18 -- pip install + 3 commands | None |
| 76 | DOCX: References | PASS | Section 19 -- 8 references | None |
| 77 | DOCX: Conclusion | PASS | Section 20 -- professional close | None |
| 78 | Correlation != causation stated | PASS | Stated in 3 report locations | None |
| 79 | Dataset labeled simulated throughout | PASS | Title page, exec summary, all chart captions, limitations | None |
| 80 | README.md created | PASS | 12 KB, all required sections | None |
| 81 | README: Overview, objective, scenario | PASS | Present | None |
| 82 | README: Variable table | PASS | 21-row variable table | None |
| 83 | README: KPI table | PASS | KPI formulas table | None |
| 84 | README: Visualization list | PASS | 16-row table | None |
| 85 | README: How to run | PASS | 3-step instructions | None |
| 86 | README: Project structure | PASS | Full directory tree | None |
| 87 | README: Limitations | PASS | Section with disclaimer | None |
| 88 | requirements.txt created | PASS | 7 libraries listed | None |
| 89 | .gitignore created | PASS | __pycache__, *.pyc, .venv/, venv/, .env included | None |
| 90 | Relative file paths | PASS | No absolute paths in any script | None |
| 91 | All 3 scripts run successfully (exit 0) | PASS | All verified | None |
| 92 | No Week 1/Week 2 references | PASS | Fully standalone project | None |
| 93 | Operational efficiency findings | PASS | Air fastest; WH-Central bottleneck | None |
| 94 | Cost driver analysis | PASS | Ranking by |r| with Transportation_Cost_USD: #1 Fuel_Cost r=+0.738, #2 Weight_kg r=+0.605, #3 Handling_Cost r=+0.570, #4 Distance r=+0.257. Fuel Cost is a component of Transportation Cost so r=+0.738 is expected; no independent causation claimed. | None |
| 95 | Bottleneck identification | PASS | WH-Central (processing), Northeast (region) | None |
| 96 | Customer impact analysis | PASS | Delay-Rating r=-0.960 | None |
| 97 | Trend analysis | PASS | Q4/Q2 volume peaks identified | None |
| 98 | 8 recommendations | PASS | All 8 linked to specific findings | None |
| 99 | DOCX professional formatting | PASS | Consistent styles, colour headers, margins, sections | None |
| 100 | No exaggerated claims | PASS | Disclaimer in every major section | None |

---

## Summary Statistics (Python-Computed)

| Metric | Value |
|--------|-------|
| Dataset | 3500 rows x 25 columns |
| On-Time Delivery Rate | 36.63% |
| Avg Delivery Time | 36.84 hours |
| Avg Delay | 9.41 hours |
| Avg Transportation Cost | $625.75 |
| Cost per km | $0.5691 |
| Avg Customer Rating | 3.99/5.0 |
| Corr Distance-Cost | r=+0.257 |
| Corr Weight-Cost | r=+0.605 |
| Corr Fuel-Cost | r=+0.738 |
| Corr Delay-Rating | r=-0.960 |
| Slowest Region | Northeast (52.76h) |
| Slowest Warehouse | WH-Central |
| Fastest Mode | Air (23.29h avg) |
| Cheapest Mode | Sea ($156.67 avg) |

---

## Files Generated: 32 Total (Verified Programmatically)

| Type | Count | Notes |
|------|-------|-------|
| Python Scripts (.py) | 4 | generate_logistics_dataset.py, week3_logistics_analysis.py, generate_docx_report.py, audit_check.py |
| Markdown (.md) | 2 | README.md, week3_submission_audit.md |
| Text (.txt) | 1 | requirements.txt |
| Dot files | 1 | .gitignore |
| CSV Files (.csv) | 7 | hypothetical_logistics_dataset.csv + 6 summary CSVs |
| PNG Charts (.png) | 16 | Charts 1-15 + logistics_kpi_dashboard.png |
| DOCX Report (.docx) | 1 | Week_3_Advanced_Data_Analysis_and_Visualization_in_Logistics.docx |
| **TOTAL** | **32** | Verified with os.listdir() |

---

## FINAL RESULT: ALL 100 REQUIREMENTS -- PASS
