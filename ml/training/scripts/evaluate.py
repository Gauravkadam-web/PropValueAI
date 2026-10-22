"""
Model Evaluation Script for PropValueAI.

Loads the fitted model.joblib artifact and metadata.json, evaluates predictions
against a supplied CSV dataset, and reports MAE, RMSE, and R2 metrics.

Usage:
    python evaluate.py [--model-path PATH] [--data-path PATH]
"""

import argparse
import json
import os
import sys
import numpy as np
import pandas as pd
import joblib

from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score

# Ensure repository root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from ml.common.constants import TARGET_COLUMN, TARGET_UNIT


def evaluate_artifact(model_path: str, data_path: str, metadata_path: str = None):
    print("=" * 70)
    print("PROPVALUEAI MODEL ARTIFACT EVALUATION")
    print("=" * 70)

    if not os.path.exists(model_path):
        print(f"Error: Model artifact not found at '{model_path}'.", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(data_path):
        print(f"Error: Data file not found at '{data_path}'.", file=sys.stderr)
        sys.exit(1)

    print(f"Loading pipeline artifact: {model_path}")
    pipeline = joblib.load(model_path)

    if metadata_path and os.path.exists(metadata_path):
        with open(metadata_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
        print(f"Model Name:       {meta.get('model_name')}")
        print(f"Training Date:    {meta.get('phase')}")
        print(f"Target Variable:  {meta.get('target_variable')} ({meta.get('target_unit')})")

    print(f"Loading evaluation data:   {data_path}")
    df = pd.read_csv(data_path)

    if TARGET_COLUMN not in df.columns:
        print(f"Error: Target column '{TARGET_COLUMN}' not found in '{data_path}'.", file=sys.stderr)
        sys.exit(1)

    X = df[["total_sqft", "size", "bath", "balcony", "area_type"]]
    y = df[TARGET_COLUMN]

    print(f"Evaluating {len(df):,} records...")
    y_pred = pipeline.predict(X)

    # Filter out NaNs if any target values were missing
    valid_mask = y.notna() & np.isfinite(y_pred)
    y_clean = y[valid_mask]
    y_pred_clean = y_pred[valid_mask]

    mae = mean_absolute_error(y_clean, y_pred_clean)
    rmse = root_mean_squared_error(y_clean, y_pred_clean)
    r2 = r2_score(y_clean, y_pred_clean)

    print("\nEVALUATION METRICS:")
    print(f"  - Mean Absolute Error (MAE): {mae:.2f} {TARGET_UNIT}")
    print(f"  - Root Mean Squared Error (RMSE): {rmse:.2f} {TARGET_UNIT}")
    print(f"  - Coefficient of Determination (R²): {r2:.4f}")
    print("=" * 70)
    print("EVALUATION COMPLETE")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="Evaluate a saved model.joblib artifact.")
    parser.add_argument(
        "--model-path",
        default="ml/inference/artifacts/model.joblib",
        help="Path to saved model.joblib artifact"
    )
    parser.add_argument(
        "--data-path",
        default="ml/training/data/raw/Pune_House_Data.csv",
        help="Path to evaluation CSV dataset"
    )
    parser.add_argument(
        "--metadata-path",
        default="ml/inference/artifacts/metadata.json",
        help="Path to metadata.json"
    )
    args = parser.parse_args()
    evaluate_artifact(args.model_path, args.data_path, args.metadata_path)


if __name__ == "__main__":
    main()
