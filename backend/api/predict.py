from fastapi import FastAPI, HTTPException, Form
from pydantic import BaseModel
from enum import Enum
import joblib
import pandas as pd
import numpy as np
from typing import Optional

app = FastAPI()

model_data = joblib.load('stroke_prediction_model.pkl')
model = model_data['model']
optimal_threshold = model_data['optimal_threshold']
feature_columns = model_data['feature_columns']
explainer = model_data['explainer']

class Gender(str, Enum):
    male = "Male"
    female = "Female"
    other = "Other"

class MaritalStatus(str, Enum):
    yes = "Yes"
    no = "No"

class WorkType(str, Enum):
    private = "Private"
    self_employed = "Self-employed"
    govt_job = "Govt_job"
    children = "children"
    never_worked = "Never_worked"

class ResidenceType(str, Enum):
    urban = "Urban"
    rural = "Rural"

class SmokingStatus(str, Enum):
    formerly_smoked = "formerly smoked"
    never_smoked = "never smoked"
    smokes = "smokes"
    unknown = "Unknown"

class PatientData(BaseModel):
    gender: Gender
    age: float
    hypertension: int
    heart_disease: int
    ever_married: MaritalStatus
    work_type: WorkType
    Residence_type: ResidenceType
    avg_glucose_level: Optional[float] = None
    bmi: float
    smoking_status: SmokingStatus

@app.post("/predict")
def predict_stroke(
    gender: Gender = Form(...),
    age: float = Form(...),
    hypertension: int = Form(...),
    heart_disease: int = Form(...),
    ever_married: MaritalStatus = Form(...),
    work_type: WorkType = Form(...),
    Residence_type: ResidenceType = Form(...),
    bmi: float = Form(...),
    smoking_status: SmokingStatus = Form(...),
    avg_glucose_level: Optional[float] = Form(None)
):
    try:
        input_dict = {
            'gender': gender.value,
            'age': age,
            'hypertension': hypertension,
            'heart_disease': heart_disease,
            'ever_married': ever_married.value,
            'work_type': work_type.value,
            'Residence_type': Residence_type.value,
            'bmi': bmi,
            'smoking_status': smoking_status.value,
            'avg_glucose_level': avg_glucose_level if avg_glucose_level is not None else 106.0
        }
        
        df = pd.DataFrame([input_dict])
        
        proba = model.predict_proba(df)[0, 1]
        prediction = int(proba >= optimal_threshold)
        
        X_transformed = model.named_steps['preprocessor'].transform(df)
        shap_values = explainer.shap_values(X_transformed)[0]
        feature_names = model.named_steps['preprocessor'].get_feature_names_out()
        
        shap_dict = {str(name): round(float(val), 4) for name, val in zip(feature_names, shap_values)}
        
        return {
            "stroke_probability": round(float(proba) * 100, 2),
            "prediction": prediction,
            "risk_level": "High" if prediction == 1 else "Low",
            "shap_explanation": shap_dict
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
def root():
    return {"message": "Stroke Prediction API", "status": "active"}
