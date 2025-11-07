import streamlit as st
import pandas as pd
import io
from pages.repo import guionisioRepo as logic

st.title("Guionisio - Generador de campañas para Redes Sociales ✍️")
st.divider()
st.write("Genera campañas y guiones para posts de redes sociales usando IA.\nSi te gustaría tener esta solución de manera integral en tu negocio, contáctame 😉.")
st.write("Hecho por [Juan Camilo Ibáñez](https://www.linkedin.com/in/juan-ibanez-patino/).")
st.divider()

with st.form("Crea tu campaña"):
    brandbook = st.file_uploader("### 1. Sube tu brandbook o guía de estilo en PDF (opcional):", type=["pdf"], key="brandbook")

    socnet = st.text_input("### 2. ¿En qué redes sociales quieres publicar? (Ejemplo: Instagram, TikTok, LinkedIn...)", key="social_networks")
    mode = st.text_input("### 3. ¿Cuál es el formato de las publicaciones? (Ejemplo: post, carrusel, video...)", key="format")

    theme = st.text_area("### 4. ¿Sobre qué temas quieres que sean las publicaciones? (Ejemplo: marketing digital, desarrollo personal...)", key="theme")
    example_contents = st.file_uploader("### 5. Si tienes ejemplos de publicación que te guste, subelos aquí (opcional):", type=["png", "jpg", "jpeg", "mp4"], accept_multiple_files=True, key="example_content")

    strategy = st.text_input("### 6. ¿Qué estrategia quieres seguir? (Ejemplo: educar, entretener, vender...)", key="strategy")
    periodity = st.text_input("### 7. ¿Con qué periodicidad quieres publicar? (Ejemplo: diariamente, semanalmente...)", key="periodicity")
    full_period = st.text_input("### 8. ¿Por cuánto tiempo quieres que se generen las publicaciones? (Ejemplo: 1 mes, 3 meses...)", key="full_period")

    api = st.text_input("### 9. Ingresa tu API Key de Google Gemini (necesario para ejecutar el modelo)", type="password")
    st.markdown("Si no tienes una API Key, obtenla en este [link](https://aistudio.google.com/app/api-keys).")

    submitted = st.form_submit_button("Generar campaña 🚀")

st.divider()

if submitted:
    if not all([socnet, mode, theme, strategy, periodity, full_period, api]):
        st.error("Por favor, completa todos los campos obligatorios.")
    else:
        with st.spinner("Generando campaña, esto puede tardar unos minutos... ⏳"):
            prompt = logic.guionisio_prompt(
                st.session_state['nombreEmpresa'],
                st.session_state['nombreEmpresa'], 
                socnet, 
                mode, 
                theme, 
                strategy, 
                periodity, 
                full_period
                )
            result = logic.modelExec(
                brandbook, 
                example_contents, 
                prompt, 
                api
                )
        st.success("¡Campaña generada con éxito! 🎉")
        st.markdown("### Resultado:")

        csv_buffer = io.StringIO(result)
        df = pd.read_csv(csv_buffer)
        st.dataframe(df)