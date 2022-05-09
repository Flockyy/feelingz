import streamlit as st 
from streamlit import caching
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    
    st.title("AI service for Emotion prediction based on a sentence")
    st.header("Emotion prediction")
    st.write("This application enables to report the feeling associated to a text")
    
    caching.clear_cache()
    activities = ["About this AI application", "Data visualisation", "Prediction"]
    st.sidebar.title("Navigation")
    choices = st.sidebar.radio("",activities)
    
    if choices == 'About this AI application':
        st.header("About this application")
        st.write("This application will report the Feeling associated to a sentence.")
        st.markdown("""The NLP algorithm used is a custom one made by.""")
        
    if choices == 'About this AI application':
        
        st.header("About this application")
        st.write("This application will report the Feeling associated to a sentence.")
        st.markdown("""The NLP algorithm used is a custom one made by.""")
        
    if choices == 'Prediction':
        
        st.header("Real-time prediction")
        url_entities="http://backend.docker:8000/prediction/"
        
        if 'predict' in st.session_state:
            pass