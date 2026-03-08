import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="MedCentral AI", layout="wide")

# ---------- CSS FIX ----------
st.markdown("""
<style>

/* MAIN BACKGROUND */
.stApp {
    background-color:#eef2f7;
}

/* SIDEBAR BACKGROUND */
[data-testid="stSidebar"]{
    background-color:#0B2545;
}

/* SIDEBAR TITLE */
[data-testid="stSidebar"] h1{
    color:white;
    font-size:24px;
}

/* SIDEBAR RADIO TEXT */
[data-testid="stSidebar"] span{
    color:white !important;
    font-size:18px !important;
    font-weight:600;
}

/* SEARCH BAR */
.stTextInput input{
    background-color:white;
    color:black;
    border-radius:20px;
}

/* CARD STYLE */
.card{
    padding:25px;
    border-radius:15px;
    font-size:20px;
    font-weight:600;
    color:black;
}

/* CARD VALUE */
.card-value{
    font-size:28px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)



st.sidebar.title("🏥 MedCentral AI")

menu = st.sidebar.radio(
    "",
    ["📊 Dashboard","👨‍⚕️ Patients","🛏 Resources","👩‍⚕️ Staff"]
)



col1,col2 = st.columns([8,1])

with col1:
    st.text_input("",placeholder="🔎 Search patient, doctor, ward...")

with col2:
    st.markdown("### 🔔")

st.markdown("<h1 style='text-align:center;color:#1f2c3c;'>AI Hospital Resource Management Dashboard</h1>",unsafe_allow_html=True)

# ---------- KPI CARDS ----------

c1,c2,c3,c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class="card" style="background:#4e73df;">
    👥 Current Patients
    <div class="card-value">120</div>
    </div>
    """,unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="card" style="background:#1cc88a;">
    🛏 Available Beds
    <div class="card-value">80</div>
    </div>
    """,unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="card" style="background:#f6c23e;">
    ⏱ Avg ER Wait Time
    <div class="card-value">30 min</div>
    </div>
    """,unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="card" style="background:#36b9cc;">
    👩‍⚕️ Active Staff
    <div class="card-value">60</div>
    </div>
    """,unsafe_allow_html=True)

st.write("")



st.subheader("📈 Patient Inflow")

data = pd.DataFrame({
"Day":["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
"Patients":[115,120,150,108,135,122,140]
})

fig = px.line(
    data,
    x="Day",
    y="Patients",
    markers=True,
    template="plotly_white"
)

st.plotly_chart(fig,use_container_width=True)