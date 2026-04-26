import streamlit as st
import pandas as pd
import numpy as np
import pickle

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(layout="wide")

# -------------------------
# AESTHETIC DARK UI
# -------------------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: radial-gradient(circle at top, #0f2027, #203a43, #2c5364);
}

/* Title */
h1 {
    text-align: center;
    color: #00e5ff;
    font-weight: 800;
    text-shadow: 2px 2px 10px #000;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background-color: rgba(0, 229, 255, 0.1);
    border-radius: 12px;
    padding: 5px;
}

.stTabs [data-baseweb="tab"] {
    color: white;
    font-weight: bold;
}

.stTabs [aria-selected="true"] {
    background-color: #00e5ff !important;
    color: black !important;
    border-radius: 10px;
}

/* Buttons */
div.stButton > button {
    background: linear-gradient(90deg, #00e5ff, #00bcd4);
    color: black;
    border-radius: 12px;
    padding: 10px;
    font-weight: bold;
    border: none;
    box-shadow: 0px 0px 10px #00e5ff;
}

div.stButton > button:hover {
    transform: scale(1.05);
}

/* Metrics */
[data-testid="stMetric"] {
    background: rgba(0, 229, 255, 0.1);
    border: 1px solid #00e5ff;
    padding: 15px;
    border-radius: 15px;
    box-shadow: 0px 0px 10px #00e5ff;
}

/* Inputs */
input, select {
    background-color: rgba(0,0,0,0.3) !important;
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# LOAD DATA
# -------------------------
df = pd.read_csv("notebook/ambulance_updated_dataset (3).csv")
df.columns = df.columns.str.strip()

# -------------------------
# LOAD MODEL
# -------------------------
with open("notebook/model.pkl", "rb") as f:
    model = pickle.load(f)

with open("notebook/scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

# -------------------------
# TITLE
# -------------------------
st.title("🚑 Smart Ambulance AI System")

# -------------------------
# TABS
# -------------------------
tab1, tab2, tab3 = st.tabs([
    "📊 Demand Prediction",
    "🚨 Allocation System",
    "📍 Emergency Insights"
])

# =====================================================
# TAB 1 - ML PREDICTION
# =====================================================
with tab1:

    st.header("AI Demand Prediction")

    col1, col2 = st.columns(2)

    with col1:
        latitude = st.number_input("Latitude", value=40.2)
        longitude = st.number_input("Longitude", value=-75.3)
        hour = st.slider("Hour", 0, 23, 12)
        traffic = st.slider("Traffic (0-1)", 0.0, 1.0, 0.5)
        temperature = st.slider("Temperature", 10, 50, 30)

    with col2:
        emergency_type = st.number_input("Emergency Type", value=1)
        datetime_val = st.number_input("Datetime", value=10)
        day = st.number_input("Day", value=2)
        month = st.number_input("Month", value=5)
        priority = st.number_input("Priority", value=1)

    if st.button("Predict Demand 🚨"):

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
            st.write("Ambulances Needed: 3")
        elif demand == 1:
            st.warning("🟡 MEDIUM DEMAND")
            st.write("Ambulances Needed: 2")
        else:
            st.success("🟢 LOW DEMAND")
            st.write("Ambulances Needed: 1")

# =====================================================
# TAB 2 - ALLOCATION
# =====================================================
with tab2:

    st.header("Ambulance Allocation System")

    priority2 = st.selectbox("Priority", ["Low", "Medium", "High"])
    traffic2 = st.selectbox("Traffic", ["Low", "Medium", "High"])

    if st.button("Find Ambulance 🚑"):

        base = {"Low": 1, "Medium": 2, "High": 4}
        delay = {"Low": 5, "Medium": 10, "High": 20}

        st.metric("Ambulances", base[priority2])
        st.metric("Response Time", 10 + delay[traffic2])
        st.metric("Traffic", traffic2)
        st.metric("Priority", priority2)

# =====================================================
# TAB 3 - INSIGHTS
# =====================================================
with tab3:

    st.header("Emergency Insights")

    emergency3 = st.selectbox(
        "Emergency Type",
        df['emergency_type'].unique()
    )

    if st.button("Analyze 📊"):

        data = df[df['emergency_type'] == emergency3]

        st.metric("Total Cases", len(data))
        st.metric("Avg Temperature", round(data['temperature'].mean(), 2))

        st.dataframe(data.head(10))