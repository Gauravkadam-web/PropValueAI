# Dataset Evaluation & Source Comparison

**Project:** PropValueAI — Real Estate Price Prediction Using Python and Machine Learning  
**Phase:** Phase 1 — Dataset Inspection & Validation (Post-Review Gate)  
**Date of Inspection:** 2026-10-21 (Updated after empirical provenance & license verification)  

---

## 1. Objective and Scope

The objective of Phase 1 is to discover, inspect, profile, and validate candidate datasets for predicting residential property prices in Pune, India.

Key evaluation criteria:
- **Geographic focus:** Authentic or representative Pune residential property locations.
- **Target quality:** A well-defined, continuous numeric target variable representing property price.
- **Predictive features:** Essential residential attributes, specifically location, usable area (square feet), bedrooms/BHK, bathrooms, and property type.
- **Data cleanliness and usability:** Manageable missingness, consistent units, absence of data leakage, and realistic ranges.
- **Provenance and licensing:** Transparent data origins, empirical verification of authenticity, and verifiable usage terms.

---

## 2. Candidate Datasets Investigated

Three primary candidates were investigated:

| Candidate | Identifier / URL | Source Type | Status & Accessibility |
| :--- | :--- | :--- | :--- |
| **Candidate A** | [Sahil9822/Pune-House-Price-Prediction](https://github.com/Sahil9822/Pune-House-Price-Prediction) (`Pune_House_Data.csv`) | Public GitHub Repository | **Accessible.** Downloaded to `ml/training/data/raw/Pune_House_Data.csv` (917,208 bytes, 13,320 rows, 9 columns). |
| **Candidate B** | [prashantmane92/dataset/Pune_House_Data.csv](https://raw.githubusercontent.com/prashantmane92/dataset/main/Pune_House_Data.csv) | Raw GitHub CSV Link | **Inaccessible.** The URL returns an HTTP 404 Not Found error (repository removed, renamed, or private). |
| **Candidate C** | [Kaggle: Indian Urban House Price Prediction](https://www.kaggle.com/competitions/indian-urban-house-price-prediction/data) | Kaggle Competition | **Rejected & Gated.** Gated behind Kaggle authentication. Explicitly declared in official competition metadata as a *100,000-row synthetic dataset across multiple Indian cities*, violating project constraints against synthetic training data. |

---

## 3. Provenance Verification: Empirical Findings

A rigorous automated comparison was conducted between `Pune_House_Data.csv` and the upstream benchmark Kaggle **`Bengaluru_House_Data.csv`** (13,320 rows × 9 columns, canonical source of Indian housing tutorials):

### Column-by-Column Equality Check (13,320 rows):

| Column | Equality with Bengaluru Benchmark | Verified Finding |
| :--- | :--- | :--- |
| `area_type` | **Identical (100.0%)** | Exact match across all 13,320 rows |
| `availability` | **Identical (100.0%)** | Exact match across all 13,320 rows |
| `size` | **Identical (100.0%)** | Exact match across all 13,320 rows |
| `society` | **Identical (100.0%)** | Exact match across all 13,320 rows |
| `total_sqft` | **Identical (100.0%)** | Exact match across all 13,320 rows |
| `bath` | **Identical (100.0%)** | Exact match across all 13,320 rows |
| `balcony` | **Identical (100.0%)** | Exact match across all 13,320 rows |
| `price` | **Identical (100.0%)** | Exact match across all 13,320 rows |
| `site_location` vs `location` | **Synthetically Mapped** | Bengaluru's 1,305 authentic locations were replaced with 97 Pune locations |

### Provenance Fact vs. Inference:
- **Verified Fact:** `Pune_House_Data.csv` is **not** an authentic collection of Pune real-estate transactions. The physical property features (`total_sqft`, `bath`, `balcony`, `size`, `society`, `area_type`) and prices (`price`) are identical copies of the Bengaluru real estate dataset.
- **Verified Fact:** The 97 Pune localities are synthetically mapped labels. Exactly 96 Pune localities appear uniformly 138 or 139 times each, plus `'other'` with 1 occurrence, confirming mechanical distribution rather than organic market transaction density.
- **Inference/Context:** The dataset was constructed as a portfolio/educational proxy to demonstrate full-stack real-estate regression models for Pune without collecting proprietary local cadastral records.

---

## 4. Licensing Verification Results

1. **Candidate A Repository (`Sahil9822/Pune-House-Price-Prediction`):**
   - GitHub API inspection (`GET /repos/Sahil9822/Pune-House-Price-Prediction`) confirms: `license: null`.
   - The repository contains no `LICENSE` file. Under standard copyright law, public accessibility on GitHub does not automatically grant MIT or public domain rights.
2. **Upstream Source Data (`Bengaluru_House_Data.csv`):**
   - The original dataset hosted on Kaggle is released under **CC0: Public Domain** (dedicating all property attributes and records to the public domain without copyright restrictions).
3. **Licensing Conclusion:**
   - The underlying tabular data attributes and pricing relationships are in the public domain via CC0.
   - The specific derivative repository has unstated licensing terms. For an educational and portfolio web application, fair educational use of public domain-derived data applies, but commercial redistribution rights cannot be claimed.

---

## 5. Candidate Comparison Matrix

| Evaluation Criterion | Candidate A (Sahil9822 Pune CSV) | Candidate B (Prashant Mane CSV) | Candidate C (Kaggle Indian Urban) |
| :--- | :--- | :--- | :--- |
| **Accessibility** | Public raw download available | Inaccessible (404 Not Found) | Requires Kaggle login/API key |
| **Geographic Relevance** | Mapped Pune localities (97 locations) | Inaccessible | Multi-city across India |
| **Data Nature** | Benchmark real estate data with mapped Pune localities | Inaccessible | **100% Synthetic** (per official metadata) |
| **Target Variable** | `price` in Lakhs INR (continuous, 0 nulls) | Inaccessible | `price` (synthetic) |
| **Property Features** | Location, Area, BHK, Bath, Balcony, Area Type | Inaccessible | Multi-city housing features |
| **Missing Values** | `society` 41.3%, `balcony` 4.6%, `bath` 0.5%, `size` 0.1% | Inaccessible | Not accessible |
| **Upstream License** | Underlying data is **CC0: Public Domain**; repo license is unstated | Inaccessible | Kaggle Competition terms |
| **Overall Verdict** | **Approved for Educational Demo (Option C/A)** | **Failed (Inaccessible)** | **Rejected (Synthetic data violation)** |

---

## 6. Strategic Dataset Recommendation & Boundary Constraints

### Recommendation: Combined Option C / Option A (Educational Demonstration with Explicit Constraints)

We recommend using **Candidate A (`Pune_House_Data.csv`)** as an **educational regression demonstration dataset**, while explicitly documenting that real-world Pune cadastral prediction remains a future roadmap objective.

### What the Eventual Model CAN Support:
- Full end-to-end integration across Next.js, Spring Boot, FastAPI, PostgreSQL, and scikit-learn.
- Real regression workflows: data cleaning, unit standardisation, BHK parsing, train/validation/test evaluation (MAE, RMSE, $R^2$), pipeline serialization (`model.joblib`), and runtime inference.
- Realistic pricing behavior based on genuine Indian metropolitan property dynamics (where 2 BHKs in standard societies scale realistically with square footage).

### What the Eventual Model CANNOT Support:
- The model **cannot** claim to provide legally binding, accurate cadastral valuations for physical properties in Pune.
- The model **cannot** capture micro-market real-estate pricing discrepancies specific to Pune (e.g., Koregaon Park luxury premiums vs. Hadapsar suburban rates), because locality labels were uniformly distributed across benchmark records.
- All UI screens in the Next.js frontend must display an explicit disclaimer: *"PropValueAI provides simulated estimates for educational demonstration purposes only."*

---

## 7. Next Steps for Phase 2 Preprocessing

1. Clean `total_sqft` strings: parse numerical ranges by calculating their mean, convert metric units (Sq. Meter, Sq. Yards, Acres) into square feet.
2. Extract integer `bhk` from `size` strings.
3. Drop high-cardinality, heavily incomplete `society` column (41.3% null).
4. Implement stratified/grouped train-test splitting before fitting scikit-learn transformers to guarantee zero data leakage.
