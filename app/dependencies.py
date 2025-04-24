from typing import Annotated
from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.database import SessionLocal
from app.models import User
from app.utils.auth import SECRET_KEY, ALGORITHM  


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dep = Annotated[Session, Depends(get_db)]


def get_current_user(
    request: Request,
    db: db_dep
  ):
    auth_header = request.headers.get("Authorization")
    is_bearer = auth_header.startswith("Bearer ") if auth_header else False
    token = auth_header.split(" ")[1] if is_bearer else ""

    if not auth_header or not is_bearer:
        raise HTTPException(status_code=401, detail="Siz tasdiqlanmagansiz.")

    try:
        decoded_jwt = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = decoded_jwt.get("email")
        if not email:
            raise HTTPException(status_code=401, detail="Tokenda e-pochta yetishmayapti.")

        db_user = db.query(User).filter(User.email == email).first()
        if not db_user:
            raise HTTPException(status_code=401, detail="Foydalanuvchi topilmadi.")

    except JWTError:
        raise HTTPException(status_code=401, detail="Token yaroqsiz.")

    return db_user


def get_admin_user(user: User = Depends(get_current_user)):
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail="Sizda administrator huquqlari yo'q.")
    return user


current_user_dep = Annotated[User, Depends(get_current_user)]
admin_user_dep = Annotated[User, Depends(get_admin_user)]
