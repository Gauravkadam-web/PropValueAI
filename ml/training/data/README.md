# ML Training Data Management

This directory manages datasets used for offline exploratory data analysis, feature engineering, and model training in the PropValueAI project.

## Directory Structure and Purposes

- **`raw/`**:
  Stores original, immutable source datasets exactly as retrieved from official or verified candidate sources. No manual editing, script-driven in-place modification, or deletion of raw files is permitted.
- **`processed/`**:
  Stores intermediate or final cleaned datasets produced by reproducible preprocessing scripts (e.g., encoded features, train/validation/test splits, imputed data). Every file in `processed/` must be reproducible by running a script from `ml/training/scripts/`.
- **`external/`**:
  Stores auxiliary reference datasets such as geographic metadata (pincodes, coordinates), city tier mappings, inflation indices, or external economic indicators.

## Dataset Storage and Versioning Conventions

1. **File Naming**: Use descriptive lowercase snake_case or canonical dataset names (e.g., `pune_house_data.csv`).
2. **Immutability of Raw Data**: Raw source files must never be modified or overwritten.
3. **Reproducibility**: Any transformation from `raw/` to `processed/` must be completely automated through code.
4. **Exclusion from Git**:
   - All dataset files inside `raw/`, `processed/`, and `external/` are explicitly excluded from Git version control via `.gitignore`.
   - Only `.gitkeep` files are tracked to preserve the directory tree.
   - Large binary or tabular data files must never be committed to GitHub to prevent repository bloat, accidental exposure of proprietary data, and Git performance degradation.

## Provenance and Licensing Requirements

Before placing any dataset in `raw/`, record:
- **Source URL**: Canonical download URL or repository source.
- **Acquisition Date**: Date and timestamp when the file was downloaded.
- **License / Terms of Use**: Permitted usage rights (e.g., MIT, CC-BY, Public Domain, educational only).
- **Target Variable Definition & Units**: Explicitly verify what the target column represents, including its currency (e.g., Lakhs INR) and whether it is a total price or price-per-unit.
- **Feature Units**: Document area measurement units (e.g., square feet, square meters, acres) and property classifications.
