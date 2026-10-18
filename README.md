# Sales Analytics Dashboard

A portfolio-ready sales dashboard built with Python, Streamlit, Pandas, and Plotly.

## Features

- Upload a sales CSV or explore included sample data
- Validate required columns and clean invalid rows
- Filter by date range, region, and category
- KPI cards for revenue, units sold, record count, and average record value
- Monthly revenue trend
- Revenue by category and region
- Top 10 products by revenue
- Interactive filtered data table and CSV export

## Tech stack

- Python 3.10+
- Streamlit
- Pandas
- Plotly

## Run locally

1. Create and activate a virtual environment (recommended).
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the dashboard:

   ```bash
   streamlit run app.py
   ```

Streamlit will print a local URL, usually `http://localhost:8501`.

## CSV format

The uploaded CSV must include these columns:

| Column | Meaning | Example |
|---|---|---|
| `date` | Sale date | `2026-01-04` |
| `product` | Product name | `Wireless Mouse` |
| `category` | Product category | `Accessories` |
| `region` | Sales region | `North` |
| `quantity` | Units sold | `12` |
| `unit_price` | Price per unit | `18.50` |

Column names are case-insensitive and spaces are converted to underscores.

## Example use case

A small retailer exports monthly sales from a spreadsheet and wants to quickly see which products, categories, and regions drive revenue. This dashboard lets them upload the CSV, filter results, and export a report without manually creating charts.

## Screenshots

Run the app and capture:
- Full dashboard with KPI cards
- Monthly trend and category chart
- Filtered table with the CSV download control

Add screenshots to a `screenshots/` folder before sharing the repository with clients.

## Limitations

- Revenue is calculated as `quantity × unit_price`; costs, profit, refunds, and tax are not modeled.
- Sample data is fictional and for demonstration only.
- The app does not save uploaded data to a database.
- Validate business definitions with a client before using real financial data.

## Next improvements

- Add unit tests for data validation and revenue calculations
- Add profit and discount fields
- Add PDF report export
- Deploy a demo on Streamlit Community Cloud
