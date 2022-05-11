from requests import Session
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from schemas.PYDTchemas import UserCreate
from models.database import Base, engine


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    documents = relationship("Document", back_populates="owner")


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="documents")

# ========= Database CRUDs

async def create_user(db: Session, user: UserCreate):
    """_summary_

    Args:
        db (Session): _description_
        user (UserCreate): _description_

    Returns:
        _type_: _description_
    """
    # async with engine.begin() as conn:
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

async def get_user_by_email(db: Session, email: str):
    """_summary_

    Args:
        db (Session): _description_
        email (str): _description_

    Returns:
        _type_: _description_
    """
    
    # async with engine.begin() as conn:
    return db.query(User).filter(User.email == email).first()