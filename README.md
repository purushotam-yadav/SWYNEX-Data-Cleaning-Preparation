# SWYNEX – Data Cleaning & Preparation

## Project overview
This project cleans the public **UCI Bank Marketing** dataset. The data describes direct marketing campaigns conducted by a Portuguese banking institution. The target column `y` indicates whether a client subscribed to a term deposit.

**Dataset source:** UCI Machine Learning Repository – Bank Marketing (ID 222)  
**Citation:** Moro, S., Rita, P., & Cortez, P. (2014). *Bank Marketing*. UCI Machine Learning Repository. https://doi.org/10.24432/C5K306  
**License:** CC BY 4.0. Please retain attribution when redistributing the dataset.

## Repository structure
```text
SWYNEX-Data-Cleaning-Preparation/
├── data/
│   ├── raw/                 # Original downloaded dataset snapshot
│   └── cleaned/             # Final cleaned CSV
├── reports/
│   ├── cleaning_report.json
│   └── data_quality_report.csv
├── sql/
│   └── bank_marketing_schema.sql
├── src/
│   └── clean_data.py
├── requirements.txt
└── README.md
```

## How to run
1. Install Python 3.10 or newer.
2. Open this folder in VS Code.
3. Create and activate a virtual environment (optional but recommended).
4. Install packages:
   ```bash
   pip install -r requirements.txt
   ```
5. Run:
   ```bash
   python src/clean_data.py
   ```

The script downloads dataset ID 222 from UCI, saves an untouched raw snapshot, creates the cleaned CSV, and writes two quality reports.

## Data cleaning performed
- Checked missing cells and exact duplicate rows.
- Trimmed whitespace and standardized text to lowercase.
- Converted numeric columns to numeric types.
- Removed exact duplicate records.
- Validated `age`, `day`, `duration`, `campaign`, and `previous`.
- Filled actual missing categorical values with `unknown`.
- Filled actual missing numeric values with the column median.
- Kept documented `unknown` category values rather than treating them as accidental blanks.
- Preserved `pdays = -1`, because the UCI documentation defines it as “client was not previously contacted”.

## Important notes
- The source dataset uses semicolon-separated CSV files in its downloadable archive; this script uses the official UCI repository interface and returns structured columns.
- Do not claim that the dataset contains missing values or duplicates until you inspect the generated reports. The script records the actual counts.
- `default` is a reserved SQL keyword in some contexts, so the SQL table uses `default_status`. Rename the CSV header during import or map the column in MySQL Workbench.

## Tools used
Python, Pandas, UCI ML Repository, MySQL, Excel, GitHub.

## Excel review (optional)
Open `data/cleaned/bank_marketing_cleaned.csv` in Excel. Use filters to inspect `unknown` categories, sort numeric columns to review ranges, and use Remove Duplicates only on a copy. Keep the Python-generated cleaned CSV as the reproducible final output.

## Author
Add your name, course, and internship details here before submission.
