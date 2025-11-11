from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class HealthDataBase(BaseModel):
    gender: Optional[str] = None
    age: Optional[float] = None
    hypertension: Optional[int] = Field(None, ge=0, le=1)
    heart_disease: Optional[int] = Field(None, ge=0, le=1)
    ever_married: Optional[str] = None
    work_type: Optional[str] = None
    residence_type: Optional[str] = None
    avg_glucose_level: Optional[float] = None
    bmi: Optional[float] = None
    smoking_status: Optional[str] = None

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    gender: Optional[str] = None
    age: Optional[float] = None
    hypertension: Optional[int] = Field(None, ge=0, le=1)
    heart_disease: Optional[int] = Field(None, ge=0, le=1)
    ever_married: Optional[str] = None
    work_type: Optional[str] = None
    residence_type: Optional[str] = None
    avg_glucose_level: Optional[float] = None
    bmi: Optional[float] = None
    smoking_status: Optional[str] = None

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[float] = None
    hypertension: Optional[int] = Field(None, ge=0, le=1)
    heart_disease: Optional[int] = Field(None, ge=0, le=1)
    ever_married: Optional[str] = None
    work_type: Optional[str] = None
    residence_type: Optional[str] = None
    avg_glucose_level: Optional[float] = None
    bmi: Optional[float] = None
    smoking_status: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    gender: Optional[str]
    age: Optional[float]
    hypertension: Optional[int]
    heart_disease: Optional[int]
    ever_married: Optional[str]
    work_type: Optional[str]
    residence_type: Optional[str]
    avg_glucose_level: Optional[float]
    bmi: Optional[float]
    smoking_status: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
