# Antigravity IDE Prompt — Phase 1: Dataset Inspection & Validation
## Project: PropValueAI — Real Estate Price Prediction Using Python and ML

You are working on **PropValueAI**, a Real Estate Price Prediction project.

**Phase 0 (Project Foundation) is complete.** The repository already contains the project documentation, architecture, development roadmap, API contracts, `.gitignore`, and the predefined folder structure.

Your task is to implement **Phase 1 only: Dataset Inspection and Validation**.

Do not start Phase 2 or implement any application features.

---

## 1. First: Inspect the Existing Project

Before making changes:

1. Read these files:
   - `AGENTS.md`
   - `README.md`
   - `docs/architecture.md`
   - `docs/development-roadmap.md`
   - `docs/api-contracts.md`
   - `ml/README.md`

2. Inspect the existing directory structure and Git state.
3. Confirm the current branch, working-tree status, and latest commit.
4. Preserve the existing project structure and Phase 0 documentation.
5. Do not overwrite existing files without understanding their purpose.
6. Follow all rules defined in `AGENTS.md`.

The current repository/workspace name is **PropValueAI**. Do not rename the project or create a second project root.

## 2. Phase 1 Objective

Identify and validate a suitable real-estate dataset for building a house-price prediction model.

The dataset should ideally contain:

- Property location
- Property area and its unit
- Number of bedrooms or BHK
- Number of bathrooms, if available
- Property price or price per relevant unit
- Property type, if available
- Additional useful property features, if available

These are desired features, not assumptions about any dataset. Inspect the actual columns before deciding whether a dataset is suitable.

The initial preference is to investigate **Pune residential property data**, provided a suitable dataset with acceptable quality and usage terms can be found.

## 3. Candidate Datasets to Investigate

Start by investigating these candidate sources:

### Candidate A — Pune House Price Prediction

Repository:
https://github.com/Sahil9822/Pune-House-Price-Prediction

Inspect the repository, dataset files, README, available documentation, and any dataset provenance or licensing information.

### Candidate B — Pune House Data CSV

Candidate CSV:
https://raw.githubusercontent.com/prashantmane92/dataset/main/Pune_House_Data.csv

Verify that the URL is accessible, inspect the actual CSV, and identify its origin and usage terms where possible.

### Candidate C — Indian Urban House Price Prediction

Dataset page:
https://www.kaggle.com/competitions/indian-urban-house-price-prediction/data

Check whether the dataset is accessible and whether its geographic coverage, features, target variable, and usage terms fit this project.

If a source requires authentication or is inaccessible, record that limitation. Do not bypass access controls.

**Important:** These are unverified candidates. Do not assume that any candidate is reliable, licensed for our intended use, or suitable before inspecting it.

You may investigate other credible sources if the initial candidates are unsuitable, but document why an alternative is needed.

## 4. Dataset Download and Storage Rules

If a candidate dataset is accessible and its usage terms permit inspection:

- Download only the data needed for evaluation.
- Keep downloaded original datasets under the existing directory:

  `ml/training/data/raw/`

- Preserve original files without silently modifying or overwriting them.
- Record the source URL, download date, filename, format, and known license or usage restrictions.
- Do not upload raw datasets to GitHub.
- Do not commit large datasets, generated data, or proprietary/restricted data.
- Do not create synthetic data to fill gaps in a real dataset.
- Do not merge multiple datasets automatically.
- Do not assume that two datasets use the same currency, area unit, location convention, or price definition.

If a candidate cannot be downloaded, document the problem and continue inspecting other accessible candidates.

## 5. Required Data Quality Checks

For every accessible candidate, inspect and report the following.

### A. Basic Dataset Profile

- Dataset filename and source
- File format and file size, where available
- Number of rows and columns
- Column names and data types
- Sample records, with unnecessary personal or sensitive information excluded
- Target variable representing property price
- Geographic coverage
- Dataset provenance and license/usage terms, if verifiable

### B. Data Quality

Check for:

- Missing values by column
- Duplicate rows
- Invalid or inconsistent data types
- Unexpected categorical values
- Inconsistent location names
- Non-positive or implausible prices
- Non-positive or implausible property areas
- Inconsistent area units
- Inconsistent currency or price definitions
- Potential outliers requiring investigation
- Columns with little or no predictive value
- Potential data leakage

Do not automatically delete outliers or rows just because values look unusual. Report the findings and recommend an appropriate treatment for a later phase.

### C. Target Variable Assessment

Determine:

- Which column represents the target price
- Whether the target is total property price, price per square foot, or another measure
- Its data type and missing-value count
- Its observed range and distribution
- Whether the target is suitable for a regression problem
- Whether the available data supports a meaningful prediction scope

Do not assume that a column called `price` has a particular currency or unit without evidence.

### D. Feature Assessment

Identify:

- Numeric features
- Categorical features
- Location-related features
- Potentially useful property attributes
- Features with excessive missing values
- Features that may introduce leakage
- Features that cannot be used reliably at prediction time

Explain how each important finding affects future model development.

## 6. Dataset Comparison and Selection

Compare all accessible candidates using a consistent set of criteria:

| Criterion | What to evaluate |
|---|---|
| Geographic relevance | Suitability for the intended Pune-focused project |
| Target quality | Clear, meaningful property-price target |
| Feature quality | Useful property attributes |
| Data completeness | Missing-value severity |
| Data consistency | Price, area, location, and type consistency |
| Dataset size | Adequate usable observations |
| Provenance | Traceable original source |
| Usage rights | Clear permission for the intended use |
| Overall suitability | Suitability for a future regression model |

Recommend one primary dataset only if the evidence supports the decision.

If no candidate is sufficiently reliable, explain why and recommend the next investigation step instead of forcing a selection.

Do not combine datasets merely to increase row count. Any future merging decision must be justified by compatible schemas, units, targets, geography, provenance, and usage rights.

## 7. Deliverables

Create the following documentation under the existing `docs/` directory.

### `docs/dataset-evaluation.md`

Include:

- Objective and scope
- Candidate sources investigated
- Inspection methodology
- Dataset profiles
- Column and target analysis
- Data-quality findings
- Candidate comparison table
- Provenance and licensing findings
- Limitations and risks
- Recommended primary dataset, if justified
- Reasoning behind the recommendation
- Remaining questions and next steps

### `docs/dataset-validation-report.md`

Include:

- Exact dataset file(s) inspected
- Source and inspection date
- Row and column counts
- Column names and data types
- Missing-value summary
- Duplicate count
- Target variable and observed range
- Area and currency/unit findings
- Data-quality issues
- Validation checks performed and their outcomes
- Warnings and unresolved issues
- Overall validation status: Pass, Pass with Warnings, or Fail

Distinguish verified facts from assumptions and unresolved questions.

### `ml/training/data/README.md`

Document:

- Purpose of `raw/`, `processed/`, and `external/`
- Dataset storage conventions
- Raw-data preservation rules
- Dataset provenance requirements
- Why datasets should not be committed to Git by default
- How to record dataset source, license, and units

Create this file only if it does not already exist. Preserve existing content where applicable.

### `ml/training/scripts/inspect_dataset.py`

Create a small, reusable Python script for inspecting an explicitly supplied local CSV dataset.

Requirements:

- Accept the dataset path as a command-line argument.
- Validate that the file exists and is readable.
- Use pandas for inspection.
- Display row and column counts.
- Display column names and inferred data types.
- Display missing-value counts and percentages.
- Report duplicate-row count.
- Show basic descriptive statistics.
- Summarize categorical columns without printing excessively large outputs.
- Handle empty files, invalid paths, and unreadable CSVs with clear error messages.
- Avoid printing entire datasets.
- Do not modify, clean, overwrite, or delete the source dataset.
- Do not hardcode a particular dataset filename or target column.
- Keep the implementation simple and beginner-friendly.

Use only the dependencies necessary for this script. Inspect existing requirements files before changing them. If an appropriate dependency is already declared, do not duplicate it.

Do not introduce a large framework or unnecessary dependency.

## 8. Scope Restrictions

During Phase 1, do NOT:

- Train Linear Regression, Decision Tree, Random Forest, KNN, or any other model.
- Create or save a trained ML model.
- Build preprocessing or prediction pipelines.
- Perform model evaluation or hyperparameter tuning.
- Build FastAPI endpoints.
- Implement Spring Boot APIs or database entities.
- Implement Next.js pages or frontend components.
- Introduce authentication or authorization.
- Add Docker or Docker Compose.
- Add PostgreSQL tables or migrations for application features.
- Add synthetic data or fabricate inspection results.
- Make unrelated changes to Phase 0 documentation or project configuration.
- Change the approved architecture or folder structure without reporting the reason first.

The purpose of Phase 1 is to make an evidence-based dataset decision and prepare a reusable inspection utility, not to build the ML system.

## 9. Testing and Verification

After implementation:

1. Verify the inspection script against an accessible real candidate CSV.
2. If no candidate can be downloaded, test using a temporary, clearly identified test fixture outside the committed project data. Do not present fixture results as real dataset findings.
3. Verify missing-value and duplicate calculations.
4. Verify invalid-path and unreadable-file handling.
5. Confirm the original dataset was not modified.
6. Confirm raw datasets and generated files remain excluded from Git as intended.
7. Run `git status` and inspect the final diff.
8. Check that all newly created files follow `AGENTS.md`.
9. Do not run model training.

Do not install unrelated dependencies or change the existing environment unnecessarily.

## 10. Git and Safety Rules

- Do not delete or reset existing work.
- Do not use destructive Git commands.
- Do not amend or rewrite existing commits.
- Do not commit or push automatically.
- Do not modify the Git remote.
- Do not stage unrelated files.
- Report any changes to `.gitignore` or dependency files and explain why they are needed.
- Preserve all existing Phase 0 files and folder structure.

## 11. Final Report

When Phase 1 is complete, report:

1. Files created or modified.
2. Candidate datasets investigated and their accessibility.
3. Primary dataset recommendation and supporting evidence, if any.
4. Data-quality findings.
5. Script tests performed and their results.
6. Licensing or provenance uncertainties.
7. Any unresolved blockers.
8. Exact Git working-tree status.
9. Confirmation that no ML model was trained and no later-phase application code was implemented.

**Stop after Phase 1. Do not begin Phase 2 until I review the report and explicitly authorize the next phase.**