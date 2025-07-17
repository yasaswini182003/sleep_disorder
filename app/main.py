from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd

# Load model
with open("app/model.pkl", "rb") as f:
    model = pickle.load(f)

app = FastAPI()

# Pydantic schema
class SleepFeatures(BaseModel):
    Gender: str
    Age: int
    Occupation: str
    Sleep_Duration: float
    Quality_of_Sleep: int
    Physical_Activity_Level: int
    Stress_Level: int
    BMI_Category: str
    Heart_Rate: int
    Daily_Steps: int
    Systolic_BP: int
    Diastolic_BP: int

@app.post("/predict")
def predict(data: SleepFeatures):
    df = pd.DataFrame([data.dict()])
    df.columns = ["Gender", "Age", "Occupation", "Sleep Duration", "Quality of Sleep",
                  "Physical Activity Level", "Stress Level", "BMI Category", "Heart Rate",
                  "Daily Steps", "Systolic_BP", "Diastolic_BP"]
    prediction = model.predict(df)[0]
    return {"predicted_sleep_disorder": prediction}
