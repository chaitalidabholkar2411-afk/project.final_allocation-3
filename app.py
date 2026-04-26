import streamlit as st
import pandas as pd
import numpy as np
import pickle

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(layout="wide")

# -------------------------
# LOAD DATASET
# -------------------------
df = pd.read_csv("notebook/ambulance_updated_dataset (3).csv")
df.columns = df.columns.str.strip()

# -------------------------
# LOAD MODEL + SCALER
# -------------------------
with open("notebook/model.pkl", "rb") as f:
    model = pickle.load(f)

with open("notebook/scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

# -------------------------
# TITLE
# -------------------------
st.title("🚑 Smart Ambulance Demand & Allocation System")

# -------------------------
# TABS (TAB 4 REMOVED)
# -------------------------
tab1, tab2, tab3 = st.tabs([
    "📊 Demand Prediction",
    "🚨 Allocation System",
    "📍 Emergency Insights"
])

# =====================================================
# 📊 TAB 1 - DEMAND PREDICTION (LAT/LON ADDED)
# =====================================================
with tab1:

    st.header("Demand Prediction (ML Model)")

    col1, col2 = st.columns(2)

    with col1:
        latitude = st.number_input("Latitude", value=40.2)
        longitude = st.number_input("Longitude", value=-75.3)
        hour = st.slider("Hour", 0, 23, 12)
        traffic = st.slider("Traffic (0-1)", 0.0, 1.0, 0.5)
        temperature = st.slider("Temperature", 10, 50, 30)

    with col2:
        emergency_type = st.number_input("Emergency Type (encoded)", value=1)
        datetime_val = st.number_input("Datetime (encoded)", value=10)
        day = st.number_input("Day (encoded)", value=2)
        month = st.number_input("Month", value=5)
        priority = st.number_input("Priority (encoded)", value=1)

    if st.button("Predict Demand 🚨"):

        # -------------------------
        # 10 FEATURES INPUT (FIXED ORDER)
        # -------------------------
        input_data = np.array([[
            latitude,
            longitude,
            hour,
            traffic,
            temperature,
            emergency_type,
            datetime_val,
            day,
            month,
            priority
        ]])

        input_scaled = scaler.transform(input_data)
        demand = model.predict(input_scaled)[0]

        if demand == 1 and traffic > 0.7:
            st.error("🔴 HIGH DEMAND 🚑")
        elif demand == 1:
            st.warning("🟡 MEDIUM DEMAND")
        else:
            st.success("🟢 LOW DEMAND")

# =====================================================
# 🚨 TAB 2 - ALLOCATION SYSTEM
# =====================================================
with tab2:

    st.header("Ambulance Allocation")

    priority2 = st.selectbox("Priority Level", ["Low", "Medium", "High"])
    traffic2 = st.selectbox("Traffic", ["Low", "Medium", "High"])

    if st.button("Find Ambulance"):

        base_ambulance = {"Low": 1, "Medium": 2, "High": 4}
        traffic_delay = {"Low": 5, "Medium": 10, "High": 20}

        st.metric("🚑 Ambulances Required", base_ambulance[priority2])
        st.metric("⏱️ Response Time", 10 + traffic_delay[traffic2])
        st.metric("🚦 Traffic", traffic2)
        st.metric("⚡ Priority", priority2)

# =====================================================
# 📍 TAB 3 - EMERGENCY INSIGHTS
# =====================================================
with tab3:

    st.header("Emergency Insights")

    emergency3 = st.selectbox(
        "Select Emergency Type",
        df['emergency_type'].unique()
    )

    if st.button("Analyze"):

        data = df[df['emergency_type'] == emergency3]

        st.metric("Total Cases", len(data))
        st.metric("Avg Temperature", round(data['temperature'].mean(), 2))

        st.dataframe(data.head(10))