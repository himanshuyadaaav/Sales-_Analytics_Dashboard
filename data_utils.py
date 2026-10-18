"""Reusable data cleaning and validation for the sales dashboard."""

import re
import pandas as pd

REQUIRED_COLUMNS = {"date", "product", "category", "region", "quantity", "unit_price"}


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    """Validate sales columns, clean invalid rows, and calculate revenue/month."""
    df = df.copy()
    normalized = [re.sub(r"\s+", "_", str(column).strip().lower()) for column in df.columns]
    if len(normalized) != len(set(normalized)):
        raise ValueError("Duplicate column names found after normalization.")
    df.columns = normalized

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(sorted(missing)))

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    for column in ("quantity", "unit_price"):
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df.dropna(subset=["date", "product", "category", "region", "quantity", "unit_price"])
    for column in ("product", "category", "region"):
        df[column] = df[column].astype(str).str.strip()
        df = df[df[column] != ""]

    # Negative values are not accepted in this demo's sales data.
    df = df[(df["quantity"] >= 0) & (df["unit_price"] >= 0)].copy()
    df["revenue"] = df["quantity"] * df["unit_price"]
    df["month"] = df["date"].dt.to_period("M").astype(str)
    return df
