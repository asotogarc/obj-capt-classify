import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av

def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    return av.VideoFrame.from_ndarray(img, format="bgr24")

st.title("Aplicación Streamlit con Webcam")
st.write("Haga clic en 'Start' para activar la webcam.")

webrtc_streamer(key="example", video_frame_callback=video_frame_callback)
