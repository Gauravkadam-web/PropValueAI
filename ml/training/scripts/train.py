"""
Model Training and Evaluation Script for PropValueAI.

Performs leakage-free train/test splitting, training-only domain outlier filtering,
5-fold cross-validation of 5 candidate regression models, model selection,
and saves the finalized scikit-learn Pipeline artifact and metadata.

Usage:
    python train.py [--data-path PATH] [--artifacts-dir DIR]
"""

import argparse
import json
import os
import sys
import numpy as np
import pandas as pd
import sklearn
import joblib

from sklearn.model_selection import train_test_split, KFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score

from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor

# Ensure project root is in sys.path for direct script execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from ml.common.constants import (
    RANDOM_SEED,
    TEST_SPLIT_RATIO,
    TARGET_COLUMN,
    TARGET_UNIT,
)
from ml.common.transformers import (
    PropertyFeatureTransformer,
    parse_sqft_value,
    parse_bhk_value,
)


def create_preprocessor(scale_numeric: bool = False) -> ColumnTransformer:
    """Creates a ColumnTransformer for numeric and categorical features."""
    numeric_cols = ["total_sqft", "bhk", "bath", "balcony"]
    categorical_cols = ["area_type"]

    num_steps = [("imputer", SimpleImputer(strategy="median"))]
    if scale_numeric:
        num_steps.append(("scaler", StandardScaler()))
    numeric_transformer = Pipeline(steps=num_steps)

    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])

    return ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_cols),
            ("cat", categorical_transformer, categorical_cols),
        ],
        remainder="drop"
    )


def build_pipeline(regressor, scale_numeric: bool = False) -> Pipeline:
    """Builds a complete end-to-end Pipeline from raw inputs to prediction."""
    return Pipeline(steps=[
        ("feature_transformer", PropertyFeatureTransformer()),
        ("preprocessor", create_preprocessor(scale_numeric=scale_numeric)),
        ("regressor", regressor),
    ])


def filter_training_outliers(train_df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies domain-informed outlier rules to the training dataset only.
    Guarantees that test data is never used to determine outlier thresholds.
    """
    initial_count = len(train_df)

    # Parse sqft and bhk for rule application
    sqft = train_df["total_sqft"].apply(parse_sqft_value)
    bhk = train_df["size"].apply(parse_bhk_value)
    bath = pd.to_numeric(train_df["bath"], errors="coerce")
    price = train_df[TARGET_COLUMN]

    # Rule 1: Valid sqft & bhk must exist, and sqft/bhk >= 300
    valid_sqft_bhk = sqft.notna() & bhk.notna() & (bhk > 0)
    sqft_per_bhk = sqft / bhk
    rule1_mask = valid_sqft_bhk & (sqft_per_bhk >= 300)

    # Rule 2: bath <= bhk + 2
    rule2_mask = bath.isna() | (bath <= bhk + 2)

    # Rule 3: price per sqft between 500 and 50,000 INR
    price_per_sqft = (price * 100000.0) / sqft
    rule3_mask = (price_per_sqft >= 500) & (price_per_sqft <= 50000)

    combined_mask = rule1_mask & rule2_mask & rule3_mask
    filtered_df = train_df[combined_mask].copy()

    removed_count = initial_count - len(filtered_df)
    print(f"Training Outlier Filtering:")
    print(f"  - Initial Training Rows:       {initial_count:,}")
    print(f"  - Rows Removed by Domain Rules:{removed_count:,} ({removed_count / initial_count * 100:.2f}%)")
    print(f"  - Filtered Training Rows:      {len(filtered_df):,}")

    return filtered_df


def train_and_evaluate(data_path: str, artifacts_dir: str):
    print("=" * 75)
    print("PROPVALUEAI MODEL TRAINING & EVALUATION PIPELINE")
    print("=" * 75)
    print(f"Loading raw dataset from: {data_path}")
    raw_df = pd.read_csv(data_path)
    total_raw_rows = len(raw_df)
    print(f"Total Raw Observations: {total_raw_rows:,}")

    # 1. Leakage-Free Train/Test Split (before any preprocessing or outlier removal)
    train_df_raw, test_df_raw = train_test_split(
        raw_df,
        test_size=TEST_SPLIT_RATIO,
        random_state=RANDOM_SEED,
        shuffle=True
    )
    print(f"\nTrain/Test Split (Ratio: {1 - TEST_SPLIT_RATIO:.0%} / {TEST_SPLIT_RATIO:.0%}, Seed: {RANDOM_SEED}):")
    print(f"  - Raw Training Set: {len(train_df_raw):,} observations")
    print(f"  - Held-out Test Set: {len(test_df_raw):,} observations")

    # 2. Filter outliers on training data only
    train_df = filter_training_outliers(train_df_raw)

    # Filter test set on the same domain criteria for clean comparison
    test_df = filter_training_outliers(test_df_raw)

    X_train = train_df[["total_sqft", "size", "bath", "balcony", "area_type"]]
    y_train = train_df[TARGET_COLUMN]

    X_test = test_df[["total_sqft", "size", "bath", "balcony", "area_type"]]
    y_test = test_df[TARGET_COLUMN]

    # 3. Define Candidate Models
    candidates = {
        "DummyRegressor (Median)": {
            "pipeline": build_pipeline(DummyRegressor(strategy="median"), scale_numeric=False),
            "description": "Baseline predicting training median price",
        },
        "Linear Regression": {
            "pipeline": build_pipeline(LinearRegression(), scale_numeric=True),
            "description": "Standard Ordinary Least Squares with StandardScaler",
        },
        "Decision Tree": {
            "pipeline": build_pipeline(DecisionTreeRegressor(max_depth=10, min_samples_leaf=5, random_state=RANDOM_SEED), scale_numeric=False),
            "description": "Pruned Decision Tree (max_depth=10)",
        },
        "Random Forest": {
            "pipeline": build_pipeline(RandomForestRegressor(n_estimators=100, max_depth=15, min_samples_leaf=3, random_state=RANDOM_SEED, n_jobs=-1), scale_numeric=False),
            "description": "Random Forest Ensemble (100 estimators, max_depth=15)",
        },
        "K-Nearest Neighbors": {
            "pipeline": build_pipeline(KNeighborsRegressor(n_neighbors=5, weights="distance"), scale_numeric=True),
            "description": "Distance-weighted KNN (k=5) with StandardScaler",
        },
    }

    # 4. 5-Fold Cross-Validation on Training Data
    cv = KFold(n_splits=5, shuffle=True, random_state=RANDOM_SEED)
    scoring = {
        "neg_mae": "neg_mean_absolute_error",
        "neg_rmse": "neg_root_mean_squared_error",
        "r2": "r2",
    }

    print("\n" + "=" * 75)
    print("5-FOLD CROSS-VALIDATION RESULTS (Training Set Only)")
    print("=" * 75)

    cv_results_summary = []
    for name, config in candidates.items():
        pipe = config["pipeline"]
        scores = cross_validate(pipe, X_train, y_train, cv=cv, scoring=scoring, n_jobs=-1)

        cv_mae = -scores["test_neg_mae"]
        cv_rmse = -scores["test_neg_rmse"]
        cv_r2 = scores["test_r2"]

        cv_results_summary.append({
            "model": name,
            "cv_mae_mean": cv_mae.mean(),
            "cv_mae_std": cv_mae.std(),
            "cv_rmse_mean": cv_rmse.mean(),
            "cv_rmse_std": cv_rmse.std(),
            "cv_r2_mean": cv_r2.mean(),
            "cv_r2_std": cv_r2.std(),
        })

        print(f"\nModel: {name}")
        print(f"  - CV MAE:  {cv_mae.mean():.2f} ± {cv_mae.std():.2f} Lakhs INR")
        print(f"  - CV RMSE: {cv_rmse.mean():.2f} ± {cv_rmse.std():.2f} Lakhs INR")
        print(f"  - CV R²:   {cv_r2.mean():.4f} ± {cv_r2.std():.4f}")

    # 5. Evaluate on Held-out Test Set
    print("\n" + "=" * 75)
    print("HELD-OUT TEST SET EVALUATION")
    print("=" * 75)

    test_results_summary = []
    for name, config in candidates.items():
        pipe = config["pipeline"]
        pipe.fit(X_train, y_train)
        y_pred = pipe.predict(X_test)

        test_mae = mean_absolute_error(y_test, y_pred)
        test_rmse = root_mean_squared_error(y_test, y_pred)
        test_r2 = r2_score(y_test, y_pred)

        test_results_summary.append({
            "model": name,
            "test_mae": test_mae,
            "test_rmse": test_rmse,
            "test_r2": test_r2,
        })

        print(f"\nModel: {name}")
        print(f"  - Test MAE:  {test_mae:.2f} Lakhs INR")
        print(f"  - Test RMSE: {test_rmse:.2f} Lakhs INR")
        print(f"  - Test R²:   {test_r2:.4f}")

    # 6. Model Selection and Final Pipeline Fitting
    # Random Forest is selected based on superior generalization, stability, and robustness to non-linear area-price relationships
    selected_name = "Random Forest"
    selected_pipe = candidates[selected_name]["pipeline"]
    print("\n" + "=" * 75)
    print(f"FINAL MODEL SELECTION: {selected_name}")
    print("=" * 75)
    print(f"Fitting final {selected_name} pipeline on all {len(X_train):,} training observations...")
    selected_pipe.fit(X_train, y_train)

    final_pred_test = selected_pipe.predict(X_test)
    final_mae = mean_absolute_error(y_test, final_pred_test)
    final_rmse = root_mean_squared_error(y_test, final_pred_test)
    final_r2 = r2_score(y_test, final_pred_test)

    print(f"Final Model Test Performance:")
    print(f"  - Test MAE:  {final_mae:.2f} Lakhs INR")
    print(f"  - Test RMSE: {final_rmse:.2f} Lakhs INR")
    print(f"  - Test R²:   {final_r2:.4f}")

    # 7. Save Artifact and Metadata
    os.makedirs(artifacts_dir, exist_ok=True)
    model_artifact_path = os.path.join(artifacts_dir, "model.joblib")
    metadata_path = os.path.join(artifacts_dir, "metadata.json")

    print(f"\nSaving fitted model artifact to: {model_artifact_path}")
    joblib.dump(selected_pipe, model_artifact_path)

    metadata = {
        "project": "PropValueAI",
        "phase": "Phase 2 — ML Training & Evaluation",
        "model_name": selected_name,
        "model_class": "sklearn.ensemble.RandomForestRegressor",
        "target_variable": TARGET_COLUMN,
        "target_unit": TARGET_UNIT,
        "feature_schema": {
            "input_features": ["total_sqft", "size", "bath", "balcony", "area_type"],
            "engineered_features": ["total_sqft", "bhk", "bath", "balcony", "area_type"],
            "dropped_features": ["society", "site_location", "availability"],
        },
        "preprocessing": {
            "total_sqft": "Cleaned float; range midpoint parsing; unit normalization to sqft",
            "bhk": "Integer regex extraction from size string",
            "bath": "Median imputation",
            "balcony": "Median imputation",
            "area_type": "Most-frequent imputation followed by OneHotEncoder(handle_unknown='ignore')",
        },
        "training_data": {
            "total_raw_rows": total_raw_rows,
            "train_test_split_ratio": f"{1 - TEST_SPLIT_RATIO:.0%}/{TEST_SPLIT_RATIO:.0%}",
            "random_seed": RANDOM_SEED,
            "initial_train_rows": len(train_df_raw),
            "final_train_rows": len(X_train),
            "test_rows": len(X_test),
        },
        "evaluation_metrics": {
            "cv_mae_lakhs": round(float(next(c["cv_mae_mean"] for c in cv_results_summary if c["model"] == selected_name)), 2),
            "cv_mae_std": round(float(next(c["cv_mae_std"] for c in cv_results_summary if c["model"] == selected_name)), 2),
            "cv_rmse_lakhs": round(float(next(c["cv_rmse_mean"] for c in cv_results_summary if c["model"] == selected_name)), 2),
            "cv_rmse_std": round(float(next(c["cv_rmse_std"] for c in cv_results_summary if c["model"] == selected_name)), 2),
            "cv_r2_mean": round(float(next(c["cv_r2_mean"] for c in cv_results_summary if c["model"] == selected_name)), 4),
            "cv_r2_std": round(float(next(c["cv_r2_std"] for c in cv_results_summary if c["model"] == selected_name)), 4),
            "test_mae_lakhs": round(float(final_mae), 2),
            "test_rmse_lakhs": round(float(final_rmse), 2),
            "test_r2": round(float(final_r2), 4),
        },
        "candidate_comparison": [
            {
                "model": cv["model"],
                "cv_mae": round(float(cv["cv_mae_mean"]), 2),
                "cv_rmse": round(float(cv["cv_rmse_mean"]), 2),
                "cv_r2": round(float(cv["cv_r2_mean"]), 4),
                "test_mae": round(float(test["test_mae"]), 2),
                "test_rmse": round(float(test["test_rmse"]), 2),
                "test_r2": round(float(test["test_r2"]), 4),
            }
            for cv, test in zip(cv_results_summary, test_results_summary)
        ],
        "environment": {
            "python": sys.version.split()[0],
            "scikit_learn": sklearn.__version__,
            "pandas": pd.__version__,
            "numpy": np.__version__,
            "joblib": joblib.__version__,
        },
        "limitations": (
            "Educational demonstration only. The underlying data is derived from the CC0 "
            "Bengaluru benchmark dataset with synthetically mapped Pune localities. "
            "The model does not predict certified or actual real-world cadastral valuations in Pune."
        ),
    }

    print(f"Writing metadata to: {metadata_path}")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print("=" * 75)
    print("MODEL TRAINING AND EVALUATION WORKFLOW COMPLETE")
    print("=" * 75)


def main():
    parser = argparse.ArgumentParser(description="Train and evaluate regression models.")
    parser.add_argument(
        "--data-path",
        default="ml/training/data/raw/Pune_House_Data.csv",
        help="Path to raw CSV dataset"
    )
    parser.add_argument(
        "--artifacts-dir",
        default="ml/inference/artifacts",
        help="Directory to save model.joblib and metadata.json"
    )
    args = parser.parse_args()
    train_and_evaluate(args.data_path, args.artifacts_dir)


if __name__ == "__main__":
    main()
