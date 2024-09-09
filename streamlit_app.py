import streamlit as st

# Ocultar el footer de Streamlit
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True) 

# Tu contenido de la aplicación
st.write('hi')
