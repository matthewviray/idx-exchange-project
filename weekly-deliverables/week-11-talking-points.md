# Week 11 Final Presentation Talking Points

These notes cover only presentation points 1 and 2 of the example structure that will be possibly used in the final presentation. Brainstorm introduction of final presentation.
## 1. The Problem We’re Solving

### Opening

- Our goal is to predict the final sale price, or `ClosePrice`, of a California single-family home from information available in CRMLS listings.
- We used eight months of sold-listing data, from November 2025 through June 2026, and restricted the data to California residential single-family homes.
- This is not just a regression problem; it is also a geography, data-quality, and changing-market problem.

### Why California home-price prediction is difficult

- California is extremely heterogeneous. A home’s value depends heavily on location, and the relationship between price and physical features is different in coastal metros, inland counties, and the Central Valley.
- Prices have a strongly right-skewed, long-tail distribution. Most transactions are far below the small number of luxury sales, but those expensive homes can have a large effect on averages and error metrics.
- Two houses with similar square footage, bedrooms, bathrooms, and lot size can sell for very different prices because of city, ZIP code, school district, neighborhood, views, and access to jobs or amenities.
- Listing data is imperfect. Fields can be missing, inconsistent, entered in different formats, or contain implausible values. Location fields and optional features such as garage space or lot size are not always complete.
- Luxury and unusual homes are relatively sparse and idiosyncratic. The model has fewer comparable examples from which to learn, so prediction errors can grow at the high end.
- Housing markets also change over time. Interest rates, inventory, seasonality, and local demand mean that a model evaluated on a random sample may appear stronger than it will be on future sales.

### How the problem shaped our modeling choices

- experimented with modeling the logarithm of `ClosePrice`. This reduces the influence of the longest part of the price tail and makes the model focus more on relative error across price levels.
- We included both property characteristics and detailed location features, including county, latitude and longitude, ZIP code, city, MLS area, and school district.
- We used a time-based holdout: Using the most recent month as the test set. This better represents the real task of predicting a future month.
- We compare models with R², MAPE,, MdAPE instead of relying on one number. MdAPE is our headline measure of typical accuracy because it is less distorted by unusual luxury sales.

### Suggested transition

> Because price relationships are nonlinear, location-dependent, and affected by outliers, we did not assume that one model family would automatically be best. We tested models ranging from a simple linear baseline to advanced gradient-boosting methods.

## 2. Models Explored

All model families were ultimately evaluated on the same time-based train/test window. The main comparison used the expanded feature set; LightGBM and CatBoost were also tested with their native categorical handling.

| Model | Why it was a reasonable candidate | What it helped us learn |
|---|---|---|
| Linear Regression | Simple, fast, and interpretable; provides a baseline for deciding whether model complexity is justified. | How much of price can be explained by an additive, approximately linear relationship. |
| Decision Tree | Captures nonlinear thresholds and feature interactions without requiring a linear relationship. | Whether rules such as location and size splits can improve on the baseline. |
| Random Forest | Averages many trees to reduce the instability and overfitting of a single decision tree. | Whether a bagged tree ensemble can capture nonlinear housing patterns more reliably. |
| XGBoost | Sequentially corrects earlier tree errors and is strong on structured tabular data. | Whether tuned gradient boosting can improve accuracy while handling complex interactions. |
| LightGBM | Efficient gradient boosting that handles large tabular datasets and complex splits well. | Whether a faster boosting method, especially with native categorical features, improves performance. |
| CatBoost | Designed to handle categorical variables effectively and reduce common categorical-encoding problems. | Whether direct treatment of high-cardinality location fields is better than one-hot encoding. |

### Important comparison detail
- Testing simpler and more complex models gave us a useful progression: linear baseline → individual tree → bagged trees → boosted trees → native categorical boosting.

### Suggested transition

> The boosted models were substantially stronger than the linear and single-tree baselines.

