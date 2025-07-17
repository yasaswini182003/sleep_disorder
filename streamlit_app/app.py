import streamlit as st
import requests
import json
from streamlit_lottie import st_lottie
from PIL import Image
image=Image.open("sleep image.png")
st.image(image,use_container_width=True)

# -----------------------------
# Function to load lottie animation
# -----------------------------
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# -----------------------------
# Page Config and Styling
# -----------------------------
st.set_page_config(page_title="Sleep Disorder Predictor", page_icon="🛌", layout="centered")

# Background style
st.markdown("""
    <style>
    .main {
        background: linear-gradient(145deg, #e0f7fa, #fce4ec);
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# Lottie Animation
# -----------------------------
lottie_sleep = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_8wREpI.json")
st_lottie(lottie_sleep, speed=1, reverse=False, loop=True, quality="high", height=200)

# -----------------------------
# Title
# -----------------------------
st.markdown("<h1 style='text-align: center; color: #4a148c;'>🌙 Sleep Disorder Prediction App</h1>", unsafe_allow_html=True)
st.markdown("##### _Enter the patient's lifestyle and health metrics below to predict their sleep disorder._")

# -----------------------------
# Input Form
# -----------------------------
with st.form("predict_form"):
    st.subheader("💡 Patient Details")
    col1, col2 = st.columns(2)

    with col1:
        gender = st.selectbox("🧍 Gender", ["Male", "Female"])
        age = st.number_input("🎂 Age", min_value=18, max_value=100, value=30)
        occupation = st.selectbox("💼 Occupation", [
            "Doctor", "Engineer", "Nurse", "Teacher", "Lawyer", "Accountant",
            "Salesperson", "Scientist", "Software Engineer", "Sales Representative", "Manager"
        ])
        bmi_category = st.selectbox("📊 BMI Category", ["Normal", "Overweight", "Obese", "Normal Weight"])
        heart_rate = st.number_input("❤️ Heart Rate (bpm)", min_value=40, max_value=120, value=70)
        sleep_duration = st.number_input("🕒 Sleep Duration (hrs)", min_value=0.0, max_value=24.0, value=7.0, step=0.1)

    with col2:
        quality_of_sleep = st.number_input("🌟 Quality of Sleep (1-10)", min_value=1, max_value=10, value=7)
        physical_activity = st.number_input("🏃 Physical Activity Level (0-100)", min_value=0, max_value=100, value=60)
        stress_level = st.number_input("😰 Stress Level (1-10)", min_value=1, max_value=10, value=5)
        daily_steps = st.number_input("👣 Daily Steps", min_value=1000, max_value=20000, value=7000)
        systolic_bp = st.number_input("🩺 Systolic BP", min_value=90, max_value=200, value=130)
        diastolic_bp = st.number_input("🩸 Diastolic BP", min_value=60, max_value=120, value=85)

    submit = st.form_submit_button("🔍 Predict")

# -----------------------------
# Prediction
# -----------------------------
if submit:
    st.markdown("---")
    with st.spinner("Predicting Sleep Disorder...⏳"):
        input_data = {
            "Gender": gender,
            "Age": age,
            "Occupation": occupation,
            "Sleep_Duration": sleep_duration,
            "Quality_of_Sleep": quality_of_sleep,
            "Physical_Activity_Level": physical_activity,
            "Stress_Level": stress_level,
            "BMI_Category": bmi_category,
            "Heart_Rate": heart_rate,
            "Daily_Steps": daily_steps,
            "Systolic_BP": systolic_bp,
            "Diastolic_BP": diastolic_bp
        }

        try:
            response = requests.post("http://localhost:8000/predict", json=input_data)
            prediction = response.json()["predicted_sleep_disorder"]
            st.success(f"✅ Predicted Sleep Disorder: **{prediction}**")
        except Exception as e:
            st.error("❌ Could not connect to FastAPI server. Make sure it is running at `localhost:8000`.")
