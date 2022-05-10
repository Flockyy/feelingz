from cgi import test
from fastapi import FastAPI
from pydantic import BaseModel
# import numpy as np
import tensorflow as tf
import uvicorn
import numpy as np
from typing import List
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from models.SQLModels import Document

app = FastAPI()

#Creating a class for the attributes input to the ML model.
class Document(BaseModel):
    text : str
    prediction: List[float] = []

def load_model():
    """
    Loads and returns the pretrained model
    """
    model = tf.keras.models.load_model("./FastAPI_Backend/Conv1d")
    print("Model loaded")
    return model

model = load_model()

# np.testing.assert_allclose(
#     loaded_model.predict(test_input)
# )

@app.get("/")
def root():
    return {"message": "Welcome from the API"}

@app.post('/prediction')
async def get_prediction():
    #Creating df with the row
    test_input = [('Because i am happy')]
    df = pd.DataFrame(test_input, columns=['content'])
    print(df)

    #Make a prediction
    predictions = model.predict(df['content'])[0]
    prediction = predictions.tolist()
    

    return {
        'Input': test_input,
        'Prediction': prediction,
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8555)