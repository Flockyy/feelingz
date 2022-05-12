from sqlalchemy.orm import Session

import models

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: models.User):
    user.password = user.password + "notreallyhashed"
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_predictions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Prediction).offset(skip).limit(limit).all()

def get_predictions_by_user(db: Session, id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Prediction).filter(models.Prediction.owner_id == id).offset(skip).limit(limit).all()

def create_user_prediction(db: Session, pred: models.Prediction, user_id: int):
    db_item = models.Prediction(**pred.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

