# Automated Data Quality & MIS Reporting Pipeline

## Project Overview

The Automated Data Quality & MIS Reporting Pipeline is a data analytics project developed using Python, Pandas, SQL, and Tableau. The project aims to identify data quality issues, validate business records, reconcile related datasets, and automate the generation of Management Information System (MIS) reports.

The pipeline processes sales and customer data, detects inconsistencies, generates summary reports, and prepares business metrics for visualization.

## Objectives

- Identify duplicate records and order IDs.
- Detect missing values and invalid data.
- Validate quantities, prices, and transaction dates.
- Identify inconsistent formatting in categorical fields.
- Reconcile sales records with customer master data using SQL.
- Automate data quality and MIS report generation.
- Visualize data quality metrics using Tableau.

## Tools and Technologies

| Tool | Purpose |
|---|---|
| Python | Data processing and automation |
| Pandas | Data cleaning, validation, and reporting |
| SQLite | Database storage and SQL analysis |
| SQL | Aggregation, joins, and reconciliation |
| Tableau Desktop | Dashboard development |
| Excel / CSV | Report storage and data exchange |
| GitHub | Version control and project documentation |

## Project Structure

```text
Automated-Data-Quality-MIS/
│
├── data/
│   ├── sales.csv
│   ├── customers.csv
│   └── mis_database.db
│
├── scripts/
│   ├── data_quality_check.py
│   ├── sql_analysis.py
│   └── mis_report.py
│
├── sql/
│
├── reports/
│   ├── data_quality_issues.csv
│   ├── data_quality_summary.csv
│   ├── sales_review_copy.csv
│   ├── sql_revenue_summary.csv
│   ├── sql_duplicate_orders.csv
│   ├── sql_customer_reconciliation.csv
│   ├── sql_unmatched_customers.csv
│   ├── Automated_MIS_Report.xlsx
│   └── MIS_Executive_Summary.txt
│
├── tableau/
│   └── Tableau workbook and dashboard screenshots
│
└── README.md
```

*Note: The listed files should be included only if they have actually been created. Add your Tableau workbook to the `tableau` folder after saving it.*

## Dataset Description

The project uses sample sales and customer datasets.

### Sales Dataset

Contains transaction details such as:

- Order ID
- Customer ID
- Order date
- Product
- Quantity
- Unit price
- Region

### Customer Dataset

Contains customer identifiers and customer names. It acts as the customer master table for reconciliation.

The sample data includes intentionally introduced data quality issues for testing and demonstration purposes. It does not contain real customer information.

## Implementation

### 1. Data Quality Validation

Python and Pandas are used to load the sales dataset and identify:

- Duplicate rows
- Duplicate order IDs
- Missing values
- Invalid dates
- Invalid quantities
- Negative prices
- Inconsistent region formatting
- Customer IDs that do not match the customer master table

The detected issues are exported to CSV reports for further analysis.

### 2. SQL Analysis and Reconciliation

SQLite is used to store the sales and customer tables. SQL queries are executed to:

- Calculate preliminary sales revenue.
- Identify duplicate order IDs.
- Join sales data with customer records.
- Identify unmatched customer IDs.
- Export query results for reporting.

### 3. Automated MIS Reporting

Python and Pandas consolidate the outputs into an Excel workbook containing separate worksheets for data quality issues, summary metrics, revenue, duplicates, and customer reconciliation.

A text-based executive summary is also generated automatically.

### 4. Tableau Dashboard

Tableau Desktop is used to visualize data quality metrics and business reporting results.

Planned dashboard components include:

- Total data quality issue entries
- Issues by category
- Revenue summary
- Duplicate order details
- Unmatched customer records

Dashboard metrics should be validated against the generated reports before being presented as final business results.

## How to Run the Project

### Prerequisites

- Python 3
- Pandas
- OpenPyXL
- Tableau Desktop (for dashboard development)

SQLite support is included with Python's standard library.

### Install Dependencies

Open a terminal in the project folder and run:

```bash
python -m pip install pandas openpyxl
```

### Run the Pipeline

Execute the scripts in this order:

```bash
python scripts/data_quality_check.py
python scripts/sql_analysis.py
python scripts/mis_report.py
```

The generated reports will be saved in the `reports` directory.

If you run commands from inside the `scripts` directory, use the filenames without the `scripts/` prefix.

## Key Learning Outcomes

- Practical data validation and data quality monitoring
- Data manipulation using Pandas
- SQL queries, aggregation, and joins
- Reconciliation between related datasets
- Automated report generation
- Business intelligence and Tableau visualization
- Project organization and technical documentation

## Limitations and Future Enhancements

- Add automated scheduling for daily or weekly report generation.
- Implement more comprehensive validation rules.
- Add data quality scorecards and trend analysis.
- Improve revenue reconciliation by excluding duplicate transactions and resolving invalid records.
- Expand the Tableau dashboard with regional and product-level sales analysis.
- Add automated logging, error handling, and validation tests.

## Disclaimer

This project uses synthetic sample data for educational and portfolio purposes. Revenue figures are preliminary until duplicate transactions and other data quality issues have been fully reconciled.

## Author

**Your Name**

Data Analytics | Python | SQL | Tableau