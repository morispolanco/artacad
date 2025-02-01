import streamlit as st
import requests
from fpdf import FPDF

# Configuración de la API
API_URL = "https://api.kluster.ai/v1/chat/completions"
API_KEY = st.secrets["API_KEY"]

# Función para generar contenido
def generate_content(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "klusterai/Meta-Llama-3.1-405B-Instruct-Turbo",
        "max_completion_tokens": 5000,
        "temperature": 1,
        "top_p": 1,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        st.error(f"Error al conectar con la API: {e}")
        return None

# Función para crear un PDF
def create_pdf(tesis, articulo):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Agregar la tesis al PDF
    pdf.cell(200, 10, txt="Tesis Generada", ln=True, align="C")
    pdf.multi_cell(0, 10, txt=tesis)

    # Agregar el artículo académico al PDF
    pdf.add_page()
    pdf.cell(200, 10, txt="Artículo Académico", ln=True, align="C")
    pdf.multi_cell(0, 10, txt=articulo)

    # Guardar el PDF en un archivo temporal
    pdf_output = "tesis_y_articulo.pdf"
    pdf.output(pdf_output)
    return pdf_output

# Interfaz de Streamlit
st.title("Generador de Tesis y Artículo Académico")

# Entrada del usuario
area = st.text_input("Ingresa el área científica o filosófica de tu interés:")

if area:
    if not area.strip():
        st.warning("Por favor, ingresa un área válida.")
    else:
        # Generar tesis
        tesis_prompt = f"Genera una tesis original en el área de {area}."
        tesis = generate_content(tesis_prompt)
        if tesis:
            st.subheader("Tesis Generada")
            st.write(tesis)

            # Generar artículo académico con secciones de 5 a 7 párrafos
            articulo_prompt = (
                f"Escribe un artículo académico que desarrolle la siguiente tesis: {tesis}. "
                "El artículo debe estar dividido en secciones largas, cada una con un título descriptivo. "
                "Cada sección debe tener entre 5 y 7 párrafos bien desarrollados. "
                "Asegúrate de que el contenido sea coherente y profundice en los aspectos clave de la tesis."
            )
            articulo = generate_content(articulo_prompt)
            if articulo:
                st.subheader("Artículo Académico")
                st.write(articulo)

                # Crear y descargar PDF
                st.subheader("Descargar en PDF")
                if st.button("Generar PDF"):
                    pdf_file = create_pdf(tesis, articulo)
                    with open(pdf_file, "rb") as file:
                        st.download_button(
                            label="Descargar PDF",
                            data=file,
                            file_name="tesis_y_articulo.pdf",
                            mime="application/pdf"
                        )

# Footer
st.markdown(
    """
    <div style="text-align: center; margin-top: 50px;">
        <p>Copyright 2025 <a href="https://hablemosbien.org" target="_blank">Hablemosbien.org</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
