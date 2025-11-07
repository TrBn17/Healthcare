from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255))
    
    # Thông tin sức khỏe
    gender = Column(String(50))
    age = Column(Float)
    hypertension = Column(Integer)
    heart_disease = Column(Integer)
    ever_married = Column(String(50))
    work_type = Column(String(100))
    residence_type = Column(String(50))
    avg_glucose_level = Column(Float, nullable=True)
    bmi = Column(Float)
    smoking_status = Column(String(100))
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class ChatHistory(Base):
    __tablename__ = "chat_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    session_id = Column(String(255), index=True)
    role = Column(String(50))
    message = Column(Text)
    function_call = Column(Text, nullable=True)
    function_result = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
