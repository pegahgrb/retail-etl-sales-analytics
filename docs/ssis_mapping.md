# SSIS to Public Portfolio Mapping

This note explains how this public repository relates to the type of ETL work done in an SSIS-based retail BI project.

## Why this mapping matters

The original project files from a company environment contain internal information such as:

- connection manager definitions
- private server addresses
- deployment artifacts
- environment-specific package settings

Those files should not be uploaded directly to a public GitHub repository. Instead, this project recreates the ETL logic in a safe and portable way.

## Conceptual mapping

### Source layer

In a typical SSIS project, data comes from operational systems or SQL Server source databases.

In this public project:

- [`data/sample/branches.csv`](/C:/Users/pegah/Desktop/git/data/sample/branches.csv)
- [`data/sample/products.csv`](/C:/Users/pegah/Desktop/git/data/sample/products.csv)
- [`data/sample/sales_raw.csv`](/C:/Users/pegah/Desktop/git/data/sample/sales_raw.csv)

represent the source data.

### ETL package logic

In SSIS, transformations are usually implemented in control flow and data flow tasks.

In this public project:

- [`src/etl.py`](/C:/Users/pegah/Desktop/git/src/etl.py)

performs the same conceptual steps:

- extract source data
- clean and standardize values
- create dimensions
- join keys
- calculate measures
- load the final warehouse tables

### Warehouse layer

In an enterprise BI environment, the target may be a SQL Server data warehouse.

In this public project:

- [`sql/01_create_tables.sql`](/C:/Users/pegah/Desktop/git/sql/01_create_tables.sql)
- [`output/retail_dw.db`](/C:/Users/pegah/Desktop/git/output/retail_dw.db)

represent the warehouse layer.

### Reporting layer

In BI projects, reporting is usually delivered through Power BI, SSRS, or SQL reporting logic.

In this public project:

- [`sql/02_analytics_queries.sql`](/C:/Users/pegah/Desktop/git/sql/02_analytics_queries.sql)

represents the KPI and reporting layer that could later feed a dashboard.

## What to say in interviews

You can describe this project like this:

"I worked on retail BI and ETL workflows and rebuilt a public-safe version of that experience as a portfolio project. The original implementation used enterprise BI tools, but this repository demonstrates the same logic using Python, SQL, and a small warehouse model with dimension and fact tables."

## Safe publishing rules

Do not publish:

- real connection manager files
- private IP addresses
- user-specific `.dtproj.user` files
- deployment artifacts such as `.ispac`
- internal business data

Do publish:

- sample data
- recreated transformation logic
- warehouse design
- reporting queries
- screenshots or diagrams that do not reveal private information
