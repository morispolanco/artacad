import streamlit as st
import requests
import os

# Configuración de la API
API_URL = "https://api.kluster.ai/v1/chat/completions"
API_KEY = st.secrets["API_KEY"]

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
    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.text}"

# Interfaz de Streamlit
st.title("Generador de Tesis y Artículos Académicos")

# Entrada del usuario
area = st.text_input("Ingresa el área científica o filosófica de tu interés:")

if area:
    # Generar tesis
    tesis_prompt = f"Genera una tesis original en el área de {area}."
    tesis = generate_content(tesis_prompt)
    st.subheader("Tesis Generada")
    st.write(tesis)

    # Generar plan de desarrollo
    plan_prompt = f"Genera un plan para desarrollar la siguiente tesis: {tesis}"
    plan = generate_content(plan_prompt)
    st.subheader("Plan de Desarrollo")
    st.write(plan)

    # Generar apartados del artículo académico
    apartados_prompt = f"Genera los apartados que contendrá un artículo académico que desarrolle la siguiente tesis: {tesis}"
    apartados = generate_content(apartados_prompt)
    st.subheader("Apartados del Artículo Académico")
    st.write(apartados)

    # Escribir cada apartado
    st.subheader("Desarrollo de los Apartados")
    apartados_list = apartados.split("\n")
    for apartado in apartados_list:
        if apartado.strip():
            st.write(f"**{apartado}**")
            contenido_apartado = generate_content(f"Escribe el contenido del apartado: {apartado} para la tesis: {tesis}")
            st.write(contenido_apartado)
