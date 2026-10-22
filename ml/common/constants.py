"""
Common Constants for PropValueAI Machine Learning Module.
"""

# Random seed for reproducible splitting and model training
RANDOM_SEED = 42

# Train / Test split ratio
TEST_SPLIT_RATIO = 0.20

# Unit conversion factors to square feet
SQFT_UNIT_CONVERSIONS = {
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

# Supported feature names for baseline models
CATEGORICAL_FEATURES = ["area_type"]
NUMERIC_FEATURES = ["total_sqft", "bhk", "bath", "balcony"]

# Target column name and unit
TARGET_COLUMN = "price"
TARGET_UNIT = "Lakhs INR"
