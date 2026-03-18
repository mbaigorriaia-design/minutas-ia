import streamlit as st
import requests

st.title("📝 Generador de Minutas")

# Input de texto
texto = st.text_area("Pegá la transcripción o texto de la reunión")

# Botón
if st.button("Generar minuta"):
    if texto:
        try:
            response = requests.post(
                "http://n8n:5678/webhook/minuta",  # clave: nombre del servicio docker
                json={"meeting_text": texto}
            )

            if response.status_code == 200:
                data = response.json()
                st.success("Minuta generada")
                st.write(data)
            else:
                st.error(f"Error: {response.text}")

        except Exception as e:
            st.error(str(e))