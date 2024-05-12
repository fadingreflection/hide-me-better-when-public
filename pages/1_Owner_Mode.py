import streamlit as st
import pandas as pd
import numpy as np
from Predictor2 import Predictor as Predictor_
import sys
sys.tracebacklimit=0
import warnings
import pickle
warnings.filterwarnings("ignore")
from streamlit_extras.stateful_button import button as stbutton



CUTOFF=0.5

def initial_set_page():
    st.set_page_config( 
        
        page_title="Owner Mode",
        page_icon="♿",
        layout="wide",
    )
    st.image('mts_logo.jpg', caption=[''], width=200)
    
    st.title(':red[LIVE для всех и каждого]')

    st.header("")
    st.subheader(':red[Здравствуйте, Username]')
    st.header("")
    st.subheader(':black[Проверьте, какие возможности предоставляет Ваша площадка]')
    
initial_set_page()


df_approved=pd.read_csv('df_orgs.csv')
with open('embeddings_dostup.pickle', 'rb') as file:
    dostup_embeddings = pickle.load(file)
df_approved['embeddings']=dostup_embeddings['embeddings']

_predictor2=Predictor_(df_approved)



@st.cache_data
def find_most_similar(_predictor_instance, target):
    indexes, res, distance =_predictor_instance.find_matches(target)
    return indexes, res, distance


col1,col2,col3,col4= st.columns([1,1,1,1])


selected_site=col1.text_input('Название площадки', 'Театр на Таганке', max_chars=50)
selected_city=col2.text_input('Город', 'Москва')
selected_street=col3.text_input('Улица', 'Земляной Вал', max_chars=50)
selected_building=col4.text_input('Дом', '76/21 строение 1', max_chars=6)
selected_site=selected_site.title()
selected_street=selected_street.title()



venue=selected_site + ' ' + selected_city + ' ' + selected_street + ' ' + selected_building
st.session_state.venue=venue
st.write('Ваша площадка:', venue)

st.header("")    
    
checkbox= st.checkbox('Узнать про возможности Вашей площадки')
if checkbox:
    indexes, res, distance=find_most_similar(_predictor2, st.session_state.venue) 
    if distance>CUTOFF:
        st.write('\n')
        st.write(':red[Не найдено сведений в реестре доступности]')
    else:
        st.write('По Вашему запросу найдена площадка:', res.values[0])
        df_temp=df_approved.drop(['Unnamed: 0', 'Адрес', 'Название учреждения', 'vector'], axis=1).loc[indexes]
        df_temp=df_temp.reset_index().drop('index', axis=1).T.rename({0:'Доступность объекта'}, axis=1)
        
        def map_labels(x):
            if x=='1':
                res='✅   да'
            elif x=='0':
                res='❌   нет'
            else:
                res=x
            return res
                
        df_temp['Доступность объекта']=df_temp['Доступность объекта'].apply(lambda x: map_labels(str(x)))     
        df_temp.index.rename('Категории посетителей', inplace=True)  
        st.write('\n')
        st.write('\n')
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric(df_temp['Доступность объекта'][0], "👁️‍🗨️")
        col2.metric(df_temp['Доступность объекта'][1], "🦻🏻")
        col3.metric(df_temp['Доступность объекта'][2], "👨🏾‍🦽")
        col4.metric(df_temp['Доступность объекта'][3], "🩼")
        col5.metric(df_temp['Доступность объекта'][4], "🧠")
        st.write('\n')
        st.write('Сведения о площадке представлены реестром доступности социальных объектов', 'https://zhit-vmeste.ru/map/') 

        st.write('\n')
        st.write('\n')
        

update_button=stbutton('Обновить информацию о площадке', key='update')
st.write('\n')

if update_button:   
                
    with st.form("owner_form"):
        st.subheader('Заполните сведения о Вашей площадке')
        st.write('**Вход в здание**')
        
        st.write('Есть ли на площадке пандусы для обеспечения доступа для инвалидных колясок?')
        col1, col2, col3 = st.columns([0.5,0.5, 0.5])
        with col1:
            agree1=st.checkbox('✅   да', key='option1')
            if agree1:
                print('Ваш ответ принят ✅')
        with col2:
            disagree1=st.checkbox('❌   нет', key='option2')
            if disagree1:
                print('Ваш ответ принят ✅')                        
        with col3:
            no_info1=st.checkbox('❔   не располагаю информацией', key='option3')
            if no_info1:
                print('Ваш ответ принят ✅')
                
                
        st.write('Ширина дверных проходов и проемов соответствует нормативам для прохода инвалидных колясок? ')
        col1, col2, col3 = st.columns([0.5,0.5, 0.5])
        with col1:
            agree1=st.checkbox('✅   да', key='option4')
            if agree1:
                print('Ваш ответ принят ✅')
        with col2:
            disagree1=st.checkbox('❌   нет', key='option5')
            if disagree1:
                print('Ваш ответ принят ✅')                        
        with col3:
            no_info1=st.checkbox('❔   не располагаю информацией', key='option6')
            if no_info1:
                print('Ваш ответ принят ✅')
                
                
        st.write('Соответствует ли уровень порогов и плинтусов нормативам безбарьерного доступа?')
        col1, col2, col3 = st.columns([0.5,0.5, 0.5])
        with col1:
            agree1=st.checkbox('✅   да', key='option7')
            if agree1:
                print('Ваш ответ принят ✅')
        with col2:
            disagree1=st.checkbox('❌   нет', key='option8')
            if disagree1:
                print('Ваш ответ принят ✅')                        
        with col3:
            no_info1=st.checkbox('❔   не располагаю информацией', key='option9')
            if no_info1:
                print('Ваш ответ принят ✅')

            
        st.write('Оборудованы ли двери специальными механизмами для удобства использования лицами с ОВЗ?')
        col1, col2, col3 = st.columns([0.5,0.5, 0.5])
        with col1:
            agree1=st.checkbox('✅   да', key='option10')
            if agree1:
                print('Ваш ответ принят ✅')
        with col2:
            disagree1=st.checkbox('❌   нет', key='option11')
            if disagree1:
                print('Ваш ответ принят ✅')                        
        with col3:
            no_info1=st.checkbox('❔   не располагаю информацией', key='option12')
            if no_info1:
                print('Ваш ответ принят ✅')            

        st.write('Существует ли специально оборудованная крытая зона для защиты иц с ОВЗ от погодных условий?')
        col1, col2, col3 = st.columns([0.5,0.5, 0.5])
        with col1:
            agree1=st.checkbox('✅   да', key='option13')
            if agree1:
                print('Ваш ответ принят ✅')
        with col2:
            disagree1=st.checkbox('❌   нет', key='option14')
            if disagree1:
                print('Ваш ответ принят ✅')                        
        with col3:
            no_info1=st.checkbox('❔   не располагаю информацией', key='option15')
            if no_info1:
                print('Ваш ответ принят ✅')              
            
        st.write('\n')
        st.write('\n')
        st.write('**Лифты, лестницы и проходы**')
        
        st.write('Обеспечивается ли в лифтах достаточное пространство для комфортного перемещения инвалидных колясок?')
        col1, col2, col3 = st.columns([0.5,0.5, 0.5])
        with col1:
            agree1=st.checkbox('✅   да', key='option16')
            if agree1:
                print('Ваш ответ принят ✅')
        with col2:
            disagree1=st.checkbox('❌   нет', key='option17')
            if disagree1:
                print('Ваш ответ принят ✅')                        
        with col3:
            no_info1=st.checkbox('❔   не располагаю информацией', key='option18')
            if no_info1:
                print('Ваш ответ принят ✅')      
                
        st.write('Предусмотрено ли достаточное пространство для маневрирования и передвижения внутри помещения для обеспечения доступа инвалидных колясок?')
        col1, col2, col3 = st.columns([0.5,0.5, 0.5])
        with col1:
            agree1=st.checkbox('✅   да', key='option19')
            if agree1:
                print('Ваш ответ принят ✅')
        with col2:
            disagree1=st.checkbox('❌   нет', key='option20')
            if disagree1:
                print('Ваш ответ принят ✅')                        
        with col3:
            no_info1=st.checkbox('❔   не располагаю информацией', key='option21')
            if no_info1:
                print('Ваш ответ принят ✅')          
        
        st.write('\n')  
        st.write('\n')
        st.write('**Освещение**')
        
        st.write('Обеспечивается ли наличие адекватного освещения во всех зонах помещения для обеспечения видимости и безопасности лиц с ОВЗ?')
        col1, col2, col3 = st.columns([0.5,0.5, 0.5])
        with col1:
            agree1=st.checkbox('✅   да', key='option22')
            if agree1:
                print('Ваш ответ принят ✅')
        with col2:
            disagree1=st.checkbox('❌   нет', key='option23')
            if disagree1:
                print('Ваш ответ принят ✅')                        
        with col3:
            no_info1=st.checkbox('❔   не располагаю информацией', key='option24')
            if no_info1:
                print('Ваш ответ принят ✅')             
          
        st.write('\n')
        st.write('\n')
        st.write('**Системы навигации и информационный доступ**')
        
        st.write('Предусмотрены ли на площадке специальные маркировки или указатели для ориентации в пространстве лиц с ОВЗ?')
        col1, col2, col3 = st.columns([0.5,0.5, 0.5])
        with col1:
            agree1=st.checkbox('✅   да', key='option25')
            if agree1:
                print('Ваш ответ принят ✅')
        with col2:
            disagree1=st.checkbox('❌   нет', key='option26')
            if disagree1:
                print('Ваш ответ принят ✅')                        
        with col3:
            no_info1=st.checkbox('❔   не располагаю информацией', key='option27')
            if no_info1:
                print('Ваш ответ принят ✅')      
        
        st.write('\n') 
        st.write('\n')       
        st.write('**Туалетные комнаты**')
        
        st.write('Туалетные удобства для лиц с ОВЗ имеют специальное сантехническое оборудование, адаптированное под нужды лиц с ОВЗ (подъемные унитазы, раковины разной высоты и др.)?')
        col1, col2, col3 = st.columns([0.5,0.5, 0.5])
        with col1:
            agree1=st.checkbox('✅   да', key='option28')
            if agree1:
                print('Ваш ответ принят ✅')
        with col2:
            disagree1=st.checkbox('❌   нет', key='option29')
            if disagree1:
                print('Ваш ответ принят ✅')                        
        with col3:
            no_info1=st.checkbox('❔   не располагаю информацией', key='option30')
            if no_info1:
                print('Ваш ответ принят ✅')      
                
        st.write('Туалетные удобства для лиц с ОВЗ имеют кнопку срочного вызова персонала в случае возникновения экстренной ситуации?')
        col1, col2, col3 = st.columns([0.5,0.5, 0.5])
        with col1:
            agree1=st.checkbox('✅   да', key='option31')
            if agree1:
                print('Ваш ответ принят ✅')
        with col2:
            disagree1=st.checkbox('❌   нет', key='option32')
            if disagree1:
                print('Ваш ответ принят ✅')                        
        with col3:
            no_info1=st.checkbox('❔   не располагаю информацией', key='option33')
            if no_info1:
                print('Ваш ответ принят ✅')     
                
        st.write('\n') 
        st.write('\n')       
        st.write('**Парковка**')
        
        st.write('Предусмотрены ли специально отведенные парковочные места для лиц с ОВЗ?')
        col1, col2, col3 = st.columns([0.5,0.5, 0.5])
        with col1:
            agree1=st.checkbox('✅   да', key='option34')
            if agree1:
                print('Ваш ответ принят ✅')
        with col2:
            disagree1=st.checkbox('❌   нет', key='option35')
            if disagree1:
                print('Ваш ответ принят ✅')                        
        with col3:
            no_info1=st.checkbox('❔   не располагаю информацией', key='option36')
            if no_info1:
                print('Ваш ответ принят ✅')         
        
        st.write('\n')
        st.write('\n')
        st.write('**Персонал площадки**')
        
        st.write('Проводится ли аттестация персонала площадки с целью подтверждения квалификации по оказанию помощи лицам с ОВЗ?')
        col1, col2, col3 = st.columns([0.5,0.5, 0.5])
        with col1:
            agree1=st.checkbox('✅   да', key='option37')
            if agree1:
                print('Ваш ответ принят ✅')
        with col2:
            disagree1=st.checkbox('❌   нет', key='option38')
            if disagree1:
                print('Ваш ответ принят ✅')                        
        with col3:
            no_info1=st.checkbox('❔   не располагаю информацией', key='option39')
            if no_info1:
                print('Ваш ответ принят ✅')     
                
        st.write('\n')   
        st.write('\n')     
        st.write('**Безопасность и чрезвычайные ситуации**')
        
        st.write('Проводятся ли регулярные инспекции и техническое обслуживание оборудования (включая лифты, подъемники и пр.) для обеспечения их надежной работы и безопасности?')
        col1, col2, col3 = st.columns([0.5,0.5, 0.5])
        with col1:
            agree1=st.checkbox('✅   да', key='option40')
            if agree1:
                print('Ваш ответ принят ✅')
        with col2:
            disagree1=st.checkbox('❌   нет', key='option41')
            if disagree1:
                print('Ваш ответ принят ✅')                        
        with col3:
            no_info1=st.checkbox('❔   не располагаю информацией', key='option42')
            if no_info1:
                print('Ваш ответ принят ✅')         
                
        st.write('\n')
        st.write('\n')        
        st.write('**Прочее**')
        
        st.write('Предоставляется ли возможность регистрации на мероприятия онлайн с возможностью указания особых потребностей?')
        col1, col2, col3 = st.columns([0.5,0.5, 0.5])
        with col1:
            agree1=st.checkbox('✅   да', key='option43')
            if agree1:
                print('Ваш ответ принят ✅')
        with col2:
            disagree1=st.checkbox('❌   нет', key='option44')
            if disagree1:
                print('Ваш ответ принят ✅')                        
        with col3:
            no_info1=st.checkbox('❔   не располагаю информацией', key='option45')
            if no_info1:
                print('Ваш ответ принят ✅')   
 
            
            
        st.write('')   
        st.text_area("Введите дополнительную информацию о Вашей площадке")

        # Every form must have a submit button.
        st.write('')
        submitted = st.form_submit_button("Отправить")
        if submitted:
            st.write(':green[**Спасибо, Ваш ответ принят!**]')  
            
    
        
        st.write('\n')
        st.write('\n')
        uploaded_files = st.file_uploader("Приложите файлы, подтверждающие информацию о возможностях, предоставляемых Вашей площадкой. Допускается использование форматов .doc, .pdf, .jpg, .jpeg, .png ", accept_multiple_files=True)
        for uploaded_file in uploaded_files:
            bytes_data = uploaded_file.read()
            st.write("Вложение:", uploaded_file.name)
            st.write(bytes_data)
            
        
            
