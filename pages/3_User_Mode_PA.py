import streamlit as st
import pandas as pd
import numpy as np
from Predictor import Predictor as Predictor_
import sys
sys.tracebacklimit=0
import warnings
warnings.filterwarnings("ignore")
from streamlit_star_rating import st_star_rating
from streamlit_extras.stateful_button import button as stbutton



def initial_set_page():
    st.set_page_config( 
        
        page_title="User Mode PA",
        page_icon="♿",
        layout="wide",
    )
    st.image('mts_logo.jpg', caption=[''], width=200)
    # st.image('dostup_sreda.jpg', caption='Доступная среда')
    st.image('live_venue.jpg', width=500)
    
    st.title(':red[LIVE на полную]')

    st.header("")
    st.subheader(':red[Здравствуйте, Username]')
    st.header("")
    st.subheader('Ниже Вы можете просмотреть список посещенных и предстоящих мероприятий')    
    
initial_set_page()

st.header("")

col1, col2, col3,col5, col4 = st.columns([0.5,1,1,0.3,2])


button1=stbutton('Прошедшие мероприятия', key=1)
if button1:
    with col1:
        st.subheader("Дата")
        st.write('')
        st.write("2024-05-06")
        st.write('')
        st.write("2024-02-20")
        st.write('')
        st.write("2023-12-31")

    with col2:
        st.subheader("Название")
        st.write('')
        st.write("Женитьба Фигаро, спектакль")
        st.write('')
        st.write("КороЛЕВство")
        st.write('')
        st.write("Щелкунчик, балет")

    with col3:
        st.subheader("Площадка")
        st.write('')
        st.write("Театр на Таганке")
        st.write('')
        st.write("Большой Московский цирк")
        st.write('')
        st.write("Государственный академический Большой театр")
    
    with col4:
        st.subheader("Оцените доступность площадки")
        stars1 = st_star_rating('', maxValue=5, defaultValue=5, key="rating1", size=27.5, read_only=True)
        stars2 = st_star_rating('', maxValue=5, defaultValue=4, key="rating2", size=27.5, read_only=True)
        stars3 = st_star_rating('', maxValue=5, defaultValue=0, key="rating3", size=27.5, read_only=True)
   

col1, col2, col3, col4 = st.columns([1,1,1,1])
button2=stbutton('Предстоящие мероприятия', key=2)
if button2:
    with col1:
        st.subheader("Название")
        st.write('')
        st.write("**Мастер и Маргарита**, спектакль")
        st.write('')

    with col2:
        st.subheader("Площадка")
        st.write('')
        st.write("**МХТ имени А.П. Чехова**")
        st.write('')
    
    with col3:
        st.subheader("Дата")
        st.write('')
        st.write("**2024-07-26**")
        
    with col4:
        st.subheader("")
        st.write('')
        st.write('')
        st.write('')
        st.checkbox("Мне потребуется помощь сопровождающего")


st.write('')
rate_button=stbutton('Оценить доступность площадки', key='button_rating')

if rate_button:
    st.write('')
    st.header('Для оценки доступна площадка: Государственный академический Большой театр  🏦')
    st.write('')
    st.write('')
  
    
    with st.form("my_form"):
        st.subheader('Оцените общее впечатление от площадки')
        stars4 = st_star_rating('', maxValue=5, defaultValue=None, key="rating3", size=27.5, read_only=False)
        
        st.write('Вам понравилась парковка?')
        col1, col2 = st.columns([0.5,0.5])
        with col1:
            agree1=st.checkbox('✅   да', key='option1')
            if agree1:
                print('Ваш ответ принят ✅')
        with col2:
            disagree1=st.checkbox('❌   нет', key='option2')
            if disagree1:
                print('Ваш ответ принят ✅')

        st.write('Вам понравились удобства площадки?')
        col1, col2 = st.columns([0.5,0.5])
        with col1:
            agree1=st.checkbox('✅   да', key='option3')
        with col2:
            disagree1=st.checkbox('❌   нет', key='option4')
            
        st.write('Вам была оказана помощь персонала?')
        col1, col2 = st.columns([0.5,0.5])
        with col1:
            agree1=st.checkbox('✅   да', key='option5')
        with col2:
            disagree1=st.checkbox('❌   нет', key='option6')
            
        st.write('')   
        st.text_area("Оставьте комментарии или пожелания к площадке")

        # Every form must have a submit button.
        st.write('')
        submitted = st.form_submit_button("Отправить отзыв")
        if submitted:
            st.write(':green[**Спасибо, Ваш отзыв принят!**]')

