
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from app.conversation import clasificar_siniestro
import streamlit as st

'''streamlit run frontend/app.py'''
carga = False
st.title("Asistente para Clasificación de Siniestros")
st.markdown("Este modelo usa información de casos reales a la hora de clasificar, ya que esta información se encuentra en su conocimiento gracias al ajuste fino (Fine-Tuning).")
st.text_input("Introduce la descripción del siniestro para clasificarlo", key="input")
if st.button("Clasificar"):
    st.write("Clasificando...")
resultado, carga = clasificar_siniestro(st.session_state.input)
if carga:
    st.write("Gremio:", resultado["gremio"])
    st.write("Garantía:", resultado["garantia"])