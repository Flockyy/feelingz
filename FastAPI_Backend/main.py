from turtle import textinput
from fastapi import FastAPI
from pydantic import BaseModel
# import numpy as np
import tensorflow as tf
import uvicorn
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from models.SQLModels import Document

app = FastAPI()

#Creating a class for the attributes input to the ML model.
class Document(BaseModel):
	text : str
 
test_input = 'Because i\'m happy !'

#Loading the trained model
loaded_model = tf.keras.models.load_model("./FastAPI_Backend/Conv1d")


# np.testing.assert_allclose(
#     loaded_model.predict(test_input)
# )

@app.get("/")
def root():
    return {"message": "Welcome from the API"}

@app.post('/prediction')
def get_prediction():
# data: test_input
    # received = data.dict()
    # text = received['text']
    pred_res = loaded_model.predict(textinput).tolist()[0]
    return {'Prediction':  pred_res}

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8555)