from pathlib import Path
import json
import pandas as pd
from ucimlrepo import fetch_ucirepo

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
CLEAN_DIR = ROOT / "data" / "cleaned"
REPORT_DIR = ROOT / "reports"

RAW_DIR.mkdir(parents=True, exist_ok=True)
CLEAN_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def load_dataset():
    """Fetch the official UCI Bank Marketing dataset (ID 222)."""
    dataset = fetch_ucirepo(id=222)
    features = dataset.data.features.copy()
    target = dataset.data.targets.copy()
    target.columns = ["y"]
    df = pd.concat([features, target], axis=1)
    # Save a reproducible raw snapshot before changing anything.
    df.to_csv(RAW_DIR / "bank_marketing_raw.csv", index=False)
    return df

def clean_dataset(df):
    original_rows = len(df)
    original_columns = len(df.columns)
    missing_before = int(df.isna().sum().sum())
    duplicate_rows = int(df.duplicated().sum())

    # Normalize text: trim whitespace and standardize case.
    text_cols = df.select_dtypes(include=["object", "string"]).columns
    for col in text_cols:
        df[col] = df[col].astype("string").str.strip().str.lower()

    # UCI documents 'unknown' as a valid code for unavailable categorical data.
    # Keep it as an explicit category instead of silently deleting information.
    # Actual blank/NA values are handled separately below.
    categorical_cols = [
        "job", "marital", "education", "default", "housing",
        "loan", "contact", "month", "poutcome", "y"
    ]
    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].replace({"": pd.NA, "nan": pd.NA, "none": pd.NA})

    numeric_cols = [
        "age", "balance", "day", "duration", "campaign",
        "pdays", "previous"
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Remove exact duplicate records.
    df = df.drop_duplicates().copy()

    # Validate impossible values; set them to missing rather than inventing values.
    if "age" in df.columns:
        df.loc[~df["age"].between(18, 100), "age"] = pd.NA
    if "day" in df.columns:
        df.loc[~df["day"].between(1, 31), "day"] = pd.NA
    for col in ["duration", "previous"]:
        if col in df.columns:
            df.loc[df[col] < 0, col] = pd.NA
    if "campaign" in df.columns:
        df.loc[df["campaign"] < 1, "campaign"] = pd.NA

    # Fill true missing categorical values with an explicit label.
    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].fillna("unknown")

    # Numeric missing values use the median; retain integer-like columns as nullable integers.
    for col in numeric_cols:
        if col in df.columns and df[col].isna().any():
            median_value = df[col].median()
            df[col] = df[col].fillna(median_value)

    integer_cols = ["age", "balance", "day", "duration", "campaign", "pdays", "previous"]
    for col in integer_cols:
        if col in df.columns:
            df[col] = df[col].round().astype("int64")

    # Keep pdays == -1: UCI defines -1 as "not previously contacted", not an error.
    # Standardize category values without changing their meaning.
    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.lower()

    # Consistent column order and stable row numbering.
    df = df.reset_index(drop=True)
    final_missing = int(df.isna().sum().sum())

    report = {
        "dataset": "UCI Bank Marketing (ID 222)",
        "rows_before": original_rows,
        "rows_after": len(df),
        "columns": original_columns,
        "duplicate_rows_removed": duplicate_rows,
        "missing_cells_before": missing_before,
        "missing_cells_after": final_missing,
        "cleaning_actions": [
            "Standardized text by trimming whitespace and converting to lowercase",
            "Converted numeric fields to numeric data types",
            "Removed exact duplicate records",
            "Validated age, day, duration, campaign and previous-contact values",
            "Filled true missing categorical values with 'unknown'",
            "Filled true missing numeric values with the column median",
            "Preserved pdays = -1 because UCI defines it as not previously contacted",
            "Preserved documented 'unknown' categories as meaningful source codes"
        ]
    }
    return df, report

def main():
    print("Downloading official UCI Bank Marketing dataset...")
    raw = load_dataset()
    print(f"Raw dataset: {raw.shape[0]:,} rows x {raw.shape[1]} columns")

    cleaned, report = clean_dataset(raw)
    output_csv = CLEAN_DIR / "bank_marketing_cleaned.csv"
    cleaned.to_csv(output_csv, index=False)

    with open(REPORT_DIR / "cleaning_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)

    # Save a compact column-level quality report.
    quality = pd.DataFrame({
        "column": cleaned.columns,
        "data_type": [str(cleaned[c].dtype) for c in cleaned.columns],
        "missing_values": [int(cleaned[c].isna().sum()) for c in cleaned.columns],
        "unique_values": [int(cleaned[c].nunique(dropna=False)) for c in cleaned.columns]
    })
    quality.to_csv(REPORT_DIR / "data_quality_report.csv", index=False)

    print("\nCleaning completed.")
    print(f"Cleaned file: {output_csv}")
    print(f"Rows before: {report['rows_before']:,}")
    print(f"Rows after:  {report['rows_after']:,}")
    print(f"Duplicates removed: {report['duplicate_rows_removed']:,}")
    print(f"Missing cells after cleaning: {report['missing_cells_after']:,}")
    print("Reports saved in the reports/ folder.")

if __name__ == "__main__":
    main()
