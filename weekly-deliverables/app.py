"""Streamlit app: predicts a California home's close price with the trained CatBoost model."""

import joblib
import numpy as np
import pandas as pd
import streamlit as st

MODEL_PATH = "../models/catboost_price_model.pkl"
METADATA_PATH = "../models/catboost_price_model_metadata.pkl"

st.set_page_config(page_title="CA Home Price Predictor", page_icon="🏡", layout="centered")


@st.cache_resource
def load_model():
    pipeline = joblib.load(MODEL_PATH)
    metadata = joblib.load(METADATA_PATH)
    return pipeline, metadata


pipeline, metadata = load_model()
numeric_ranges = metadata["numeric_ranges"]
feature_choices = metadata["feature_choices"]

st.markdown(
    """
    <style>
    .main .block-container {padding-top: 2.5rem; max-width: 760px;}
    div[data-testid="stMetricValue"] {font-size: 2.75rem; color: #1f6f4a;}
    .price-card {
        background: linear-gradient(135deg, #f0faf5 0%, #e6f5ee 100%);
        border: 1px solid #cdeee0;
        border-radius: 14px;
        padding: 1.5rem 2rem;
        margin-top: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🏡 California Home Price Predictor")
st.caption(
    "Estimates a residential close price from a CatBoost model trained on CRMLS sales data. "
    f"Test-set performance: R² {metadata['test_r2']:.3f} · MAPE {metadata['test_mape']:.1%} · "
    f"MAE ${metadata['test_mae']:,.0f}"
)

st.divider()

with st.form("prediction_form"):
    st.subheader("Property details")

    col1, col2 = st.columns(2)
    with col1:
        living_area = st.number_input(
            "Living area (sq ft)", min_value=200, max_value=15000,
            value=int(numeric_ranges["LivingArea"]["median"]), step=50,
        )
        bedrooms = st.number_input(
            "Bedrooms", min_value=1, max_value=15,
            value=int(numeric_ranges["BedroomsTotal"]["median"]), step=1,
        )
        bathrooms = st.number_input(
            "Bathrooms", min_value=0, max_value=15,
            value=int(numeric_ranges["BathroomsTotalInteger"]["median"]), step=1,
        )
        garage_spaces = st.number_input(
            "Garage spaces", min_value=0, max_value=10,
            value=int(numeric_ranges["GarageSpaces"]["median"]), step=1,
        )
    with col2:
        lot_size = st.number_input(
            "Lot size (sq ft)", min_value=0, max_value=200000,
            value=int(numeric_ranges["LotSizeSquareFeet"]["median"]), step=100,
        )
        year_built = st.number_input(
            "Year built", min_value=1800, max_value=2026,
            value=int(numeric_ranges["YearBuilt"]["median"]), step=1,
        )
        pool = st.selectbox("Pool", feature_choices["PoolPrivateYN"])
        view = st.selectbox("View", feature_choices["ViewYN"])

    col3, col4 = st.columns(2)
    with col3:
        fireplace = st.selectbox("Fireplace", feature_choices["FireplaceYN"])
        new_construction = st.selectbox("New construction", feature_choices["NewConstructionYN"])
    with col4:
        hoa = st.selectbox("Has association fee (HOA)", feature_choices["HasAssociationFee"])
        county = st.selectbox("County", feature_choices["CountyOrParish"], index=0)

    st.subheader("Location")
    col5, col6 = st.columns(2)
    with col5:
        city = st.selectbox("City", feature_choices["City"])
        postal_code = st.selectbox("Postal code", feature_choices["PostalCode"])
    with col6:
        district = st.selectbox("School district", feature_choices["DistrictName"])
        mls_area = st.selectbox("MLS area", feature_choices["MLSAreaMajor"])

    col7, col8 = st.columns(2)
    with col7:
        latitude = st.number_input(
            "Latitude", value=round(numeric_ranges["Latitude"]["median"], 4), format="%.4f"
        )
    with col8:
        longitude = st.number_input(
            "Longitude", value=round(numeric_ranges["Longitude"]["median"], 4), format="%.4f"
        )

    submitted = st.form_submit_button("Predict price", use_container_width=True)

if submitted:
    input_row = {
        "LivingArea": living_area,
        "LotSizeSquareFeet": lot_size,
        "BedroomsTotal": bedrooms,
        "BathroomsTotalInteger": bathrooms,
        "YearBuilt": year_built,
        "GarageSpaces": garage_spaces,
        "Latitude": latitude,
        "Longitude": longitude,
        "PoolPrivateYN": pool,
        "ViewYN": view,
        "FireplaceYN": fireplace,
        "NewConstructionYN": new_construction,
        "HasAssociationFee": hoa,
        "CountyOrParish": county,
        "PostalCode": postal_code,
        "City": city,
        "DistrictName": district,
        "MLSAreaMajor": mls_area,
    }
    input_df = pd.DataFrame([input_row])
    pred_log = pipeline.predict(input_df)[0]
    predicted_price = float(np.exp(pred_log)) if metadata["log_target"] else float(pred_log)

    st.markdown('<div class="price-card">', unsafe_allow_html=True)
    st.metric("Predicted close price", f"${predicted_price:,.0f}")
    st.markdown("</div>", unsafe_allow_html=True)
