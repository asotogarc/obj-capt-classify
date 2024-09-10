import streamlit as st


def main():
    st.title("Aplicación de Webcam con Streamlit")

    # Usar st.camera_input para capturar imágenes de la webcam
    img_file_buffer = st.camera_input("Toma una foto")

    if img_file_buffer is not None:
        # Convertir la imagen a un array de numpy
        img = Image.open(img_file_buffer)
        img_array = np.array(img)

        # Mostrar la imagen capturada
        st.image(img_array, caption="Imagen Capturada", use_column_width=True)

        # Mostrar información sobre la imagen
        st.write("Tipo de dato de la imagen:", type(img_array))
        st.write("Forma de la imagen:", img_array.shape)

if __name__ == "__main__":
    main()
