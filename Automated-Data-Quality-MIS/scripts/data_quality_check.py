
import pandas as pd
from pathlib import Path


from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(
    r"C:\Users\nehab\OneDrive\Desktop\sem3\Automated-Data-Quality-MIS"
)

DATA_DIR = PROJECT_DIR / "data"
REPORT_DIR = PROJECT_DIR / "reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Read CSV files
sales = pd.read_csv(DATA_DIR / "sales.csv")
customers = pd.read_csv(DATA_DIR / "customers.csv")

print("Sales data loaded successfully!")
print(sales.head())

print("\nCustomer data loaded successfully!")
print(customers.head())


# Store all detected issues here
issues = []

def add_issue(order_id, column, issue_type, details):
    issues.append({
        "order_id": order_id,
        "column": column,
        "issue_type": issue_type,
        "details": details
    })

# 1. Check for completely duplicated rows
duplicate_rows = sales.duplicated(keep=False)

for idx in sales.index[duplicate_rows]:
    add_issue(
        sales.loc[idx, "order_id"],
        "all columns",
        "Duplicate row",
        "This row duplicates another complete row."
    )

# 2. Check for duplicate order IDs
duplicate_orders = sales["order_id"].duplicated(keep=False)

for idx in sales.index[duplicate_orders]:
    add_issue(
        sales.loc[idx, "order_id"],
        "order_id",
        "Duplicate order ID",
        "Order ID occurs more than once."
    )

# 3. Check for missing values
for column in sales.columns:
    missing_rows = sales.index[sales[column].isna()]

    for idx in missing_rows:
        add_issue(
            sales.loc[idx, "order_id"],
            column,
            "Missing value",
            f"{column} is missing."
        )

# 4. Validate order dates
parsed_dates = pd.to_datetime(
    sales["order_date"], errors="coerce"
)

invalid_dates = parsed_dates.isna()

for idx in sales.index[invalid_dates]:
    add_issue(
        sales.loc[idx, "order_id"],
        "order_date",
        "Invalid date",
        "Date is missing or cannot be interpreted."
    )

# 5. Validate quantities
invalid_quantity = (
    sales["quantity"].isna() | (sales["quantity"] <= 0)
)

for idx in sales.index[invalid_quantity]:
    add_issue(
        sales.loc[idx, "order_id"],
        "quantity",
        "Invalid quantity",
        "Quantity must be greater than zero."
    )

# 6. Validate unit prices
invalid_price = (
    sales["unit_price"].isna() | (sales["unit_price"] < 0)
)

for idx in sales.index[invalid_price]:
    add_issue(
        sales.loc[idx, "order_id"],
        "unit_price",
        "Invalid price",
        "Unit price must not be negative."
    )

# 7. Check inconsistent region formatting
normalized_regions = sales["region"].astype("string").str.strip().str.title()

for idx in sales.index[
    sales["region"].notna()
    & (sales["region"] != normalized_regions)
]:
    add_issue(
        sales.loc[idx, "order_id"],
        "region",
        "Inconsistent formatting",
        "Region has inconsistent capitalization or whitespace."
    )

# 8. Check customer IDs against the customer master table
known_customers = set(customers["customer_id"].dropna())

unmatched_customers = (
    sales["customer_id"].notna()
    & ~sales["customer_id"].isin(known_customers)
)

for idx in sales.index[unmatched_customers]:
    add_issue(
        sales.loc[idx, "order_id"],
        "customer_id",
        "Unmatched customer",
        "Customer ID does not exist in the customer master table."
    )

# Export detailed issue report
issue_report = pd.DataFrame(
    issues,
    columns=["order_id", "column", "issue_type", "details"]
)

issue_report.to_csv(
    REPORT_DIR / "data_quality_issues.csv",
    index=False
)

# Create a summary report
if not issue_report.empty:
    summary = (
        issue_report.groupby("issue_type")
        .size()
        .reset_index(name="issue_count")
    )
else:
    summary = pd.DataFrame(
        columns=["issue_type", "issue_count"]
    )

summary.to_csv(
    REPORT_DIR / "data_quality_summary.csv",
    index=False
)

# Create a review copy with region formatting standardized
cleaned_sales = sales.copy()
cleaned_sales["region"] = normalized_regions

cleaned_sales.to_csv(
    REPORT_DIR / "sales_review_copy.csv",
    index=False
)

print("\nData quality checks completed!")
print("\nIssues by type:")
print(summary.to_string(index=False))
print("\nTotal issue entries:", len(issue_report))
print("Reports saved in:", REPORT_DIR)
