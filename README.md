# 🧠 MoodGuide AI – Emotion Prediction System

## 📌 Overview

MoodGuide AI is an end-to-end machine learning system that predicts a user’s emotional state and intensity based on journal text and behavioral signals. It also provides actionable recommendations to improve mental well-being.

## 🚀 Features

* 🔍 Emotion State Prediction (calm, stressed, focused, etc.)
* 📊 Intensity Prediction (low → high)
* 🧠 NLP-based text understanding (TF-IDF)
* 📈 Feature comparison (Text vs Metadata vs Combined)
* ⚠️ Error analysis & edge case handling
* 🧭 Decision Engine for actionable suggestions
* 🌐 Interactive Streamlit Web App

## 🏗️ Project Structure

```
project/
│
├── app/
│   ├── app.py
│   ├── utils.py
│
├── data/
│   ├── train.csv
│   ├── test.csv
│
├── notebooks/
│   ├── eda_modeling.ipynb
│
├── outputs/
│   ├── model_state.pkl
│   ├── model_intensity.pkl
│   ├── predictions.csv
│
├── src/
│   ├── decision_engine.py
│
├── README.md
```

## ⚙️ Tech Stack

* Python
* Pandas, NumPy
* Scikit-learn
* Streamlit
* Joblib

## 🧪 Model Details

* Algorithm: Logistic Regression
* Text Processing: TF-IDF Vectorization
* Inputs:

  * Journal Text
  * Sleep, Stress, Energy
  * Time of Day
  * Mood Context Features

## 📊 Results

| Model Type     | Accuracy |
| -------------- | -------- |
| Text Only      | 0.6458   |
| Metadata Only  | 0.1625   |
| Combined Model | 0.5750   |

### 🔍 Insights

* Text is the primary signal for emotion detection
* Metadata acts as supporting context
* Model struggles with:

  * Short text ("ok", "fine")
  * Conflicting emotions ("tired but excited")

## ⚠️ Error Analysis

* Short inputs lack sufficient signal
* Mixed emotional statements confuse model
* Subtle emotional cues often misclassified

## 🧭 Decision Engine

A rule-based system converts predictions into:

* Action recommendations
* Timing suggestions
* Confidence score

Example:

* High stress → breathing + grounding
* Low energy → rest / relaxation
* Productive state → deep work

## 🌐 Run the App

```bash
streamlit run app/app.py
```
## 🔮 Future Improvements

* Use BERT / Transformer models
* Add mood history tracking dashboard
* Deploy on Streamlit Cloud
* Add user authentication
* Improve contextual understanding

## ⭐ Conclusion

This is not meant to replace therapists or human support.
It’s just a simple system that gives basic suggestions.
Real emotions are complex, and real help should always come from people.


# 💡 Summary

This project explores how simple ML models + basic logic  
can be combined to create a system that not only predicts  
but also suggests small, useful actions.