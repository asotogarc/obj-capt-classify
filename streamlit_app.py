import streamlit as st

# Ocultar la cabecera y el pie de página
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Mostrar "Hi"
st.write("Hi")
