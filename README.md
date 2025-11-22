#  Feelingz - Emotion Analysis Platform
<div align="center">

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

**AI-powered sentiment analysis web application for life coaching professionals**

[Features](#-key-features)  [Architecture](#-architecture)  [Installation](#-quick-start)  [Usage](#-usage)  [ML Model](#-ml-model)  [API Docs](#-api-endpoints)

</div>

---

##  Overview

**Feelingz** is a full-stack emotion detection platform designed for life coaches to track and analyze their clients' emotional journeys. Built with microservices architecture using **FastAPI backend** and **Streamlit frontend**, the application leverages deep learning (Conv1D neural networks) trained on sentiment datasets to predict emotions from daily journal entries.

###  Key Features

- ** NLP Emotion Detection**: CNN-based sentiment analysis trained on Kaggle + Twitter datasets
- ** Daily Journal Tracking**: Clients submit daily text entries with automatic emotion classification
- ** Analytics Dashboard**: Visual insights and trends for coaching professionals
- ** Client Management**: CRUD operations for coach-client relationships
- ** Docker Deployment**: Fully containerized with docker-compose for easy setup
- ** Database Persistence**: SQLite backend for data storage
- ** Interactive UI**: Clean Streamlit interface for users and coaches
- ** RESTful API**: FastAPI backend with automatic OpenAPI documentation

---

##  Architecture

\\\

         Docker Compose Orchestration           
                                                
        
    Streamlit          FastAPI         
    Frontend               Backend         
    Port: 8501             Port: 8000      
                                           
    Client views         CRUD API        
    Coach dashboard      ML inference    
    Data input           SQLite DB       
        
                                               
                                   
                            Conv1D            
                           NLP Model          
                           (Keras)            
                                   

\\\

### Technology Stack

| Component | Technologies |
|-----------|-------------|
| **Backend** | FastAPI, SQLAlchemy, Uvicorn |
| **Frontend** | Streamlit, Requests |
| **ML/NLP** | TensorFlow/Keras, Conv1D, Word2Vec, texthero |
| **Database** | SQLite |
| **Deployment** | Docker, Docker Compose |
| **Python** | 3.9.7+ |

---

##  Project Structure

\\\
feelingz/
 docker-compose.yml           # Orchestration configuration
 README.md
 FastAPI_Backend/
    main.py                  # FastAPI application
    models.py                # SQLAlchemy models
    database.py              # DB session management
    cruds.py                 # CRUD operations
    requirements.txt         # Backend dependencies
    Dockerfile               # Backend container
    sql_app.db               # SQLite database
    Conv1d/                  # Trained emotion model
        saved_model.pb
        keras_metadata.pb
        variables/
 Streamlit_Frontend/
    app.py                   # Streamlit UI application
    requirements.txt         # Frontend dependencies
    Dockerfile               # Frontend container
 flo/                         # Model development notebooks
    eda.ipynb                # Exploratory data analysis
    mod_keras.ipynb          # Keras model training
    mod_hugging.ipynb        # HuggingFace experiments
 arnold/
    texthero_partage_2.ipynb # Text preprocessing experiments
 theophile/
    Projet_wordvectgo.ipynb  # Word2Vec implementation
    Projet_wordvectJournal.ipynb
 mlruns/                      # MLflow experiment tracking
\\\

---

##  Quick Start

### Prerequisites

- **Python** >= 3.9.7
- **Docker Desktop** (for containerized deployment)
- **Git**

### Installation & Deployment

1. **Clone the repository**
\\\ash
git clone https://github.com/Flockyy/feelingz.git
cd feelingz
\\\

2. **Launch with Docker Compose**
\\\ash
docker-compose up --build
\\\

This will start:
- **FastAPI Backend**: http://localhost:8000
- **Streamlit Frontend**: http://localhost:8501

3. **Access the application**
- Open browser at **http://localhost:8501** for the Streamlit UI
- API docs available at **http://localhost:8000/docs**

### Manual Setup (Without Docker)

<details>
<summary><b>Backend Setup</b> (Click to expand)</summary>

\\\ash
cd FastAPI_Backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
\\\

</details>

<details>
<summary><b>Frontend Setup</b> (Click to expand)</summary>

\\\ash
cd Streamlit_Frontend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py --server.port 8501
\\\

</details>

---

##  Usage

### For Clients (Users)

1. **Submit Daily Entry**
   - Navigate to "Daily Journal" section
   - Write today's thoughts and feelings
   - Click "Submit" - AI automatically detects emotion

2. **View History**
   - Browse past journal entries
   - See predicted emotions for each day
   - Edit or delete previous entries

3. **Emotion Tracking**
   - View emotion trends over time
   - Identify patterns in mood changes

### For Coaches (Professionals)

1. **Client Management**
   - Add new clients with contact info
   - Update client details
   - Remove inactive clients

2. **Analytics Dashboard**
   - View aggregated emotion data per client
   - Generate reports for coaching sessions
   - Track client progress over time

3. **Data Insights**
   - Identify emotional patterns
   - Correlate emotions with life events
   - Make data-driven coaching decisions

---

##  ML Model

### Architecture

**Conv1D Neural Network for Text Classification**:
\\\python
Model: Sequential
- Embedding Layer (Word2Vec pre-trained)
- Conv1D (128 filters, kernel size 5, ReLU)
- GlobalMaxPooling1D
- Dense (64 units, ReLU)
- Dropout (0.5)
- Dense (6 units, Softmax)  # 6 emotion classes
\\\

### Training Data

- **Kaggle Sentiment Analysis Dataset**: 1M+ labeled tweets
- **Data.world Twitter Dataset**: Domain-specific emotion labels
- **Combined preprocessing** with texthero library

### Emotion Classes

| Class | Description |
|-------|-------------|
|  Joy | Positive, happy, excited |
|  Sadness | Depressed, melancholic |
|  Anger | Frustrated, annoyed |
|  Fear | Anxious, worried |
|  Surprise | Astonished, shocked |
|  Neutral | Balanced, calm |

### Model Performance

- **Accuracy**: ~85% on validation set
- **F1-Score**: 0.82 (macro-averaged)
- **Inference Time**: <50ms per prediction

### Retraining (Advanced)

\\\ash
# Explore training notebooks in flo/ directory
jupyter notebook flo/mod_keras.ipynb

# Run MLflow tracking
mlflow ui --backend-store-uri mlruns/
\\\

---

##  API Endpoints

### Client Operations

| Method | Endpoint | Description |
|--------|----------|-------------|
| \POST\ | \/clients/\ | Create new client |
| \GET\ | \/clients/\ | List all clients |
| \GET\ | \/clients/{id}\ | Get client details |
| \PUT\ | \/clients/{id}\ | Update client info |
| \DELETE\ | \/clients/{id}\ | Delete client |

### Journal Entry Operations

| Method | Endpoint | Description |
|--------|----------|-------------|
| \POST\ | \/entries/\ | Submit journal entry + predict emotion |
| \GET\ | \/entries/{client_id}\ | Get all entries for client |
| \PUT\ | \/entries/{id}\ | Edit entry text |
| \DELETE\ | \/entries/{id}\ | Delete entry |

### ML Prediction

| Method | Endpoint | Description |
|--------|----------|-------------|
| \POST\ | \/predict/\ | Get emotion prediction for text |

### Example API Request

\\\ash
# Predict emotion from text
curl -X POST http://localhost:8000/predict/ \\
  -H "Content-Type: application/json" \\
  -d '{"text": "I feel amazing today! Everything is going perfectly."}'

# Response:
# {"emotion": "joy", "confidence": 0.92, "probabilities": {...}}
\\\

---

##  Docker Configuration

### docker-compose.yml

\\\yaml
version: '3.8'
services:
  backend:
    build: ./FastAPI_Backend
    ports:
      - "8000:8000"
    volumes:
      - ./FastAPI_Backend:/app
    environment:
      - DATABASE_URL=sqlite:///./sql_app.db

  frontend:
    build: ./Streamlit_Frontend
    ports:
      - "8501:8501"
    depends_on:
      - backend
    environment:
      - BACKEND_URL=http://backend:8000
\\\

---

##  Development

### Running Tests

\\\ash
# Backend tests
cd FastAPI_Backend
pytest tests/ -v

# Model evaluation
python -m notebooks.flo.mod_keras
\\\

### Database Management

\\\ash
# Reset database
rm FastAPI_Backend/sql_app.db
python FastAPI_Backend/database.py
\\\

---

##  Contributing

This project was developed as a team collaboration for coursework. Contributions are welcome!

**Team Members**:
- **Florian** (flo/) - ML model development, Keras implementation
- **Arnold** (arnold/) - Text preprocessing, texthero integration
- **Théophile** (theophile/) - Word2Vec embeddings, NLP experiments

### Contribution Guidelines

1. Fork the repository
2. Create feature branch (\git checkout -b feature/new-feature\)
3. Test locally with \docker-compose up\
4. Commit changes (\git commit -m 'Add feature'\)
5. Push to branch (\git push origin feature/new-feature\)
6. Open Pull Request

---

##  License

This project is a training application for educational purposes.

---

##  Acknowledgments

- **Kaggle** for sentiment analysis datasets
- **Data.world** for Twitter emotion corpus
- **FastAPI** framework by Sebastián Ramírez
- **Streamlit** team for the frontend framework
- **TensorFlow/Keras** for deep learning tools
- Course instructors and fellow students

---

##  Feedback

Feel free to try this app and send feedback! We appreciate your input for improving the platform.

---

<div align="center">

**[ Back to Top](#-feelingz---emotion-analysis-platform)**

Made with  by [Florian Abgrall](https://github.com/Flockyy) & Team

</div>
