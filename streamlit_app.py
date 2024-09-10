import streamlit as st
import io

def main():
    st.title("Aplicación de Webcam con Streamlit")

    # Usar st.camera_input para capturar imágenes de la webcam
    img_file_buffer = st.camera_input("Toma una foto")

    if img_file_buffer is not None:
        try:
            # Leer los bytes de la imagen
            bytes_data = img_file_buffer.getvalue()
            
            # Usar BytesIO para crear un objeto similar a un archivo
            img = Image.open(io.BytesIO(bytes_data))
            
            # Convertir la imagen a un array de numpy
            img_array = np.array(img)

            # Mostrar la imagen capturada
            st.image(img_array, caption="Imagen Capturada", use_column_width=True)

            # Mostrar información sobre la imagen
            st.write("Tipo de dato de la imagen:", type(img_array))
            st.write("Forma de la imagen:", img_array.shape)
        except Exception as e:
            st.error(f"Ocurrió un error al procesar la imagen: {e}")
    else:
        st.info("Esperando a que se capture una imagen...")

if __name__ == "__main__":
    main()
