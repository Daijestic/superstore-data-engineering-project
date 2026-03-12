# Superstore Data Warehouse Project

## Overview

This project builds a simple data warehouse using the Superstore sales
dataset.

The raw CSV data is cleaned and transformed using Python (Pandas) to
create a **star schema** with dimension tables and a fact table. The
data is then loaded into **PostgreSQL** and connected to **Power BI**
for visualization.

## Tech Stack

-   Python (Pandas)
-   PostgreSQL
-   SQL
-   Power BI
-   Jupyter Notebook

## Data Model

Star Schema design:

Dimension tables: - dim_customer - dim_product - dim_location

Fact table: - fact_sales

Primary key: (order_id, product_id)

## ETL Pipeline

1.  Load raw CSV dataset
2.  Clean and rename columns
3.  Create dimension tables
4.  Generate surrogate keys
5.  Build fact table
6.  Load data into PostgreSQL

Pipeline:

CSV Dataset -> Python ETL (Pandas) -> PostgreSQL Data Warehouse -> Power BI
Dashboard

## Dashboard

Power BI dashboard includes:

-   Total Sales
-   Total Profit
-   Total Quantity
-   Profit Margin
-   Monthly Sales Trend
-   Monthly Profit Trend
-   Sales by Category
-   Sales by Region
-   Top Products
-   Top Customers

## Project Structure

superstore-data-warehouse/

data/ dim_customer.csv dim_product.csv dim_location.csv fact_sales.csv

etl/ etl_superstore.ipynb

sql/ create_tables.sql analytics_queries.sql

README.md

## Key Skills Demonstrated

-   ETL pipeline development
-   Star schema modeling
-   SQL analytics queries
-   Data warehouse design
-   Data visualization with Power BI
