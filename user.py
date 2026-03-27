
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal
from auth import create_access_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(
        email=user.email,
        password=user.password,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}


@router.post("/login")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user or db_user.password != user.password:
        return {"error": "Invalid credentials"}

    token = create_access_token({"user_id": db_user.id})

    return {"access_token": token}