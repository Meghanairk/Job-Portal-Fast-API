
from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

# ✅ USER TABLE
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="candidate")  # candidate / recruiter


# ✅ JOB TABLE
class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    company = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))


# ✅ APPLICATION TABLE (VERY IMPORTANT)
class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    job_id = Column(Integer) 