from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path

import pandas as pd
import pickle


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="MindTrack AI",
    description="Mental Health Score Prediction API",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# MODEL PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "mental_health.pkl"

print("======================================")
print("Model path:")
print(MODEL_PATH)
print("======================================")


# =========================================================
# LOAD MODEL
# =========================================================

try:

    with open(MODEL_PATH, "rb") as file:
        model = pickle.load(file)

    print("✅ Model loaded successfully!")

except Exception as e:

    model = None

    print("❌ Model loading failed!")
    print("Error:", e)


# =========================================================
# INPUT MODEL
# =========================================================

class PredictionInput(BaseModel):

    Age: int

    Gender: str

    Country: str

    Academic_Level: str

    Most_Used_Platform: str

    Purpose_Of_Use: str

    Avg_Daily_Usage_Hours: float

    Daily_Unlocks: int

    Study_Hours: float

    Physical_Activity_Hours: float

    Sleep_Hours_Per_Night: float

    Stress_Level: str


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return {
        "message": "MindTrack AI API is running",
        "model_loaded": model is not None
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "model_loaded": model is not None
    }


# =========================================================
# PREDICTION
# =========================================================

@app.post("/predict")
def predict(data: PredictionInput):

    if model is None:

        raise HTTPException(
            status_code=500,
            detail="Model is not loaded."
        )

    try:

        # Convert request to dictionary
        input_data = data.model_dump()

        print("\nInput received:")
        print(input_data)


        # =================================================
        # IMPORTANT:
        # Keep EXACT same column names used during training
        # =================================================

        input_df = pd.DataFrame(
            [input_data],
            columns=[
                "Age",
                "Gender",
                "Country",
                "Academic_Level",
                "Most_Used_Platform",
                "Purpose_Of_Use",
                "Avg_Daily_Usage_Hours",
                "Daily_Unlocks",
                "Study_Hours",
                "Physical_Activity_Hours",
                "Sleep_Hours_Per_Night",
                "Stress_Level"
            ]
        )


        print("\nDataFrame:")
        print(input_df)

        print("\nColumns:")
        print(input_df.columns.tolist())


        # =================================================
        # PREDICTION
        # =================================================

        prediction = model.predict(input_df)[0]

        prediction = float(prediction)


        print("\nPrediction:")
        print(prediction)


        # =================================================
        # CATEGORY
        # =================================================

        if prediction >= 7.5:

            category = "Good"

        elif prediction >= 5:

            category = "Moderate"

        else:

            category = "Needs Attention"


        # =================================================
        # RESPONSE
        # =================================================

        return {

            "success": True,

            "mental_health_score": round(
                prediction,
                2
            ),

            "category": category

        }


    except Exception as e:

        print("\n❌ Prediction error:")
        print(e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )