DROP TABLE IF EXISTS fact_sales;
DROP TABLE IF EXISTS dim_product;
DROP TABLE IF EXISTS dim_branch;

CREATE TABLE dim_branch (
    branch_key INTEGER PRIMARY KEY,
    branch_id TEXT NOT NULL UNIQUE,
    branch_name TEXT NOT NULL,
    city TEXT NOT NULL
);

CREATE TABLE dim_product (
    product_key INTEGER PRIMARY KEY,
    product_id TEXT NOT NULL UNIQUE,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    unit_price REAL NOT NULL
);

CREATE TABLE fact_sales (
    sales_key INTEGER PRIMARY KEY,
    sale_id TEXT NOT NULL UNIQUE,
    sale_date TEXT NOT NULL,
    branch_key INTEGER NOT NULL,
    product_key INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    sales_amount REAL NOT NULL,
    payment_method TEXT NOT NULL,
    FOREIGN KEY (branch_key) REFERENCES dim_branch(branch_key),
    FOREIGN KEY (product_key) REFERENCES dim_product(product_key)
);

