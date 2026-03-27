
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import models
from database import SessionLocal
from auth import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/apply")
def apply_job(
    job_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user["user_id"]

    application = models.Application(
        user_id=user_id,
        job_id=job_id
    )
    db.add(application)
    db.commit()

    return {"message": "Applied successfully"}

@router.get("/applications")
def get_applications(db: Session = Depends(get_db)):
    return db.query(models.Application).all()