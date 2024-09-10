import streamlit as st
import torch
from torchvision.transforms import functional as F
from PIL import Image
import numpy as np
import io
import requests
from typing import Dict, List, Tuple

# Función para descargar el modelo
@st.cache_resource
def download_model(url: str) -> str:
    response = requests.get(url)
    if response.status_code == 200:
        model_path = "model.pt"
        with open(model_path, "wb") as f:
            f.write(response.content)
        return model_path
    else:
        raise Exception("No se pudo descargar el modelo")

# Función para cargar el modelo
@st.cache_resource
def load_model(model_path: str) -> torch.nn.Module:
    model = fasterrcnn_resnet50_fpn_v2(weights=FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT)
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()
    return model

# Función para realizar la detección de objetos
def detect_objects(model: torch.nn.Module, image: Image.Image) -> Tuple[List[Dict[str, torch.Tensor]], torch.Tensor]:
    transform = torchvision.transforms.Compose([torchvision.transforms.ToTensor()])
    input_tensor = transform(image)
    input_batch = input_tensor.unsqueeze(0)
    
    with torch.no_grad():
        prediction = model(input_batch)
    
    return prediction[0], input_tensor

# Función para dibujar las cajas delimitadoras
def draw_boxes(image: np.ndarray, boxes: torch.Tensor, labels: torch.Tensor, scores: torch.Tensor) -> np.ndarray:
    for box, label, score in zip(boxes, labels, scores):
        if score > 0.5:
            x1, y1, x2, y2 = box.tolist()
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
            cv2.putText(image, f"{label}: {score:.2f}", (int(x1), int(y1) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
    return image

def main():
    st.title("Detección de Objetos con Webcam")

    # Descargar y cargar el modelo
    model_url = "https://drive.google.com/uc?export=download&id=12PrKKkYMbFEtYVaNS0aldM-3NejVGuQj"
    try:
        model_path = download_model(model_url)
        model = load_model(model_path)
        st.success("Modelo cargado correctamente")
    except Exception as e:
        st.error(f"Error al cargar el modelo: {e}")
        return

    # Capturar imagen de la webcam
    img_file_buffer = st.camera_input("Toma una foto para detectar objetos")

    if img_file_buffer is not None:
        try:
            # Procesar la imagen
            bytes_data = img_file_buffer.getvalue()
            img = Image.open(io.BytesIO(bytes_data))
            
            # Realizar la detección de objetos
            predictions, input_tensor = detect_objects(model, img)
            
            # Dibujar las cajas delimitadoras
            img_with_boxes = draw_boxes(np.array(img), predictions['boxes'], predictions['labels'], predictions['scores'])
            
            # Mostrar la imagen con las detecciones
            st.image(img_with_boxes, caption="Detecciones de Objetos", use_column_width=True)
            
            # Mostrar información sobre las detecciones
            st.write(f"Se detectaron {len(predictions['boxes'])} objetos")
            
        except Exception as e:
            st.error(f"Ocurrió un error al procesar la imagen: {e}")
    else:
        st.info("Esperando a que se capture una imagen...")

if __name__ == "__main__":
    main()
