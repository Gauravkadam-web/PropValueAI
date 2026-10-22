# Exploratory Data Analysis (EDA) Report

**Project:** PropValueAI — Real Estate Price Prediction Using Python and Machine Learning  
**Phase:** Phase 2 — EDA, Preprocessing, Model Training & Evaluation  
**Dataset:** `ml/training/data/raw/Pune_House_Data.csv` (13,320 rows × 9 columns)  
**Target Variable:** `price` (in Lakhs of Indian Rupees, where ₹1 Lakh = ₹100,000)  

---

## 1. Executive Summary & Context

This exploratory data analysis establishes empirical baselines, identifies anomalies, and justifies the preprocessing transformations for the PropValueAI machine learning pipeline. 

As established in Phase 1, the dataset originates as a derivative of the CC0 benchmark Bengaluru real-estate dataset with 97 uniformly mapped Pune residential localities. Therefore, this EDA treats the dataset strictly as an **educational regression benchmark** reflecting authentic Indian metropolitan housing distributions, while explicitly excluding `site_location` from the feature set to prevent learning synthetic geographic artifacts.

---

## 2. Dataset Dimensions & Schema Overview

- **Total Rows:** 13,320
- **Total Columns:** 9
- **Duplicate Observations:** 11 duplicate rows (0.08%)

### Initial Column Inventory

| Column Name | Inferred Type | Missing Count | Missing Pct (%) | Cardinality | Distinct Values / Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `area_type` | Categorical (str) | 0 | 0.00% | 4 | Super built-up Area (66.0%), Built-up Area (18.2%), Plot Area (15.2%), Carpet Area (0.7%) |
| `availability` | Categorical (str) | 0 | 0.00% | 81 | 'Ready To Move' (79.4%), remaining 20.6% are month-year delivery strings |
| `size` | Text (str) | 16 | 0.12% | 31 | Combines bedroom count with nomenclature ('2 BHK', '4 Bedroom', '1 RK') |
| `society` | Categorical (str) | 5,502 | 41.31% | 2,688 | High-sparsity residential society names |
| `total_sqft` | Mixed (str) | 0 | 0.00% | 2,117 | Standard numbers, numeric ranges ('2100 - 2850'), and non-standard units |
| `bath` | Numeric (float64) | 73 | 0.55% | 19 | Bathroom count; discrete integer values from 1.0 to 40.0 |
| `balcony` | Numeric (float64) | 609 | 4.57% | 4 | Balcony count; values 0.0, 1.0, 2.0, 3.0 |
| `price` | Numeric (float64) | 0 | 0.00% | 1,994 | Target variable; continuous float in Lakhs INR |
| `site_location` | Categorical (str) | 1 | 0.01% | 97 | 96 Pune localities evenly distributed (~138-139 rows each), plus 'other' (1 row) |

---

## 3. Target Variable Analysis (`price`)

The target `price` represents total property price denominated in **Lakhs of Indian Rupees**.

### Descriptive Statistics:
- **Count:** 13,320 (100% complete)
- **Mean:** ₹112.57 Lakhs
- **Standard Deviation:** ₹148.97 Lakhs
- **Minimum:** ₹8.00 Lakhs
- **25th Percentile ($Q_1$):** ₹50.00 Lakhs
- **Median (50th Percentile):** ₹72.00 Lakhs
- **75th Percentile ($Q_3$):** ₹120.00 Lakhs
- **90th Percentile:** ₹220.00 Lakhs
- **95th Percentile:** ₹324.00 Lakhs
- **99th Percentile:** ₹658.10 Lakhs
- **Maximum:** ₹3,600.00 Lakhs (₹36 Crores)
- **Skewness:** +8.06 (heavily right-skewed)
- **Kurtosis:** +108.17 (heavy-tailed leptokurtic distribution)

### Target Distribution Insights:
- 50% of all properties are priced between ₹50 Lakhs and ₹120 Lakhs, representing typical urban middle-class residential inventory.
- Extreme luxury properties (up to ₹36 Crores) cause substantial right-skew. Tree-based ensemble models (Random Forest) handle this heavy-tailed distribution without requiring artificial target truncation.
- *Plot Generated:* `ml/training/experiments/plots/price_distribution.png` compares the linear histogram against the log-transformed distribution.

---

## 4. Feature Profiling & Deep Column Audits

### A. Total Square Feet (`total_sqft`) Format Breakdown
The `total_sqft` column is nominally text because of non-numeric formats:

| Format Category | Description | Count | Percentage | Preprocessing Treatment |
| :--- | :--- | :--- | :--- | :--- |
| **Pure Numeric** | e.g., `'1056'`, `'2600'` | 13,073 | 98.15% | Converted directly to `float64` |
| **Range String** | e.g., `'2100 - 2850'` | 201 | 1.51% | Average midpoint computed: $(low + high) / 2$ |
| **Alternative Units** | e.g., `'1000Sq. Yards'`, `'100Sq. Meter'`, `'1Acres'` | 33 | 0.25% | Multiplied by verified unit conversion factors |
| **Invalid / Ambiguous** | Multiple decimals, unparseable text | 13 | 0.10% | Parsed as `np.nan` and imputed with median |

#### Unit Conversion Table:
- 1 Square Meter = 10.7639 Square Feet
- 1 Square Yard = 9.0 Square Feet
- 1 Acre = 43,560.0 Square Feet
- 1 Guntha = 1,089.0 Square Feet
- 1 Perch = 272.25 Square Feet
- 1 Cent = 435.6 Square Feet

### B. Bedroom Count (`size` -> `bhk`)
- Parsing `size` with regular expression `(\d+)` successfully extracts clean integer bedroom counts across both `'2 BHK'` and `'4 Bedroom'` notations.
- **Distribution:** 
  - 2 BHK: 5,528 (41.50%)
  - 3 BHK: 4,857 (36.46%)
  - 4 BHK: 1,417 (10.64%)
  - 1 BHK: 656 (4.92%)
  - 5 BHK: 356 (2.67%)
  - 6+ BHK: 490 (3.68%)
  - Missing (`NaN`): 16 (0.12%) — Imputed with median BHK (2.0).

### C. Bathrooms (`bath`) and Balconies (`balcony`)
- **Bathrooms:** Median is 2.0. 73 rows are missing (0.55%). Severe anomalies include properties with up to 40 bathrooms.
- **Balconies:** Discrete values range from 0 to 3. Median is 2.0. 609 rows are missing (4.57%), imputed with median.

### D. Area Type vs. Price
Plot Area properties command the highest mean and median prices due to independent land ownership:
- **Plot Area:** Count 2,025 | Median ₹140.00 Lakhs | Mean ₹208.50 Lakhs
- **Built-up Area:** Count 2,418 | Median ₹70.00 Lakhs | Mean ₹104.29 Lakhs
- **Carpet Area:** Count 87 | Median ₹70.00 Lakhs | Mean ₹89.50 Lakhs
- **Super built-up Area:** Count 8,790 | Median ₹65.00 Lakhs | Mean ₹92.97 Lakhs

---

## 5. Anomaly and Domain Outlier Diagnostics

We audited three specific real-estate domain violations:

1. **Unrealistic Area per Bedroom (`sqft / bhk < 300`):**
   - 747 rows (5.61%) possess implausibly tiny areas per bedroom (e.g., an 8 BHK home in 600 sqft, or 43 bedrooms in 1,020 sqft).
   - In residential architecture, standard habitable rooms require at least 300 sqft total space per bedroom including circulation.
2. **Excessive Bathroom Count (`bath > bhk + 2`):**
   - 16 rows (0.12%) have more bathrooms than bedrooms plus two (e.g., 2 BHK apartment with 6 bathrooms).
3. **Extreme Price-to-Area Outliers:**
   - 33 rows have prices below ₹500/sqft or above ₹50,000/sqft, representing data entry errors.

### Leakage-Free Outlier Protocol:
To prevent data leakage, **all outlier filtering is applied strictly to the training fold (`X_train`) after the train/test split**. Held-out test observations are never filtered using target-dependent criteria.

---

## 6. Preprocessing Decisions & Feature Selection

| Feature | Decision | Implementation | Justification |
| :--- | :--- | :--- | :--- |
| `total_sqft` | **Retained** | Parsed range midpoint & unit conversion -> Median Imputer | Core continuous physical predictor |
| `size` (`bhk`) | **Retained** | Regex integer extraction -> Median Imputer | Primary residential configuration metric |
| `bath` | **Retained** | Median Imputer | High correlation with property size and luxury |
| `balcony` | **Retained** | Median Imputer | Amenity indicator |
| `area_type` | **Retained** | Most-frequent Imputer -> `OneHotEncoder(handle_unknown='ignore')` | Clean 4-class categorization with pricing variance |
| `society` | **Dropped** | Excluded from pipeline | 41.31% missing; 2,688 high-cardinality categories causing sparsity |
| `site_location`| **Dropped** | Excluded from pipeline | Artificially mapped labels; prevents learning spurious geographic effects |
| `availability`| **Dropped** | Excluded from pipeline | 79.4% 'Ready To Move'; remaining 20% are noise/past dates prone to leakage |

---

## 7. Artifacts Generated During EDA

The following plots were generated and stored in `ml/training/experiments/plots/` (ignored by Git):
1. `price_distribution.png`: Linear vs. log-transformed target histograms.
2. `price_vs_sqft.png`: Scatter plot illustrating the positive non-linear relationship between square footage and price.
3. `price_by_bhk.png`: Box plots showing median price progression across 1 BHK to 6 BHK configurations.
4. `price_by_area_type.png`: Box plots confirming Plot Area premium over apartment configurations.
