import streamlit as st

def initial_set_page():
    st.set_page_config( 
        
        page_title="Hello",
        page_icon="♿",
        layout="wide",
    )

def intro():
    import streamlit as st
    st.image('mts_logo.jpg', caption=[''], width=300)
    st.write('# :red[LIVE без границ]')
    st.write('#  :red[LIVE на полную]')
    st.write('#  :red[LIVE чтобы делать мир лучше]')
    st.write('#  :red[LIVE для всех и каждого]')

intro()