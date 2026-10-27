
from pathlib import Path
import pandas as pd
from datetime import datetime

# Locate project folders
PROJECT_DIR = Path(__file__).resolve().parent.parent
REPORT_DIR = PROJECT_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Define report inputs
files = {
    "Data Quality Issues": "data_quality_issues.csv",
    "Quality Summary": "data_quality_summary.csv",
    "Revenue Summary": "sql_revenue_summary.csv",
    "Duplicate Orders": "sql_duplicate_orders.csv",
    "Customer Reconciliation": "sql_customer_reconciliation.csv",
    "Unmatched Customers": "sql_unmatched_customers.csv",
}

# Read available reports
report_data = {}

for sheet_name, filename in files.items():
    file_path = REPORT_DIR / filename

    if file_path.exists():
        report_data[sheet_name] = pd.read_csv(file_path)
    else:
        print(f"Warning: {filename} not found. Skipping it.")

if not report_data:
    raise FileNotFoundError(
        "No input reports found. Run the data quality "
        "and SQL analysis scripts first."
    )

# Create a consolidated Excel workbook
output_file = REPORT_DIR / "Automated_MIS_Report.xlsx"

with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    for sheet_name, dataframe in report_data.items():
        dataframe.to_excel(
            writer,
            sheet_name=sheet_name[:31],
            index=False
        )

        # Format each worksheet
        worksheet = writer.sheets[sheet_name[:31]]
        worksheet.freeze_panes = "A2"
        worksheet.auto_filter.ref = worksheet.dimensions

        for column_cells in worksheet.columns:
            max_length = max(
                len(str(cell.value)) if cell.value is not None else 0
                for cell in column_cells
            )
            worksheet.column_dimensions[
                column_cells[0].column_letter
            ].width = min(max_length + 2, 40)

# Create a brief text summary
summary_file = REPORT_DIR / "MIS_Executive_Summary.txt"

quality_summary = report_data.get(
    "Quality Summary", pd.DataFrame()
)

revenue_summary = report_data.get(
    "Revenue Summary", pd.DataFrame()
)

with open(summary_file, "w", encoding="utf-8") as file:
    file.write("AUTOMATED MIS REPORT\n")
    file.write("=" * 35 + "\n")
    file.write(
        "Generated: "
        + datetime.now().strftime("%d-%m-%Y %H:%M")
        + "\n\n"
    )

    file.write("DATA QUALITY SUMMARY\n")
    file.write("-" * 25 + "\n")

    if not quality_summary.empty:
        file.write(quality_summary.to_string(index=False))
    else:
        file.write("No quality summary available.")

    file.write("\n\nREVENUE SUMMARY\n")
    file.write("-" * 25 + "\n")

    if not revenue_summary.empty:
        file.write(revenue_summary.to_string(index=False))
    else:
        file.write("No revenue summary available.")

print("\nMIS report generated successfully!")
print("Excel report:", output_file)
print("Executive summary:", summary_file)
