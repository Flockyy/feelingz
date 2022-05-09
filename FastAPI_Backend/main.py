from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import tensorflow as tf
from tensorflow import keras
# import pickle
import uvicorn

app = FastAPI()

#Creating a class for the attributes input to the ML model.
class Text(BaseModel):
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