# ML Module

**Status:** Planned; training and inference implementation has not started.

## Responsibilities
- `training/`: offline dataset inspection, EDA, training, evaluation, and experiment records.
- `inference/`: loading the trusted fitted pipeline and serving predictions through FastAPI.
- `pipeline/`: optional orchestration only when it removes duplication or improves maintenance.
- `common/`: genuinely shared utilities/constants.
- `tests/`: unit and integration tests for training, preprocessing, artifact loading, and predictions.

## Agreed structure

```text
ml/
├── training/
│   ├── data/
│   │   ├── raw/
│   │   ├── processed/
│   │   └── external/
│   ├── scripts/
│   │   ├── train.py                 # planned
│   │   ├── evaluate.py              # planned
│   │   └── generate_data.py         # optional; test/demo data only
│   ├── experiments/
│   └── requirements.txt
├── inference/
│   ├── model/
│   │   ├── loader.py                # planned
│   │   └── predictor.py             # planned
│   ├── preprocessing/
│   │   └── preprocess.py            # optional if not already in fitted pipeline
│   ├── services/
│   │   └── prediction_service.py    # planned
│   ├── artifacts/
│   │   ├── model.joblib             # generated after training; not committed by default
│   │   └── metadata.json            # generated after training
│   ├── config/
│   │   └── settings.py              # planned
│   └── main.py                      # planned FastAPI entry point
├── pipeline/
│   └── pipeline.py                  # optional orchestration
├── common/
│   ├── utils.py
│   └── constants.py
├── tests/
│   ├── test_training.py
│   ├── test_predictor.py
│   └── test_preprocessing.py
├── requirements.txt
└── README.md
```

The agreed paths are preserved, but not every optional file must be implemented. Avoid empty abstractions and duplicate preprocessing.

## Training-to-inference lifecycle
1. Inspect and approve a real dataset.
2. Validate columns, target, currency, units, and data quality.
3. Split data appropriately and fit preprocessing only on training data.
4. Train a baseline and compare suitable models.
5. Evaluate on held-out data with MAE, RMSE, and R².
6. Save the fitted preprocessing + estimator pipeline as a trusted joblib artifact.
7. Save metadata such as model version, data reference, feature schema, dependency versions, and evaluation metrics.
8. Load the artifact for inference; do not retrain per request.

## Dataset status
Pune House Price and Indian Urban House Price candidates are not yet validated. See `../docs/development-roadmap.md`. Do not assume their schema or merge them before compatibility review.

## Dependency management
Training and inference dependency files may be separate. Pin tested versions during implementation and keep scikit-learn versions compatible with serialized artifacts. Do not install dependencies during Phase 0.
