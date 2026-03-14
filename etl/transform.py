from __future__ import annotations

from typing import Tuple
import pandas as pd


class TransformError(Exception):
    """Raised when the transform step fails."""


def build_dimensions_and_fact(
    raw_df: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Rebuild notebook logic in pure Python modules.

    Notebook logic:
    1. Create dim_customer from Customer ID, Customer Name, Segment
    2. Create dim_product from Product ID, Product Name, Category, Sub-Category
       and resolve inconsistent product records by deduplicating on product_id
    3. Create dim_location from Postal Code, Country, Region, State, City
       then generate location_id = row_number
    4. Rename raw columns and merge location_id back into the raw dataframe
    5. Create fact_sales
    6. Aggregate duplicate (order_id, product_id) pairs
    7. Format date columns to YYYY-MM-DD
    """
    required_columns = {
        "Customer ID",
        "Customer Name",
        "Segment",
        "Product ID",
        "Product Name",
        "Category",
        "Sub-Category",
        "Postal Code",
        "Country",
        "Region",
        "State",
        "City",
        "Order ID",
        "Order Date",
        "Ship Date",
        "Ship Mode",
        "Sales",
        "Quantity",
        "Discount",
        "Profit",
    }

    missing = sorted(required_columns.difference(raw_df.columns))
    if missing:
        raise TransformError(
            "Thiếu cột bắt buộc theo đúng logic notebook: " + ", ".join(missing)
        )

    df = raw_df.copy()

    # -------------------------
    # dim_customer
    # -------------------------
    dim_customer = df[["Customer ID", "Customer Name", "Segment"]].copy()
    dim_customer = dim_customer.rename(
        columns={
            "Customer ID": "customer_id",
            "Customer Name": "customer_name",
            "Segment": "segment",
        }
    )
    dim_customer = dim_customer.drop_duplicates().reset_index(drop=True)

    # -------------------------
    # dim_product
    # -------------------------
    dim_product = df[["Product ID", "Product Name", "Category", "Sub-Category"]].copy()
    dim_product = dim_product.rename(
        columns={
            "Product ID": "product_id",
            "Product Name": "product_name",
            "Category": "category",
            "Sub-Category": "sub_category",
        }
    )
    dim_product = dim_product.drop_duplicates()
    # Keep the first observed attributes for the same product_id
    dim_product = dim_product.drop_duplicates(subset=["product_id"]).reset_index(drop=True)

    # -------------------------
    # dim_location
    # -------------------------
    dim_location = df[["Postal Code", "Country", "Region", "State", "City"]].copy()
    dim_location = dim_location.rename(
        columns={
            "Postal Code": "postal_code",
            "Country": "country",
            "Region": "region",
            "State": "state",
            "City": "city",
        }
    )
    dim_location["postal_code"] = dim_location["postal_code"].astype(str)
    dim_location = dim_location.drop_duplicates().reset_index(drop=True)
    dim_location["location_id"] = dim_location.index + 1

    # -------------------------
    # rename raw df
    # -------------------------
    df = df.rename(
        columns={
            "Postal Code": "postal_code",
            "Country": "country",
            "Region": "region",
            "State": "state",
            "City": "city",
            "Order ID": "order_id",
            "Order Date": "order_date",
            "Ship Date": "ship_date",
            "Ship Mode": "ship_mode",
            "Customer ID": "customer_id",
            "Product ID": "product_id",
            "Sales": "sales",
            "Quantity": "quantity",
            "Discount": "discount",
            "Profit": "profit",
        }
    )

    df["postal_code"] = df["postal_code"].astype(str)

    # bring location_id into raw df
    df = df.merge(
        dim_location,
        on=["postal_code", "country", "region", "state", "city"],
        how="left",
    )

    if df["location_id"].isnull().any():
        null_count = int(df["location_id"].isnull().sum())
        raise TransformError(
            f"Có {null_count} dòng không map được location_id sau khi merge dim_location."
        )

    # -------------------------
    # fact_sales
    # -------------------------
    fact_sales = df[
        [
            "order_id",
            "order_date",
            "ship_date",
            "ship_mode",
            "customer_id",
            "product_id",
            "location_id",
            "sales",
            "quantity",
            "discount",
            "profit",
        ]
    ].copy()

    # same notebook logic: aggregate duplicated (order_id, product_id)
    fact_sales = fact_sales.groupby(
        ["order_id", "product_id"],
        as_index=False,
    ).agg(
        {
            "order_date": "first",
            "ship_date": "first",
            "ship_mode": "first",
            "customer_id": "first",
            "location_id": "first",
            "discount": "first",
            "quantity": "sum",
            "sales": "sum",
            "profit": "sum",
        }
    )

    fact_sales = fact_sales[
        [
            "order_id",
            "order_date",
            "ship_date",
            "ship_mode",
            "customer_id",
            "product_id",
            "location_id",
            "sales",
            "quantity",
            "discount",
            "profit",
        ]
    ].copy()

    fact_sales["order_date"] = pd.to_datetime(
        fact_sales["order_date"], dayfirst=True, errors="raise"
    ).dt.strftime("%Y-%m-%d")
    fact_sales["ship_date"] = pd.to_datetime(
        fact_sales["ship_date"], dayfirst=True, errors="raise"
    ).dt.strftime("%Y-%m-%d")

    # Order columns for dimension tables
    dim_customer = dim_customer[["customer_id", "customer_name", "segment"]]
    dim_product = dim_product[["product_id", "product_name", "category", "sub_category"]]
    dim_location = dim_location[
        ["location_id", "postal_code", "country", "region", "state", "city"]
    ]

    return dim_customer, dim_product, dim_location, fact_sales
