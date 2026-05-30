
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from app.conversation import clasificar_siniestro
import streamlit as st

st.set_page_config(page_title="Asistente para Clasificación de Siniestros", layout="centered")
carga = False
st.title("Asistente para Clasificación de Siniestros")
st.markdown("Este modelo usa información de casos reales a la hora de clasificar, ya que esta información se encuentra en su conocimiento gracias al **ajuste fino (Fine-Tuning)**.")

st.divider()

descripcion = st.text_area("📋 Describe el siniestro", height=100, key="input")
usar_rag = st.toggle("Usar RAG", value=True)
if st.button("🔍 Clasificar", type="primary"):
    with st.spinner("Clasificando siniestro..."):
        resultado, carga = clasificar_siniestro(st.session_state.input, usar_rag)
    if carga:
        st.divider()
        st.success("✅ Clasificación completada")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="🔧 Gremio", value=resultado['gremio'])
        with col2:
            st.metric(label="📄 Garantía", value=resultado['garantia'])