from pathlib import Path
import sqlite3

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data" / "sample"
SQL_DIR = BASE_DIR / "sql"
OUTPUT_DIR = BASE_DIR / "output"
DB_PATH = OUTPUT_DIR / "retail_dw.db"


def load_csv_files() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    branches = pd.read_csv(DATA_DIR / "branches.csv")
    products = pd.read_csv(DATA_DIR / "products.csv")
    sales = pd.read_csv(DATA_DIR / "sales_raw.csv")
    return branches, products, sales


def clean_data(
    branches: pd.DataFrame, products: pd.DataFrame, sales: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    for frame in (branches, products, sales):
        text_columns = frame.select_dtypes(include="object").columns
        for column in text_columns:
            frame[column] = frame[column].astype(str).str.strip()

    products["category"] = products["category"].replace(
        {
            "home care": "Home Care",
            "personal care": "Personal Care",
            "cold food": "Cold Food",
            "grocery": "Grocery",
        }
    )
    sales["sale_date"] = pd.to_datetime(sales["sale_date"]).dt.date.astype(str)
    sales["payment_method"] = sales["payment_method"].str.title()
    return branches, products, sales


def build_dimensions(
    branches: pd.DataFrame, products: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    dim_branch = branches.copy()
    dim_branch.insert(0, "branch_key", range(1, len(dim_branch) + 1))

    dim_product = products.copy()
    dim_product.insert(0, "product_key", range(1, len(dim_product) + 1))
    return dim_branch, dim_product


def build_fact_sales(
    sales: pd.DataFrame, dim_branch: pd.DataFrame, dim_product: pd.DataFrame
) -> pd.DataFrame:
    fact_sales = sales.merge(
        dim_branch[["branch_key", "branch_id"]],
        on="branch_id",
        how="left",
    ).merge(
        dim_product[["product_key", "product_id", "unit_price"]],
        on="product_id",
        how="left",
    )

    fact_sales["sales_amount"] = fact_sales["quantity"] * fact_sales["unit_price"]
    fact_sales.insert(0, "sales_key", range(1, len(fact_sales) + 1))

    fact_sales = fact_sales[
        [
            "sales_key",
            "sale_id",
            "sale_date",
            "branch_key",
            "product_key",
            "quantity",
            "unit_price",
            "sales_amount",
            "payment_method",
        ]
    ]
    return fact_sales


def create_database(connection: sqlite3.Connection) -> None:
    create_tables_sql = (SQL_DIR / "01_create_tables.sql").read_text(encoding="utf-8")
    connection.executescript(create_tables_sql)


def load_to_sqlite(
    dim_branch: pd.DataFrame, dim_product: pd.DataFrame, fact_sales: pd.DataFrame
) -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    with sqlite3.connect(DB_PATH) as connection:
        create_database(connection)
        dim_branch.to_sql("dim_branch", connection, if_exists="append", index=False)
        dim_product.to_sql("dim_product", connection, if_exists="append", index=False)
        fact_sales.to_sql("fact_sales", connection, if_exists="append", index=False)


def print_kpis() -> None:
    with sqlite3.connect(DB_PATH) as connection:
        total_sales = pd.read_sql_query(
            "SELECT ROUND(SUM(sales_amount), 2) AS total_sales FROM fact_sales",
            connection,
        )
        sales_by_branch = pd.read_sql_query(
            """
            SELECT b.branch_name, ROUND(SUM(f.sales_amount), 2) AS total_sales
            FROM fact_sales f
            JOIN dim_branch b ON f.branch_key = b.branch_key
            GROUP BY b.branch_name
            ORDER BY total_sales DESC
            """,
            connection,
        )

    print("ETL completed successfully.")
    print(f"Database created at: {DB_PATH}")
    print()
    print("Total sales:")
    print(total_sales.to_string(index=False))
    print()
    print("Sales by branch:")
    print(sales_by_branch.to_string(index=False))


def main() -> None:
    branches, products, sales = load_csv_files()
    branches, products, sales = clean_data(branches, products, sales)
    dim_branch, dim_product = build_dimensions(branches, products)
    fact_sales = build_fact_sales(sales, dim_branch, dim_product)
    load_to_sqlite(dim_branch, dim_product, fact_sales)
    print_kpis()


if __name__ == "__main__":
    main()
