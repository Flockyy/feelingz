from requests import Session
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

# ========= User

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    f_name = Column(String, nullable=False, index=True)
    l_name = Column(String, nullable=False, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False, index=True)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

# ========= Document

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    text = Column(String, index=True, nullable=False)
    results = Column(String, index=True, nullable=False)
    best_result = Column(Integer, index=True, nullable=False)
    emotion = Column(String, index=True, nullable=False)
    time_created = Column(DateTime(timezone=False), server_default=func.now())
    time_updated = Column(DateTime(timezone=False), onupdate=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"))

# ========= Database CRUDs

def create_user(db: Session, user: User):

    fake_hashed_password = user.password + "notreallyhashed"
    db_user = User(email=user.email, password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):

    return db.query(User).filter(User.email == email).first()