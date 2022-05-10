from unittest import result
import streamlit as st 
import requests
# import altair as alt
# import matplotlib.pyplot as plt
# import seaborn as sns

def main():
    
    st.title("AI service for Emotion prediction based on a sentence")
    st.header("Emotion prediction")
    st.write("This application enables to report the feeling associated to a text")
    
    activities = ["About this AI application", "Data visualisation", "Prediction"]
    st.sidebar.title("Navigation")
    choices = st.sidebar.radio("",activities)
    
    if choices == 'About this AI application':
        st.header("About this application")
        st.write("This application will report the Feeling associated to a sentence.")
        st.markdown("""The NLP algorithm used is a custom one made by.""")
        
    if choices == 'Data visualisation':
        # Add plot
        st.header("Data visualisation based on Kaggle and Data world datasets")
        st.write("Data viz inc in v2")
        
    if choices == 'Prediction':
        
        st.header("Real-time prediction")
        url_get_pred = "http://host.docker.internal:8000/prediction"
        url_add_user = "http://host.docker.internal:8000/add_user" 

        if st.button(label='Add_User'):
            response = requests.post(url = url_add_user, json={'email':'test@test.com' , 'password':'1234'}, timeout=5, verify=False )
            st.success(response.text)

        if st.button(label='Predict'):
            response = requests.post(url = url_get_pred, timeout=5, verify=False )
            st.success(response.text)
                    
if __name__ == '__main__':
    main()