import streamlit as st
import pandas as pd

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
# TITLE
# -------------------------
st.title("🚑 Smart Ambulance Demand & Allocation System")

# -------------------------
# TABS (4 TABS)
# -------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Demand Prediction",
    "🚨 Allocation System",
    "📍 Emergency Insights",
    "⚡ Surge Prediction"
])

# =====================================================
# 📊 TAB 1 - DEMAND PREDICTION
# =====================================================
with tab1:

    st.header("Demand Prediction")

    col1, col2 = st.columns(2)

    with col1:
        hour = st.slider("Hour", 0, 23, 12)
        traffic = st.selectbox("Traffic Level", ["Low", "Medium", "High"])
        temp = st.slider("Temperature", 10, 50, 30)

    with col2:
        rain = st.selectbox("Rain", ["No", "Yes"])
        emergency = st.selectbox("Emergency Type", ["Accident", "Heart Attack", "Fire", "Other"])
        day_name = st.selectbox(
            "Day of Week",
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        )

    traffic_map = {"Low": 5, "Medium": 10, "High": 20}
    rain_map = {"No": 0, "Yes": 15}
    emergency_map = {
        "Accident": 15,
        "Heart Attack": 25,
        "Fire": 30,
        "Other": 5
    }
    day_map = {
        "Monday": 5,
        "Tuesday": 5,
        "Wednesday": 5,
        "Thursday": 5,
        "Friday": 10,
        "Saturday": 15,
        "Sunday": 15
    }

    if st.button("Predict Demand"):

        score = (
            hour +
            traffic_map[traffic] +
            temp +
            rain_map[rain] +
            emergency_map[emergency] +
            day_map[day_name]
        )

        if score > 120:
            st.error("🔴 HIGH DEMAND 🚑")
        elif score > 80:
            st.warning("🟡 MEDIUM DEMAND")
        else:
            st.success("🟢 LOW DEMAND")

# =====================================================
# 🚨 TAB 2 - ALLOCATION SYSTEM
# =====================================================
with tab2:

    st.header("Ambulance Allocation")

    priority = st.selectbox("Priority Level", ["Low", "Medium", "High"])
    traffic = st.selectbox("Traffic", ["Low", "Medium", "High"])

    if st.button("Find Ambulance"):

        base_ambulance = {
            "Low": 1,
            "Medium": 2,
            "High": 4
        }

        traffic_delay = {
            "Low": 5,
            "Medium": 10,
            "High": 20
        }

        st.metric("🚑 Ambulances Required", base_ambulance[priority])
        st.metric("⏱️ Response Time (mins)", 10 + traffic_delay[traffic])
        st.metric("🚦 Traffic Level", traffic)
        st.metric("⚡ Priority", priority)

# =====================================================
# 📍 TAB 3 - EMERGENCY INSIGHTS
# =====================================================
with tab3:

    st.header("Emergency Insights Dashboard")

    emergency = st.selectbox("Select Emergency Type", df['emergency_type'].unique())

    if st.button("Analyze"):

        data = df[df['emergency_type'] == emergency]

        total_cases = len(data)
        avg_temp = data['temperature'].mean()

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Total Cases", total_cases)

        with col2:
            st.metric("Avg Temperature", round(avg_temp, 2))

        if avg_temp > 30:
            st.error("High Risk Area")
        else:
            st.dataframe(data.head(10))

# =====================================================
# ⚡ TAB 4 - SURGE PREDICTION (NEW FEATURE)
# =====================================================
with tab4:

    st.header("⚡ Emergency Surge Prediction")

    col1, col2 = st.columns(2)

    with col1:
        past = st.number_input("Past 1 Hour Demand", value=5)
        traffic = st.slider("Traffic Level", 0.0, 1.0, 0.5)

    with col2:
        hour = st.slider("Hour", 0, 23, 12)

    peak_hour = 1 if (8 <= hour <= 11 or 17 <= hour <= 21) else 0

    def detect_surge(past_demand, traffic, peak_hour):
        surge_score = (past_demand * 1.5) + (traffic * 50) + (peak_hour * 30)

        if surge_score > 120:
            return "HIGH SURGE ⚠️"
        elif surge_score > 80:
            return "MEDIUM SURGE"
        else:
            return "NO SURGE"

    if st.button("Predict Surge"):

        result = detect_surge(past, traffic, peak_hour)

        st.subheader("⚡ Result")

        if "HIGH" in result:
            st.error(result)
        elif "MEDIUM" in result:
            st.warning(result)
        else:
            st.success(result)