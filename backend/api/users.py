from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from db.repository import UserRepository
from schemas.user import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Tạo người dùng mới
    """
    user_repo = UserRepository(db)
    
    # Kiểm tra email đã tồn tại
    existing_user = user_repo.get_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Tách health_data từ user_data
    health_data = {
        "gender": user_data.gender,
        "age": user_data.age,
        "hypertension": user_data.hypertension,
        "heart_disease": user_data.heart_disease,
        "ever_married": user_data.ever_married,
        "work_type": user_data.work_type,
        "Residence_type": user_data.residence_type,
        "avg_glucose_level": user_data.avg_glucose_level,
        "bmi": user_data.bmi,
        "smoking_status": user_data.smoking_status
    }
    
    user = user_repo.create(
        email=user_data.email,
        full_name=user_data.full_name,
        health_data=health_data
    )
    return user

@router.get("/", response_model=List[UserResponse])
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Lấy danh sách tất cả người dùng
    """
    user_repo = UserRepository(db)
    users = user_repo.get_all(skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Lấy thông tin người dùng theo ID
    """
    user_repo = UserRepository(db)
    user = user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.get("/email/{email}", response_model=UserResponse)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    """
    Lấy thông tin người dùng theo email
    """
    user_repo = UserRepository(db)
    user = user_repo.get_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    """
    Cập nhật thông tin người dùng
    """
    user_repo = UserRepository(db)
    
    # Kiểm tra user tồn tại
    existing_user = user_repo.get_by_id(user_id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Nếu cập nhật email, kiểm tra email mới có trùng không
    if user_data.email and user_data.email != existing_user.email:
        email_check = user_repo.get_by_email(user_data.email)
        if email_check:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
    
    # Chuyển đổi user_data thành dict, loại bỏ các giá trị None
    update_data = user_data.model_dump(exclude_unset=True)
    
    user = user_repo.update(user_id, update_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Xóa người dùng
    """
    user_repo = UserRepository(db)
    success = user_repo.delete(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return None
