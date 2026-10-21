"""
Dataset Inspection Utility for PropValueAI.

This script performs read-only data profiling and basic quality checks on a supplied
local CSV dataset using pandas. It does not modify or overwrite the source dataset.

Usage:
    python inspect_dataset.py <path_to_csv>
"""

import argparse
import os
import sys
import pandas as pd


def inspect_dataset(csv_path: str) -> None:
    """Inspects a CSV file and prints a comprehensive data profile."""
    # 1. Path existence and read permissions validation
    if not os.path.exists(csv_path):
        print(f"Error: File not found at path '{csv_path}'.", file=sys.stderr)
        sys.exit(1)

    if not os.path.isfile(csv_path):
        print(f"Error: Specified path '{csv_path}' is not a regular file.", file=sys.stderr)
        sys.exit(1)

    if not os.access(csv_path, os.R_OK):
        print(f"Error: File at '{csv_path}' is not readable.", file=sys.stderr)
        sys.exit(1)

    file_size_bytes = os.path.getsize(csv_path)
    if file_size_bytes == 0:
        print(f"Error: File '{csv_path}' is empty (0 bytes).", file=sys.stderr)
        sys.exit(1)

    # 2. Loading the CSV with pandas
    try:
        df = pd.read_csv(csv_path)
    except pd.errors.EmptyDataError:
        print(f"Error: CSV file '{csv_path}' contains no data or headers.", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(f"Error: Failed to parse CSV file '{csv_path}': {exc}", file=sys.stderr)
        sys.exit(1)

    # 3. Basic Dataset Profile
    rows, cols = df.shape
    print("=" * 70)
    print("DATASET PROFILE REPORT")
    print("=" * 70)
    print(f"File Path:        {os.path.abspath(csv_path)}")
    print(f"File Size:        {file_size_bytes:,} bytes ({file_size_bytes / (1024 * 1024):.2f} MB)")
    print(f"Total Rows:       {rows:,}")
    print(f"Total Columns:    {cols}")
    print("-" * 70)

    # 4. Column Names, Data Types, and Missing Values
    print("\nCOLUMNS & MISSING VALUES:")
    missing_counts = df.isnull().sum()
    missing_pcts = (missing_counts / rows) * 100

    col_summary = pd.DataFrame({
        "Column": df.columns,
        "Dtype": df.dtypes.astype(str),
        "Non-Null Count": df.notnull().sum(),
        "Missing Count": missing_counts,
        "Missing Pct (%)": missing_pcts.round(2)
    })
    print(col_summary.to_string(index=False))

    # 5. Duplicate Rows
    duplicate_count = df.duplicated().sum()
    duplicate_pct = (duplicate_count / rows) * 100 if rows > 0 else 0.0
    print(f"\nDuplicate Rows:   {duplicate_count:,} ({duplicate_pct:.2f}%)")

    # 6. Sample Records (First 3 rows, truncated width)
    print("\nSAMPLE RECORDS (Top 3):")
    print(df.head(3).to_string())

    # 7. Descriptive Statistics for Numeric Columns
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    if numeric_cols:
        print("\n" + "=" * 70)
        print("NUMERIC COLUMNS SUMMARY (Descriptive Statistics):")
        print("=" * 70)
        desc = df[numeric_cols].describe().round(2)
        print(desc.to_string())
    else:
        print("\nNo numeric columns detected.")

    # 8. Categorical Columns Summary
    categorical_cols = df.select_dtypes(exclude=["number"]).columns.tolist()
    if categorical_cols:
        print("\n" + "=" * 70)
        print("CATEGORICAL COLUMNS SUMMARY:")
        print("=" * 70)
        for col in categorical_cols:
            n_unique = df[col].nunique(dropna=True)
            n_missing = df[col].isnull().sum()
            print(f"\nColumn: '{col}' | Unique values: {n_unique:,} | Missing: {n_missing:,}")
            # Show top 5 most frequent values
            top_vals = df[col].value_counts(dropna=True).head(5)
            if not top_vals.empty:
                print("  Top frequent values:")
                for val, cnt in top_vals.items():
                    pct = (cnt / rows) * 100
                    print(f"    - {str(val)!r}: {cnt:,} ({pct:.2f}%)")
    else:
        print("\nNo categorical columns detected.")

    print("\n" + "=" * 70)
    print("INSPECTION COMPLETE (Source dataset remains unchanged)")
    print("=" * 70)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Inspect and profile a local CSV dataset for PropValueAI."
    )
    parser.add_argument(
        "csv_path",
        type=str,
        help="Path to the local CSV file to inspect."
    )
    args = parser.parse_args()
    inspect_dataset(args.csv_path)


if __name__ == "__main__":
    main()
