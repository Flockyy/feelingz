from unittest import result
import streamlit as st 
import requests
import pandas as pd 
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import plotly.express as px 

def main():

    if 'is_active' not in st.session_state or st.session_state.is_active == False:

        sign_up = st.sidebar.checkbox('Sign up')

        if sign_up:
            st.markdown("### $1000000000 for an account pls :money_with_wings:")

            with st.form(key='signup_form'):
                
                url_add_user = "http://host.docker.internal:8000/add_user" 
                st.write('Sign up')
                email = st.text_input(label='Email')
                f_name = st.text_input(label='First name')
                l_name = st.text_input(label='Last name')
                password = st.text_input(label='Password', type='password')
                pred_button = st.form_submit_button(label='Submit')

                if pred_button:

                    response = requests.post(url = url_add_user, json={ 'f_name': f_name, 'l_name': l_name, 'email':email , 'password':password})
                    response_json = response.json() 

                    if response.status_code == 401:
                        st.error('Email already exists')

                    else:
                        st.session_state['user_id'] = response_json['user_id']
                        st.session_state.is_active = True
                        st.experimental_rerun()
                    
                        

        else:
            with st.form(key='login_form'):

                url_login = "http://host.docker.internal:8000/login" 

                st.write('Login')
                email = st.text_input(label='Email')
                password = st.text_input(label='Password', type='password')
                pred_button = st.form_submit_button(label='Submit')
                
                if pred_button:

                    response = requests.post(url = url_login, json={'email':email , 'password':password})
                    response_json = response.json()

                    if response.status_code == 200:
                        st.session_state.is_active = True

                        st.experimental_rerun()
                    else:
                        st.error('Invalid credentials')

    elif 'is_active' in st.session_state and st.session_state.is_active == True:

        logout = st.sidebar.button('Logout')
        if logout:
            st.session_state.is_active = False
            st.experimental_rerun()

        activities = ["About this AI application", "Data visualisation", "Prediction"]
        st.sidebar.title("Navigation")
        choices = st.sidebar.radio("",activities)
        
        if choices == 'About this AI application':
            st.header("About this application")
            st.write("This application will report the Feeling associated to a sentence.")
            st.markdown("""The NLP algorithm used is a custom one made by.""")
            
        if choices == 'Data visualisation':
            # Add plot
            st.header("Data visualisation based on Kaggle quora question and Data world twitter datasets")
            url_get_all_pred = "http://host.docker.internal:8000/get_all_prediction/" + str(st.session_state.user_id)

            response = requests.get(url = url_get_all_pred)
            response_json = response.json()

            if response_json['pred_list'] != []:
                df = pd.DataFrame(response_json['pred_list'])
                df = df.drop(['owner_id', 'best_result', 'id'], axis=1)
                fig=px.bar(df['emotion'])
                fig2=px.pie(df['emotion'])
                st.write(fig2)
                st.write(fig)

            else:
                st.write(data='nodata')

            
        if choices == 'Prediction':
            url_get_all_pred = "http://host.docker.internal:8000/get_all_prediction/" + str(st.session_state.user_id)
            url_get_pred = "http://host.docker.internal:8000/prediction"

            response = requests.get(url = url_get_all_pred)
            response_json = response.json()

            if response_json['pred_list'] != []:
                df = pd.DataFrame(response_json['pred_list'])
                df = df.drop(['owner_id', 'best_result', 'id', 'results', 'time_updated'], axis=1)
                # st.table(data=df)
                AgGrid(df)

            else:
                st.header('Please feel free to make your first prediction')
            
            with st.form(key='pred_form'):
                with st.sidebar:
                    st.sidebar.header("Real-time prediction")
                    input = st.sidebar.text_input(label='Enter some text')
                    pred_button = st.form_submit_button(label='Submit')

                    if pred_button:
                        response = requests.post(url = url_get_pred, json={'text': input, 'user_id': st.session_state.user_id})
                        response_json = response.json()
                        if response_json['msg']:
                            st.success('Prediction added')
                            st.experimental_rerun()

            
if __name__ == '__main__':
    main()