from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Sales Analytics Dashboard", page_icon="📊", layout="wide")

REQUIRED_COLUMNS = {"date", "product", "category", "region", "quantity", "unit_price"}

st.title("📊 Sales Analytics Dashboard")
st.caption("Explore revenue, product performance, regional trends, and downloadable reports.")

@st.cache_data
def load_sample_data():
    return pd.read_csv(Path(__file__).parent / "sample_sales.csv", parse_dates=["date"])

def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Normalize headers so "Unit Price", "unit price", and "unit_price" match.
    df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(sorted(missing)))
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    for col in ["quantity", "unit_price"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["date", "product", "category", "region", "quantity", "unit_price"])
    # Prevent blank text fields from appearing as valid products/categories/regions.
    for col in ["product", "category", "region"]:
        df[col] = df[col].astype(str).str.strip()
        df = df[df[col] != ""]
    # Negative quantity/price values are not accepted in this demo dataset.
    df = df[(df["quantity"] >= 0) & (df["unit_price"] >= 0)]
    df["revenue"] = df["quantity"] * df["unit_price"]
    df["month"] = df["date"].dt.to_period("M").astype(str)
    return df

with st.sidebar:
    st.header("Data source")
    uploaded = st.file_uploader("Upload a sales CSV", type=["csv"])
    st.caption("Required columns: date, product, category, region, quantity, unit_price")
    if uploaded:
        try:
            raw = pd.read_csv(uploaded)
            data = prepare_data(raw)
            st.success(f"Loaded {len(data):,} valid rows.")
        except Exception as exc:
            st.error(str(exc))
            st.stop()
    else:
        data = prepare_data(load_sample_data())
        st.info("Showing included sample data.")

if data.empty:
    st.warning("No valid rows found. Check your CSV data.")
    st.stop()

with st.sidebar:
    st.divider()
    date_min = data["date"].min().date()
    date_max = data["date"].max().date()
    date_range = st.date_input("Date range", value=(date_min, date_max), min_value=date_min, max_value=date_max)
    regions = sorted(data["region"].astype(str).unique())
    selected_regions = st.multiselect("Region", regions, default=regions)
    categories = sorted(data["category"].astype(str).unique())
    selected_categories = st.multiselect("Category", categories, default=categories)

filtered = data.copy()
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1]) + pd.Timedelta(days=1) - pd.Timedelta(microseconds=1)
    filtered = filtered[(filtered["date"] >= start) & (filtered["date"] <= end)]
filtered = filtered[
    filtered["region"].isin(selected_regions) &
    filtered["category"].isin(selected_categories)
]

if filtered.empty:
    st.warning("No sales match these filters. Adjust the filters in the sidebar.")
    st.stop()

total_revenue = filtered["revenue"].sum()
total_units = filtered["quantity"].sum()
orders = len(filtered)
avg_record_value = total_revenue / orders if orders else 0

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Revenue", f"${total_revenue:,.2f}")
m2.metric("Units Sold", f"{total_units:,.0f}")
m3.metric("Sales Records", f"{orders:,}")
m4.metric("Avg. Record Value", f"${avg_record_value:,.2f}")

st.divider()
left, right = st.columns(2)
with left:
    monthly = filtered.groupby("month", as_index=False)["revenue"].sum().sort_values("month")
    fig = px.line(monthly, x="month", y="revenue", markers=True, title="Monthly Revenue Trend",
                  labels={"month": "Month", "revenue": "Revenue"})
    fig.update_layout(margin=dict(l=10, r=10, t=55, b=10))
    st.plotly_chart(fig, use_container_width=True)
with right:
    by_category = filtered.groupby("category", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
    fig = px.bar(by_category, x="category", y="revenue", title="Revenue by Category",
                 labels={"category": "Category", "revenue": "Revenue"}, text_auto=".2s")
    fig.update_layout(margin=dict(l=10, r=10, t=55, b=10))
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    by_region = filtered.groupby("region", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
    fig = px.bar(by_region, x="region", y="revenue", title="Revenue by Region",
                 labels={"region": "Region", "revenue": "Revenue"}, text_auto=".2s")
    fig.update_layout(margin=dict(l=10, r=10, t=55, b=10))
    st.plotly_chart(fig, use_container_width=True)
with right:
    by_product = (filtered.groupby("product", as_index=False)
                  .agg(revenue=("revenue", "sum"), units=("quantity", "sum"))
                  .sort_values("revenue", ascending=False).head(10))
    fig = px.bar(by_product, x="revenue", y="product", orientation="h", title="Top 10 Products by Revenue",
                 labels={"product": "Product", "revenue": "Revenue"}, text_auto=".2s")
    fig.update_layout(yaxis={"categoryorder": "total ascending"}, margin=dict(l=10, r=10, t=55, b=10))
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Filtered sales data")
display_columns = ["date", "product", "category", "region", "quantity", "unit_price", "revenue"]
st.dataframe(filtered[display_columns].sort_values("date", ascending=False), use_container_width=True, hide_index=True)
csv_bytes = filtered[display_columns].to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download filtered report (CSV)", data=csv_bytes, file_name="filtered_sales_report.csv", mime="text/csv")

st.caption("Portfolio demo only. Revenue is calculated as quantity × unit price; it is not an accounting or tax report.")
