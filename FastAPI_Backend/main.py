# Core
from fastapi import FastAPI, Depends
from starlette.responses import RedirectResponse
import uvicorn
import asyncio
# Model
import tensorflow as tf
import pandas as pd
from pydantic import BaseModel

# Database
from sqlalchemy.orm import Session
from schemas import PYDTchemas
from models.SQLModels import create_user, get_user_by_email
from models.database import SessionLocal, init_db

# ========= Launch app

app = FastAPI()

# ========= Create database structure

init_db()

# ========= Database dependency function

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ========= Model loading

def load_model():
    """
    Loads and returns the pretrained model
    """
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
class tmpUser(BaseModel):
    email: str
    password: str
    
@app.post('/add_user')
async def add_user(user: tmpUser, db: Session = Depends(get_db)):
    """_summary_

    Args:
        user (UserCreate): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Returns:
        _type_: _description_
    """
    create_user(db=db, user=user)
    return {'Success' : 'user_created'}

# ========= Login

@app.post('/login')
async def login(user: tmpUser, db: Session = Depends(get_db)):
    """_summary_

    Args:
        user (UserCreate): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Returns:
        _type_: _description_
    """
    # Find by mail
    
    db_user = await get_user_by_email(db=db, email=user.email)
    
    # Check password
    
    if db_user.password == user.password + "notreallyhashed":
        user.is_active = 1
        return {'Success': 'Connected'}
    else:
        return {'Error': 'Connection failed'}
    
# ========= Prediction routes

# ========= Prediction

class Input(BaseModel):
    text: str
    
@app.post('/prediction')
async def make_prediction(input: Input):
    """_summary_

    Returns:
        _type_: _description_
    """
    # Creating df with the row
    text_input = [(input.text)]
    
    df = pd.DataFrame(text_input, columns=['content'])

    emotions = ['anger', 'fear', 'happy', 'sadness']
    
    # Make a prediction
    predictions = model.predict(df['content'])[0]
    prediction = predictions.tolist()

    return {
        'Input': input,
        'Emotions': emotions,
        'Prediction': prediction,
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8555)