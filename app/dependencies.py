# app/dependencies.py

from typing import Annotated
from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.database import SessionLocal
from app.models import User
from app.utils import SECRET_KEY, ALGORITHM  # config.py ga ajratildi

# Ma'lumotlar bazasi sessiyasini olish
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dep = Annotated[Session, Depends(get_db)]

# Joriy foydalanuvchini olish (token orqali)
def get_current_user(
    request: Request,
    db: db_dep
) -> User:
    auth_header = request.headers.get("Authorization")
    is_bearer = auth_header.startswith("Bearer ") if auth_header else False
    token = auth_header.split(" ")[1] if is_bearer else ""

    if not auth_header or not is_bearer:
        raise HTTPException(status_code=401, detail="You are not authenticated.")

    try:
        decoded_jwt = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = decoded_jwt.get("email")
        if not email:
            raise HTTPException(status_code=401, detail="Token is missing email.")

        db_user = db.query(User).filter(User.email == email).first()
        if not db_user:
            raise HTTPException(status_code=401, detail="User not found.")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token.")

    return db_user

# Faqat admin foydalanuvchini olish
def get_admin_user(user: User = Depends(get_current_user)) -> User:
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="You do not have admin privileges.")
    return user

current_user_dep = Annotated[User, Depends(get_current_user)]
