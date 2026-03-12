CREATE TABLE dim_customer (
    customer_id VARCHAR PRIMARY KEY,
    customer_name VARCHAR,
    segment VARCHAR
);

CREATE TABLE dim_product (
    product_id VARCHAR PRIMARY KEY,
    product_name VARCHAR,
    category VARCHAR,
    sub_category VARCHAR
);

CREATE TABLE dim_location (
    location_id SERIAL PRIMARY KEY,
    postal_code VARCHAR,
    country VARCHAR,
    region VARCHAR,
    state VARCHAR,
    city VARCHAR
);

CREATE TABLE fact_sales (
    order_id VARCHAR,
    order_date DATE,
    ship_date DATE,
    ship_mode VARCHAR,
    customer_id VARCHAR,
    product_id VARCHAR,
    location_id INT,
    sales FLOAT,
    quantity INT,
    discount FLOAT,
    profit FLOAT,

    PRIMARY KEY (order_id, product_id),

    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
    FOREIGN KEY (product_id) REFERENCES dim_product(product_id),
    FOREIGN KEY (location_id) REFERENCES dim_location(location_id)
);