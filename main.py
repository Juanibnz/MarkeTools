import streamlit as st

st.title("Bienvenido a MarkeTools 📣🛠️")
st.write("Tu caja de herramientas para marketing digital.")
st.divider()

st.write("Selecciona una herramienta del menú lateral para comenzar.")
st.write("Creado por [Juan Camilo Ibáñez](https://www.linkedin.com/in/juan-ibanez-patino/).")
st.divider()

st.header("¿Qué es MarkeTools?")
st.write("""
MarkeTools es un repositorio de herramientas para marketing con inteligencia artificial generativa. Llega del deseo de ayudar a emprendedores que aún tienen una base débil en terminos de markting y difusión de su marca. Esta hecho para todo mundo: emprendedores, startuperos, freelancers, marketers y cualquier persona que quiera mejorar su presencia en línea. Me es dificil prometerte más clientes, pero te prometo que estas herramientas te ayudarán a mejorar tu marketing digital.
         """)

st.write("""
Cada tool tiene un nombre único. Si crees que algo puede ser mejor o quieres ayudar a expandir este proyecto, escríbeme a LinkedIn.
         """)

st.divider()
st.header("Configura tu empresa 🏢")
nombreEmpresa = st.text_input("¿Cuál es el nombre de tu empresa?")
descEmpresa = st.text_area("Describe brevemente qué hace tu empresa:")
guardarInfo = st.button("Guardar información de la empresa")

if guardarInfo:
    st.session_state['nombreEmpresa'] = nombreEmpresa
    st.session_state['descEmpresa'] = descEmpresa
    st.success("Información de la empresa guardada.")
