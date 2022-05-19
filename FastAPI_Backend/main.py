# Core
from fastapi import FastAPI, Depends, status, HTTPException
from starlette.responses import RedirectResponse
import uvicorn
# Model
import tensorflow as tf
import pandas as pd
from pydantic import BaseModel
from typing import List

# Database
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import cruds
import models

# ========= Create database structure

models.Base.metadata.create_all(bind=engine)

# ========= Launch app

app = FastAPI()

# ========= Database dependency function

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ========= Model loading

def load_model():
    model = tf.keras.models.load_model("Conv1d")
    print("Model loaded")
    return model

model = load_model()

# ========= Root redirecting to api swaggers

@app.get("/")
def root():
    response = RedirectResponse(url='/docs')
    return response

# ========= User related routes

# ========= Add

class User(BaseModel):
    f_name: str
    l_name: str
    email: str
    password: str

@app.on_event("startup")
def on_startup():
    db = SessionLocal()
    already_done = cruds.get_user(db=db, user_id=1)
    
    if not already_done:
        admin = models.User(f_name='mr', l_name= 'zen', email='admin', password='1234notreallyhashed', is_admin=True)
        db.add(admin)
        guest = models.User(f_name='guest', l_name= 'guest', email='guest', password='1234notreallyhashed', is_admin=True)
        db.add(guest)
        db.commit()
        db.refresh(admin)
        db.refresh(guest)
        print('Admin created')
        print('Guest created')


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}


@app.post('/add_user')
def add_user(user: User, db: Session = Depends(get_db)):
    """Create a user

    Args:
        user (User): User
        db (Session, optional): db dependency. Defaults to Depends(get_db).

    Raises:
        HTTPException: 401 Email already exists

    Returns:
        _type_: User created status and user values
    """
    db_user = cruds.get_user_by_email(db=db, email=user.email)

    if db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Email already exists')

    else:
        current_user = cruds.create_user(db=db, user=user)
        return {'msg': 'user_created',
            'f_name': current_user.f_name,
            'l_name': current_user.l_name,
            'user_id': current_user.id,
            'is_admin:': current_user.is_admin}
    
# ========= Login

class LogUser(BaseModel):
    email: str
    password: str

@app.post('/login')
def login(user: LogUser, db: Session = Depends(get_db)):
    """Log user in

    Args:
        user (LogUser): Email and password
        db (Session, optional): db dependency. Defaults to Depends(get_db).

    Raises:
        HTTPException: 401 Password don't match
        HTTPException: 401 Account don't exists

    Returns:
        _type_: Connected status and user values
    """
    # Find by mail
    
    db_user = cruds.get_user_by_email(db=db, email=user.email)
    
    # Check password

    if db_user:
        if db_user.password == user.password + "notreallyhashed":
            return {'msg': 'connected',
            'f_name': db_user.f_name,
            'l_name': db_user.l_name,
            'user_id': db_user.id,
            'is_admin': db_user.is_admin}
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Password don\'t match')

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Le compte n\'existe pas')

    
# ========= Prediction routes

class Input(BaseModel):
    text: str
    user_id: int
class Prediction(BaseModel):
    text: str
    results: str
    best_result:  int
    emotion: str

@app.post('/prediction')
def make_prediction(input: Input, db: Session = Depends(get_db)):
    """Model predict

    Args:
        input (Input): Necessary values for prediction
        db (Session, optional): db dependency. Defaults to Depends(get_db).

    Returns:
        _type_: Added status and predicted values
    """
    text_input = [(input.text)]
    
    df = pd.DataFrame(text_input, columns=['content'])

    emotions = ['anger', 'fear', 'happy', 'sadness']
    
    # Make a prediction

    predictions = model.predict(df['content'])[0]
    results = predictions.tolist()
    results_str = str(results)
    best_result = max(results)
    best_result_index = results.index(best_result)
    emotion = emotions[best_result_index]

    cruds.create_user_prediction(db=db, pred=Prediction(
        text=input.text,
        results=results_str,
        best_result=best_result,
        emotion=emotion,
    ), user_id=input.user_id)

    return {
        'msg': 'added',
        'input': input,
        'emotions': emotions,
        'prediction': results,
        'best_pred': best_result,
        'most_accurate_emotion': emotion
    }

@app.get('/get_predictions_by_user/{id}')
def get_predictions_by_user(id, db: Session = Depends(get_db)):
    """Get all predictions of an user

    Args:
        id (_type_): User id
        db (Session, optional): db dependency. Defaults to Depends(get_db).

    Returns:
        _type_: Received status and user predictions
    """
    predictions = cruds.get_predictions_by_user(db=db, id=id)

    return {
        'msg': 'received',
        'pred_list': predictions
    }
class ModifyInput(BaseModel):
    pred_id: int
    text: str  

@app.patch("/update_pred")
def update_pred(input: ModifyInput, db: Session = Depends(get_db)):
    """Update selected prediction

    Args:
        input (ModifyInput): input values for the prediction update
        db (Session, optional): db dependency. Defaults to Depends(get_db).

    Raises:
        HTTPException: 404 (Old prediction not found)

    Returns:
        _type_: Updated status and predicted values
    """
    text_input = [(input.text)]
    df_pred = pd.DataFrame(text_input, columns=['content'])
    predictions = model.predict(df_pred['content'])[0]

    emotions = ['anger', 'fear', 'happy', 'sadness']
    
    results = predictions.tolist()
    results_str = str(results)
    best_result = max(results)
    best_result_index = results.index(best_result)
    emotion = emotions[best_result_index]
    print(input.pred_id)
    old_prediction = db.query(models.Prediction).filter(models.Prediction.id == input.pred_id)
    if not old_prediction.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Old prediction with the id {input.pred_id} is not available')
    old_prediction.update({'text':input.text, 'results':results_str, 'best_result':best_result, 'emotion':emotion})
    db.commit()
    db.refresh(old_prediction.first())
    
    return {
        'msg': 'Updated',
        'input': input.text,
        'emotions': emotions,
        'prediction': results,
        'best_pred': best_result,
        'most_accurate_emotion': emotion
    }
        
@app.get('/get_all_users')
def get_all_users(db: Session = Depends(get_db)):
    """get all users in db

    Args:
        db (Session, optional): db dependency. Defaults to Depends(get_db).

    Returns:
        _type_: User
    """
    user_list = cruds.get_users(db=db)

    return {
        'user_list': user_list
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8555)