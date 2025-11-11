from sqlalchemy.orm import Session
from models.database import User, ChatHistory
from typing import Optional
import uuid

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, email: str, full_name: str, health_data: dict) -> User:
        user = User(
            email=email,
            full_name=full_name,
            gender=health_data.get('gender'),
            age=health_data.get('age'),
            hypertension=health_data.get('hypertension'),
            heart_disease=health_data.get('heart_disease'),
            ever_married=health_data.get('ever_married'),
            work_type=health_data.get('work_type'),
            residence_type=health_data.get('Residence_type'),
            avg_glucose_level=health_data.get('avg_glucose_level'),
            bmi=health_data.get('bmi'),
            smoking_status=health_data.get('smoking_status')
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        return self.db.query(User).offset(skip).limit(limit).all()
    
    def update(self, user_id: int, user_data: dict) -> Optional[User]:
        user = self.get_by_id(user_id)
        if user:
            for key, value in user_data.items():
                if value is not None and hasattr(user, key):
                    setattr(user, key, value)
            self.db.commit()
            self.db.refresh(user)
        return user
    
    def update_health_data(self, user_id: int, health_data: dict) -> Optional[User]:
        user = self.get_by_id(user_id)
        if user:
            for key, value in health_data.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            self.db.commit()
            self.db.refresh(user)
        return user
    
    def delete(self, user_id: int) -> bool:
        user = self.get_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False

class ChatRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_message(self, user_id: Optional[int], session_id: str, role: str, 
                      message: str, function_call: str = None, function_result: str = None) -> ChatHistory:
        chat = ChatHistory(
            user_id=user_id,
            session_id=session_id,
            role=role,
            message=message,
            function_call=function_call,
            function_result=function_result
        )
        self.db.add(chat)
        self.db.commit()
        self.db.refresh(chat)
        return chat
    
    def get_history(self, session_id: str, limit: int = 50):
        return self.db.query(ChatHistory)\
            .filter(ChatHistory.session_id == session_id)\
            .order_by(ChatHistory.created_at.desc())\
            .limit(limit)\
            .all()
    
    def get_user_history(self, user_id: int, limit: int = 50):
        return self.db.query(ChatHistory)\
            .filter(ChatHistory.user_id == user_id)\
            .order_by(ChatHistory.created_at.desc())\
            .limit(limit)\
            .all()
