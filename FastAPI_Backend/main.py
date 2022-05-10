from fastapi import FastAPI, Depends
from starlette.responses import RedirectResponse
import tensorflow as tf
import uvicorn
import pandas as pd
from models.SQLModels import User
from models import SQLModels
from sqlalchemy.orm import Session
from schemas import PDTSchemas
from models.database import SessionLocal, engine

SQLModels.Base.metadata.create_all(bind=engine)

# from models.SQLModels import Document
app = FastAPI()

def create_user(db: Session, user: PDTSchemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def load_model():
    """
    Loads and returns the pretrained model
    """
    model = tf.keras.models.load_model("Conv1d")
    print("Model loaded")
    return model

model = load_model()

# np.testing.assert_allclose(
#     loaded_model.predict(test_input)
# )

@app.get("/")
def root():
    response = RedirectResponse(url='/docs')
    return response

@app.post('/add_user', response_model=PDTSchemas.User)
async def add_user(user: PDTSchemas.UserCreate, db: Session = Depends(get_db)):
    create_user(db=db, user=user)
    return {'Success' : 'user_created'}

@app.post('/prediction')
async def get_prediction():
    #Creating df with the row
    test_input = [('Because i am happy')]
    df = pd.DataFrame(test_input, columns=['content'])

    #Make a prediction
    predictions = model.predict(df['content'])[0]
    prediction = predictions.tolist()
    

    return {
        'Input': test_input,
        'Prediction': prediction,
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8555)