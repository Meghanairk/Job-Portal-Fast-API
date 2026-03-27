from auth import get_current_user
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from auth import create_access_token
from jose import jwt, JWTError
import auth
# SECRET (same as in auth.py)
#SECRET_KEY = "your_secret_key"
#ALGORITHM = "HS256"

app = FastAPI()

# Create tables
models.Base.metadata.create_all(bind=engine)

# DB connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# OAuth scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# ✅ Get current user from token
#def get_current_user(token: str = Depends(oauth2_scheme)):
 #   try:
  #      payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
   #     return payload
    #except JWTError:
     #   return {"error": "Invalid token"}

# ✅ LOGIN API (OAuth2 form)
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email == form_data.username).first()

    if not user or user.password != form_data.password:
        return {"error": "Invalid credentials"}

    token = create_access_token({"user_id": user.id})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# ✅ APPLY JOB (Protected + DB Save)
@app.post("/apply")
def apply_job(job_id: int,
              db: Session = Depends(get_db),
              current_user: dict = Depends(get_current_user)):

    new_application = models.Application(
        user_id=current_user["user_id"],
        job_id=job_id
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return {
        "message": "Application saved successfully",
        "application_id": new_application.id
    }
@app.post("/create-job")
def create_job(
    title: str,
    description: str,
    company: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    print("USER:", current_user)
    print("CURRENT USER:", current_user)  # 👈 ADD THIS

    if "user_id" not in current_user:
        return {"error": "Invalid token data"}

    new_job = models.Job(
        title=title,
        description=description,
        company=company,
        owner_id=current_user["user_id"]
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return {
        "message": "Job created successfully",
        "job_id": new_job.id
    }
@app.post("/register")
def register(email: str, password: str, role: str, db: Session = Depends(get_db)):

    new_user = models.User(
        email=email,
        password=password,  # ❌ NO HASH (just for testing)
        role=role
    )

    db.add(new_user)
    db.commit()

    return {"message": "User registered"}

@app.post("/apply")
def apply_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user)
):
    # check if job exists
    job = db.query(models.Job).filter(models.Job.id == job_id).first()

    if not job:
        return {"error": "Job not found"}

    new_application = models.Application(
        user_id=current_user["user_id"],
        job_id=job_id
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)
    return {"message": "Applied successfully"}
@app.get("/jobs")
def get_jobs(db: Session = Depends(get_db)):
    jobs = db.query(models.Job).all()
    return jobs
@app.get("/applications")
def get_applications(db: Session = Depends(get_db)):
    apps = db.query(models.Application).all()
    return apps  