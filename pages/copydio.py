import streamlit as st
from pages.repo import copydioRepo as utils

st.title("Copydio - Generador de Copys para Redes Sociales 🧑‍💻")
st.divider()
st.write("Genera copys, captions y hashtags para posts de redes sociales usando IA. Este agente está optimizado puede optimizarse para tí. \n Si te gustaría tener esta solución en tu negocio, contáctame 😉.")
st.write("Hecho por [Juan Camilo Ibáñez](https://www.linkedin.com/in/juan-ibanez-patino/).")
st.divider()

with st.form("Infórmale a Copydio 🫡"):
    redesSociales = st.text_input("### Paso 1: ¿En que redes sociales va a estar este copy?")
    intencionComunica = st.text_area("### Paso 2: ¿Qué quieres comunicar?", height=200)
    api = st.text_input("### Paso 3: Ingresa tu API Key de Google Gemini (necesario para ejecutar el modelo)", type="password")
    st.markdown("Si no tienes una API Key, obtenla en este [link](https://aistudio.google.com/app/api-keys).")
    files = st.file_uploader("### Paso 4: Sube el contenido base para generar el copy")

    submitted = st.form_submit_button("Generar copys 🚀")

if submitted:
    st.divider()
    st.subheader("Aquí están tus copys generados por Copydio:")
    with st.spinner("Esto puede tardar unos minutos ⏳, por favor espera...", show_time=False):
        show_response = utils.modelExec(
            files,
            redesSociales,
            intencionComunica,
            st.session_state['nombreEmpresa'],
            st.session_state['nombreEmpresa'],
            api
            )

    if show_response:
        st.divider()
        st.markdown(show_response)