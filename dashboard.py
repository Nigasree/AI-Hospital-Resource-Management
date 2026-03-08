import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import mysql.connector
import joblib
import random
from streamlit_autorefresh import st_autorefresh

from fetch_weather import get_weather_data
from fetch_traffic import get_traffic_data


st.set_page_config(page_title="AI Hospital Dashboard", layout="wide")


# AUTO REFRESH
st_autorefresh(interval=5000, key="datarefresh")


connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="hospital_ai"
)

data = pd.read_sql(
    "SELECT * FROM hospital_dataset ORDER BY date DESC LIMIT 50",
    connection
)

connection.close()


model = joblib.load("hospital_prediction_model.pkl")


# REALTIME DATA

weather = get_weather_data()
traffic = get_traffic_data()



# DYNAMIC PATIENT SIMULATION

base_patients = int(data["patient_count"].iloc[0])

if "dynamic_patients" not in st.session_state:
    st.session_state.dynamic_patients = base_patients

st.session_state.dynamic_patients += random.randint(-3, 6)

if st.session_state.dynamic_patients < 0:
    st.session_state.dynamic_patients = base_patients

current_patients = st.session_state.dynamic_patients


# HOSPITAL STATUS
TOTAL_BEDS = 200
available_beds = TOTAL_BEDS - current_patients

wait_time = int(current_patients * 0.25)
active_staff = int(current_patients * 0.5)



# UI STYLE (PREMIUM THEME)

st.markdown("""
<style>

/* --- MAIN APP BACKGROUND --- */
[data-testid="stAppViewContainer"]{
    background: #e2e8f0; /* Soft light gray-blue, absolutely no white */
}

/* --- EXPLICIT FONT COLORS --- */
p, label, li, [data-testid="stMetricLabel"] { 
    color: #0f172a !important; /* Almost black / deep slate */
}

h1, .title { 
    color: #1d4ed8 !important; /* Royal Blue (replaced pink/violet) */
}

h2 { 
    color: #ea580c !important; /* Deep Orange */
}

h3 { 
    color: #047857 !important; /* Emerald Green */
}

[data-testid="stMetricValue"] { 
    color: #dc2626 !important; /* Crimson Red */
}

[data-testid="stDataFrame"] { 
    color: #0f172a !important; 
}

/* --- UPGRADED SIDEBAR --- */
section[data-testid="stSidebar"]{
    background: #1e293b; /* Premium dark slate */
    border-right: 2px solid #cbd5e1;
}

section[data-testid="stSidebar"] *{
    color: #f1f5f9 !important; /* Soft off-gray instead of bright white */
}

/* Styling the radio menu items in the sidebar */
.stRadio > div[role="radiogroup"] > label {
    background: #334155;
    padding: 12px 15px;
    border-radius: 10px;
    margin-bottom: 8px;
    transition: all 0.3s ease;
}

.stRadio > div[role="radiogroup"] > label:hover {
    background: #475569;
}

/* --- TITLE & CONTAINERS --- */
.title{
    text-align:center;
    font-size:36px;
    font-weight:700;
    margin-bottom:20px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* --- METRIC CARDS --- */
.card{
    padding:25px;
    border-radius:16px;
    color: #f1f5f9 !important; /* Soft off-gray */
    font-size:24px;
    font-weight:600;
    text-align: center;
    box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
    border: 1px solid rgba(255,255,255,0.1);
}

.blue{ background: linear-gradient(135deg, #1e3a8a, #3b82f6); }
.green{ background: linear-gradient(135deg, #064e3b, #10b981); }
.orange{ background: linear-gradient(135deg, #7c2d12, #f59e0b); }
.red{ background: linear-gradient(135deg, #7f1d1d, #ef4444); }

/* --- SECTIONS (REPLACED WHITE BACKGROUND) --- */
.section{
    background: #cbd5e1; /* Smooth slate, no white */
    padding:25px;
    border-radius:16px;
    margin-top:20px;
    box-shadow: inset 0 2px 4px 0 rgba(0,0,0,0.06);
    border: 1px solid #94a3b8;
}

</style>
""", unsafe_allow_html=True)

st.sidebar.title("🏥 MedCentral AI")

page = st.sidebar.radio(
    "",
    ["📊 Dashboard","🧑 Patients","🛏 Resources","👨‍⚕️ Staff"]
)


# ---------------------------------------------------------
# TOP BAR
# ---------------------------------------------------------

c1,c2,c3 = st.columns([1,4,1])

with c2:
    st.text_input(
        "Search",
        placeholder="🔎 Search patient, doctor, ward",
        label_visibility="collapsed"
    )

with c3:
    st.markdown("### 🔔")


if page == "📊 Dashboard":

    st.markdown("<div class='title'>AI Hospital Resource Management Dashboard</div>", unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="card blue">
        Current Patients<br><br>
        {current_patients}
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="card green">
        Available Beds<br><br>
        {available_beds}
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="card orange">
        Avg ER Wait Time<br><br>
        {wait_time} min
        </div>
        """, unsafe_allow_html=True)

    with c4:

        alert_color = "red" if available_beds < 20 else "green"

        st.markdown(f"""
        <div class="card {alert_color}">
        Active Staff<br><br>
        {active_staff}
        </div>
        """, unsafe_allow_html=True)



    st.markdown("<div class='section'>", unsafe_allow_html=True)

    st.subheader("Hospital Activity")

    chart_data = data.sort_values("date").tail(10).copy()

    trend = []
    value = current_patients

    for i in range(len(chart_data)):
        value += random.randint(-4,6)
        if value < 0:
            value = 0
        trend.append(value)

    chart_data["patient_count"] = trend

    col1, col2 = st.columns(2)

    with col1:

        area_chart = px.area(
            chart_data,
            x="date",
            y="patient_count",
            title="Patient Inflow Trend",
            color_discrete_sequence=["#2563eb"]
        )
        
        # Transparent background for charts to match the new UI
        area_chart.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(area_chart, use_container_width=True)

    with col2:

        bar_chart = px.bar(
            chart_data,
            x="date",
            y="patient_count",
            title="Daily Patient Load",
            color="patient_count",
            color_continuous_scale="Blues"
        )
        
        # Transparent background for charts to match the new UI
        bar_chart.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(bar_chart, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)


    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=current_patients,
        title={'text': "Hospital Capacity"},
        gauge={
            'axis': {'range': [None, 200]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 100], 'color': "lightgreen"},
                {'range': [100, 160], 'color': "yellow"},
                {'range': [160, 200], 'color': "red"}
            ]
        }
    ))
    
    gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': "#0f172a"})
    st.plotly_chart(gauge, use_container_width=True)



    st.markdown("<div class='section'>", unsafe_allow_html=True)

    st.subheader("Environmental Signals")

    c1,c2 = st.columns(2)

    with c1:
        st.metric("Temperature",f"{weather['temperature']} °C")

    with c2:
        st.metric("Traffic Risk",traffic)

    st.markdown("</div>", unsafe_allow_html=True)




elif page == "🧑 Patients":

    st.title("Patient Records")

    st.dataframe(data,use_container_width=True)


elif page == "🛏 Resources":

    st.title("Hospital Resources")

    st.metric("Total Beds",200)
    st.metric("Available Beds",available_beds)

    progress_value = max(0, min(current_patients/200,1))
    st.progress(progress_value)



elif page == "👨‍⚕️ Staff":

    st.title("Staff Allocation")

    doctors_required = int(current_patients/10)
    nurses_required = int(current_patients/5)

    staff_df = pd.DataFrame({
        "Role":["Doctors","Nurses","Technicians"],
        "Required":[doctors_required,nurses_required,int(current_patients/8)]
    })

    st.dataframe(staff_df,use_container_width=True)

    st.subheader("AI Patient Forecast")

    input_data = pd.DataFrame([{
        "temperature":weather["temperature"],
        "rainfall":weather["rainfall"],
        "accident_reports":traffic,
        "disease_cases":10,
        "emergency_cases":20,
        "waiting_time_minutes":30,
        "day_of_week":2,
        "month":4
    }])

    prediction = model.predict(input_data)

    st.metric("Predicted Incoming Patients",int(prediction[0]))
