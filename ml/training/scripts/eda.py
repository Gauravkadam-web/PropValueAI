"""
Exploratory Data Analysis (EDA) Script for PropValueAI.

This script performs exploratory data analysis on the raw real estate dataset,
computes summary tables, audits anomalies/outliers, and saves diagnostic plots
to an ignored experiment directory.

Usage:
    python eda.py [--data-path PATH] [--output-dir DIR]
"""

import argparse
import os
import re
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt


def parse_total_sqft(val):
    """Parses total_sqft string into (float_val, category_type)."""
    if pd.isna(val):
        return np.nan, "missing"
    val = str(val).strip()

    # Pure numeric
    try:
        return float(val), "numeric"
    except ValueError:
        pass

    # Range pattern: e.g. "2100 - 2850"
    if "-" in val:
        tokens = val.split("-")
        if len(tokens) == 2:
            try:
                low = float(tokens[0].strip())
                high = float(tokens[1].strip())
                return (low + high) / 2.0, "range"
            except ValueError:
                return np.nan, "invalid_range"

    # Known alternative units conversion to sqft
    val_lower = val.lower()
    unit_conversions = {
        "sq. meter": 10.7639,
        "sq. meters": 10.7639,
        "sq. yard": 9.0,
        "sq. yards": 9.0,
        "acres": 43560.0,
        "acre": 43560.0,
        "guntha": 1089.0,
        "perch": 272.25,
        "cents": 435.6,
    }
    for unit, factor in unit_conversions.items():
        if unit in val_lower:
            num_part = re.sub(r"[^\d.]", "", val_lower)
            try:
                return float(num_part) * factor, f"unit_{unit.replace(' ', '_')}"
            except ValueError:
                return np.nan, "invalid_unit"

    return np.nan, "unrecognized_string"


def parse_bhk(val):
    """Extracts integer bedroom count from size string."""
    if pd.isna(val):
        return np.nan
    match = re.search(r"(\d+)", str(val))
    if match:
        return int(match.group(1))
    return np.nan


def run_eda(data_path: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    plots_dir = os.path.join(output_dir, "plots")
    os.makedirs(plots_dir, exist_ok=True)

    print(f"Loading raw data from: {data_path}")
    df = pd.read_csv(data_path)
    total_rows, total_cols = df.shape

    print("=" * 70)
    print("EXPLORATORY DATA ANALYSIS (EDA)")
    print("=" * 70)
    print(f"Dataset Shape: {total_rows:,} rows, {total_cols} columns")

    # 1. Target Variable: price
    prices = df["price"]
    print("\n--- Target Variable: price (in Lakhs INR) ---")
    print(f"Count:         {prices.count():,}")
    print(f"Mean:          {prices.mean():.2f} Lakhs")
    print(f"Std Dev:       {prices.std():.2f} Lakhs")
    print(f"Median:        {prices.median():.2f} Lakhs")
    print(f"Min:           {prices.min():.2f} Lakhs")
    print(f"25th Pct:      {prices.quantile(0.25):.2f} Lakhs")
    print(f"75th Pct:      {prices.quantile(0.75):.2f} Lakhs")
    print(f"90th Pct:      {prices.quantile(0.90):.2f} Lakhs")
    print(f"95th Pct:      {prices.quantile(0.95):.2f} Lakhs")
    print(f"99th Pct:      {prices.quantile(0.99):.2f} Lakhs")
    print(f"Max:           {prices.max():.2f} Lakhs")
    print(f"Skewness:      {prices.skew():.2f}")
    print(f"Kurtosis:      {prices.kurtosis():.2f}")

    # Plot Price Distribution
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    ax[0].hist(prices, bins=50, color="steelblue", edgecolor="black")
    ax[0].set_title("Price Distribution (Linear Scale)")
    ax[0].set_xlabel("Price (Lakhs INR)")
    ax[0].set_ylabel("Frequency")

    ax[1].hist(np.log1p(prices), bins=50, color="teal", edgecolor="black")
    ax[1].set_title("Log(1 + Price) Distribution")
    ax[1].set_xlabel("Log(1 + Price)")
    ax[1].set_ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "price_distribution.png"), dpi=150)
    plt.close()

    # 2. Parsing total_sqft
    parsed_results = [parse_total_sqft(v) for v in df["total_sqft"]]
    sqft_values = [p[0] for p in parsed_results]
    sqft_types = [p[1] for p in parsed_results]
    df["clean_sqft"] = sqft_values
    df["sqft_format"] = sqft_types

    print("\n--- total_sqft Formats Breakdown ---")
    format_counts = df["sqft_format"].value_counts()
    for fmt, cnt in format_counts.items():
        print(f"  - {fmt:25s}: {cnt:,} ({cnt / total_rows * 100:.2f}%)")

    # 3. Parsing size -> bhk
    df["bhk"] = df["size"].apply(parse_bhk)
    print("\n--- BHK Distribution ---")
    bhk_counts = df["bhk"].value_counts(dropna=False).sort_index()
    for bhk_val, cnt in bhk_counts.items():
        label = f"{int(bhk_val)} BHK" if pd.notna(bhk_val) else "Missing (NaN)"
        print(f"  - {label:15s}: {cnt:,} ({cnt / total_rows * 100:.2f}%)")

    # 4. Bathrooms and Balconies
    print("\n--- Bathrooms Distribution ---")
    bath_counts = df["bath"].value_counts(dropna=False).sort_index()
    for b_val, cnt in bath_counts.items():
        label = f"{b_val} Baths" if pd.notna(b_val) else "Missing (NaN)"
        print(f"  - {label:15s}: {cnt:,} ({cnt / total_rows * 100:.2f}%)")

    # 5. Outlier Auditing
    print("\n--- Outlier and Anomaly Diagnostics ---")
    # Implausible sqft per bedroom (< 300 sqft/bhk)
    valid_sqft_bhk = df["clean_sqft"].notna() & df["bhk"].notna() & (df["bhk"] > 0)
    df["sqft_per_bhk"] = np.nan
    df.loc[valid_sqft_bhk, "sqft_per_bhk"] = df.loc[valid_sqft_bhk, "clean_sqft"] / df.loc[valid_sqft_bhk, "bhk"]

    low_sqft_per_bhk = df[df["sqft_per_bhk"] < 300]
    print(f"Properties with < 300 sqft/BHK:         {len(low_sqft_per_bhk):,} ({len(low_sqft_per_bhk) / total_rows * 100:.2f}%)")

    # Bathrooms > BHK + 2
    valid_bath_bhk = df["bath"].notna() & df["bhk"].notna()
    excess_bath = df[valid_bath_bhk & (df["bath"] > df["bhk"] + 2)]
    print(f"Properties with bath > BHK + 2:         {len(excess_bath):,} ({len(excess_bath) / total_rows * 100:.2f}%)")

    # Extreme prices / area
    extreme_price = df[df["price"] > 1000]
    print(f"Properties with price > 1,000 Lakhs:     {len(extreme_price):,} ({len(extreme_price) / total_rows * 100:.2f}%)")

    # 6. Area Type vs Price
    print("\n--- Area Type vs Median Price ---")
    area_type_stats = df.groupby("area_type")["price"].agg(["count", "mean", "median", "std"]).round(2)
    print(area_type_stats.to_string())

    # Plot Price by Area Type
    fig, ax = plt.subplots(figsize=(8, 5))
    area_types = df["area_type"].unique()
    area_data = [df[df["area_type"] == at]["price"].dropna() for at in area_types]
    ax.boxplot(area_data, tick_labels=area_types, showfliers=False)
    ax.set_title("Price Distribution by Area Type (Outliers Hidden)")
    ax.set_ylabel("Price (Lakhs INR)")
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "price_by_area_type.png"), dpi=150)
    plt.close()

    # Plot Price vs Clean Sqft
    fig, ax = plt.subplots(figsize=(8, 5))
    clean_subset = df[df["clean_sqft"].notna() & (df["clean_sqft"] < 5000) & (df["price"] < 500)]
    ax.scatter(clean_subset["clean_sqft"], clean_subset["price"], alpha=0.3, color="navy", s=15)
    ax.set_title("Price vs Total Sqft (Area < 5000 sqft, Price < 500 Lakhs)")
    ax.set_xlabel("Total Sqft")
    ax.set_ylabel("Price (Lakhs INR)")
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "price_vs_sqft.png"), dpi=150)
    plt.close()

    # Plot Price by BHK
    fig, ax = plt.subplots(figsize=(10, 5))
    bhk_subset = df[df["bhk"].isin([1, 2, 3, 4, 5, 6])]
    bhk_groups = [bhk_subset[bhk_subset["bhk"] == b]["price"].dropna() for b in [1, 2, 3, 4, 5, 6]]
    ax.boxplot(bhk_groups, tick_labels=[f"{b} BHK" for b in [1, 2, 3, 4, 5, 6]], showfliers=False)
    ax.set_title("Price Distribution by Bedroom Count (1-6 BHK, Outliers Hidden)")
    ax.set_ylabel("Price (Lakhs INR)")
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "price_by_bhk.png"), dpi=150)
    plt.close()

    print(f"\nAll plots saved to: {plots_dir}")
    print("=" * 70)
    print("EDA EXECUTION COMPLETE")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="Run Exploratory Data Analysis.")
    parser.add_argument(
        "--data-path",
        default="ml/training/data/raw/Pune_House_Data.csv",
        help="Path to raw CSV dataset"
    )
    parser.add_argument(
        "--output-dir",
        default="ml/training/experiments",
        help="Directory to save EDA outputs and plots"
    )
    args = parser.parse_args()
    run_eda(args.data_path, args.output_dir)


if __name__ == "__main__":
    main()
