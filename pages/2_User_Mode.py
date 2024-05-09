import streamlit as st
import pandas as pd
import numpy as np
from Predictor import Predictor as Predictor_
import sys
sys.tracebacklimit=0
import warnings
warnings.filterwarnings("ignore")
from streamlit_extras.stateful_button import button as stbutton


df_mts=pd.read_csv('venues_mts.csv').dropna()
df_approved=pd.read_csv('df_orgs.csv')

# _predictor1=Predictor_(df_mts)
# _predictor2=Predictor_(df_approved)

CUTOFF=0.5    
    
def initial_set_page():
    st.set_page_config( 
        
        page_title="User Mode",
        page_icon="♿",
        layout="wide",
    )
    st.image('mts_logo.jpg', caption=[''], width=200)
    
    st.title(':red[LIVE без границ]')

    st.header("")
    st.subheader(':black[Проверьте, какие возможности предоставляет площадка]')
    
initial_set_page()



# @st.cache_data
# def find_most_similar(_predictor_instance, target):
#     indexes, res, distance =_predictor_instance.find_matches(target)
#     return indexes, res, distance

@st.cache_data
def find_most_similar(df, target):
    predictor_instance=Predictor_(df, target)
    indexes, res,distance=predictor_instance.find_matches()
    return indexes, res, distance




col1,col2,col3,col4= st.columns([1,1,1,1])


selected_site=col1.text_input('Название площадки', max_chars=50)
selected_city=col2.text_input('Город', 'Москва')
selected_street=col3.text_input('Улица', max_chars=50)
selected_building=col4.text_input('Дом', max_chars=10)
selected_site=selected_site.title()
selected_street=selected_street.title()

venue=selected_site + ' ' + selected_city + ' ' + selected_street + ' ' + selected_building
st.write('Вы выбрали площадку:', venue)


  
if not selected_site or not selected_street or not selected_building:
    st.write(':red[Не введено название площадки, улица или номер дома]')

else:
    button=st.button('Искать', key='primary_search')
    if button:
        indexes, res, distance=find_most_similar(df_mts, venue)  
        # indexes, res, distance=find_most_similar(_predictor1, venue)  
        mts_venue_found=res.values[0]
        if distance>CUTOFF:
            st.write('\n')
            st.write(':red[Данная площадка не зарегистрирована на сайте]')
            st.session_state.button = False
        else:
            st.write('На сайте МТС-Live найдена площадка по Вашему запросу:', mts_venue_found)
            st.session_state.mts_venue_found=mts_venue_found
            st.session_state.button = True

    if st.session_state.button:         
        checkbox= st.checkbox('Узнать про возможности площадки')
        if checkbox:
            indexes, res, distance=find_most_similar(df_approved, st.session_state.mts_venue_found)
            # indexes, res, distance=find_most_similar(_predictor2, st.session_state.mts_venue_found)
            if distance>CUTOFF:
                st.write('\n')
                st.write(':red[Не найдено сведений в реестре доступности для выбранной площадки]')
            else:
                st.write('По Вашему запросу найдена площадка:  🏦  ', res.values[0])
                st.write('Сведения о площадке представлены реестром доступности социальных объектов', 'https://zhit-vmeste.ru/map/')
                df_temp=df_approved.drop(['Unnamed: 0', 'Адрес', 'Название учреждения', 'vector'], axis=1).loc[indexes]
                df_temp=df_temp.reset_index().drop('index', axis=1).T.rename({0:'Доступность объекта'}, axis=1)
                df_temp['Доступность объекта']=df_temp['Доступность объекта'].apply(lambda x: '✅   да' if x==1 else '❌   нет')     
                df_temp.index.rename('Категории посетителей', inplace=True)   

                st.write(df_temp)
                
