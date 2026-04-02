

import pandas as pd
import os

#DECISION ENGIN
def decision_engine(row):

    state = row['predicted_state']
    intensity = row['predicted_intensity']
    stress = row['stress_level']
    energy = row['energy_level']
    time_of_day = row['time_of_day']
    sleep = row['sleep_hours']

    #Handling missing values 
    if pd.isna(stress): stress = 3
    if pd.isna(energy): energy = 3
    if pd.isna(time_of_day): time_of_day = "afternoon"

    # 1 State Group
    if state in ['calm', 'focused']:
        state_group = "productive_state"
    elif state in ['restless', 'mixed']:
        state_group = "active_mind_state"
    elif state == 'overwhelmed':
        state_group = "high_load_state"
    else:
        state_group = "baseline_state"

    # 2.Support Level
    if intensity >= 4 or stress >= 4:
        support_level = "needs_support"
    elif intensity == 3 or stress == 3:
        support_level = "balanced"
    else:
        support_level = "stable"

    # 3.Energy Actions
    if energy <= 2:
        energy_action = "rest 😌 / breathing 🌬 / reflection 📝"
    elif energy == 3:
        energy_action = "grounding 🌱 / light stretch 🤸 / yoga nidra 🧘"
    else:
        energy_action = "deep work 💻 / movement 🚶 / goal setting 🎯"

    # 4.Time-based Actions
    if time_of_day == "early_morning":
        time_action = "gratitude 🙏 + meditation 🧘 + grounding 🌱"
    elif time_of_day == "morning":
        time_action = "deep work 💻 + mindfulness 🧠 + sunlight ☀️ + breathing 🌬"
    elif time_of_day == "afternoon":
        time_action = "light work 📘 + walking 🚶 + movement 🏃"
    elif time_of_day == "evening":
        time_action = "relax 🌇 + nature walk 🌳 + light activity 🎧"
    else:
        time_action = "reflection 🌙 + journaling 📓 + breathing 🌬 + stretching 🧘"

    # 5 Decision Logic
    what_to_do = energy_action
    when_to_do = "later_today"

    if state_group == "high_load_state" or support_level == "needs_support":
        what_to_do = "breathing 🌬 + grounding 🌱"
        when_to_do = "now"

    elif state_group == "active_mind_state":
        what_to_do = "grounding 🌱 + movement 🚶"
        when_to_do = "within_15_min"

    elif state_group == "productive_state" and energy >= 3:
        what_to_do = "deep work 💻"
        when_to_do = "now"

    elif state_group == "baseline_state":
        what_to_do = time_action
        when_to_do = "later_today"

    # sleep override
    if pd.notna(sleep) and sleep < 5:
        what_to_do = "rest 😴 + recovery"
        when_to_do = "within_15_min"

    # night override
    if time_of_day == "night":
        when_to_do = "tonight"

    # 6. Confidence
    confidence = 0.5

    if state in ['calm', 'focused'] and energy >= 3:
        confidence += 0.2

    if intensity >= 4 or stress >= 4:
        confidence += 0.2

    if state == 'mixed':
        confidence -= 0.2

    confidence = max(0.3, min(confidence, 0.95))

    uncertain_flag = 1 if confidence < 0.65 else 0

    return pd.Series([
        state_group,
        support_level,
        what_to_do,
        when_to_do,
        confidence,
        uncertain_flag
    ])


# PIPELINE 

# Make paths relative to the script location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRAIN_PATH = os.path.join(BASE_DIR, "../data/train.csv")
PRED_PATH  = os.path.join(BASE_DIR, "../outputs/predictions.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "../outputs")

# Read train CSV
train_df = pd.read_csv(TRAIN_PATH)

# Read predictions CSV if exists, else initialize with defaults
if os.path.exists(PRED_PATH) and os.path.getsize(PRED_PATH) > 0:
    pred_df = pd.read_csv(PRED_PATH)
else:
    # <-- FIX: populate initial predictions so df has rows -->
    pred_df = train_df[['id']].copy()
    pred_df['predicted_state'] = 'baseline'
    pred_df['predicted_intensity'] = 3

# Merge features from train_df
df = pred_df.merge(
    train_df[['id', 'stress_level', 'energy_level', 'time_of_day', 'sleep_hours']],
    on='id',
    how='left'
)

# Apply decision engine
df[['state_group', 'support_level', 'what_to_do', 'when_to_do', 'confidence', 'uncertain_flag']] = df.apply(decision_engine, axis=1)

# Ensure output folder exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Save predictions
df.to_csv(PRED_PATH, index=False)
print("Predictions saved successfully!")