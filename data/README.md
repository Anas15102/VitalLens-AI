# VitalLens Data Notes

This folder keeps the small files that are useful to version with the code and excludes the large datasets and generated artifacts that make the repository heavy.

## Tracked locally

- `data/raw/diabetes.csv`
- `data/raw/heart.csv`

## Not tracked in git

- `data/raw/archive/` - brain tumor image dataset copies used for training and testing
- `data/raw/COVID-19_Radiography_Dataset/` - chest X-ray dataset files and metadata exports
- `data/kaggle_downloads/` - temporary download cache
- `data/processed/` - derived or preprocessed outputs

## If you need the full training data

Download the original datasets locally and place them in the ignored folders above. The application code uses the trained models in `models/`, so the web app can still run without checking the raw datasets into git.