# Project Structure

This project follows a standard data science layout to keep code, data, and results organized.

## Folder Overview

### `data/`
Stores all datasets.

- `raw/` → original data (never modified)
- `processed/` → cleaned and transformed data
- `external/` → third-party datasets

Purpose: keep input data separate from code and results.

---

### `notebooks/`
Contains Jupyter notebooks for exploration and experimentation.

Used for:
- data analysis (EDA)
- visualization
- model testing
- quick experiments

Note: notebooks are for experimentation, not production code.

---

### `src/`
Reusable Python code used across the project.

Contains:
- data cleaning functions
- feature engineering
- training scripts
- utility functions

Purpose: keep logic modular and avoid duplication.

---

### `models/`
Stores trained machine learning models.

Examples:
- saved `.pkl` or `.joblib` models
- exported model files

Purpose: reuse models for inference or deployment.

---

### `outputs/`
Stores generated results.

Examples:
- charts and plots
- reports
- prediction files
- evaluation results

Purpose: reproducible outputs from analysis and modeling.

---

## Workflow

1. Data is placed in `data/raw/`
2. Cleaning and transformation is done via `src/`
3. Exploration and experimentation happen in `notebooks/`
4. Trained models are saved in `models/`
5. Results and exports go to `outputs/`

---

## Summary

- `data/` → input
- `notebooks/` → exploration
- `src/` → reusable code
- `models/` → trained models
- `outputs/` → results
