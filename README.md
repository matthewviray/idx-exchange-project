# California Property Close Price Prediction

## Project Description

This project develops a machine learning model to predict the close price (final sale price) of residential properties in California. Using historical sales data sourced from CRMLS (California Regional Multiple Listing Service), the model learns the relationship between a property's characteristics, such as living area, number of bedrooms and bathrooms, and lot size, and its final sale price. The trained model can then estimate the close price of any single-family residential property in California, whether it is currently for sale or not, based on its characteristics at the time of the query.

The dataset is restricted to observations where `PropertyType = "Residential"` and `PropertySubType = "SingleFamilyResidence"`.

## Objectives

- Explore and understand the structure, features, and patterns in the CRMLS sales dataset.
- Preprocess the data, including handling missing values, encoding categorical variables, and scaling numerical features as needed.
- Select and train one or more machine learning models (e.g., linear regression, decision trees, random forests, gradient boosting) to predict `ClosePrice`.
- Evaluate model performance using appropriate metrics (e.g., R-squared, MAPE, MdAPE) and identify areas for improvement.
- Use the trained model to predict the close price of a given property based on its characteristics.
- Document the full process, including data exploration, preprocessing, model selection, training, evaluation, and prediction, for reproducibility and stakeholder review.

## Dataset

- **Source:** CRMLS (California Regional Multiple Listing Service) monthly sold-listing exports, `data/CRMLSSold<YYYYMM>.csv` for November 2025 through June 2026 (8 months), CA School District Areas 2024-25 boundaries from https://data.ca.gov/dataset/california-school-district-areas-2024-25/resource/7dfaf005-58eb-45db-93b1-7aff091b2172 .
- **Scope:** filtered to `PropertyType = "Residential"`, `PropertySubType = "SingleFamilyResidence"`, and `StateOrProvince = "CA"`.
- **Target:** `ClosePrice` (final sale price), modeled in log space (`LogClosePrice`) so error scales relatively across the price range rather than in raw dollars as 'ClosePrice is highly right skewed.
- **Feature groups:**
  - *Size/structure:* `LivingArea`, `BedroomsTotal`, `BathroomsTotalInteger`, `YearBuilt`, `GarageSpaces`, `LotSizeSquareFeet`
  - *Location:* `CountyOrParish`, `Latitude`, `Longitude`, plus `PostalCode`, `City`, `MLSAreaMajor`, and a school `DistrictName` joined in from `data/ca_school_districts.geojson` (used by the tree/boosting models, not the linear baseline)
  - *Amenity flags:* `PoolPrivateYN`, `ViewYN`, `FireplaceYN`, `NewConstructionYN`, `HasAssociationFee`


## Preprocessing (`notebooks/02_preprocessing.ipynb`)

- Concatenate the 8 monthly CSVs, filter to single-family residential CA listings, and de-duplicate by `ListingKey`.
- Clean up bad/missing values: null out corrupted lat/long pairs, derive a 3-level `HasAssociationFee` flag, apply sanity filters (e.g. `ClosePrice > 0`), trim outlier tails, and fill missing categorical fields with `'Unknown'`.
- Drop rows still missing a *required* column; leave `GarageSpaces`/`LotSizeSquareFeet` as `NaN` for median imputation inside the modeling pipeline (fit on train only).
- Save two cleaned CSVs: `cleaned_CRMLSSOLD_baseline.csv` (linear baseline) and `cleaned_CRMLSSOLD_all_features.csv` (adds postal/city/area, used by tree/boosting models).
- Split train/test **by time** (most recent month held out) rather than randomly, since the model's real use case is predicting future sales from past data.

## Models Tested (`notebooks/03`–`06`)

`LinearRegression`, `DecisionTree`, `RandomForest`, `XGBoost`, `LightGBM`, and `CatBoost` were each trained on the same one-hot encoded feature set for a like-for-like comparison; `LightGBM` and `CatBoost` were also refit on the raw (unencoded) categorical columns to use their native categorical handling, for 8 model/encoding combinations total. `03_baseline_model.ipynb` and `04_model_comparison.ipynb` iterate on feature sets; `05_advanced_models.ipynb` grid-searches XGBoost/LightGBM/CatBoost hyperparameters (winners: `n_estimators`/`iterations`=1000, `learning_rate`=0.1, `max_depth`/`depth`=8); `06_evaluation.ipynb` refits all 8 with those settings on the full feature set and does the final comparison.


## Model Results

Eight models/feature-encoding combinations were trained and evaluated on a held-out test month (see `notebooks/06_evaluation.ipynb`). Metrics below are on the test set, sorted by R².

| Model | Test R² | RMSE ($) | MAE ($) | MdAPE (%) | MAPE (%) |
|---|---|---|---|---|---|
| **LightGBM (native cat)** | **0.9359** | **$280,659** | **$145,355** | **7.61%** | **10.91%** |
| CatBoost (native cat) | 0.9351 | $285,349 | $147,746 | 7.70% | 11.02% |
| CatBoost | 0.9335 | $285,480 | $149,841 | 8.04% | 11.24% |
| LightGBM | 0.9333 | $283,380 | $148,965 | 7.99% | 11.24% |
| XGBoost | 0.9323 | $288,908 | $150,360 | 7.96% | 11.23% |
| RandomForest | 0.9112 | $340,559 | $173,184 | 8.63% | 12.69% |
| LinearRegression | 0.8528 | $420,609 | $224,150 | 12.76% | 17.04% |
| DecisionTree | 0.8432 | $434,679 | $231,705 | 11.54% | 17.18% |

**CatBoost** (one-hot encoded) was selected for deployment — it performs best on the price bands that make up the bulk of the test set ($500K-$2M, ~74% of listings), even though the native-categorical LightGBM/CatBoost variants edge it out on the blended metric. See `notebooks/06_evaluation.ipynb` for the full price-band breakdown.

## Live App

[CA Home Price Predictor](https://matthewviray-idx-exchange-project-weekly-deliverablesapp-ikt3in.streamlit.app/) — deployed Streamlit app using the saved CatBoost pipeline.

## How to Re-run

**1. Install dependencies:**

```bash
pip install pandas numpy scikit-learn xgboost lightgbm catboost geopandas seaborn matplotlib joblib streamlit
```

**2. Run the notebooks in order** (each one reads a CSV the previous notebook produced):

| Notebook | Produces |
|---|---|
| `01_exploration.ipynb` | Initial EDA, feature selection notes |
| `02_preprocessing.ipynb` | `data/cleaned_CRMLSSOLD_baseline.csv`, `data/cleaned_CRMLSSOLD_all_features.csv` |
| `03_baseline_model.ipynb` | Linear regression baseline |
| `04_model_comparison.ipynb` | Feature-set iteration across models |
| `05_advanced_models.ipynb` | XGBoost/LightGBM/CatBoost hyperparameter search |
| `06_evaluation.ipynb` | Final 8-model comparison, price-band breakdown, `metric_summary/metrics_summary.csv`, and the deployed model (last cell) |

The raw monthly CSVs (`data/CRMLSSold<YYYYMM>.csv`) and the school-district shapefile (`data/ca_school_districts.geojson`) must already be present in `data/` before running `02_preprocessing.ipynb`.

**3. Save the deployment model:** run the last cell of `06_evaluation.ipynb` ("Save the CatBoost pipeline for deployment"). This writes `models/catboost_price_model.pkl` and `models/catboost_price_model_metadata.pkl`, which are committed to the repo so the deployed app can load them directly.

**4. Launch the app:**

```bash
cd weekly-deliverables
streamlit run app.py
```

This opens a form for a property's characteristics and returns a predicted close price with an approximate error margin, using the saved CatBoost pipeline from step 3.
