import streamlit as st
import pandas as pd
from utils import recommend_action, load_models

model_state, model_intensity = load_models()

st.set_page_config(page_title="MoodGuide AI", layout="wide")

st.title("🧠 MoodGuide AI")
st.markdown("Understand your mood and get smart suggestions")

st.sidebar.header("Your Inputs")

journal_text = st.sidebar.text_area("How are you feeling?")

# Inputs
ambience_type = st.sidebar.selectbox("Ambience", ["home", "office", "outdoor"])
previous_day_mood = st.sidebar.selectbox("Yesterday Mood", ["happy","neutral","sad"])
face_emotion_hint = st.sidebar.selectbox("Face Emotion", ["happy","neutral","sad","unknown"])
reflection_quality = st.sidebar.selectbox("Reflection Quality", ["low","medium","high"])

duration_min = st.sidebar.slider("Activity Duration (min)", 0, 180, 30)
sleep_hours = st.sidebar.slider("Sleep Hours", 0, 12, 7)
energy_level = st.sidebar.slider("Energy Level", 1, 5, 3)
stress_level = st.sidebar.slider("Stress Level", 1, 5, 3)
time_of_day = st.sidebar.selectbox("Time of Day", ["morning","afternoon","evening","night"])

if st.button("Analyze"):

    # Prevent empty input
    if journal_text.strip() == "":
        st.warning("Please write something about your day")
        st.stop()

    input_df = pd.DataFrame([{
        "journal_text": journal_text,
        "ambience_type": ambience_type,
        "previous_day_mood": previous_day_mood,
        "face_emotion_hint": face_emotion_hint,
        "reflection_quality": reflection_quality,
        "duration_min": duration_min,
        "sleep_hours": sleep_hours,
        "energy_level": energy_level,
        "stress_level": stress_level,
        "time_of_day": time_of_day
    }])

    state = model_state.predict(input_df)[0]
    intensity = model_intensity.predict(input_df)[0]

    action, timing, confidence, note = recommend_action(
        state, intensity, energy_level, stress_level, time_of_day, sleep_hours
    )

    # 🔹 Mood Analysis
    st.subheader("🧾 Mood Analysis")
    st.write(f"State: {state}")
    st.write(f"Intensity: {intensity}")
    st.progress(float(confidence))

    # ✅ STATUS MESSAGE (FIXED POSITION)
    if state in ["calm", "focused"]:
        st.success("🟢 You are in a positive state")
    elif state in ["restless", "mixed"]:
        st.warning("🟡 Slight mental fluctuation detected")
    else:
        st.error("🔴 High emotional load detected")

    # 🔹 Recommendation
    st.subheader("🧭 What you can do")
    st.write(f"👉 {action}")
    st.write(f"⏰ {timing}")

    # 🔹 Suggestion
    st.subheader("💬 Suggestion")
    st.info(note)