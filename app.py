import streamlit as st
import requests
import os

# Configuración de la API
API_URL = "https://api.kluster.ai/v1/chat/completions"
API_KEY = st.secrets["API_KEY"] if "API_KEY" in st.secrets else os.getenv("API_KEY")

# Función para generar contenido usando la API de Kluster.ai
def generate_content(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "klusterai/Meta-Llama-3.1-405B-Instruct-Turbo",
        "max_completion_tokens": 7500,
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
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except Exception as err:
        return f"An error occurred: {err}"

# Interfaz de Streamlit
st.title("Generador de Tesis y Artículos Académicos")
st.warning("El contenido generado por esta herramienta debe ser revisado y validado antes de su uso en trabajos académicos.")

area = st.text_input("Ingresa el área científica o filosófica de tu interés:")
if st.button("Generar Contenido"):
    if area:
        with st.spinner("Generando tesis..."):
            tesis_prompt = f"Genera una tesis original en el área de {area}."
            tesis = generate_content(tesis_prompt)
        st.subheader("Tesis Generada")
        st.write(tesis)

        with st.spinner("Generando plan de desarrollo..."):
            plan_prompt = f"Genera un plan para desarrollar la siguiente tesis: {tesis}"
            plan = generate_content(plan_prompt)
        st.subheader("Plan de Desarrollo")
        st.write(plan)

        with st.spinner("Generando apartados del artículo..."):
            apartados_prompt = f"Genera los apartados que contendrá un artículo académico que desarrolle la siguiente tesis: {tesis}"
            apartados = generate_content(apartados_prompt)
        st.subheader("Apartados del Artículo Académico")
        st.write(apartados)

        st.subheader("Desarrollo de los Apartados")
        apartados_list = [apartado.strip() for apartado in apartados.split("\n") if apartado.strip()]
        for apartado in apartados_list:
            st.write(f"**{apartado}**")
            with st.spinner(f"Escribiendo contenido para: {apartado}"):
                contenido_apartado = generate_content(f"Escribe el contenido del apartado: {apartado} para la tesis: {tesis}")
            st.write(contenido_apartado)
