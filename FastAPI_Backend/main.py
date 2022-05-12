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

# models.Base.metadata.drop_all(bind=engine)
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
    
@app.post('/add_user')
def add_user(user: User, db: Session = Depends(get_db)):

    db_user = cruds.get_user_by_email(db=db, email=user.email)

    if db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Email already exists')

    else:
        current_user = cruds.create_user(db=db, user=user)
        return {'msg' : 'user_created',
            'user_id' : current_user.id}
    
# ========= Login

class LogUser(BaseModel):
    email: str
    password: str

@app.post('/login')
def login(user: LogUser, db: Session = Depends(get_db)):

    # Find by mail
    
    db_user = cruds.get_user_by_email(db=db, email=user.email)
    
    # Check password

    if db_user:
        if db_user.password == user.password + "notreallyhashed":
            return {'msg': 'connected',
            'user_id' : db_user.id}
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

@app.get('/get_all_prediction/{id}')
def make_prediction(id, db: Session = Depends(get_db)):

    predictions = cruds.get_predictions_by_user(db=db, id=id)

    return {
        'msg': 'received',
        'pred_list': predictions
    }
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8555)