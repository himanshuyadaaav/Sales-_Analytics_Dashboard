# Sales Analytics Dashboard

An interactive sales analytics dashboard built with Python, Streamlit, Pandas, and Plotly. Upload a sales CSV to explore revenue trends and compare product categories and regions.

## Features

- Upload a sales CSV or explore the included fictional sample dataset
- Validate required columns and clean invalid rows
- Filter by date range, region, and category
- KPI cards for total revenue, units sold, sales-record count, and average record value
- Monthly revenue trend
- Revenue by category and region
- Top 10 products by revenue
- Interactive filtered data table and CSV export

## Tech stack

- Python 3.10+
- Streamlit
- Pandas
- Plotly
- unittest for data-preparation tests

## Live demo

Replace the placeholder below with your deployed Streamlit URL:

**[Open the Sales Analytics Dashboard](https://sales-analytics-dashboard9.streamlit.app/)**

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

## Run tests

The data preparation logic is isolated in `data_utils.py`, so tests do not need to start the Streamlit interface. Run from the project root:

```bash
python -m unittest -v
```

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

Column names are lowercased and spaces are converted to underscores.

## Example use case

A small retailer exports sales from a spreadsheet and wants to see which products, categories, and regions drive revenue. The dashboard lets them upload the CSV, filter results, and export the filtered data without manually creating charts.

## Screenshots

Add screenshots from the live dashboard to a `screenshots/` folder and embed them here. Suggested screenshots: KPI cards, trend/category charts, and filtered table.

## Limitations

- Revenue is calculated as `quantity × unit_price`; costs, profit, refunds, and tax are not modeled.
- Sample data is fictional and for demonstration only.
- Uploaded data is not stored in a database.
- Confirm business definitions before using the dashboard with real financial data.

## Possible improvements

- Add profit and discount fields
- Add PDF report export
- Add more data-quality summaries and tests
