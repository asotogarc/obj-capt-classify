import streamlit as st

# Configuración de logging mejorada
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configurar un manejador de logging para Streamlit
class StreamlitHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        st.error(log_entry)

streamlit_handler = StreamlitHandler()
streamlit_handler.setLevel(logging.ERROR)
logger.addHandler(streamlit_handler)


def read_pdf(file):
    pdf_reader = pypdf.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_json_from_text(text):
    json_match = re.search(r'\{[\s\S]*\}', text)
    if json_match:
        return json_match.group()
    return None

def generate_json_from_pdf(pdf_content):
    prompt = f"""
    Analiza minuciosamente el siguiente contenido de una factura PDF y genera un JSON estructurado y detallado. Sé extremadamente preciso y asegúrate de que cada clave tenga un único valor, no listas. Incluye absolutamente toda la información relevante de la factura.

    Realiza las siguientes tareas específicas con máxima precisión:
    1. Identifica el tipo de servicio recibido o producto comprado y devuélvelo con el formato "tipo: [descripción breve y precisa]".
    2. Identifica el tipo de pago realizado entre estas opciones: pago en efectivo, pago por recibo domiciliado, pago por transferencia y pago por tarjeta. Devuélvelo con el formato "pago: [tipo de pago]". Si no se especifica, indica "pago: no especificado".
    3. Basándote en la información anterior, proporciona el asiento contable que mejor se ajuste según la contabilidad española. El asiento contable debe ser una cadena de texto con el siguiente formato:
       "asiento_contable: (DEBE) Cuenta1 XXXX€ (Número), Cuenta2 YYYY€ (Número) a (HABER) Cuenta3 ZZZZ€ (Número), Cuenta4 WWWW€ (Número)"
       Donde las cuentas deben ser específicas del Plan General Contable español, los importes deben cuadrar, y se debe incluir el número de cuenta entre paréntesis. Incluye todos los detalles, como descuentos si los hubiera.
    4. Genera un resumen general que incluya una descripción de la factura, un resumen del asiento contable e información tributaria y fiscal para gestionar la factura.

    Contenido del PDF:
    {pdf_content}

    Genera un JSON que incluya todos estos detalles de manera estructurada y precisa. Asegúrate de que cada campo tenga un valor único y específico. SOLO DEVUELVE EL JSON, sin ningún texto adicional antes o después.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres un experto contable de alta precisión especializado en análisis detallado de facturas y contabilidad española. Debes generar únicamente un JSON válido sin ningún texto adicional."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )

        json_content = response.choices[0].message.content.strip()
        logger.info(f"JSON content generated: {json_content[:500]}...")
        
        json_string = extract_json_from_text(json_content)
        if json_string is None:
            logger.error("No se pudo extraer un JSON válido de la respuesta.")
            return None

        try:
            parsed_json = json.loads(json_string)
            return parsed_json
        except json.JSONDecodeError as je:
            logger.error(f"Error al decodificar JSON: {str(je)}")
            logger.error(f"Contenido JSON que causó el error: {json_string}")
            return None
    except Exception as e:
        logger.error(f"Error al generar el JSON: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return None



# Configuración de la página
st.set_page_config(page_title="Analizador Inteligente de Facturas", layout="wide")

# Estilos personalizados
st.markdown("""
    <style>
    .main {
        background-color: #99006A ;
        padding: 2rem;
        border-radius: 10px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .stDownloadButton>button {
        width: 100%;
        border-radius: 20px;
        background-color: #008CBA;
        color: white;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stDownloadButton>button:hover {
        background-color: #007B9A;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    h1 {
        color: #3A5199;
        font-family: 'Helvetica Neue', sans-serif;
        text-align: center;
    }

    h2 {
    color: #ffffff;
    font-family: 'Nunito Sans', sans-serif;
    text-align: center;
    top: 0; /* Ajusta el valor según tus necesidades */

}

h3 {
    color: #2F2E33;
    font-family: 'Helvetica Neue', sans-serif;
    text-align: center;
    margin-top: 90px; /* Ajusta el valor según tus necesidades */
}
    
    .stAlert {
        background-color: #f8d7da;
        color: #721c24;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .info-box {
    background-color: #d5d6d2;
    margin-bottom: 15px;
    padding: 15px;
    border-radius: 5px;
    color: #ffffff;
    width: 300px; /* Ajusta el valor según tus necesidades */
}

    .success-box {
        background-color: #ddffdd;
        border-left: 6px solid #4CAF50;
        margin-bottom: 15px;
        padding: 15px;
        border-radius: 5px;
        text-align: center;
        color: black;
    }
    .warning-box {
        background-color: #ffffcc;
        border-left: 6px solid #ffeb3b;
        margin-bottom: 15px;
        padding: 15px;
        border-radius: 5px;
    }
    .dataframe {
        font-size: 12px;
        width: 100%;
        border-collapse: collapse;
    }
    .dataframe th, .dataframe td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }
    .dataframe th {
        background-color: #f2f2f2;
        color: #333;
    }
    .dataframe tr:nth-child(even) {
        background-color: #f9f9f9;
    }
    .dataframe tr:hover {
        background-color: #f5f5f5;
    }
    .centered-text {
        text-align: center;
    }
    .black-text {
        color: black;
    }
    .factura-details, .asiento-contable, .resumen-general {
        background-color: #f0f8ff;
        border: 1px solid #b0d4ff;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 15px;
        text-align: center;
        color: black;
    }

    .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
        header {visibility: hidden;}
        [data-testid="stToolbar"] {visibility: hidden !important;}
    </style>
    """, unsafe_allow_html=True)

# Título

# Descripción
# Descripción



st.markdown("<h2 style='text-align: center;'>📤 SUBE TU FACTURA 📤</h2>", unsafe_allow_html=True)

# Footer
st.markdown("""
    <hr>
""", unsafe_allow_html=True)
