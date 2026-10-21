# Dataset Validation Report

**Project:** PropValueAI — Real Estate Price Prediction Using Python and Machine Learning  
**Phase:** Phase 1 — Dataset Inspection & Validation (Post-Review Gate)  
**Date of Inspection:** 2026-10-21 (Updated after empirical provenance & license verification)  
**Inspection Utility:** `ml/training/scripts/inspect_dataset.py` (pandas 3.0.6, Python 3.12)  
**Overall Validation Status:** **Pass with Warnings (Approved for Educational Demonstration Only)**  

---

## 1. Dataset Identification

- **File Inspected:** `ml/training/data/raw/Pune_House_Data.csv`
- **File Format:** Comma-Separated Values (CSV, UTF-8)
- **File Size:** 917,208 bytes (0.87 MB)
- **Source Repository:** `https://github.com/Sahil9822/Pune-House-Price-Prediction`
- **Raw Download URL:** `https://raw.githubusercontent.com/Sahil9822/Pune-House-Price-Prediction/main/Pune_House_Data.csv`
- **Underlying Upstream Source:** Kaggle `Bengaluru_House_Data.csv` (CC0: Public Domain)
- **Local SHA-256 Checksum:** `e45a6b471fe6e257fb4a5eac31e7ce011d760f39`

---

## 2. Basic Dataset Profile

- **Total Rows:** 13,320
- **Total Columns:** 9
- **Duplicate Rows:** 11 (0.08%)
- **Target Variable:** `price` (Continuous numeric, `float64`, denominated in Lakhs INR)

### Column Summary Table

| Column Name | Inferred Dtype | Non-Null Count | Missing Count | Missing Pct (%) | Cardinality (Unique) | Verified Upstream Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `area_type` | `object` (str) | 13,320 | 0 | 0.00% | 4 | 100% Identical to Bengaluru benchmark |
| `availability` | `object` (str) | 13,320 | 0 | 0.00% | 81 | 100% Identical to Bengaluru benchmark |
| `size` | `object` (str) | 13,304 | 16 | 0.12% | 31 | 100% Identical to Bengaluru benchmark |
| `society` | `object` (str) | 7,818 | 5,502 | 41.31% | 2,688 | 100% Identical to Bengaluru benchmark |
| `total_sqft` | `object` (str) | 13,320 | 0 | 0.00% | 2,117 | 100% Identical to Bengaluru benchmark |
| `bath` | `float64` | 13,247 | 73 | 0.55% | 19 | 100% Identical to Bengaluru benchmark |
| `balcony` | `float64` | 12,711 | 609 | 4.57% | 4 | 100% Identical to Bengaluru benchmark |
| `price` | `float64` | 13,320 | 0 | 0.00% | 1,994 | 100% Identical to Bengaluru benchmark |
| `site_location` | `object` (str) | 13,319 | 1 | 0.01% | 97 | Synthetically mapped Pune localities |

---

## 3. Verified Facts vs. Inferences & Assumptions

### Verified Facts
1. **Verbatim Column Matching:** Exactly 8 of the 9 columns (`area_type`, `availability`, `size`, `society`, `total_sqft`, `bath`, `balcony`, `price`) in `Pune_House_Data.csv` match the Kaggle `Bengaluru_House_Data.csv` dataset across all 13,320 rows with 100% equality.
2. **Mapped Location Column:** The original 1,305 Bengaluru locations were systematically substituted with 97 Pune locations. The distribution is uniform: 96 locations have exactly 138 or 139 records each, and 1 location (`'other'`) has 1 record.
3. **Repository Licensing:** `Sahil9822/Pune-House-Price-Prediction` contains no license file (GitHub API returns `license: null`). Public availability on GitHub does not constitute an explicit open-source license.
4. **Upstream Licensing:** The underlying Kaggle `Bengaluru_House_Data.csv` dataset is dedicated to the **Public Domain under CC0**.
5. **Target Units:** `price` is in Lakhs INR (₹100,000 increments) and has zero null values.
6. **Data Quirks:** ~200 rows in `total_sqft` contain range intervals; ~47 rows contain non-standard units (`Sq. Meter`, `Sq. Yards`, `Acres`).

### Unresolved Inferences & Strategic Scope
- *Limitation:* The dataset cannot be characterized as genuine Pune market transaction data.
- *Permitted Scope:* The dataset is valid for demonstrating real-estate machine learning pipelines, preprocessing transformations, model evaluation, and full-stack software architecture (Next.js + Spring Boot + FastAPI), but cannot support commercial or certified appraisal claims.

---

## 4. Summary of Validation Checks

| Validation Check | Target Metric / Requirement | Outcome | Status |
| :--- | :--- | :--- | :--- |
| **File Integrity** | Valid CSV structure | 917,208 bytes, 13,320 rows parsed | **PASS** |
| **Target Variable** | Continuous, non-null numeric target | `price` is 100% complete, float64 | **PASS** |
| **Target Units** | Currency and scale verified | Confirmed as Lakhs INR | **PASS** |
| **Predictive Features** | Essential housing attributes present | Location, total area, size, bath present | **PASS** |
| **Duplicate Rows** | Minimal duplicate observations | 11 duplicate rows (0.08%) | **PASS** |
| **Area Homogeneity** | Numeric square feet values | 98.1% clean, ~247 rows require parsing | **WARNING** |
| **Missing Values** | Low missingness in key features | `society` is 41.3% null; `balcony` is 4.6% null | **WARNING** |
| **Geographic Provenance** | Authentic Pune transactional records | Mapped labels from CC0 Bengaluru dataset | **WARNING** |
| **Repository License** | Explicit open license | Unstated in candidate repo; CC0 upstream | **WARNING** |

---

## 5. Final Validation Verdict

**Validation Status: PASS WITH WARNINGS**  
**Approved Classification:** **Educational Demonstration Dataset**

Candidate A is accepted for Phase 2 development subject to the following project constraints:
1. Documentation and user-facing UI must explicitly state that predictions are educational estimates based on a benchmark dataset with mapped Pune localities.
2. The preprocessing pipeline in Phase 2 must parse `total_sqft` ranges and units, extract `bhk` from `size`, and exclude `society` to prevent extreme sparsity.
3. Train/validation/test splits must be executed prior to fitting transformers to guarantee zero data leakage.
