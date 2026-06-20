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
