import os
import joblib

def load_models():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_state = joblib.load(os.path.join(BASE_DIR, "outputs/model_state.pkl"))
    model_intensity = joblib.load(os.path.join(BASE_DIR, "outputs/model_intensity.pkl"))
    return model_state, model_intensity


def recommend_action(state, intensity, energy, stress, time_of_day, sleep):

    # Default
    action = "Take a small pause and reflect"
    timing = "later today"
    confidence = 0.6

    # Low sleep override
    if sleep < 5:
        return "Rest or take a short nap 😴", "as soon as possible", 0.8, \
               "You seem low on rest. Recovery should come first."

    # High stress
    if stress >= 4 or state == "overwhelmed":
        return "Try deep breathing or a short walk 🌬🚶", "now", 0.85, \
               "Your system looks overloaded. Slow things down."

    # Low energy
    if energy <= 2:
        return "Light stretching or relaxing activity 🧘", "within 30 mins", 0.7, \
               "Your energy is low. Avoid pushing too hard."

    # Productive state
    if state in ["focused", "calm"] and energy >= 3:
        return "Start a focused task or deep work 💻", "now", 0.9, \
               "You're in a good state to be productive."

    # Restless / mixed
    if state in ["restless", "mixed"]:
        return "Go for movement or grounding 🌱🚶", "soon", 0.65, \
               "You might benefit from resetting your mind."

    # Night logic
    if time_of_day == "night":
        return "Wind down with journaling or reading 📓", "tonight", 0.75, \
               "End your day calmly."

    return action, timing, confidence, "Take it step by step."