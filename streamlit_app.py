import streamlit as st

st.title("Webcam Live Feed")

try:
    import cv2
    run = st.checkbox('Run')
    FRAME_WINDOW = st.image([])
    camera = cv2.VideoCapture(0)

    while run:
        _, frame = camera.read()
        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            FRAME_WINDOW.image(frame)
        else:
            st.error("Failed to capture frame from camera")
            break
    else:
        st.write('Stopped')
    
    if camera.isOpened():
        camera.release()

except ImportError:
    st.error("Failed to import cv2. Make sure OpenCV is installed: pip install opencv-python")
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
