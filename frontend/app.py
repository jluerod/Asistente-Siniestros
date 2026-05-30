
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from app.conversation import clasificar_siniestro
import streamlit as st
import requests
st.set_page_config(page_title="Asistente para Clasificación de Siniestros", layout="centered")
if 'token' not in st.session_state:
    nombre = st.text_input("Usuario", key="username")
    password = st.text_input("Contraseña", type="password", key="password")
    if st.button("Iniciar Sesión", type="primary"):
        token = requests.post("http://localhost:8000/login", json={"name": st.session_state.username, "password": password}).json().get("token")
        if token:
            st.session_state['token'] = token
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos")
else:
    
    carga = False
    st.title("Asistente para Clasificación de Siniestros")
    if st.button("🚪 Cerrar sesión"):
        del st.session_state['token']
        st.rerun()
    st.markdown("Este modelo usa información de casos reales a la hora de clasificar, ya que esta información se encuentra en su conocimiento gracias al **ajuste fino (Fine-Tuning)**.")

    st.divider()

    descripcion = st.text_area("📋 Describe el siniestro", height=100, key="input")
    usar_rag = st.toggle("Usar RAG", value=True)
    if st.button("🔍 Clasificar", type="primary"):
        with st.spinner("Clasificando siniestro..."):
            response = requests.post(
            "http://localhost:8000/clasificar",
            json={"descripcion": st.session_state.input, "usar_rag": usar_rag},
            headers={"Authorization": f"Bearer {st.session_state['token']}"}
        )   
            print(response.json())
            st.session_state['resultado'] = response.json()
    if 'resultado' in st.session_state:
        resultado = st.session_state['resultado']
        if resultado is None:
            st.stop()
        st.divider()
        st.success("✅ Clasificación completada")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="🔧 Gremio", value=resultado['gremio'])
        with col2:
            st.metric(label="📄 Garantía", value=resultado['garantia'])
        
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Correcto"):
                if 'input' in st.session_state:
                    del st.session_state['input']
                requests.post(
                    "http://localhost:8000/validar",
                    json={
                        "descripcion": st.session_state.input,
                        "gremio_correcto": resultado['gremio'],
                        "garantia_correcta": resultado['garantia'],
                        "gremio_predicho": resultado['gremio'],
                        "garantia_predicha": resultado['garantia']
                    },
                    headers={"Authorization": f"Bearer {st.session_state['token']}"}
                )
                st.success("✅ Validación guardada")
                del st.session_state['resultado']
                del st.session_state['input']
                st.rerun()
                
        with col2:
            if st.button("✏️ Corregir"):
                st.session_state['corrigiendo'] = True
                st.session_state['resultado_guardado'] = resultado      

    if st.session_state.get('corrigiendo'):
        
        gremios = ['Electricidad', 'Bricolaje', 'Pocería', 'Fontanería', 'Albañilería', 'Pintura', 'Cerrajería', 'Toldos', 'Mantenimiento', 'Carpintería', 'Loza Sanitaria', 'Persianas', 'Otros', 'Carpintería Metálica', 'Marmolista', 'Tejados', 'Carpintería de Aluminio', 'Desatascos', 'Parquet', 'Jardinería', 'Localización de Fugas', 'Limpiezas', 'Cerrajería y Carpintería metálica', 'Escayola', 'Piscinas', 'Aislamiento', 'Urgencias Fontanería', 'Urgencias Cerrajería', 'Urgencias Electricidad', 'Manitas', 'Bricomanitas', 'Mamparas', 'Moquetas', 'Cristalería']
        gremio_correcto = st.selectbox("Gremio correcto", gremios)
        garantia_correcta = st.text_input("Garantía correcta")
        if st.button("💾 Guardar corrección"):
            requests.post(
                "http://localhost:8000/validar",
                json={
                    "descripcion": st.session_state.input,
                    "gremio_correcto": gremio_correcto,
                    "garantia_correcta": garantia_correcta,
                    "gremio_predicho": resultado['gremio'],
                    "garantia_predicha": resultado['garantia']
                },
                headers={"Authorization": f"Bearer {st.session_state['token']}"}
            )
            st.success("✅ Corrección guardada")
            
            del st.session_state['resultado']
            del st.session_state['input']
            del st.session_state['corrigiendo']
            st.rerun()