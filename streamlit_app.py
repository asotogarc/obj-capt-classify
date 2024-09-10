import cv2
import streamlit as st

st.title("Webcam Live Feed")

run = st.checkbox('Run')
FRAME_WINDOW = st.image([])

def init_camera():
    return cv2.VideoCapture(0)

camera = None

if run:
    camera = init_camera()
    
    if not camera.isOpened():
        st.error("No se pudo acceder a la cámara. Por favor, verifica tu conexión.")
    else:
        while run:
            ret, frame = camera.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FRAME_WINDOW.image(frame)
            else:
                st.error("Error al leer el frame de la cámara.")
                break
else:
    st.write('Cámara detenida')

if camera is not None:
    camera.release()
