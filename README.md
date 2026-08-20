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
- **Target:** `ClosePrice` (final sale price), modeled in log space (`LogClosePrice`) so error scales relatively across the price range rather than in raw dollars.
- **Feature groups:**
  - *Size/structure:* `LivingArea`, `BedroomsTotal`, `BathroomsTotalInteger`, `YearBuilt`, `GarageSpaces`, `LotSizeSquareFeet`
  - *Location:* `CountyOrParish`, `Latitude`, `Longitude`, plus `PostalCode`, `City`, `MLSAreaMajor`, and a school `DistrictName` joined in from `data/ca_school_districts.geojson` (used by the tree/boosting models, not the linear baseline)
  - *Amenity flags:* `PoolPrivateYN`, `ViewYN`, `FireplaceYN`, `NewConstructionYN`, `HasAssociationFee`


## Preprocessing (`notebooks/02_preprocessing.ipynb`)

1. **Concatenate the 8 monthly CSVs, filter to single-family residential CA listings, drop duplicate `ListingKey`s, and null out any lat/long pairs falling outside California's bounding box.**
   *Why:* the raw exports are per-month and include property types (condos, land, multi-family) outside this project's scope; a listing can appear more than once across monthly pulls (relisted, re-exported) so de-duping by its unique key avoids double-counting a single sale; a handful of listings carry corrupted coordinates (e.g. `(0, 0)` or swapped lat/long) that would silently poison any location feature, so those get nulled out to be handled by imputation/filtering downstream instead of treated as real geography.

2. **Derive `HasAssociationFee` (`'True'`/`'False'`/`'Unknown'`) from `AssociationFee`.**
   *Why:* `AssociationFee` itself is ~30% missing, and `0` is a legitimate "no HOA" value — so a raw numeric imputation (e.g. filling missing with the median fee) would incorrectly assign a nonzero fee to homes that either have no HOA or simply didn't report one. Collapsing to a 3-level flag sidesteps that ambiguity and keeps the "we don't actually know" case (`'Unknown'`) distinct from "no HOA" (`'False'`).

3. **Apply hard sanity filters** (`ClosePrice > 0`, `LivingArea > 0`, `BedroomsTotal > 0`, `YearBuilt` between 1800–2026).
   *Why:* these values are physically impossible or clear data-entry errors (a $0 sale, a 0 sq ft living area) — not real signal a model should try to learn from.

4. **Trim the 1st/99th percentile tails of `ClosePrice`, `LivingArea`, and `LotSizeSquareFeet`, and cap `BedroomsTotal`/`BathroomsTotalInteger` at their 99th percentile.**
   *Why:* the intent is to remove extreme outliers (data-entry typos, unusual luxury/estate listings) that would otherwise dominate the loss function and distort what the model learns for typical homes. 
5. **Fill missing amenity flags (`ViewYN`, `PoolPrivateYN`, `FireplaceYN`, `NewConstructionYN`) and `PostalCode`/`City`/`MLSAreaMajor` with `'Unknown'`**, collapsing `MLSAreaMajor`'s own `"699 - Not Defined"` placeholder into `'Unknown'` too.
   *Why:* these are categorical fields where "missing" is itself informative (the listing agent didn't report it) rather than something to guess at — treating it as its own category lets the model use that signal instead of losing the row or fabricating a value. `"699 - Not Defined"` is the MLS's own way of saying "unknown," so folding it into the same bucket avoids treating it as a real, distinct area.

6. **Drop rows still missing a value in a *required* baseline column** (`ClosePrice`, `LivingArea`, `BedroomsTotal`, `BathroomsTotalInteger`, `YearBuilt`, `CountyOrParish`, `Latitude`, `Longitude`, and the now-filled amenity flags), **but not `GarageSpaces`/`LotSizeSquareFeet`.**
   *Why we don't just impute everything:* `GarageSpaces` (3.60% missing) and `LotSizeSquareFeet` (1.76% missing) are numeric and reasonably approximated by the training median, so they're left as `NaN` here and median-imputed later *inside* the modeling pipeline (fit on train only, to avoid leaking test statistics into train). The other required columns are either the target itself (can't impute what you're trying to predict) or fields with negligible missingness to begin with (`Latitude`/`Longitude`/`YearBuilt` are each under 0.05% missing, and the amenity flags/postal/city were already backfilled to `'Unknown'` in step 5) — so in practice this drop removes a negligible fraction of rows; it isn't the primary way missing data gets handled. Median imputation, not row-dropping, does most of the work here.

7. **Save two cleaned CSVs:** `cleaned_CRMLSSOLD_baseline.csv` (county + lat/long, no postal — used for the linear baseline) and `cleaned_CRMLSSOLD_all_features.csv` (adds `PostalCode`/`City`/`MLSAreaMajor` — used by the tree/boosting models).
 

8. **Train/test split is time-based, not random:** the most recent month is held out entirely as the test set, and all prior months are training data.
   *Why:* the model's real use case is predicting a *future* sale from past sales, not interpolating within a single time period — a random split would let the model see listings from the same month (and often similar market conditions) in both train and test, overstating how well it'd generalize to genuinely new, later data.

## Models Tested (`notebooks/03`–`06`)

`LinearRegression`, `DecisionTree`, `RandomForest`, `XGBoost`, `LightGBM`, and `CatBoost` were each trained on the same one-hot encoded feature set for a like-for-like comparison; `LightGBM` and `CatBoost` were also refit on the raw (unencoded) categorical columns to use their native categorical handling, for 8 model/encoding combinations total. `03_baseline_model.ipynb` and `04_model_comparison.ipynb` iterate on feature sets; `05_advanced_models.ipynb` grid-searches XGBoost/LightGBM/CatBoost hyperparameters (winners: `n_estimators`/`iterations`=1000, `learning_rate`=0.1, `max_depth`/`depth`=8); `06_evaluation.ipynb` refits all 8 with those settings on the full feature set and does the final comparison.


## Model Results

Eight models/feature-encoding combinations were trained and evaluated on a held-out test month (see `notebooks/06_evaluation.ipynb`). Metrics below are on the test set, sorted by R².

| Model | Test R² | RMSE ($) | MAE ($) | MdAPE (%) | MAPE (%) |
|---|---|---|---|---|---|
| LightGBM (native cat) | 0.9359 | $280,659 | $145,355 | 7.61% | 10.91% |
| CatBoost (native cat) | 0.9351 | $285,349 | $147,746 | 7.70% | 11.02% |
| CatBoost | 0.9335 | $285,480 | $149,841 | 8.04% | 11.24% |
| LightGBM | 0.9333 | $283,380 | $148,965 | 7.99% | 11.24% |
| XGBoost | 0.9323 | $288,908 | $150,360 | 7.96% | 11.23% |
| RandomForest | 0.9112 | $340,559 | $173,184 | 8.63% | 12.69% |
| LinearRegression | 0.8528 | $420,609 | $224,150 | 12.76% | 17.04% |
| DecisionTree | 0.8432 | $434,679 | $231,705 | 11.54% | 17.18% |

**CatBoost** (one-hot encoded) was selected for deployment — it performs best on the price bands that make up the bulk of the test set ($500K-$2M, ~74% of listings), even though the native-categorical LightGBM/CatBoost variants edge it out on the blended metric. See `notebooks/06_evaluation.ipynb` for the full price-band breakdown.

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

**3. Save the deployment model:** run the last cell of `06_evaluation.ipynb` ("Save the CatBoost pipeline for deployment"). This writes `models/catboost_price_model.pkl` and `models/catboost_price_model_metadata.pkl` — `models/` is git-ignored, so these are regenerated locally rather than pulled from the repo.

**4. Launch the app:**

```bash
cd weekly-deliverables
streamlit run app.py
```

This opens a form for a property's characteristics and returns a predicted close price with an approximate error margin, using the saved CatBoost pipeline from step 3.
