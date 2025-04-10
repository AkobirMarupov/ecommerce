from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models
from app.sxemas import schemas
from app.dependencies import get_db
from app.models import User
from app.services.auth import hash_password


router = APIRouter(
    prefix="/users",
    tags=["Auth"]
)


@router.post("/register", response_model=schemas.UserOutSchema)
def register_user(user: schemas.UserCreateSchema, session: Session = Depends(get_db)):

    db_email = session.query(User).filter(User.email == user.email).first()
    db_username = session.query(User).filter(User.username == user.username).first()
    if db_email:
        raise HTTPException(status_code=400, detail="Bunday e-mail bilan allaqachon ruyxatdan utilgan...")
    if db_username:
        raise HTTPException(status_code=400, detail="Bunday username band...")

    hashed_password = hash_password(user.password)
    db_user = models.User(
        email=user.email,
        hash_password=hashed_password,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        date_of_birth=user.date_of_birth
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


