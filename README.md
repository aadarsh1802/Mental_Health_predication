# Mental Health Score Predictor

A machine-learning project for predicting a **mental-health-related score** from structured questionnaire or survey data.

> **Important:** This project is for educational/research purposes only. It is not a medical diagnostic tool, and predictions should not be used to diagnose or treat a person.

## Project workflow
1. Data collection / loading
2. Exploratory Data Analysis (EDA)
3. Data cleaning and preprocessing
4. Feature engineering
5. Model training
6. Model evaluation
7. Prediction
8. Optional web/API deployment

## Suggested stack
- Python
- Pandas / NumPy
- Scikit-learn
- Matplotlib / Seaborn
- Joblib
- FastAPI or Streamlit (optional)

## Training and prediction

Install the dependencies from `requirements.txt`, then run the training pipeline
from the project root:

```powershell
python -m src.train
```

This reads the raw survey CSV, removes duplicate rows, trains a preprocessing
and random-forest regression pipeline, evaluates it on a held-out test split,
and saves it to `models/mental_health.pkl`.

Use the saved pipeline to score one survey record or a DataFrame of records:

```python
from src.predict import load_model, predict_scores

model = load_model()
score = predict_scores(
    model,
    {
        "Age": 21,
        "Gender": "Male",
        "Country": "Other",
        "Academic_Level": "Undergraduate",
        "Most_Used_Platform": "Facebook",
        "Purpose_Of_Use": "Networking",
        "Avg_Daily_Usage_Hours": 4.0,
        "Daily_Unlocks": 134,
        "Study_Hours": 4.5,
        "Physical_Activity_Hours": 2.2,
        "Sleep_Hours_Per_Night": 6.7,
        "Stress_Level": "Medium",
    },
)[0]
```

The reusable loading, EDA, preprocessing, feature engineering, training, and
evaluation functions are in `src/`. Predictions are educational estimates only
and are not diagnoses or treatment advice.
