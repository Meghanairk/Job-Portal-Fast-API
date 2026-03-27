
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import models
from database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/jobs")
def create_job(title: str, description: str, company: str, db: Session = Depends(get_db)):
    new_job = models.Job(
        title=title,
        description=description,
        company=company,
        posted_by=1   # temporary (we'll fix later with auth)
    )
    db.add(new_job)
    db.commit()
    return {"message": "Job created"}


@router.get("/jobs")
def get_jobs(db: Session = Depends(get_db)):
    jobs = db.query(models.Job).all()
    return jobs