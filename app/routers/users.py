from fastapi import APIRouter, HTTPException
from app import models
from app.schemas.users import UserLogin, UserCreate, UserResponse
from app.dependencies import db_dep, current_user_dep
from app.utils.auth import hash_password, verify_password, create_access_token
from datetime import timedelta

router = APIRouter(
    prefix="/users",
    tags=["Auth"]
)



@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, session: db_dep):
   
    db_email = session.query(models.User).filter(models.User.email == user.email).first()
    db_username = session.query(models.User).filter(models.User.username == user.username).first()
    if db_email:
        raise HTTPException(status_code=400, detail="Bunday e-mail bilan allaqachon ro'yxatdan o'tilgan.")
    if db_username:
        raise HTTPException(status_code=400, detail="Bunday username band.")

   
    username = user.username if user.username else user.email.split("@")[0]
    
    hashed_password = hash_password(user.password)
    db_user = models.User(
        email=user.email,
        hash_password=hashed_password,
        username=username,
        first_name=user.first_name,
        last_name=user.last_name,
        date_of_birth=user.date_of_birth
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user



@router.post("/login")
def login_user(user: UserLogin, session: db_dep):
    db_user = session.query(models.User).filter(models.User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Noto'g'ri email yoki parol.")
    
    if not verify_password(user.password, db_user.hash_password):
        raise HTTPException(status_code=401, detail="Noto'g'ri email yoki parol.")
    
    
    access_token_expires = timedelta(minutes=30)  
    access_token = create_access_token(
        data={"email": db_user.email},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }