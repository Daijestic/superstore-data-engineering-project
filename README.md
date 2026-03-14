# Superstore Data Warehouse Pipeline

## Overview
This project demonstrates an end-to-end data engineering workflow using the Superstore dataset.

Raw sales data is processed with Python, transformed into a star schema, loaded into PostgreSQL, and used for analytics in Power BI.

## Pipeline
`Raw CSV -> Python ETL -> Star Schema -> PostgreSQL -> Power BI`

## Tech Stack
- Python
- Pandas
- PostgreSQL
- SQL
- Power BI

## Data Model
The warehouse is designed using a star schema:

- `dim_customer`
- `dim_product`
- `dim_location`
- `fact_sales`

## What I Built
- Extracted and cleaned raw sales data
- Transformed data into dimension and fact tables
- Built a simple analytical data warehouse model
- Loaded transformed data into PostgreSQL
- Wrote SQL queries for analysis
- Created a Power BI dashboard for reporting

## Project Structure
```text
superstore-data-engineering-project/
├── data/
├── etl/
├── sql/
├── dashboard/
└── README.md
```

## Skills Demonstrated
- ETL development
- Data cleaning and transformation
- Dimensional modeling
- Star schema design
- SQL analytics
- Data warehouse implementation
- BI-ready data preparation

## Use Case
This project supports reporting and analysis for:
- sales performance
- product trends
- customer behavior
- geographic insights

