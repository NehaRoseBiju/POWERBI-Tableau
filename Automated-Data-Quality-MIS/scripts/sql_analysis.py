
import sqlite3
from pathlib import Path
import pandas as pd

# Find the main project folder automatically
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
REPORT_DIR = PROJECT_DIR / "reports"
SQL_DIR = PROJECT_DIR / "sql"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
SQL_DIR.mkdir(parents=True, exist_ok=True)

# Load CSV files
sales = pd.read_csv(DATA_DIR / "sales.csv")
customers = pd.read_csv(DATA_DIR / "customers.csv")

# Create a SQLite database inside the project
db_path = DATA_DIR / "mis_database.db"

with sqlite3.connect(db_path) as conn:

    # Import CSV data into SQLite tables
    sales.to_sql("sales", conn, if_exists="replace", index=False)
    customers.to_sql("customers", conn, if_exists="replace", index=False)

    print("Data imported into SQLite successfully!")

    # Query 1: Total sales revenue from valid quantities and prices
    revenue_query = """
    SELECT
        COUNT(*) AS valid_order_rows,
        SUM(CAST(quantity AS REAL) *
            CAST(unit_price AS REAL)) AS total_revenue
    FROM sales
    WHERE quantity > 0
      AND unit_price >= 0;
    """

    revenue = pd.read_sql_query(revenue_query, conn)
    revenue.to_csv(REPORT_DIR / "sql_revenue_summary.csv", index=False)

    print("\n1. Revenue summary")
    print(revenue.to_string(index=False))

    # Query 2: Find duplicate order IDs
    duplicates_query = """
    SELECT
        order_id,
        COUNT(*) AS occurrences
    FROM sales
    GROUP BY order_id
    HAVING COUNT(*) > 1;
    """

    duplicates = pd.read_sql_query(duplicates_query, conn)
    duplicates.to_csv(REPORT_DIR / "sql_duplicate_orders.csv", index=False)

    print("\n2. Duplicate order IDs")
    print(duplicates.to_string(index=False))

    # Query 3: Match sales with customer records
    customer_query = """
    SELECT
        s.order_id,
        s.customer_id,
        c.customer_name,
        s.product,
        s.quantity,
        s.unit_price
    FROM sales AS s
    LEFT JOIN customers AS c
        ON s.customer_id = c.customer_id;
    """

    customer_results = pd.read_sql_query(customer_query, conn)
    customer_results.to_csv(
        REPORT_DIR / "sql_customer_reconciliation.csv",
        index=False
    )

    print("\n3. Customer reconciliation")
    print(customer_results.to_string(index=False))

    # Query 4: Find unmatched customer IDs
    unmatched_query = """
    SELECT
        s.order_id,
        s.customer_id
    FROM sales AS s
    LEFT JOIN customers AS c
        ON s.customer_id = c.customer_id
    WHERE s.customer_id IS NOT NULL
      AND c.customer_id IS NULL;
    """

    unmatched = pd.read_sql_query(unmatched_query, conn)
    unmatched.to_csv(
        REPORT_DIR / "sql_unmatched_customers.csv",
        index=False
    )

    print("\n4. Unmatched customers")
    print(unmatched.to_string(index=False))

print("\nSQL analysis completed!")
print("Database:", db_path)
print("Reports saved in:", REPORT_DIR)
