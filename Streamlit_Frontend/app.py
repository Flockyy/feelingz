from unittest import result
import streamlit as st 
import requests
import pandas as pd 
# from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import plotly.express as px 

#TODO: Separate if with some commentary 

def main():

    if 'is_active' not in st.session_state or st.session_state.is_active == 0:

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
                        st.session_state['f_name'] = response_json['f_name']
                        st.session_state['l_name'] = response_json['l_name']
                        st.session_state['user_id'] = response_json['user_id']
                        st.session_state['is_admin'] = 0
                        st.session_state.is_active = 1
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
                    
                    if response.status_code == 401:
                        st.error('Invalid credentials')

                    else:
                        st.session_state['f_name'] = response_json['f_name']
                        st.session_state['l_name'] = response_json['l_name']
                        st.session_state['user_id'] = response_json['user_id']
                        st.session_state['is_admin'] = response_json['is_admin']
                        st.session_state.is_active = True
                        st.experimental_rerun()

    elif 'is_active' in st.session_state and st.session_state.is_admin == False and st.session_state.is_active == True:
        st.sidebar.header(f'Welcome, {st.session_state.f_name} {st.session_state.l_name}')
        logout = st.sidebar.button('Logout')
        
        if logout:
            st.session_state.is_active = 0
            st.experimental_rerun()

        activities = ["About this AI application", "Data visualisation", "Prediction", "Modify prediction"]
        st.sidebar.title("Navigation")
        choices = st.sidebar.radio("",activities)
        
        if choices == 'About this AI application':
            st.header("About this application")
            st.write("This application will report the Feeling associated to a sentence.")
            st.markdown("""The NLP algorithm used is a custom one made by.""")
            
        if choices == 'Data visualisation':
            # Add plot
            st.header("Data visualisation based on Kaggle quora question and Data world twitter datasets")
            url_get_all_pred = "http://host.docker.internal:8000/get_predictions_by_user/" + str(st.session_state.user_id)

            response = requests.get(url = url_get_all_pred)
            response_json = response.json()

            if response_json['pred_list'] != []:
                df = pd.DataFrame(response_json['pred_list'])
                emotions_cnt = df.groupby(by=["emotion"]).count()[['id']].rename(columns={"id":"count"}).reset_index()
                pie_fig = px.pie(emotions_cnt, names="emotion", values="count", hole=0.4)
                
                df = df.drop(['owner_id', 'best_result', 'id'], axis=1)
                bar_fig=px.bar(df['emotion'])

                st.write(bar_fig)
                st.write(pie_fig)

            else:
                st.write(data='nodata')

            
        if choices == 'Prediction':
            url_get_all_pred = "http://host.docker.internal:8000/get_predictions_by_user/" + str(st.session_state.user_id)
            url_get_pred = "http://host.docker.internal:8000/prediction"

            response = requests.get(url = url_get_all_pred)
            response_json = response.json()

            if response_json['pred_list'] != []:
                df = pd.DataFrame(response_json['pred_list'])
                df = df.drop(['owner_id', 'best_result', 'id', 'results', 'time_updated'], axis=1)
                st.table(data=df)
                # AgGrid(df)

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
                            
        if choices == 'Modify prediction':
            url_get_all_pred = "http://host.docker.internal:8000/get_predictions_by_user/" + str(st.session_state.user_id)
            response = requests.get(url = url_get_all_pred)
            response_json = response.json()
            if response_json['pred_list'] != []:
                df = pd.DataFrame(response_json['pred_list'])
                option = st.selectbox(
                'Which text du you want to modify?',
                (df['text'])
                )
                # st.write(response_json['pred_list'])
                st.write('You selected:', option)
                df_choice = df[df['text'] == option]
                idx = df_choice.index[0]
                if df_choice['time_updated'][idx]:
                    accurate_date = df_choice['time_updated'][idx]
                    accurate_label = 'Update date'
                else:
                    accurate_date = df_choice['time_created'][idx]
                    accurate_label = 'Date'
                id = response_json['pred_list'][idx]['id']

                with st.form(key='modify_text_form'):
                
                    url_modify_text = "http://host.docker.internal:8000/update_pred/"
                    st.write('Modify')
                    date = st.text_input(label=accurate_label, value=accurate_date, disabled=True)
                    text = st.text_input(label='Text', value=df_choice['text'][idx])
                    emotion = st.text_input(label='Emotion', value=df_choice['emotion'][idx], disabled=True)
                    modify_text_button = st.form_submit_button(label='Submit')
                    
                    if modify_text_button:
                        response = requests.patch(url = url_modify_text, json={'pred_id': str(id),'text': text})
                        st.success('Modified')
                        st.experimental_rerun()
                        
    else : 
        st.sidebar.header(f'Welcome, {st.session_state.f_name} {st.session_state.l_name}')
        logout = st.sidebar.button('Logout')
        
        if logout:
            st.session_state.is_active = False
            st.experimental_rerun()

        activities = ["Home", "Data visualisation", "Patient management"]
        st.sidebar.title("Navigation")
        choices = st.sidebar.radio("",activities)
        
        if choices == 'Home':
            st.header("About this application")
            st.write("This application will report the Feeling associated to a sentence.")
            st.markdown("""The NLP algorithm used is a custom one made by.""")
            
        if choices == 'Patient management':
            url_get_all_users= "http://host.docker.internal:8000/get_all_users"

            response = requests.get(url = url_get_all_users)
            response_json = response.json()

            if response_json['user_list'] != []:
                df = pd.DataFrame(response_json['user_list'])
                st.table(data=df)
        
if __name__ == '__main__':
    main()