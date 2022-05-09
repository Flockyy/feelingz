from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import tensorflow as tf
from tensorflow import keras
# import pickle
import uvicorn
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

# Database creation
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#Creating a class for the attributes input to the ML model.
class Model_input(BaseModel):
	text : str
 
test_input = 'Because i\'m happy !'

#Loading the trained model  
loaded_model = keras.models.load_model("../flo/conv1dmodel")

np.testing.assert_allclose(
    loaded_model.predict(test_input)
)

@app.get("/")
def root():
    return {"message": "Welcome from the API"}

@app.post('/prediction')
def get_prediction(data: Text):
    received = data.dict()
    text = received['text']
    pred_name = loaded_model.predict([[text]]).tolist()[0]
    return {'Prediction':  pred_name}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)